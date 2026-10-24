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

None split yet.
