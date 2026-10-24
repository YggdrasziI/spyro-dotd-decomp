# Provenance of reused code

Every file or function taken from another project, with the project, its commit
(`git -C <clone> rev-parse HEAD`), its license (or its absence and the owner's
approval, see `notes/REFERENCES.md`) and the changes made.

## Runtime.PPCEABI.H (7 units, Matching)

Source: [yannicksuter/mscharged-decomp](https://github.com/yannicksuter/mscharged-decomp)
(Mario Strikers Charged, Wii), local clone at commit
`8592d67e2865975066fa6a9065826ff0e36e610f`, license **CC0-1.0**. Fetched on 2026-10-24.
Line endings converted to LF.

| Our file | Their file | Changes |
|---|---|---|
| `src/Runtime.PPCEABI.H/global_destructor_chain.c` | `src/Runtime/global_destructor_chain.c` | none |
| `src/Runtime.PPCEABI.H/__init_cpp_exceptions.cpp` | `src/Runtime/__init_cpp_exceptions.cpp` | `#pragma force_active on` / `reset` around the `.ctors` / `.dtors` references (as in mlab-decomp) |
| `src/Runtime.PPCEABI.H/__mem.c` | `src/Runtime/__mem.c` | none |
| `src/Runtime.PPCEABI.H/__va_arg.c` | `src/Runtime/__va_arg.c` | none |
| `src/Runtime.PPCEABI.H/NMWException.cpp` | `src/Runtime/NMWException.cpp` | none (built with `-Cpp_exceptions on`, as in mscharged) |
| `src/Runtime.PPCEABI.H/ptmf.c` | `src/Runtime/ptmf.c` | `__ptmf_scall4` added, **transcribed from this game's DOL** (0x80381228) |

Headers copied unchanged: `libs/Runtime/include/{global_destructor_chain.h,__ppc_eabi_linker.h,NMWException.h,__mem.h,runtime.h}`,
`libs/MSL_C/include/{cstring,size_t.h}`.

`src/Runtime.PPCEABI.H/runtime.c` comes from `YggdrasziI/mlab-decomp` (private, same
owner), commit `55db5381722bed8ad1fe3cd096f3955ae28130c1`, unchanged. That file is
mscharged's `src/Runtime/runtime.c` (CC0) plus `__shr2u` and `__cvt_dbl_usll` from
[zeldaret/tp](https://github.com/zeldaret/tp) (CC0, commit
`c8fa8c9e2aab72cf4e5db0e5d1c84a9ea6ee6eb0`) and `__cvt_sll_dbl` transcribed from the
Monster Lab DOL (see mlab-decomp `notes/PROVENANCE.md`).

Functions of these sources that this DOL does not have (`__ptmf_cmpr`, `__shr2u`,
`__cvt_ull_dbl`, `__cvt_ull_flt`) are left in the sources and dead-stripped by the
linker (the build matches).

## MSL_C (38 units, Matching)

Source: `YggdrasziI/mlab-decomp` (private, same owner), commit
`55db5381722bed8ad1fe3cd096f3955ae28130c1`, copied unchanged. mlab-decomp's
`notes/PROVENANCE.md` traces each file to a CC0 project:

- from [yannicksuter/mscharged-decomp](https://github.com/yannicksuter/mscharged-decomp)
  (CC0-1.0, commit `126acd42cb8ca0eea1efa75c5a8da7110ef9a142`), unchanged:
  `mem_funcs.c`, `e_acos.c`, `e_atan2.c`, `e_pow.c`, `e_rem_pio2.c`, `e_sqrt.c`,
  `k_cos.c`, `k_rem_pio2.c`, `k_sin.c`, `k_tan.c`, `s_atan.c`, `s_copysign.c`,
  `s_cos.c`, `s_floor.c`, `s_frexp.c`, `s_ldexp.c`, `s_sin.c`, `s_tan.c`;
- `e_asin.c` from [SMGCommunity/Petari](https://github.com/SMGCommunity/Petari)
  (CC0-1.0, commit `6804bd31724eaa01b33b68c622fcda6d1b433e17`), include line adapted;
- `e_fmod.c`, `e_log.c`, `e_log10.c` from [zeldaret/tp](https://github.com/zeldaret/tp)
  (CC0-1.0, commit `c8fa8c9e2aab72cf4e5db0e5d1c84a9ea6ee6eb0`), include lines adapted.

Headers copied unchanged from the same mlab-decomp commit (mscharged origin):
`include/types.h`, `libs/MSL_C/include/{errno.h,mem_funcs.h}`,
`libs/MSL_C/include/internal/{fdlibm.h,math_api.h,math_nan.h}`.

Added later from the same mlab-decomp commit, copied unchanged: `mem.c`,
`math_api.c`, `qsort.c`, `signal.c`, `abort_exit_ppc_eabi.c`, `math_sun.c` and the
headers `libs/MSL_C/include/{abort_exit.h,critical_regions.h,stddef.h,stdlib.h,
string_api.h,wchar_t.h}`; `signal.h` with its include of `<revolution/types.h>`
changed to `<types.h>` (this project has no RVL_SDK headers yet). See mlab-decomp
`notes/PROVENANCE.md` for their origin.

Then, from the same commit: `alloc.c`, `ansi_fp.c`, `scanf.c` and the headers
`libs/MSL_C/include/{alloc.h,ansi_fp.h,ctype.h,float.h,internal/locale.h,math.h,
scanf.h,stdarg.h,stdint.h,stdio.h,stdio_api.h,strtold.h,strtoul.h}` and
`libs/Runtime/include/GCN_mem_alloc.h`, copied unchanged except: `ansi_fp.h` includes
`<types.h>` instead of `<revolution/types.h>`; `alloc.c` gains `__pool_alloc_clear`
and `calloc` at its end, written for this project from the DOL (mlab's DOL has no
`calloc`). `include/types.h` gains `s64`, `u64` and, in C, `bool` / `true` / `false`
(definitions as in mlab-decomp's `revolution/types.h`).

Units chosen with a scratch script: the reference unit's functions appear in the same
order with the same normalized code (`tools/ref_match.py` fingerprints), the `.text`
size is equal, and each data section is placed by pairing the symbols both functions
reference. Function and data names are mlab's, mapped by offset inside each section.

Then, from the same commit: `ansi_files.c`, `buffer_io.c`, `direct_io.c`, `file_io.c`,
`FILE_POS.c`, `mbstring.c`, the headers `libs/MSL_C/include/{ansi_files.h,
buffer_io.h,direct_io.h,file_io.h,file_struct.h,FILE_POS.h,locale.h,mbstring.h,mem.h,
misc_io.h,string.h,wchar_io.h}` and `libs/MetroTRK/include/MetroTRK/trkenum.h`, copied
unchanged except: `ansi_files.h` includes `<types.h>` instead of
`<revolution/types.h>`; the functions this DOL lacks (`__find_unopened_file`,
`__init_file`, `__flush_line_buffered_output_files`, `__load_buffer`, `setvbuf`,
`fread`, `__fread`, `fopen`, `freopen`, `__get_file_modes`, `__msl_strnicmp`,
`__msl_itoa`) are put under `#if 0`, and `mbstowcs`, which mlab had under `#if 0`, is
enabled again (this DOL has it at 0x80386D88). These units hold only part of mlab's
functions, so their `.text` sizes differ; the kept functions have the same code.

Then `string.c` from the same mlab-decomp commit, copied unchanged except for
`strrchr`, added before `strtok`: taken from
[SMGCommunity/Petari](https://github.com/SMGCommunity/Petari) `src/MSL_C/string.c`
(CC0-1.0, commit `f3defb7b21bad70d84949adfdeb66b7b1c573031`), reformatted to the
file's brace style.
