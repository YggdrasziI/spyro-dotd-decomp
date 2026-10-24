# Code and data regions

## Important: what the build does and does not prove

A split that builds and links into a matching `main.dol` proves only that the bytes
are placed back where they were. It does not prove that the range is one translation
unit of the original build: that is proven only when the unit is decompiled and
matches. Every bound below says which evidence it rests on.

## DOL sections

| Section | Start | End (excl.) | Size |
|---|---|---|---|
| `.init` | 0x80004000 | 0x800064E0 | 0x24E0 |
| `extab` | 0x800064E0 | 0x80008B80 | 0x26A0 |
| `extabindex` | 0x80008B80 | 0x8000C4E0 | 0x3960 |
| `.text` | 0x8000C4E0 | 0x804B7EC0 | 0x4AB9E0 |
| `.ctors` | 0x804B7EC0 | 0x804B88C0 | 0xA00 |
| `.dtors` | 0x804B88C0 | 0x804B88E0 | 0x20 |
| `.rodata` | 0x804B8900 | 0x804C8240 | 0xF940 |
| `.data` | 0x804C8240 | 0x80518380 | 0x50140 |
| BSS span (`.bss`, `.sbss`, `.sbss2`, around the small data sections) | 0x80518380 | 0x805D391C | 0xBB59C |
| `.sdata` | 0x805CA1C0 | 0x805CC740 | 0x2580 |
| `.sdata2` | 0x805CECE0 | 0x805D3900 | 0x4C20 |

## `.text` regions

All bounds are approximate until the units are split and matched. "Matches mlab"
means `tools/ref_match.py E:/Projets/Dev/mlab-decomp RM7P4F` (2026-10-24) found
functions with the same code as Monster Lab (`RM7P4F`, same SDK build tag), unique on
both sides; 2168 functions matched in all.

| Region | Start | End (excl.) | Content | Evidence |
|---|---|---|---|---|
| `.init` | 0x80004000 | 0x800064E0 | `__start`, `__init_hardware`, `memcpy` … | dtk names; `__ppc_eabi_init.cpp` and `__mem.c` match mlab |
| Game (Spyro) | 0x8000C4E0 | ~0x802F5BB8 | game classes | 628 static initializers point below 0x80355F60; class names such as `CKS08MenuCopyrights` (0x804BB910); `main` at 0x802F5BB8 |
| Engine (`CK*` classes) | ~0x802F5BB8 | 0x80355F60 | engine: sound (`CKSound*`), physics wrappers (`CKPx*`), text, quadtrees, input, cameras, FX | RTTI / class name strings used by the code of this range (`CKSoundManager`, `CKPxBody`, `CKQuadtree`, `CKInputAnchor`, `CKCameraConstraint` …), 104 static initializers; where game ends and engine starts is not known |
| Wii SDK (RVL) | 0x80355F60 | ~0x803EAF84 | OS, DVD, VI, PAD, AI, AX, AXFX, DSP, GX, EXI, SI, MEM, FS, IPC, NAND, SC, ARC, WPAD, WUD, BTE, USB, KPAD, TPL | matches mlab unit by unit (`RVL_SDK/os/OS.c` 0x803561AC … `RVL_SDK/kpad/KPAD.c` 0x803E801C-0x803EADD4, `RVL_SDK/tpl/TPL.c` 0x803EAE50-0x803EAF64, last function starting at 0x803EAF64); `fn_803EAE50` uses the TPL error string |
| … inside it: Runtime, MSL_C | ~0x803809A8 | ~0x80393BE8 | `Runtime.PPCEABI.H`, `MSL_C` (string, printf, scanf, math) | matches mlab (`__va_arg.c` 0x803809A8 … `s_tan.c` 0x80393900); `GCN_Mem_Alloc.c` string (0x804C27F0) used at 0x8038331C |
| … inside it: MetroTRK | ~0x80396A24 | ~0x8039C12C | MetroTRK | matches mlab (`mainloop.c` … `MWCriticalSection_gc.c`) |
| RenderWare | ~0x803EAF84 | ~0x80485310 | RenderWare Graphics (rasters, cameras), probably RW Audio | strings `rwRASTERFORMAT…` (0x804C4120 …), `Only rendering sub system`, `Invalid projection type specified` used by `fn_803EDD54`, `fn_803ED6B0`; `.RWS` stream name (0x804C01CF). Does not match mlab (except one function at 0x804117F0). Whether PhysX code is also here is unknown |
| HBM (Home Button menu) and `nw4hbm` | ~0x80485310 | ~0x804A4B84 | HBM, `nw4hbm::lyt`, `nw4hbm::ut` | matches the mlab range 0x802C5534-0x802E4408, which mlab places in its HBM area; `<< RVL_SDK - HBM` string (0x80514498), `nw4hbm::…` RTTI names (0x805151E8 …) |
| Wii SDK ESP | 0x804A4B84 | ~0x804A5278 | `ESP_*` | dtk names; matches mlab `RVL_SDK/esp/esp.c` (0x804A4B84-0x804A51A4, 10 functions) |
| Bink video | ~0x804A5278 | 0x804B7EC0 | Bink (RAD Game Tools) | matches the mlab range 0x802B3E88-0x802C3474 (Monster Lab plays `.bik` videos, `files/fmv/`); `Not a Bink file.` (0x804C590C) used at 0x804A6008 |

Open: the game / engine boundary, the SDK / RenderWare boundary (TPL, then
RenderWare from about 0x803EAF84), what lies around 0x804117F0, and where PhysX
(the `CKPx*` wrappers call into it) is linked.

## Units

MSL_C units not split yet: those whose code differs from mlab or is too short to
place. The float wrappers at 0x8038F680-0x8038F8A4 (small functions that call
`acos`, `atan`, `cos` …, probably float versions) are not identified yet.

Runtime.PPCEABI.H layout (`.text`): `__mem.c` (`strlen`), `__va_arg.c`,
`global_destructor_chain.c`, `New.cpp` (0x80380AD0-0x80380BC4), `NMWException.cpp`
(from 0x80380BC4), `ptmf.c`, `MWRTTI.cpp` (0x80381250-0x803814F8,
`__dynamic_cast`, `bad_cast`), `runtime.c`, `__init_cpp_exceptions.cpp`,
`Gecko_ExceptionPPC.cpp` (0x80381D50-0x80383498), `GCN_mem_alloc.c`. The order and the two
extra files are those of rb3 (`sdk/Runtime/*`); `extab` / `extabindex` are cut by the
functions they describe.

| Unit | Sections | Evidence |
|---|---|---|
| `RVL_SDK/os/OSAlloc.c` | `.text` 0x80357DA0-0x803580C8, `.sdata` 0x805CC068-0x805CC070, `.sbss` 0x805CE108-0x805CE118 | Matching; same layout as mlab (`DLInsert` first, `DLAddFront` / `DLExtract` inlined), plus `OSDestroyHeap` (0x803580A8, same body as tp's, after `OSCreateHeap` as in tp). `ArenaEnd`, `ArenaStart`, `NumHeaps`, `HeapArray` in mlab's `.sbss` order; `__OSCurrHeap` 4 bytes (dtk said 8). Starts after `OSGetAlarmUserData` (0x80357D98, `OSAlarm.c` not split) |
| `RVL_SDK/os/OSArena.c` | `.text` 0x803580C8-0x8035815C, `.sdata` 0x805CC070-0x805CC078, `.sbss` 0x805CE118-0x805CE120 | Matching; mlab's functions in mlab's order: `OSSetArenaHi` (0x80358108) and `OSAllocFromMEM1ArenaLo` (0x80358128) named by position; `OSAllocFromMEM2ArenaLo` dead-stripped. `__AIClockInit` follows (0x8035815C) |
| `game/unit_8032E43C.cpp` (IKAnchor) | `.text` 0x8032E43C-0x8032E5E4, `.ctors` 0x804B87FC-0x804B8800, `.data` 0x804F0288-0x804F02F8 (vtable), `.bss` 0x8052E6F0-0x8052E700, `.sbss` 0x805CDF60-0x805CDF68, `.sdata2` 0x805D23E8-0x805D23F0 | Matching. Start: after the `__sinit` of the previous unit (0x8032E3B8, `.ctors` 0x804B87F8); end: its own `__sinit` (0x8032E5A0). RTTI, base list and `vfC` / `vf5C` of IKAnchor are in the unit at 0x80327260 (weak copies, first unit wins) |
| `Runtime.PPCEABI.H/__mem.c` | `.init` 0x80004338-0x8000446C, `.text` 0x8038098C-0x803809A8 (`strlen`) | Matching; same code as mlab |
| `Runtime.PPCEABI.H/__va_arg.c` | `.text` 0x803809A8-0x80380A70 | Matching; same code as mlab |
| `Runtime.PPCEABI.H/global_destructor_chain.c` | `.text` 0x80380A70-0x80380AD0, `.sbss` 0x805CE5F0-0x805CE5F8 | Matching (objdiff 100 %, `main.dol: OK`) |
| `Runtime.PPCEABI.H/New.cpp` | `extab` 0x800064E0-0x80006514, `extabindex` 0x80008B80-0x80008B98, `.text` 0x80380AD0-0x80380BC4, `.rodata` 0x804C26B0-0x804C2708, `.data` 0x805061F8-0x80506220, `.sdata` 0x805CC1E0-0x805CC1F0, `.sbss` 0x805CE5F8-0x805CE600 | NonMatching: code 100 %, gap in `TASKS.md`. `operator new` (`__nw__FUl`), `std::bad_alloc` dtor, `what`, vtable and RTTI, `std::exception` RTTI; the exception-specification string `"!std::bad_alloc!!"` (0x804C26B0, pointed to by the `extab` of `operator new`) starts the `.rodata`. The functions from 0x80380BC4 belong to `NMWException.cpp` |
| `Runtime.PPCEABI.H/NMWException.cpp` | `extab` 0x80006514-0x8000655C, `extabindex` 0x80008B98-0x80008BD4, `.text` 0x80380BC4-0x803811D0, `.sdata` 0x805CC1F0-0x805CC1F8 | Matching; mlab's code from 0x80380E20, preceded by rb3's `std::dthandler`, `duhandler`, `terminate`, `unexpected` (`set_terminate` / `set_unexpected` dead-stripped), `__throw_catch_compare` and the `thandler` / `uhandler` pointers |
| `Runtime.PPCEABI.H/ptmf.c` | `.text` 0x803811D0-0x80381250 | Matching; `__ptmf_test`, `__ptmf_scall`, `__ptmf_scall4` |
| `Runtime.PPCEABI.H/MWRTTI.cpp` | `extab` 0x8000655C-0x8000656C, `extabindex` 0x80008BD4-0x80008BEC, `.text` 0x80381250-0x803814F8, `.rodata` 0x804C2718-0x804C2770, `.data` 0x80506220-0x80506248, `.sdata` 0x805CC1F8-0x805CC200 | NonMatching: code 100 %, data gap in `TASKS.md`. `__dynamic_cast` (calls `__throw`, 0x8038331C), `std::bad_cast` dtor and `what`, vtable and RTTI; `std::exception`'s RTTI (0x805CC1E8) sits before, with `New.cpp` |
| `Runtime.PPCEABI.H/runtime.c` | `.text` 0x803814F8-0x80381CE0, `.rodata` 0x804C2770-0x804C2788 | Matching |
| `Runtime.PPCEABI.H/__init_cpp_exceptions.cpp` | `.text` 0x80381CE0-0x80381D50, `.ctors$10` 0x804B7EC0, `.dtors$10` 0x804B88C0, `.dtors$15` 0x804B88C4, `.sdata` 0x805CC200-0x805CC208 | Matching (objdiff 100 %, `main.dol: OK`) |
| `Runtime.PPCEABI.H/Gecko_ExceptionPPC.cpp` | `extab` 0x8000656C-0x800065E0, `extabindex` 0x80008BEC-0x80008C40, `.text` 0x80381D50-0x80383498, `.rodata` 0x804C2788-0x804C27F0, `.data` 0x80506248-0x80506348, `.sdata` 0x805CC208-0x805CC210, `.bss` 0x8057ADA8-0x8057ADB8 | NonMatching: gap in `TASKS.md`. `__register_fragment` to `__end__catch` plus `std::bad_exception` dtor, `what`, vtable and RTTI; one fragment slot (`fragmentinfo`, 0x10 bytes of `.bss`) |
| `Runtime.PPCEABI.H/GCN_mem_alloc.c` | `.text` 0x80383498-0x80383608, `.rodata` 0x804C27F0-0x804C2860 | Matching; `__sys_alloc`, `__sys_free` with `InitDefaultHeap` inlined (same code as mscharged); string pool 0x6F bytes (dtk said 0x70). Callees named by their place in `OSAlloc.c` / `OSArena.c`, laid out as in mlab: `OSAllocFromHeap`, `OSFreeToHeap`, `OSInitAlloc`, `OSCreateHeap` (ref_match), `OSSetCurrentHeap` (0x80357FBC), `OSSetArenaLo` (0x80358120), `__OSCurrHeap` (0x805CC068) |
| `MSL_C/mem_funcs.c` | `.text` 0x80387070-0x80387340 | Matching; same code as mlab |
| `MSL_C/alloc.c` | `extab` 0x800065E0-0x80006630, `extabindex` 0x80008C40-0x80008CB8, `.text` 0x80383608-0x80384A40, `.rodata` 0x804C2860-0x804C2878, `.bss` 0x8057ADB8-0x8057ADF0, `.sbss` 0x805CE600-0x805CE608 | Matching. mlab's 12 functions plus `calloc` (0x80384980, 0xC0), which this DOL keeps and mlab's does not: it allocates `size * nmemb` from the malloc pool (`protopool`, `init`) and clears it with `memset`, the shape of MSL's `calloc`; it has its own `extabindex` entry and ends the unit (`ansi_files.c` matches from 0x80384A40) |
| `MSL_C/ansi_files.c` | `extab` 0x80006630-0x80006640, `extabindex` 0x80008CB8-0x80008CD0, `.text` 0x80384A40-0x80384B50, `.data` 0x80506348-0x80506488, `.bss` 0x8057ADF0-0x8057B0F0 | Matching; `__close_all`, `__flush_all` of mlab's five functions. `__files` (0x140) holds the three console `FILE`s, whose buffer pointers give `stdin_buff` (0x8057AFF0), `stdout_buff` (0x8057AEF0), `stderr_buff` (0x8057ADF0) and whose callbacks give `__read_console`, `__write_console`, `__close_console` (same code as mlab's) |
| `MSL_C/ansi_fp.c` | `extab` 0x80006640-0x80006678, `extabindex` 0x80008CD0-0x80008D24, `.text` 0x80384B50-0x803864C0, `.rodata` 0x804C2878-0x804C2958, `.data` 0x80506488-0x805065F0, `.sdata2` 0x805D2920-0x805D2958 | Matching; same code and data sizes as mlab |
| `MSL_C/scanf.c` | `extab` 0x80006730-0x80006748, `extabindex` 0x80008E38-0x80008E5C, `.text` 0x80389940-0x8038AEAC, `.rodata` 0x804C2E90-0x804C2EB8, `.data` 0x80506A38-0x80506B58 | Matching; same code and data sizes as mlab |
| `MSL_C/buffer_io.c` | `extab` 0x80006678-0x80006680, `extabindex` 0x80008D24-0x80008D30, `.text` 0x803864C0-0x803865A0 | Matching; `__prep_buffer`, `__flush_buffer` |
| `MSL_C/direct_io.c` | `extab` 0x80006680-0x80006688, `extabindex` 0x80008D30-0x80008D3C, `.text` 0x803865A0-0x803868A8 | Matching; `__fwrite` |
| `MSL_C/file_io.c` | `extab` 0x80006688-0x80006698, `extabindex` 0x80008D3C-0x80008D54, `.text` 0x803868A8-0x80386A98 | Matching; `fclose`, `fflush` |
| `MSL_C/FILE_POS.c` | `extab` 0x80006698-0x800066A0, `extabindex` 0x80008D54-0x80008D60, `.text` 0x80386A98-0x80386D08 | Matching; `_ftell`, `ftell`, `_fseek` (only `_fseek` has an `extabindex` entry) |
| `MSL_C/mbstring.c` | `extab` 0x800066A0-0x800066B0, `extabindex` 0x80008D60-0x80008D78, `.text` 0x80386D08-0x80386F00 | Matching; `mbtowc`, `__mbtowc_noconv`, `__wctomb_noconv`, `mbstowcs` (0x80386D88, absent from mlab's DOL), `wcstombs` |
| `MSL_C/mem.c` | `extab` 0x800066B0-0x800066B8, `extabindex` 0x80008D78-0x80008D84, `.text` 0x80386F00-0x80387070 | Matching; same code as mlab. `extab` / `extabindex` bounds of these MSL_C units: the `extabindex` entries (function, size, `extab` pointer) of the unit's functions |
| `MSL_C/math_api.c` | `extab` 0x800066B8-0x800066C8, `extabindex` 0x80008D84-0x80008D9C, `.text` 0x80387340-0x803873D8 | Matching; same code as mlab |
| `MSL_C/rand.c` | `.text` 0x80389920-0x80389940, `.sdata` 0x805CC218-0x805CC220 | Matching; `rand` (`srand` dead-stripped); `random_next` 4 bytes, dtk said 8 |
| `MSL_C/misc_io.c` | `.text` 0x803873D8-0x803873E8 | Matching; `__stdio_atexit` (`clearerr` dead-stripped) |
| `MSL_C/printf.c` | `extab` 0x800066C8-0x80006728, `extabindex` 0x80008D9C-0x80008E2C, `.text` 0x803873E8-0x803897B0, `.rodata` 0x804C2E60-0x804C2E90, `.data` 0x805067E8-0x80506A38, `.sdata` 0x805CC210-0x805CC218, `.sdata2` 0x805D2970-0x805D2978 | Matching; mlab's functions without `printf` and `fprintf`, same data sizes. `__lconv` (0x805065F0, referenced here, in data not split yet, as in mlab) is named by the run of data sizes it shares with mlab before `_current_locale` |
| `MSL_C/qsort.c` | `extab` 0x80006728-0x80006730, `extabindex` 0x80008E2C-0x80008E38, `.text` 0x803897B0-0x80389920 | Matching; same code as mlab |
| `MSL_C/string.c` | `extab` 0x80006750-0x80006758, `extabindex` 0x80008E68-0x80008E74, `.text` 0x8038AF5C-0x8038B43C, `.sdata` 0x805CC220-0x805CC228, `.sdata2` 0x805D2978-0x805D2980 | Matching; mlab's functions plus `strrchr` (0x8038B264, 0x48), between `strchr` and `strtok`: it scans with `lbzu`, keeps the last match of `chr & 0xFF` and returns the end of the string when `chr` is 0, the shape of MSL's `strrchr`. `.sdata` holds `strtok_null` / `strtok_ptr`, both pointing to `""` (`.sdata2`, 1 byte; dtk said 8) |
| `MSL_C/signal.c` | `extab` 0x80006748-0x80006750, `extabindex` 0x80008E5C-0x80008E68, `.text` 0x8038AEAC-0x8038AF5C, `.bss` 0x8057B0F0-0x8057B110 | Matching; `signal_funcs` has 7 entries (`raise` tests `sig > 7`), so 0x1C bytes plus padding |
| `MSL_C/strtold.c` | `extab` 0x80006758-0x80006760, `extabindex` 0x80008E74-0x80008E80, `.text` 0x8038B43C-0x8038C830, `.rodata` 0x804C2EB8-0x804C2EC8, `.sdata2` 0x805D2980-0x805D29A0 | Matching; `__strtold` (`atof` dead-stripped, so two doubles fewer in `.sdata2` than mlab). `"INFINITY"` is 9 bytes (dtk said 0x10). `lbl_805D29A0` belongs to the code at 0x8038DCB8, not to this unit. `__double_huge` (0x805CC230) named by its place after `__float_huge`, as in mlab |
| `MSL_C/strtoul.c` | `extab` 0x80006760-0x80006778, `extabindex` 0x80008E80-0x80008EA4, `.text` 0x8038C830-0x8038D1E8, `.data` 0x80506B58-0x80506BE0 | Matching (GC/3.0a5, as in mlab); `__strtoul`, `__strtoull`, `atoi` (0x8038D124; `strtoul` and `strtol` absent, `strtol` inlined into `atoi`) |
| `MSL_C/wmem.c` | `.text` 0x8038D1E8-0x8038D218 | Matching; `wmemcpy`, `wmemchr`; same code as mscharged |
| `MSL_C/wprintf.c` | `extab` 0x80006778-0x800067B0, `extabindex` 0x80008EA4-0x80008EF8, `.text` 0x8038D218-0x8038F3D4, `.rodata` 0x804C34C8-0x804C34D0, `.data` 0x80506BE0-0x80506E88, `.sdata2` 0x805D29A0-0x805D29A8 | Matching; mscharged's functions (same sizes) plus `long2str` (0x234) and `swprintf` (0x8038F2F8, 0xDC: `vswprintf` inlined, the shape of `snprintf` in `printf.c`); `vswprintf` absent. Wide string pool `lbl_80506E30` 0x56 bytes (dtk said 0x58), `lbl_804C34C8` 1 byte (dtk said 8) |
| `MSL_C/wstring.c` | `.text` 0x8038F3D4-0x8038F4B0 | Matching; `wcslen`, `wcscpy`, `wcsncpy`, `wcscmp`, `wcschr` (mlab's DOL lacks `wcscpy` and `wcschr`) |
| `MSL_C/wchar_io.c` | `.text` 0x8038F4B0-0x8038F534 | Matching; `fwide` (`__fwide` dead-stripped) |
| `MSL_C/uart_console_io_gcn.c` | `extab` 0x800067B0-0x800067B8, `extabindex` 0x80008EF8-0x80008F04, `.text` 0x8038F534-0x8038F60C, `.sbss` 0x805CE610-0x805CE618 | Matching; `__write_console`, `__close_console`; `initialized` 4 bytes (dtk said 8). Callees named from mlab matches: `__TRK_write_console` (0x8039B1B0), `InitializeUART` (0x8039DA5C), `WriteUARTN` (0x8039DAA4) |
| `MSL_C/abort_exit_ppc_eabi.c` | `extab` 0x800067B8-0x800067C0, `extabindex` 0x80008F04-0x80008F10, `.text` 0x8038F60C-0x8038F640, `.sbss` 0x805CE618-0x805CE620 | Matching; `__aborting`, `__stdio_exit` |
| `MSL_C/math_sun.c` | `extab` 0x800067C0-0x800067C8, `extabindex` 0x80008F10-0x80008F1C, `.text` 0x8038F640-0x8038F680 | Matching; `scalbn` |
| `MSL_C/extras.c` | `.text` 0x8038F8A4-0x8038F9A4 | Matching; `stricmp` (same code as mlab) and, before it, `strlwr` (0x8038F8A4, 0x58), absent from mlab: it lowers each byte in place through `_current_locale`'s `lower_map_ptr`, as `stricmp` does, the shape of MSL's `strlwr`. Written for this project |
| `MSL_C/e_acos.c` … `MSL_C/s_tan.c`, `MSL_C/e_sqrt.c` (21 fdlibm units) | `.text` 0x8038F9A4-0x80393BE0 with gaps; `.rodata`, `.sbss`, `.sdata2` per unit (see `splits.txt`) | Matching; same code and sizes as mlab |
| `MSL_C/e_exp.c` | `.text` 0x80390170-0x803903A4, `.rodata` 0x804C34D0-0x804C3500, `.sdata2` 0x805D2B10-0x805D2B88 | Matching (GC/3.0a5); fills the gap after `e_atan2.c`; `__ieee754_exp`, called by `exp` (`w_exp.c`). Absent from mlab; source from tp |
| `MSL_C/w_acos.c` … `MSL_C/w_pow.c` (8 units) | `.text` 0x80393978-0x80393998, 4 bytes each: `acos`, `asin`, `atan2`, `exp`, `fmod`, `log`, `log10`, `pow` | Matching; each is a `b __ieee754_<name>` (`-D_IEEE_LIBM`), fills the gap after `s_tan.c` |
| `MSL_C/math_ppc.c`, `MSL_C/w_sqrt.c` | `.text` 0x80393BE0-0x80393BE4 (`nan`), 0x80393BE4-0x80393BE8 (`sqrt`) | Matching; same order as mlab after `e_sqrt.c` |
