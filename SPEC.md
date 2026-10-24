# Spyro: Dawn of the Dragon decompilation — specification

## Goal

Rebuild The Legend of Spyro: Dawn of the Dragon (Wii) from C/C++ source written from
scratch so that, compiled with the original compiler and flags, it produces a
`main.dol` identical byte for byte to the original.

Out of scope: a PC port, game assets, any redistribution of game files.

## Target binary

| Item | Value | Evidence |
|---|---|---|
| Game ID | `RO8P7D` (PAL Europe, "Europe (En,Fr,De,Es,It,Nl)") | `disc/header.bin` bytes 0-5 |
| Revision | 0 | `disc/header.bin` byte 7 = `0x00` |
| Internal name | `SPYRO08` | `disc/header.bin` offset 0x20 |
| `main.dol` SHA-1 | `516dfa405567beec1e08cee1df4f7c156b7f43e9` | `config/RO8P7D/build.sha1` |
| RELs | none | no `.rel` in `files/` |
| `.map` / `.elf` | none | no `.map`, `.elf` or `.sym` on the disc |
| Entry point | `0x8000403C` (`__start`) | DOL header |
| Main `.text` | `0x8000C4E0` – `0x804B7EC0` (0x4AB9E0 bytes) | DOL header |
| Build date | unknown | — |

## Other versions

The project is set up for three versions; only `RO8P7D` is enabled. The others stay in
`DISABLED_VERSIONS` (`configure.py`) until the owner decides to support them.

| ID | Region | `main.dol` SHA-1 | Difference from `RO8P7D` | Status |
|---|---|---|---|---|
| `RO8P7D` | Europe (En,Fr,De,Es,It,Nl) | `516dfa40…` | — | enabled, reference version |
| `RO8X7D` | Scandinavia (En,Sv,No,Da,Fi) | `09e239e6b20a1f001a8a0f70b9f838c2f66991c0` | one byte: product code `"RVL-RO8X"` instead of `"RVL-RO8P"` (`.rodata` 0x804BA5AB); same sections and addresses | disabled |
| `RO8E7D` | USA (En,Fr,Es) | `e306b21b16e4caaedbe32896bbc0856374966792` | separate build: `.text` 0x200 bytes shorter, `.rodata` 0x20 longer, later sections shifted; `.init`, `extab`, `extabindex` differ | disabled |

All three discs are revision 0 with no RELs (`disc/header.bin`, `files/`).

Model (after `zeldaret/tp`):

- `configure.py`: `VERSIONS` (index = `BUILD_VERSION`, only append), `DISABLED_VERSIONS`,
  groups `ALL_PAL`, `ALL_USA`, `ALL`; `MatchingFor(...)` accepts IDs and groups.
- Source: one `src/` for all versions; differences under `#if` with the names of
  `include/version.h` (`BUILD_VERSION == VERSION_SCA`, `REGION_PAL`, `REGION_USA`),
  never a raw number.
- Per version: `config/<ID>/` (own `symbols.txt` / `splits.txt` once enabled),
  `orig/<ID>/`, a CI matrix entry and its `main.dol` in the build repository.
- Scripts take `--version` (default `RO8P7D`); progress badges and history are kept
  per version in `progress/<ID>/`, one README row each (after `Yotona/twewy`).

## Toolchain

Evidence and the candidate analysis go in `notes/COMPILER.md`.

- Linker: **GC 3.0 family** (3.0a3 … 3.0a5.2 all link a matching DOL; Wii 1.x,
  GC 2.7 and GC 2.6 do not, see `notes/COMPILER.md`). `configure.py` uses
  `GC/3.0a5.2` with `mw_comment_version: 15`, a working choice inside that family.
- Game-code compiler: **GC/3.0a5.2** by elimination on small functions, with
  `-opt nopeephole` in at least one region and peephole on in another
  (`notes/COMPILER.md`); to confirm with a linked game unit.
- Wii SDK: RVL_SDK libraries built August 2007 to January 2008, tag `0x4199_60831`
  (version strings in `main.dol`, e.g. OS at file offset 0x4EE1E8). Commercial SDK
  version name unknown.
- Game code: flags to be established per family of units, each exception justified
  in the unit's header comment.

## Acceptance criteria

- Every build ends with `build/RO8P7D/main.dol: OK` (`ninja`, checked against
  `config/RO8P7D/build.sha1`), locally and in CI.
- A unit is `Matching` in `configure.py` only when objdiff reports 100 % for all its
  functions and data and the linked DOL still matches. Anything else stays
  `NonMatching`, with the remaining gap written in `TASKS.md`.
- A split that builds proves the bytes, not the translation unit: a TU boundary is
  proven only once the unit is decompiled and matches (`notes/SPLITS.md`).
- Every name, compiler fact or structure layout rests on evidence (RTTI, assertion
  or debug strings with their offset, symbols from another project on the same
  library, an objdiff diff, a build result). Without evidence it is labelled a
  hypothesis.
- Reused code from another project is logged with its commit and license in
  `notes/PROVENANCE.md`.

## Naming conventions

- Game units: `src/game/unit_<start address>.cpp` while real file names are unknown;
  the unit table with bounds and contents is in `notes/SPLITS.md`.
- Unknown classes and structs: `Unk<Name>` or `Unk<address>`; unknown methods keep
  the address: `fn_<address>` (mangled as a member, e.g.
  `fn_80012345__10UnkExampleFv`); virtual functions are `vfXX` after their vtable
  offset.
- Real names only from evidence: RTTI class names, strings, symbols of other projects
  on the same library.
- Code, comments, notes and commit messages are in English.
- Shared game headers go in `include/game/` (listed here as they are added).
  `include/version.h` holds the version names used in `#if`.

## Repository layout

```
configure.py              project configuration and build.ninja generator
config/<ID>/              dtk config per version: config.yml, symbols.txt, splits.txt,
                          build.sha1 (RO8X7D, RO8E7D: build.sha1 only while disabled)
orig/<ID>/                original game files (git-ignored, never committed)
build/                    build output (git-ignored)
src/  include/  libs/     sources and headers (game, SDK, runtime, MSL), when added
tools/                    shared scripts (progress badges, report and asm helpers)
progress/<ID>/            progress badges and history per version (README images)
notes/                    reference documentation (see CLAUDE.md routing table)
.claude/skills/           project workflows (decomp-manager, decomp-unit,
                          unit-readiness)
.github/workflows/        CI: split, link and check main.dol in a private image
```

## Build

```
python configure.py       # generate build.ninja (options: --version RO8P7D, --map)
ninja                     # split, compile, link, check main.dol, write the report
```

Dependencies: Python and ninja (see `README.md`); on Windows use native tools, not
WSL. Outputs: `build/RO8P7D/report.json` (objdiff report), `objdiff.json` for the
objdiff GUI, disassembly of every unit under `build/RO8P7D/asm/`.
