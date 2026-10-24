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

All bounds are hypotheses until the units are split and matched.

| Region | Start | End (excl.) | Evidence |
|---|---|---|---|
| Game (+ possible middleware) | 0x8000C4E0 | 0x80355F60 ? | 628 static initializers point below 0x80355F60; `main` at 0x802F5BB8; 104 of them point between `main` and 0x80355F60 |
| Wii SDK (RVL), Runtime, MSL_C, MetroTRK | 0x80355F60 | ? | `PPCMfmsr` 0x80355F60 (first SDK function named by dtk); `strlen` … `fwide` near 0x8038xxxx; `IOS_*`, `NAND*`, `SC*` near 0x8039xxxx-0x803Axxxx |
| Unknown (Bink? other middleware) | ? | 0x804B7EC0 | 7 static initializers (0x80381CE0, 0x804922B8 …); `ESP_*` near 0x804Axxxx |

## Units

| Unit | Sections | Evidence |
|---|---|---|
| `game/unit_8032E43C.cpp` (IKAnchor) | `.text` 0x8032E43C-0x8032E5E4, `.ctors` 0x804B87FC-0x804B8800, `.data` 0x804F0288-0x804F02F8 (vtable), `.bss` 0x8052E6F0-0x8052E700, `.sbss` 0x805CDF60-0x805CDF68, `.sdata2` 0x805D23E8-0x805D23F0 | Matching. Start: after the `__sinit` of the previous unit (0x8032E3B8, `.ctors` 0x804B87F8); end: its own `__sinit` (0x8032E5A0). RTTI, base list and `vfC` / `vf5C` of IKAnchor are in the unit at 0x80327260 (weak copies, first unit wins) |
| `Runtime.PPCEABI.H/global_destructor_chain.c` | `.text` 0x80380A70-0x80380AD0, `.sbss` 0x805CE5F0-0x805CE5F8 | Matching (objdiff 100 %, `main.dol: OK`) |
| `Runtime.PPCEABI.H/__init_cpp_exceptions.cpp` | `.text` 0x80381CE0-0x80381D50, `.ctors$10` 0x804B7EC0, `.dtors$10` 0x804B88C0, `.dtors$15` 0x804B88C4, `.sdata` 0x805CC200-0x805CC208 | Matching (objdiff 100 %, `main.dol: OK`) |
