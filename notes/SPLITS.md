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

| Unit | Sections | Evidence |
|---|---|---|
| `game/unit_8032E43C.cpp` (IKAnchor) | `.text` 0x8032E43C-0x8032E5E4, `.ctors` 0x804B87FC-0x804B8800, `.data` 0x804F0288-0x804F02F8 (vtable), `.bss` 0x8052E6F0-0x8052E700, `.sbss` 0x805CDF60-0x805CDF68, `.sdata2` 0x805D23E8-0x805D23F0 | Matching. Start: after the `__sinit` of the previous unit (0x8032E3B8, `.ctors` 0x804B87F8); end: its own `__sinit` (0x8032E5A0). RTTI, base list and `vfC` / `vf5C` of IKAnchor are in the unit at 0x80327260 (weak copies, first unit wins) |
| `Runtime.PPCEABI.H/global_destructor_chain.c` | `.text` 0x80380A70-0x80380AD0, `.sbss` 0x805CE5F0-0x805CE5F8 | Matching (objdiff 100 %, `main.dol: OK`) |
| `Runtime.PPCEABI.H/__init_cpp_exceptions.cpp` | `.text` 0x80381CE0-0x80381D50, `.ctors$10` 0x804B7EC0, `.dtors$10` 0x804B88C0, `.dtors$15` 0x804B88C4, `.sdata` 0x805CC200-0x805CC208 | Matching (objdiff 100 %, `main.dol: OK`) |
