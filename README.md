# GCC Postcommit CI

This repo runs the GCC testsuite on a variety of risc-v targets.

# Dashboards
- [Main](https://patrick-rivos.github.io/gcc-postcommit-ci/)
- [All](https://patrick-rivos.github.io/gcc-postcommit-ci/all)
- [gcv](https://patrick-rivos.github.io/gcc-postcommit-ci/gcv)
- [gc](https://patrick-rivos.github.io/gcc-postcommit-ci/gc)
- [Bitmanip](https://patrick-rivos.github.io/gcc-postcommit-ci/bitmanip)
- [RVA23](https://patrick-rivos.github.io/gcc-postcommit-ci/rva23)
- [Vector Crypto](https://patrick-rivos.github.io/gcc-postcommit-ci/vector_crypto)
- [All Execution Failures](https://patrick-rivos.github.io/gcc-postcommit-ci/all-filtered)
- [gcv Execution Failures](https://patrick-rivos.github.io/gcc-postcommit-ci/gcv-filtered)
- [gc Execution Failures](https://patrick-rivos.github.io/gcc-postcommit-ci/gc-filtered)
- [Bitmanip Execution Failures](https://patrick-rivos.github.io/gcc-postcommit-ci/bitmanip-filtered)
- [RVA23 Execution Failures](https://patrick-rivos.github.io/gcc-postcommit-ci/rva23-filtered)
- [Vector Crypto Execution Failures](https://patrick-rivos.github.io/gcc-postcommit-ci/vector_crypto-filtered)

## GCV Weekly runs:
- [gcv_zvl](https://patrick-rivos.github.io/gcc-postcommit-ci/gcv_zvl)
- [gcv_zve](https://patrick-rivos.github.io/gcc-postcommit-ci/gcv_zve)
- lmul 2 TODO
- lmul 4 TODO
- lmul 8 TODO
- lmul dynamic TODO

## Current targets

### Non-multilib github runners
- rv32gc
- rv64gc
- rv32gc_zba_zbb_zbc_zbs # rv32 bitmanip
- rv64gc_zba_zbb_zbc_zbs # rv64 bitmanip

### Self-hosted multilib
- rv32gcv # rv32 vector
- rv64gcv # rv64 vector
- rv64gcv_zvbb_zvbc_zvkg_zvkn_zvknc_zvkned_zvkng_zvknha_zvknhb_zvks_zvksc_zvksed_zvksg_zvksh_zvkt # rv64 vector crypto
- rv64imafdcv_zicond_zawrs_zbc_zvkng_zvksg_zvbb_zvbc_zicsr_zba_zbb_zbs_zicbom_zicbop_zicboz_zfhmin_zkt # RVA23U64 profile with optional extensions, excluding unsupported extensions

## Build frequency
Every 8 hours
