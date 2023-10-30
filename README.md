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
- rv64imafdcv_zicond_zawrs_zbc_zvkng_zvksg_zvbb_zvbc_zicsr_zba_zbb_zbs_zicbom_zicbop_zicboz_zfhmin_zkt_zfh_zfa_zihintpause # RVA23U64 profile with optional extensions, excluding unsupported extensions

### Excluded from rva23 (Not supported by binutils 2.41):
- Zicntr Base counters and timers.
- Zihpm Hardware performance counters.
- Ziccif Main memory regions with both the cacheability and coherence PMAs must support instruction fetch, and any instruction fetches of naturally aligned power-of-2 sizes up to min(ILEN,XLEN) (i.e., 32 bits for RVA23) are atomic.
- Ziccrse Main memory regions with both the cacheability and coherence PMAs must support RsrvEventual.
- Ziccamoa Main memory regions with both the cacheability and coherence PMAs must support AMOArithmetic.
- Zicclsm Misaligned loads and stores to main memory regions with both the cacheability and coherence PMAs must be supported.
- Za64rs Reservation sets are contiguous, naturally aligned, and a maximum of 64 bytes.
- Zic64b Cache blocks must be 64 bytes in size, naturally aligned in the address space.
- Zvfhmin Vector FP16 conversion instructions.
- Zihintntl Non-temporal locality hints.
- Zimop Maybe Operations.
- Zcb Additional 16b compressed instructions.
- Zjpm Pointer masking (ignore high bits of addresses)
- Zacas Compare-and-swap
- Zvfh Vector half-precision floating-point (FP16).
- Zfbfmin Scalar BF16 FP conversions.
- Zvfbfmin Vector BF16 FP conversions.
- Zvfbfwma Vector BF16 widening mul-add.

## Build frequency
Every 8 hours
