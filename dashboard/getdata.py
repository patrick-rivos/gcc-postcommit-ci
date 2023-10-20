
import argparse
import contextlib
import shutil
import os
from typing import Dict, List, Set
from zipfile import ZipFile
import json
import requests
from compare_testsuite_log import Description, classify_by_unique_failure, parse_testsuite_failures
from download_artifact import search_for_artifact, download_artifact, extract_artifact


def parse_arguments():
    """ parse command line arguments """
    parser = argparse.ArgumentParser(description="Get issue information")
    parser.add_argument(
        "-token",
        required=True,
        type=str,
        help="Github access token",
    )
    parser.add_argument(
        "-bootstrap",
        action="store_true",
        help="Build the current_logs from scratch. Takes a long time.",
    )
    return parser.parse_args()


def get_issue_hashes(token: str, repo: str):
    issue_url = f"https://api.github.com/repos/{repo}/issues?page=1&q=is%3Aissue&state=all"
    params = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {token}",
        "X-Github-Api-Version": "2022-11-28",
    }
    r = requests.get(issue_url, headers=params)
    response = json.loads(r.text)
    print(response)
    hashes: List[str] = []

    for issue in response:
        if "pull_request" not in issue:
            hashes.append(issue["title"].split(" ")[-1])

    return hashes


def download_summaries(artifact_name: str, token: str, repo: str):
    artifact_id = search_for_artifact(artifact_name, repo, token, None)
    assert artifact_id is not None
    artifact_path = download_artifact(artifact_name, artifact_id, token, repo)
    return artifact_path


def download_logs(token: str, repo: str, existing_hashes: Set[str]):
    hashes = get_issue_hashes(token, repo)
    os.mkdir("temp")
    hashes = [gcc_hash for gcc_hash in hashes if gcc_hash not in existing_hashes]

    failure_hashes: Set[str] = set()

    for gcc_hash in hashes:
        artifact_name = f"{gcc_hash}-current-logs"
        artifact_zip = download_summaries(artifact_name, token, repo)
        os.makedirs(f"testsuite_runs/{gcc_hash}", exist_ok=True)
        extract_artifact("current_logs.zip", artifact_zip, outdir=f"testsuite_runs/{gcc_hash}")
        with ZipFile(f"./testsuite_runs/{gcc_hash}/current_logs.zip", "r") as zf:
            zf.extractall(path=f"./testsuite_runs/{gcc_hash}")
        if os.path.isfile(f"./testsuite_runs/{gcc_hash}/current_logs/failed_testsuite.txt"):
            # Failed build, drop this hash
            print(f"Testsuite(s) failed for {gcc_hash}, dropping failing testsuite runs from testsuite_runs")
            failure_hashes.add(gcc_hash)
            os.remove(f"./testsuite_runs/{gcc_hash}/current_logs/failed_testsuite.txt")
        if os.path.isfile(f"./testsuite_runs/{gcc_hash}/current_logs/failed_build.txt"):
            # Failed build, drop this hash
            print(f"Build(s) failed for {gcc_hash}, dropping failing builds from testsuite_runs")
            failure_hashes.add(gcc_hash)
            os.remove(f"./testsuite_runs/{gcc_hash}/current_logs/failed_build.txt")
        os.remove(f"./testsuite_runs/{gcc_hash}/current_logs.zip")
    shutil.rmtree("./temp")

    hashes = [gcc_hash for gcc_hash in hashes if gcc_hash not in failure_hashes]

    return hashes


def get_gcc_hash_timestamp(gcc_hash: str):
    return os.popen(
                f"cd ../riscv-gnu-toolchain/gcc && git show -s --format='%ci' {gcc_hash}"
            ).read().strip()


def aggregate_logs(logs_dir: str, gcc_hash: str):
    files = os.listdir(logs_dir)
    print(logs_dir)
    all_linux_failures: Dict[Description, List[str]] = {}
    all_newlib_failures: Dict[Description, List[str]] = {}
    for file in files:
        current_failures = parse_testsuite_failures(logs_dir + file)
        if 'linux' in file:
            all_linux_failures.update(current_failures)
        else:
            all_newlib_failures.update(current_failures)

    for target, fails in all_linux_failures.items():
        class_fails = classify_by_unique_failure(fails)

        hash_timestamp = get_gcc_hash_timestamp(gcc_hash)

        with open(f"linux.csv", "a") as csv:
            csv.write(f"{gcc_hash},{hash_timestamp},linux-{target.libname}-{target.tool},linux,{target.libname},{target.tool},{len(class_fails.keys())},{len(fails)}\n")

    for target, fails in all_newlib_failures.items():
        class_fails = classify_by_unique_failure(fails)

        hash_timestamp = get_gcc_hash_timestamp(gcc_hash)

        with open(f"newlib.csv", "a") as csv:
            csv.write(f"{gcc_hash},{hash_timestamp},newlib-{target.libname}-{target.tool},newlib,{target.libname},{target.tool},{len(class_fails.keys())},{len(fails)}\n")


def main():
    args = parse_arguments()

    hashes = []

    if args.bootstrap:
        shutil.rmtree("./testsuite_runs", ignore_errors=True)
        with contextlib.suppress(FileNotFoundError):
            os.remove("linux.csv")
            os.remove("newlib.csv")
        existing_hashes: Set[str] = set()
        download_logs(args.token, "patrick-rivos/riscv-gnu-toolchain", existing_hashes)
        download_logs(args.token, "patrick-rivos/gcc-postcommit-ci", existing_hashes)
        hashes = sorted(os.listdir('testsuite_runs'))
        with open(f"linux.csv", "a") as csv:
            csv.write(f"gcc_hash,hash_timestamp,libc-libname-tool,libc,target,tool,unique_fails,total_fails\n")
        with open(f"newlib.csv", "a") as csv:
            csv.write(f"gcc_hash,hash_timestamp,libc-libname-tool,libc,target,tool,unique_fails,total_fails\n")
    else:
        existing_hashes = set(os.listdir('testsuite_runs'))
        download_logs(args.token, "patrick-rivos/gcc-postcommit-ci", existing_hashes)
        new_hashes = sorted(set(os.listdir('testsuite_runs')) - existing_hashes)
        hashes = new_hashes

    print(hashes)

    # Get GCC ready for timestamp-getting
    os.popen('cd ../riscv-gnu-toolchain && git submodule update --init gcc && cd gcc && git fetch')

    for gcc_hash in hashes:
        aggregate_logs(f"./testsuite_runs/{gcc_hash}/current_logs/", gcc_hash)


if __name__ == '__main__':
    main()
