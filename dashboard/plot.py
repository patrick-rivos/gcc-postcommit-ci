import os
import pandas as pd
import plotly.express as px


def clean(old_df: pd.DataFrame):
    df = old_df.replace(" multilib", "", regex=True)
    df.replace("rv32gc_zba_zbb_zbc_zbs ilp32d medlow", "rv32 Bitmanip", regex=True, inplace=True)
    df.replace("rv64gc_zba_zbb_zbc_zbs lp64d medlow", "rv64 Bitmanip", regex=True, inplace=True)
    df.replace("rv64imafdcv_zicond_zawrs_zbc_zvkng_zvksg_zvbb_zvbc_zicsr_zba_zbb_zbs_zicbom_zicbop_zicboz_zfhmin_zkt lp64d medlow", "rv64 RVA", regex=True, inplace=True)
    df.replace("rv64gcv_zvbb_zvbc_zvkg_zvkn_zvknc_zvkned_zvkng_zvknha_zvknhb_zvks_zvksc_zvksed_zvksg_zvksh_zvkt lp64d medlow", "rv64 Vector Crypto", regex=True, inplace=True)
    df.replace("rv32gcv_zvbb_zvbc_zvkg_zvkn_zvknc_zvkned_zvkng_zvknha_zvknhb_zvks_zvksc_zvksed_zvksg_zvksh_zvkt ilp32d medlow", "rv32 Vector Crypto", regex=True, inplace=True)
    df.replace(" medlow", "", regex=True, inplace=True)

    df['libname'] = old_df['target'].str.replace(" multilib", "").replace(" medlow", "")

    df['libc-target'] = df['libc'] + "-" + df["target"]

    df['url'] = ''

    df['hash_timestamp'] = pd.to_datetime(df['hash_timestamp'], utc=True)

    df.sort_values(by='libc-target', inplace=True)
    df.sort_values(by='hash_timestamp', inplace=True)

    return df


def plot_cumulative_state(df: pd.DataFrame, outfile: str):
    print(df['libc-libname-tool'].to_list())

    fig = px.line(
        df,
        x="hash_timestamp",
        y=["unique_fails", "total_fails"],
        labels={
            "hash_timestamp": "hash_timestamp_utc",
            "unique_fails": "unique_fails",
        },
        text="url",
        hover_data=["gcc_hash","libname"],
        facet_col='libc-target',
        facet_col_wrap=3,
        facet_row_spacing=0.04, # default is 0.07 when facet_col_wrap is used
        facet_col_spacing=0, # default is 0.03
        # height=600, width=800,
        color='tool',
        title=f"Unique/total failures per hash<br><sup>Data sourced from <a href=\"https://github.com/patrick-rivos/gcc-postcommit-ci\">gcc-postcommit-ci</a> and older data from <a href=\"https://github.com/patrick-rivos/riscv-gnu-toolchain\">riscv-gnu-toolchain</a></sup>",

    )

    fig.write_html(outfile, include_plotlyjs='cdn')


if __name__ == "__main__":
    linux_data = pd.read_csv('linux.csv')
    newlib_data = pd.read_csv('newlib.csv')
    linux_data.update(newlib_data)
    state_data = clean(linux_data)

    print(state_data)

    os.makedirs(f"site", exist_ok=True)

    plot_cumulative_state(state_data, "site/index.html")
