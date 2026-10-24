# Compiler, SDK and runtime — evidence

The linker family is proven (GC 3.0, see "Linker test" below). The game-code
compiler is GC/3.0a5.2 by elimination on small functions (see "Game-code compiler
test" below); flags differ between at least two regions.

## Disc

| Info | Value | Evidence |
|---|---|---|
| ID | `RO8P7D` | `disc/header.bin` bytes 0-5 |
| Region | PAL / Europe | 4th character of the ID is `P` |
| Revision | 0 | `disc/header.bin` byte 7 = `0x00` |
| Internal name | `SPYRO08` | `disc/header.bin` offset 0x20 |
| RELs | none | no `.rel` in `files/` |
| `.map` / `.elf` | none | no `.map`, `.elf` or `.sym` in `files/` |

## Wii SDK (`<< RVL_SDK - … >>` strings)

Offsets are file offsets in `main.dol`.

| Offset | Library | Build | Tag |
|---|---|---|---|
| 0x4ee1e8 | OS | Jan 30 2008 01:38:43 | 0x4199_60831 |
| 0x4fc0b0 | DVD | Aug  8 2007 01:59:13 | 0x4199_60831 |
| 0x4fd9b8 | VI | Aug  8 2007 02:07:17 | 0x4199_60831 |
| 0x4fe4a0 | AI | Aug  8 2007 01:58:12 | 0x4199_60831 |
| 0x4fe4e8 | AX | Aug  8 2007 01:58:18 | 0x4199_60831 |
| 0x501970 | DSP | Aug  8 2007 01:59:06 | 0x4199_60831 |
| 0x501b40 | GX | Dec 11 2007 01:34:15 | 0x4199_60831 |
| 0x502f68 | EXI | Aug  8 2007 01:59:22 | 0x4199_60831 |
| 0x502fb0 | SI | Aug  8 2007 02:07:10 | 0x4199_60831 |
| 0x503220 | NAND | Dec 11 2007 01:35:48 | 0x4199_60831 |
| 0x503468 | SC | Aug  8 2007 02:09:03 | 0x4199_60831 |
| 0x503708 | WPAD | Dec 11 2007 01:35:07 | 0x4199_60831 |
| 0x50c2f8 | KPAD | Aug  8 2007 02:05:53 | 0x4199_60831 |
| 0x510578 | HBM | Jun 16 2008 18:35:58 | 0x4199_60831 |

The same tag and build dates appear in Monster Lab (`RM7P4F`), whose game code was
proven to use mwcc GC 3.0 (3.0a3 … 3.0a5.2). This is a lead for Spyro, not evidence.

## Other libraries (strings)

| Offset | String | Library |
|---|---|---|
| 0x4bf8f8 | `MetroTRK for Revolution v0.1` | MetroTRK |
| 0x4be906 | `Metrowerks CW runtime library initializing default heap` | Runtime / MSL |
| 0x4c19ec | `Not a Bink file.` | Bink video (RAD Game Tools) |
| 0x4b6674 | `Vivendi Games` | game (publisher string) |

## Runtime and CodeWarrior hints

- Symbols named by dtk: `__init_cpp_exceptions` (0x80381CE0), `__fini_cpp_exceptions`
  (0x80381D1C), `__init_cpp_exceptions_reference` (.ctors 0x804B7EC0),
  `__destroy_global_chain_reference` (.dtors 0x804B88C0),
  `__fini_cpp_exceptions_reference` (.dtors 0x804B88C4), `fragmentID` (.sdata
  0x805CC200): the template's "GC 2.7+ and Wii linkers" layout (two `.dtors` entries).

## Linker test (2026-10-24)

Setup: `global_destructor_chain.c` and `__init_cpp_exceptions.cpp` split and linked
(objdiff 100 % code and data with every compiler below), `mw_comment_version: 15`,
`linker_version` (also used for the runtime units) changed one at a time.

| Linker | Result |
|---|---|
| GC/2.6 | `main.dol: FAILED` |
| GC/2.7 | internal linker error (`ELF_gen.c` line 672) |
| GC/3.0a3, 3.0a3.2, 3.0a3.3, 3.0a3.4, 3.0a5, 3.0a5.2 | `main.dol: OK` |
| Wii/0x4201_127, 1.0, 1.1, 1.3, 1.7 | `main.dol: FAILED`: DOL 32 bytes longer, header and section layout differ |

Conclusion: the linker belongs to the GC 3.0 family. These two units do not tell
3.0a3 … 3.0a5.2 apart. `GC/3.0a5.2` is kept as a working choice (same choice and same
reason as in Monster Lab: SDK tag `0x4199_60831`); not proven.

Without `#pragma force_active on` around the `.ctors$10` / `.dtors$15` references,
the linker strips them and `.ctors` / `.dtors` shift (`main.dol: FAILED`).

## Game-code compiler test (2026-10-24)

Method: scratch C++ (not in the repository) compiled with every mwcc in
`build/compilers/GC` and `build/compilers/Wii`, base flags of `configure.py` plus
`-RTTI on`, then compared word by word to the original functions (relocated fields
masked, trailing padding ignored).

Classes, from RTTI (`__RTTI` objects in `.sdata`, names in `.rodata`): vtable
`lbl_804F0288` → RTTI `lbl_805CBDC0` → `"IKAnchor"` (0x804C1BC0), base list
`lbl_804EF950` → `"IKSerializable"` (0x804B8910) → `"IKBaseClass"` (0x804B8920).
The vtable `lbl_804C82A8` stored by `fn_8000CB40` points to the `IKSerializable` RTTI,
so `fn_8000CB40` is very likely `IKSerializable::IKSerializable()` and `fn_8032E43C`
`IKAnchor::IKAnchor()` (not renamed yet).

| Function | Test source | Flags | Matches with |
|---|---|---|---|
| `fn_8000CB40` (ctor, calls base ctor, stores vtable) | `B::B() {}` | default | GC 3.0a3 … 3.0a5.2, all Wii; not GC ≤ 2.7 |
| `fn_8000CB40` | same | `-opt nopeephole` | none |
| `fn_8032E43C` (ctor) | `IK::IK() {}` | `-opt nopeephole` | GC 3.0a5.2, all Wii; not GC 3.0a3 … 3.0a5, not GC ≤ 2.7 |
| `fn_8032E43C` | same | default | none (`addi r4` instead of `addi r0`, epilogue order) |
| `fn_8032E478` (deleting dtor) | `IK::~IK() {}` | `-opt nopeephole` | GC 3.0a3 … 3.0a5.2, all Wii |
| `fn_8032E520` (calls base, then `beq` over `b`) | `switch (c) { case 0: …; break; } return 1;` | `-opt nopeephole` | GC 2.0 … 3.0a5.2; not Wii (one instruction shorter) |
| `fn_8032E4D4`, `fn_8032E4D8`, `fn_8032E590` | trivial | `-opt nopeephole` | all GC 3.0 and Wii |

Conclusions:

- Game code near 0x8032E43C: **GC/3.0a5.2** is the only compiler that matches both
  `fn_8032E43C` and `fn_8032E520`, with **`-opt nopeephole`** (or a flag with the same
  effect). This rests on the test sources being the original forms: a different
  source for `fn_8032E520` could still match on a Wii compiler. Same build number
  (60831) as the SDK tag `0x4199_60831`.
- Code near 0x8000CB40 is built **with** the peephole optimizer: at least two flag
  sets exist (likely two libraries or two parts of the engine).

## Candidates

| Part | Candidates | Status |
|---|---|---|
| Linker | GC 3.0a3 … 3.0a5.2 | family proven, exact version open |
| Runtime.PPCEABI.H | GC 3.0a3 … 3.0a5.2 (2 small units only) | partial |
| MSL_C | — | not tested |
| MetroTRK | — | not tested |
| RVL_SDK | — | not tested |
| Game code | GC/3.0a5.2; `-opt nopeephole` near 0x8032E43C, peephole on near 0x8000CB40 | strong (scratch tests), to confirm with a linked unit |
