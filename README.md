The Legend of Spyro: Dawn of the Dragon (Wii)
=============================================

A work-in-progress matching decompilation of The Legend of Spyro: Dawn of the Dragon
for the Wii.

This repository does **not** contain any game assets or assembly whatsoever. An existing
copy of the game is required.

Supported versions:

- `RO8P7D`: Rev 0 (Europe)

Progress
========

| Release | Game ID | Progress |
|---|---|---|
| Spyro: Dawn of the Dragon (Europe) | `RO8P7D` | [![Fuzzy](progress/RO8P7D/fuzzy.svg)](notes/PROGRESS.md) [![Perfect](progress/RO8P7D/perfect.svg)](notes/PROGRESS.md) [![Linked](progress/RO8P7D/linked.svg)](notes/PROGRESS.md) |
| Spyro: Dawn of the Dragon (Scandinavia) | `RO8X7D` | not supported yet |
| Spyro: Dawn of the Dragon (USA) | `RO8E7D` | not supported yet |

[![Progress card](progress/RO8P7D/card.svg)](notes/PROGRESS.md)

- **Fuzzy**: objdiff fuzzy match score over all code.
- **Perfect**: code that matches byte for byte.
- **Linked**: code linked into the matching `main.dol`.

The card counts every function of the DOL, split or not: each region total is the
code between the region bounds of `notes/SPLITS.md` (approximate for game / engine and
SDK / RenderWare). The badges and the card are drawn from the objdiff report by
`tools/progress_badges.py`, one folder per version. After a build, `python tools/progress_badges.py --version <ID> --record`
redraws `progress/<ID>/` and adds the current commit to `progress/<ID>/history.csv`;
commit the `progress/` folder with it.

Dependencies
============

Windows
-------

On Windows, it's **highly recommended** to use native tooling. WSL or msys2 are **not**
required. When running under WSL, [objdiff](#diffing) is unable to get filesystem
notifications for automatic rebuilds.

- Install [Python](https://www.python.org/downloads/) and add it to `%PATH%`.
- Download [ninja](https://github.com/ninja-build/ninja/releases) and add it to `%PATH%`.
  - Quick install via pip: `pip install ninja`

macOS
-----

- Install [ninja](https://github.com/ninja-build/ninja/wiki/Pre-built-Ninja-packages):

  ```sh
  brew install ninja
  ```

[wibo](https://github.com/decompals/wibo), a minimal 32-bit Windows binary wrapper, will
be automatically downloaded and used.

Linux
-----

- Install [ninja](https://github.com/ninja-build/ninja/wiki/Pre-built-Ninja-packages).

[wibo](https://github.com/decompals/wibo) will be automatically downloaded and used.

Building
========

- Clone the repository:

  ```sh
  git clone https://github.com/YggdrasziI/spyro-dotd-decomp.git
  ```

- Copy your game's disc image to `orig/RO8P7D`.
  - Supported formats: ISO (GCM), RVZ, WIA, WBFS, CISO, NFS, GCZ, TGC
  - After the initial build, the disc image can be deleted to save space.

- Configure:

  ```sh
  python configure.py
  ```

- Build:

  ```sh
  ninja
  ```

Diffing
=======

Once the initial build succeeds, an `objdiff.json` should exist in the project root.

Download the latest release from [encounter/objdiff](https://github.com/encounter/objdiff).
Under project settings, set `Project directory`. The configuration should be loaded
automatically.

Select an object from the left sidebar to begin diffing. Changes to the project will
rebuild automatically: changes to source files, headers, `configure.py`, `splits.txt` or
`symbols.txt`.

![](assets/objdiff.png)

Based on [encounter/dtk-template](https://github.com/encounter/dtk-template).
