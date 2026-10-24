# Compiler, SDK and runtime — evidence

Nothing about the compiler is proven yet. `configure.py` holds the dtk-template
defaults (`GC/1.3.2` linker, `mw_comment_version: 15` in `config/RO8P7D/config.yml`);
they are placeholders until a matching unit settles them.

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

## Candidates

| Part | Candidates | Status |
|---|---|---|
| Linker / `mw_comment_version` | — | not tested |
| Runtime.PPCEABI.H, MSL_C | — | not tested |
| MetroTRK | — | not tested |
| RVL_SDK | — | not tested |
| Game code | — | not tested |
