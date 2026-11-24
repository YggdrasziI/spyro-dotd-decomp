# References

## Tools

- [encounter/dtk-template](https://github.com/encounter/dtk-template): project
  skeleton (`configure.py`, ninja); its docs cover dependencies, getting started,
  symbols, splits, GitHub Actions, common BSS and the `.comment` section.
- [encounter/decomp-toolkit](https://github.com/encounter/decomp-toolkit) (dtk):
  DOL analysis, `symbols.txt` / `splits.txt`, final match check.
- [encounter/objdiff](https://github.com/encounter/objdiff): local diff (reads
  `objdiff.json`).
- [YggdrasziI/decomp-tools](https://github.com/YggdrasziI/decomp-tools) and
  [YggdrasziI/wii-decomp-tools](https://github.com/YggdrasziI/wii-decomp-tools) (the
  owner's own projects, CC0-1.0): submodules `tools/common` and `tools/wii`, settings
  in `decomp.toml`. They replace this project's former copies of the report, compare
  and badge scripts, of dtk-template's build generator and of `unit_candidates.py`,
  `compiler_sweep.py`, `ref_match.py` and `ref_port.py`.
- [decomp.me](https://decomp.me): shared scratches and compiler tests.
- [decompals/wibo](https://github.com/decompals/wibo) (runs mwcc on Linux),
  [encounter/sjiswrap](https://github.com/encounter/sjiswrap) (UTF-8 to Shift-JIS).
- Ghidra (Gekko/Broadway module) and the Dolphin debugger to understand behaviour;
  Dolphin to extract the disc.
- Discord "GC/Wii Decompilation" (`#dtk` channel).

## Reference projects

When reusing code, record the commit it was taken from and the license in
`notes/PROVENANCE.md`.

Wii:

| Folder | Project | State |
|---|---|---|
| `mscharged-decomp` | [Mario Strikers Charged](https://github.com/yannicksuter/mscharged-decomp) (CC0) | 100 % |
| `Petari` | [Super Mario Galaxy](https://github.com/SMGCommunity/Petari) (CC0) | 100 % |
| `oot-vc` | [N64 Emulator for Wii](https://github.com/zeldaret/oot-vc) | partial |
| `pik2wii` | [New Play Control! Pikmin 2](https://github.com/projectPiki/pik2wii) | partial |
| `rb3` | [Rock Band 3](https://github.com/DarkRTA/rb3) | partial |
| `pik1wii` | [New Play Control! Pikmin](https://github.com/projectPiki/pik1wii) | partial |
| `ss` | [Skyward Sword](https://github.com/zeldaret/ss) | partial |
| `Garigari` | [Super Mario Galaxy 2](https://github.com/SMGCommunity/Garigari) | partial |
| `NSMBW-Decomp` | [New Super Mario Bros. Wii](https://github.com/NSMBW-Community/NSMBW-Decomp) | partial |
| `mkw` | [Mario Kart Wii](https://github.com/doldecomp/mkw) | partial |
| `Castaway` | [The Sims 2: Castaway](https://github.com/HaydnTrigg/Castaway) | partial |

GameCube:

| Folder | Project | State |
|---|---|---|
| `tp` | [Twilight Princess](https://github.com/zeldaret/tp) | 100 % |
| `melee` | [Super Smash Bros. Melee](https://github.com/doldecomp/melee) | 100 % |
| `SFA-Decomp` | [Star Fox Adventures](https://github.com/zcanann/SFA-Decomp) | 100 % |
| `pikmin` | [Pikmin](https://github.com/projectPiki/pikmin) | 100 % |
| `smstrikers-decomp` | [Super Mario Strikers](https://github.com/yannicksuter/smstrikers-decomp) | 100 % |
| `ac-decomp` | [Animal Crossing](https://github.com/ACreTeam/ac-decomp) | 100 % |
| `marioparty4` | [Mario Party 4](https://github.com/mariopartyrd/marioparty4) | 100 % |
| `oot-gc` | [N64 Emulator for GameCube](https://github.com/zeldaret/oot-gc) | 100 % |

The `doldecomp` organization hosts reusable libraries (SDK, JSystem...); check the
version of each library against this DOL.

## Finding library code by comparison

`tools/wii/ref_match.py <project root> <ID>` compares this game's functions with another
dtk project's (symbol operands and local branch offsets normalized) and prints runs of
matched functions with the reference unit names. Monster Lab
(`mlab-decomp`, `RM7P4F`, same RVL_SDK build tag) gives the region map
of `notes/SPLITS.md`; its `build/RM7P4F/asm` must exist (`ninja` there).

`tools/wii/ref_port.py <project root> <ID> <command>` ports a reference library unit by
unit (it needs the reference's compiled objects, `build/<ID>/src`): `place` shows one
unit (functions here, data section starts, names), `plan` prints `splits.txt` blocks
for a group of units with warnings, `names --write` gives reference names to generic
labels, `fixdata` copies the data symbols of a compiled unit into `symbols.txt`.
Workflow used for RVL_SDK `os/`: `plan`, copy the blocks to `splits.txt`, `names
--write`, copy the sources, build every unit `NonMatching`, `fixdata` the units whose
code matches, then switch the 100 % units to `Matching`. Static names that repeat
across units (`Callback`, `Prepared`) are skipped by `names`; give them by hand.

## Reuse permissions

- CC0 references (mscharged-decomp, Petari, TP) come first.
- `DarkRTA/rb3` (no license file): reuse allowed by the owner (granted for
  mlab-decomp on 2026-10-12, extended to this project on 2026-10-24) when the CC0
  references lack a source.
- `zeldaret/oot-vc` (no license file): reuse allowed by the owner (granted for
  mlab-decomp on 2026-10-14, extended to this project on 2026-10-24), same conditions.
- `YggdrasziI/mlab-decomp` (private, same owner): its library units (Runtime, MSL_C,
  MetroTRK, RVL_SDK with the same tag `0x4199_60831`) are a first place to look; log
  the original source of each file it took from elsewhere.
- Any other project without a known license needs the owner's approval first.
- Every reuse is logged in `notes/PROVENANCE.md` (file, commit, changes, license or
  its absence).
