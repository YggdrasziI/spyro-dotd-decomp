# Matching techniques

Techniques found on this project, each with the unit where it was proven (game code
GC/3.0a5.2, see `notes/COMPILER.md`; library units with their own flags). The
catalogue of Monster Lab (same compiler) in `mlab-decomp/notes/MATCHING.md` and the
digest `tools/common/docs/mwcceppc.md` are leads: a technique proven there is a
hypothesis here until a function of this game matches with it.

## Loads, aliasing and `const`

## Registers and stack

- `-opt nopeephole` (per unit) signs: vtable address built in `r0`
  (`addi r0, r4, ...`), epilogue `lwz r0` before `lwz r31`, `extsh` + `cmpwi` kept
  apart, no `mr.` (`unit_8032E43C`). Code near 0x8000CB40 has the opposite (peephole
  on).

## Floats

## Inlining and emission order

- RTTI (`__RTTI__<class>` in `.sdata`, name strings and base lists in `.data`) is
  emitted as weak or local copies in every unit that emits a vtable; the linker keeps
  the first unit's copy and strips the others. Rename the RTTI symbols in
  `symbols.txt` to the compiler's names and leave them in the unit that holds them
  (`unit_8032E43C`: IKAnchor RTTI lives in the unit at 0x80327260).
- Virtual functions that the DOL has only in another unit (probably inline in the
  original header): declare them out of line so this unit does not emit copies
  (`vfC`, `vf5C` of IKAnchor).

## Data layout

- A dtk-inferred object size can include the alignment padding after the object;
  objdiff then scores the data below 100 %. Set the size from the code or from the
  compiled object (`signal.c`: `signal_funcs` 0x1C, dtk said 0x20; `ansi_fp.c`:
  `@stringBase0` 0xDD, dtk said 0xE0; `alloc.c`: `init` 1 byte, dtk said 8; `string.c`: `""` in `.sdata2` 1 byte, dtk
  said 8). dtk may also make the padding its own `lbl_` symbol at the end of a
  section: remove it when nothing uses it (`dvdDeviceError.c`, `.rodata` 0x804C26AC).
- Compiler-generated data names (`@980`, `pow_10$560`, `protopool$244`) are paired by
  position; the `lbl_` names can stay, only the sizes must agree.

- Library sources may define functions this DOL lacks; the linker dead-strips
  unreferenced functions, so leave them in (`ptmf.c`, `runtime.c`). Exception: a
  function compiled with `-Cpp_exceptions on` leaves its `extab` / `extabindex`
  entries in the object and objdiff scores the unit's data below 100 %; put such
  functions under `#if 0` (`ansi_files.c`, `buffer_io.c`, `direct_io.c`, `file_io.c`).
  Same for a function whose string literals are absent from the DOL's `.data`: the
  linker strips them with it, objdiff does not (`SIGetTypeString` in `SIBios.c`), and for float
  constants in `.sdata2` (`C_MTXPerspective` in `mtx44.c`).
- A `static inline` function that the DOL also keeps as a global function: make it a
  plain global function; under `-ipa file` the compiler still inlines it into earlier
  callers (`VIGetScanMode` into `VIInit`).
- Data below 100 % with identical bytes: look for a relocation dtk invented in the
  target object (`objdump -r` on `build/RO8P7D/obj/<unit>.o`) and block it in
  `config.yml` (`gammaSet` in `vi3in1.c`).
  Conversely, re-enable a function mlab disabled when this DOL has it (`mbstowcs` in
  `mbstring.c`). A function the DOL lacks but that a kept function inlines is marked
  `inline` instead, so it is still inlined but not emitted (`strtol` in `strtoul.c`,
  as mlab did for `strtod` in `strtold.c`).

- Strings of dead-stripped functions kept in the DOL's `.data` (the linker strips the
  function, not the string pool): emit them from a stand-in function at the same place
  in the file, as tp's `OSNet.c` does with `dummyStrings` (`OSLaunch.c`).
- A constant that looks like an address (`OSPhysicalToCached(0x4000)` = 0x80004000)
  gets a dtk relocation to the symbol there; block it with `block_relocations` in
  `config.yml` (`OSInit` in `OS.c`).
- Porting a reference library unit by unit: pair each relocation of the reference's
  compiled object with this DOL's reference at the same offset of the same function;
  this gives every data section's start and the names of referenced symbols
  (RVL_SDK `os/`). Then copy the data symbol sizes of the compiled object into
  `symbols.txt` (dtk merges or splits strings and pads sizes). `tools/ref_port.py`
  does both (`plan`, `names`, `fixdata`; see `notes/REFERENCES.md`).

- `mullw rD, rD, rB` versus `mullw rD, rB, rD`: swap the operands of `*` in the
  source (`calloc` in `alloc.c`: `size * nmemb`).
- `add` operands swapped in an inlined rounding macro that swapping the source
  operands does not fix: try another reference's version of the function, written with
  separate statements (`OSAllocFromMEM1ArenaLo` in `OSArena.c`: tp's version matches,
  mlab's does not).

## Control flow

- `beq` over an unconditional `b` to the common return (`vf30__8IKAnchor`): a
  `switch` with a single `case 0` under `-opt nopeephole`; `if (!x)` gives `bne`.

## Bit fields and hardware registers

## Unsolved patterns
