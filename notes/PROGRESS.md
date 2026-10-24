# Progress log

| Date | Commit | Matched code | Matched functions | Units (split / total) | Milestone |
|---|---|---|---|---|---|
| 2026-10-24 | db65293 | 0 / 4898488 bytes (0 %) | 0 / 35557 | 0 / — | Step 1 done: dtk-template set up for RO8P7D, private repository and build image, CI checking `main.dol` |
| 2026-10-24 | 8beedb2 | 632 / 4898488 bytes (0.01 %) | 13 / 35557 | 3 / 2775 | Compiler settled: linker GC 3.0 family, game code GC/3.0a5.2 (first game unit `unit_8032E43C`, IKAnchor, Matching); runtime ctor/dtor units Matching |
| 2026-10-24 | cbb2824 | 70756 / 4898488 bytes (1.44 %) | 178 / 35557 | 68 / 2766 | MSL_C done except the float wrappers at 0x8038F680 (set aside): 60 units Matching, from mlab, mscharged and tp sources |
| 2026-10-24 | 76a5796 | 134756 / 4898488 bytes (2.75 %) | 466 / 35557 | 102 / 2795 | RVL_SDK `os/` done except `OSNet.c` (NonMatching): 33 units Matching from mlab, with the `revolution/` headers; Runtime units split (`New.cpp`, `MWRTTI.cpp`, `Gecko_ExceptionPPC.cpp` NonMatching) |
