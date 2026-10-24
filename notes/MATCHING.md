# Matching techniques

Techniques found on this project, each with the unit where it was proven. Empty
until the first units are decompiled; the catalogue of Monster Lab (mwcc GC 3.0a5.2)
in `mlab-decomp/notes/MATCHING.md` is a lead once the compiler is identified.

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
  said 8).
- Compiler-generated data names (`@980`, `pow_10$560`, `protopool$244`) are paired by
  position; the `lbl_` names can stay, only the sizes must agree.

- Library sources may define functions this DOL lacks; the linker dead-strips
  unreferenced functions, so leave them in (`ptmf.c`, `runtime.c`). Exception: a
  function compiled with `-Cpp_exceptions on` leaves its `extab` / `extabindex`
  entries in the object and objdiff scores the unit's data below 100 %; put such
  functions under `#if 0` (`ansi_files.c`, `buffer_io.c`, `direct_io.c`, `file_io.c`).
  Conversely, re-enable a function mlab disabled when this DOL has it (`mbstowcs` in
  `mbstring.c`).

- `mullw rD, rD, rB` versus `mullw rD, rB, rD`: swap the operands of `*` in the
  source (`calloc` in `alloc.c`: `size * nmemb`).

## Control flow

- `beq` over an unconditional `b` to the common return (`vf30__8IKAnchor`): a
  `switch` with a single `case 0` under `-opt nopeephole`; `if (!x)` gives `bne`.

## Bit fields and hardware registers

## Unsolved patterns
