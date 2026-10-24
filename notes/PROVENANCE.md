# Provenance of reused code

Every file or function taken from another project, with the project, its commit
(`git -C <clone> rev-parse HEAD`), its license (or its absence and the owner's
approval, see `notes/REFERENCES.md`) and the changes made.

## Runtime.PPCEABI.H (2 units, Matching)

Source: [yannicksuter/mscharged-decomp](https://github.com/yannicksuter/mscharged-decomp)
(Mario Strikers Charged, Wii), local clone at commit
`8592d67e2865975066fa6a9065826ff0e36e610f`, license **CC0-1.0**. Fetched on 2026-10-24.
Line endings converted to LF.

| Our file | Their file | Changes |
|---|---|---|
| `src/Runtime.PPCEABI.H/global_destructor_chain.c` | `src/Runtime/global_destructor_chain.c` | none |
| `src/Runtime.PPCEABI.H/__init_cpp_exceptions.cpp` | `src/Runtime/__init_cpp_exceptions.cpp` | `#pragma force_active on` / `reset` around the `.ctors` / `.dtors` references (as in mlab-decomp) |

Headers copied unchanged: `libs/Runtime/include/{global_destructor_chain.h,__ppc_eabi_linker.h,NMWException.h}`,
`libs/MSL_C/include/{cstring,size_t.h}`.
