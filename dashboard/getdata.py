
import argparse
import shutil
import os
import dateutil.parser
from typing import Dict, List
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
    return parser.parse_args()


def get_issue_hashes(token: str, repo: str):
    issue_url = f"https://api.github.com/repos/{repo}/issues?page=1&q=is%3Aissue+-label%3Abisect+-label%3Abuild-failure+-label%3Atestsuite-failure&state=all"
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


def download_logs(token: str, repo: str):
    hashes = get_issue_hashes(token, repo)
    os.mkdir("temp")
    for gcc_hash in hashes:
        artifact_name = f"{gcc_hash}-current-logs"
        artifact_zip = download_summaries(artifact_name, token, repo)
        os.makedirs(f"current_logs/{gcc_hash}", exist_ok=True)
        extract_artifact("current_logs.zip", artifact_zip, outdir=f"current_logs/{gcc_hash}")
        with ZipFile(f"./current_logs/{gcc_hash}/current_logs.zip", "r") as zf:
            zf.extractall(path=f"./current_logs/{gcc_hash}")
        os.remove(f"./current_logs/{gcc_hash}/current_logs.zip")
    shutil.rmtree("./temp")

    return hashes


def get_gcc_hash_timestamp(gcc_hash: str):
    return os.popen(
                f"cd ../riscv-gnu-toolchain/gcc && git checkout master --quiet && git pull --quiet && git show -s --format='%ci' {gcc_hash}"
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
    # download_logs(args.token, "patrick-rivos/gcc-postcommit-ci")
    # download_logs(args.token, "patrick-rivos/riscv-gnu-toolchain")

    # print(hashes)

    hashes = reversed(sorted(os.listdir('current_logs')))

    with open(f"linux.csv", "a") as csv:
        csv.write(f"gcc_hash,hash_timestamp,libc-libname-tool,libc,target,tool,unique_fails,total_fails\n")

    with open(f"newlib.csv", "a") as csv:
        csv.write(f"gcc_hash,hash_timestamp,libc-libname-tool,libc,target,tool,unique_fails,total_fails\n")

    for gcc_hash in hashes:
        aggregate_logs(f"./current_logs/{gcc_hash}/current_logs/", gcc_hash)


if __name__ == '__main__':
    main()
