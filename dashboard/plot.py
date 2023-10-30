import datetime
import os
import pandas as pd
import plotly.express as px


def clean(old_df: pd.DataFrame):
    df = old_df.replace(" multilib", "", regex=True)
    df.replace("rv32gc_zba_zbb_zbc_zbs ilp32d medlow", "rv32 Bitmanip", regex=True, inplace=True)
    df.replace("rv64gc_zba_zbb_zbc_zbs lp64d medlow", "rv64 Bitmanip", regex=True, inplace=True)
    df.replace("rv64imafdcv_zicond_zawrs_zbc_zvkng_zvksg_zvbb_zvbc_zicsr_zba_zbb_zbs_zicbom_zicbop_zicboz_zfhmin_zkt lp64d medlow", "rv64 RVA", regex=True, inplace=True)
    df.replace("rv64imafdcv_zicond_zawrs_zbc_zvkng_zvksg_zvbb_zvbc_zicsr_zba_zbb_zbs_zicbom_zicbop_zicboz_zfhmin_zkt_zfh_zfa_zihintpause lp64d medlow", "rv64 RVA", regex=True, inplace=True)
    df.replace("rv64gcv_zvbb_zvbc_zvkg_zvkn_zvknc_zvkned_zvkng_zvknha_zvknhb_zvks_zvksc_zvksed_zvksg_zvksh_zvkt lp64d medlow", "rv64 Vector Crypto", regex=True, inplace=True)
    df.replace("rv32gcv_zvbb_zvbc_zvkg_zvkn_zvknc_zvkned_zvkng_zvknha_zvknhb_zvks_zvksc_zvksed_zvksg_zvksh_zvkt ilp32d medlow", "rv32 Vector Crypto", regex=True, inplace=True)
    df.replace(" medlow", "", regex=True, inplace=True)

    df['libname'] = old_df['target'].str.replace(" multilib", "").replace(" medlow", "")

    df['libc-target'] = df['libc'] + "-" + df["target"]

    df['hash_timestamp'] = pd.to_datetime(df['hash_timestamp'], utc=True)

    df.sort_values(by='hash_timestamp', inplace=True)

    return df


def plot_cumulative_state(df: pd.DataFrame, outfile: str, wrap: int = 3):
    print(df['libc-libname-tool'].to_list())

    range_max = max(df['hash_timestamp']) + datetime.timedelta(hours=6)

    range_min = max(df['hash_timestamp']) - datetime.timedelta(days=9)

    fig = px.line(
        df,
        x="hash_timestamp",
        y=["unique_fails", "total_fails"],
        labels={
            "hash_timestamp": "hash_timestamp_utc",
            "unique_fails": "unique_fails",
        },
        markers=True,
        hover_data=["gcc_hash","libname"],
        category_orders={
            'libc-target': sorted(list(set(df["libc-target"].to_list()))),
                         },
        facet_col='libc-target',
        facet_col_wrap=wrap,
        facet_row_spacing=0.04, # default is 0.07 when facet_col_wrap is used
        facet_col_spacing=0, # default is 0.03
        # height=600, width=800,
        color='tool',
        symbol='tool',
        title=f"Unique/total failures per hash<br><sup>Data sourced from <a href=\"https://github.com/patrick-rivos/gcc-postcommit-ci\">gcc-postcommit-ci</a> and older data from <a href=\"https://github.com/patrick-rivos/riscv-gnu-toolchain\">riscv-gnu-toolchain</a></sup>",
        range_x=[range_min, range_max],
        range_y=[-5, max(df[df['hash_timestamp'] > range_min]['total_fails']) + 5],
    )

    fig.write_html(outfile, include_plotlyjs='cdn')


if __name__ == "__main__":
    linux_data = pd.read_csv('linux.csv')
    newlib_data = pd.read_csv('newlib.csv')
    raw_data = pd.concat([newlib_data, linux_data])
    all_data = clean(raw_data)

    os.makedirs(f"site", exist_ok=True)

    plot_cumulative_state(all_data, "site/index.html")

    gcv = all_data[all_data["libc-target"].str.contains("gcv")]
    print(gcv)
    plot_cumulative_state(gcv, "site/gcv.html", wrap=2)

    bitmanip = all_data[all_data["libc-target"].str.contains("Bitmanip")]
    print(bitmanip)
    plot_cumulative_state(bitmanip, "site/bitmanip.html", wrap=2)

    rva23 = all_data[all_data["libc-target"].str.contains("RVA")]
    print(rva23)
    plot_cumulative_state(rva23, "site/rva23.html", wrap=2)

    vc = all_data[all_data["libc-target"].str.contains("Vector Crypto")]
    print(vc)
    plot_cumulative_state(vc, "site/vector_crypto.html", wrap=2)

    gc = all_data[all_data["libc-target"].str.contains("gc ")]
    print(gc)
    plot_cumulative_state(gc, "site/gc.html", wrap=2)
