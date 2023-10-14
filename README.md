# GCC Postcommit CI

This repo runs the GCC testsuite on a variety of risc-v targets.

# Dashboards
- [All](https://patrick-rivos.github.io/gcc-postcommit-ci/)
- [gcv](https://patrick-rivos.github.io/gcc-postcommit-ci/gcv)
- [gc](https://patrick-rivos.github.io/gcc-postcommit-ci/gc)
- [Bitmanip](https://patrick-rivos.github.io/gcc-postcommit-ci/bitmanip)
- [RVA23](https://patrick-rivos.github.io/gcc-postcommit-ci/rva23)
- [Vector Crypto](https://patrick-rivos.github.io/gcc-postcommit-ci/vector_crypto)

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
