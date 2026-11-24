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
means `tools/ref_match.py <mlab-decomp> RM7P4F` (2026-10-24) found
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

MSL_C units not split yet: those whose code differs from mlab or is too short to
place. The float wrappers at 0x8038F680-0x8038F8A4 (small functions that call
`acos`, `atan`, `cos` …, probably float versions) are not identified yet.

RVL_SDK starts with `base/PPCArch.c` (0x80355F60) and `db/db.c` (0x803560C4), right
before `os/OS.c`; mlab links `db.c` later, after `si/`.

RVL_SDK `os/` layout: mlab's order and file names, from `OS.c` (0x803561AC) to
`__ppc_eabi_init.cpp` (ends 0x80364660); data placed by pairing the relocations of
mlab's compiled objects with this DOL's references. `time.dolphin.c` (`__get_time`) is
absent from this DOL.

Runtime.PPCEABI.H layout (`.text`): `__mem.c` (`strlen`), `__va_arg.c`,
`global_destructor_chain.c`, `New.cpp` (0x80380AD0-0x80380BC4), `NMWException.cpp`
(from 0x80380BC4), `ptmf.c`, `MWRTTI.cpp` (0x80381250-0x803814F8,
`__dynamic_cast`, `bad_cast`), `runtime.c`, `__init_cpp_exceptions.cpp`,
`Gecko_ExceptionPPC.cpp` (0x80381D50-0x80383498), `GCN_mem_alloc.c`. The order and the two
extra files are those of rb3 (`sdk/Runtime/*`); `extab` / `extabindex` are cut by the
functions they describe.

| Unit | Sections | Evidence |
|---|---|---|
| `RVL_SDK/base/PPCArch.c` | `.text` 0x80355F60-0x803560C4, `.data` 0x804F20B8-0x804F20F0 | Matching; `PPCMthid0` (0x80355F78) and `PPCSync` (0x80355F98) named by position (same code as mlab); `PPCMfwpar` dead-stripped |
| `RVL_SDK/db/db.c` | `.text` 0x803560C4-0x803561AC, `.data` 0x804F20F0-0x804F2108, `.sbss` 0x805CE0B0-0x805CE0B8 | Matching; `__DBExceptionDestinationAux` (0x803560EC) named by position |
| `RVL_SDK/os/OS.c` | `.text` 0x803561AC-0x803575BC, `.data` 0x804F2108-0x804F24F8, `.bss` 0x8055E920-0x8055E990, `.sdata` 0x805CC038-0x805CC068, `.sbss` 0x805CE0B8-0x805CE100 | Matching; `__OSGetHollywoodRev` dead-stripped. `OSInit` builds `OSPhysicalToCached(0x4000)` with `lis`/`addi`: the two relocations dtk made to `__check_pad3` (0x80356D68, 0x80356DE0) are blocked in `config.yml`, as in mlab |
| `RVL_SDK/os/OSAlarm.c` | `.text` 0x803575BC-0x80357DA0, `.data` 0x804F24F8-0x804F2508, `.sbss` 0x805CE100-0x805CE108 | Matching; all of mlab's functions (`OSSetAlarmTag`, `OSSetAlarmUserData`, `OSGetAlarmUserData` named by position) |
| `RVL_SDK/os/OSAlloc.c` | `.text` 0x80357DA0-0x803580C8, `.sdata` 0x805CC068-0x805CC070, `.sbss` 0x805CE108-0x805CE118 | Matching; same layout as mlab (`DLInsert` first, `DLAddFront` / `DLExtract` inlined), plus `OSDestroyHeap` (0x803580A8, same body as tp's, after `OSCreateHeap` as in tp). `ArenaEnd`, `ArenaStart`, `NumHeaps`, `HeapArray` in mlab's `.sbss` order; `__OSCurrHeap` 4 bytes (dtk said 8) |
| `RVL_SDK/os/OSArena.c` | `.text` 0x803580C8-0x8035815C, `.sdata` 0x805CC070-0x805CC078, `.sbss` 0x805CE118-0x805CE120 | Matching; `OSSetArenaHi` (0x80358108) and `OSAllocFromMEM1ArenaLo` (0x80358128) named by position; `OSAllocFromMEM2ArenaLo` dead-stripped |
| `RVL_SDK/os/OSAudioSystem.c` | `.text` 0x8035815C-0x80358610, `.data` 0x804F2508-0x804F2588 | Matching |
| `RVL_SDK/os/OSCache.c` | `.text` 0x80358610-0x80358A08, `.data` 0x804F2588-0x804F27C0 | Matching; the `LC*` / `L2*` functions and `DCStoreRangeNoSync` dead-stripped |
| `RVL_SDK/os/OSContext.c` | `.text` 0x80358A08-0x80359290, `.data` 0x804F27C0-0x804F29A0 | Matching |
| `RVL_SDK/os/OSError.c` | `.text` 0x80359290-0x803599C0, `.data` 0x804F29A0-0x804F2CBC, `.bss` 0x8055E990-0x8055E9D4, `.sdata` 0x805CC078-0x805CC080 | Matching; `OSVReport` dead-stripped |
| `RVL_SDK/os/OSExec.c` | `.text` 0x803599C0-0x8035B030, `.data` 0x804F2CC0-0x804F2D30, `.bss` 0x8055E9E0-0x8055EA00, `.sdata` 0x805CC080-0x805CC090, `.sbss` 0x805CE120-0x805CE138, `.sdata2` 0x805D26D0-0x805D26D8 | Matching; starts with `PackArgs` (0x803599C0, size as in mlab) |
| `RVL_SDK/os/OSFatal.c` | `.text` 0x8035B030-0x8035BC68, `.bss` 0x8055EA00-0x8055ECE0, `.sdata` 0x805CC090-0x805CC094, `.sdata2` 0x805D26D8-0x805D2718 | Matching; needs `-fp_contract off` (`Halt`) |
| `RVL_SDK/os/OSFont.c` | `.text` 0x8035BC68-0x8035CFE8, `.data` 0x804F2D30-0x804F3840, `.sdata` 0x805CC098-0x805CC0A0, `.sbss` 0x805CE138-0x805CE148, `.sdata2` 0x805D2718-0x805D2720 | Matching; `OSGetFontEncode`, `ExpandFontSheet`, `OSInitFont`, `OSGetFontTexture`, `OSGetFontWidth` named by position (same sizes as mlab) |
| `RVL_SDK/os/OSInterrupt.c` | `.text` 0x8035CFE8-0x8035D76C, `.data` 0x804F3840-0x804F3870, `.sbss` 0x805CE148-0x805CE15C | Matching |
| `RVL_SDK/os/OSLink.c` | `.text` 0x8035D76C-0x8035D784 | Matching |
| `RVL_SDK/os/OSMessage.c` | `.text` 0x8035D784-0x8035DA58 | Matching; plus `OSJamMessage` (0x8035D988, tp's body) |
| `RVL_SDK/os/OSMemory.c` | `.text` 0x8035DA58-0x8035E26C, `.data` 0x804F3870-0x804F3880 | Matching |
| `RVL_SDK/os/OSMutex.c` | `.text` 0x8035E26C-0x8035E570 | Matching; the condition-variable functions dead-stripped |
| `RVL_SDK/os/OSReboot.c` | `.text` 0x8035E570-0x8035E5F0, `.sbss` 0x805CE160-0x805CE168 | Matching; `.sbss` after a 4-byte gap |
| `RVL_SDK/os/OSReset.c` | `.text` 0x8035E5F0-0x8035EE58, `.data` 0x804F3880-0x804F3B08, `.sdata` 0x805CC0A0-0x805CC0A8, `.sbss` 0x805CE168-0x805CE178 | Matching; `OSRebootSystem`, `OSReturnToDataManager`, `OSSetBootDol` dead-stripped |
| `RVL_SDK/os/OSRtc.c` | `.text` 0x8035EE58-0x8035F8E4, `.bss` 0x8055ECE0-0x8055ED34 | Matching |
| `RVL_SDK/os/OSSemaphore.c` | `.text` 0x8035F8E4-0x8035FA5C | Matching; `OSTryWaitSemaphore` (0x8035F9AC, 0x50 bytes against mlab's 0x58) written from the DOL and named by position; `OSGetSemaphoreCount` dead-stripped |
| `RVL_SDK/os/OSSync.c` | `.text` 0x8035FA5C-0x8035FADC | Matching |
| `RVL_SDK/os/OSThread.c` | `.text` 0x8035FADC-0x803611BC, `.bss` 0x8055ED38-0x8055F740, `.sdata` 0x805CC0A8-0x805CC0AC, `.sbss` 0x805CE178-0x805CE184 | Matching; starts with `DefaultSwitchThreadCallback` (0x8035FADC). `OSSetThreadSpecific` / `OSGetThreadSpecific` (0x8036107C, 0x803610AC, absent from mlab) written from the DOL; several mlab functions dead-stripped |
| `RVL_SDK/os/OSTime.c` | `.text` 0x803611BC-0x803615D0, `.data` 0x804F3B08-0x804F3B68 | Matching |
| `RVL_SDK/os/OSUtf.c` | `.text` 0x803615D0-0x80361808, `.data` 0x804F3B68-0x804FF9A8 | Matching |
| `RVL_SDK/os/OSIpc.c` | `.text` 0x80361808-0x80361830, `.sdata` 0x805CC0B0-0x805CC0B4, `.sbss` 0x805CE188-0x805CE18C | Matching; `__OSGetIPCBufferHi` / `Lo` named by position |
| `RVL_SDK/os/OSStateTM.c` | `.text` 0x80361830-0x80361EE4, `.data` 0x804FF9A8-0x804FFA70, `.bss` 0x8055F740-0x8055F800, `.sbss` 0x805CE190-0x805CE1B0 | Matching; starts with `OSSetResetCallback` (0x80361830); `OSGetResetButtonState`, `__OSSetIdleLEDMode` dead-stripped |
| `RVL_SDK/os/OSPlayRecord.c` | `.text` 0x80361EE4-0x803625DC, `.data` 0x804FFA70-0x804FFAB8, `.bss` 0x8055F800-0x8055FA00, `.sdata` 0x805CC0B8-0x805CC0BC, `.sbss` 0x805CE1B8-0x805CE1D8 | Matching |
| `RVL_SDK/os/OSStateFlags.c` | `.text` 0x803625DC-0x803627E8, `.data` 0x804FFAB8-0x804FFAE0, `.bss` 0x8055FA00-0x8055FA20 | Matching |
| `RVL_SDK/os/OSNet.c` | `.text` 0x803627E8-0x80362D4C, `.data` 0x804FFAE0-0x804FFC48 | NonMatching (`__OSInitNet` 100 %, unit code 13 %): this SDK version has the NWC24 functions of tp's `OSNet.c` (0x8036289C-0x80362D4C), absent from mlab's source, some with helpers inlined |
| `RVL_SDK/os/OSNandbootInfo.c` | `.text` 0x80362D4C-0x80362F54, `.data` 0x804FFC48-0x804FFC68 | Matching |
| `RVL_SDK/os/OSPlayTime.c` | `.text` 0x80362F54-0x803637EC, `.data` 0x804FFC68-0x804FFCA8, `.bss` 0x8055FAE0-0x8055FB10, `.sdata` 0x805CC0C8-0x805CC0D0, `.sbss` 0x805CE1E8-0x805CE200, `.sdata2` 0x805D2720-0x805D2730 | Matching |
| `RVL_SDK/os/OSLaunch.c` | `.text` 0x803637EC-0x803645AC, `.data` 0x804FFCA8-0x804FFE98, `.sdata` 0x805CC0D0-0x805CC0D8, `.sbss` 0x805CE200-0x805CE208 | Matching; `.data` also holds the strings of three dead-stripped functions (`__OSLaunchTitlevForSystem`, `__OSLaunchTitlelForSystem`, `OSLaunchManualViewer`, from 0x804FFDC0), emitted by a stand-in `dummyStrings` |
| `RVL_SDK/os/__ppc_eabi_init.cpp` | `.text` 0x803645AC-0x80364660 | Matching; `__init_user`, `__init_cpp`, `exit` |
| `RVL_SDK/os/init/__ppc_eabi_init.cpp` | `.init` 0x800042E0-0x80004338 | Matching; `__init_hardware`, `__flush_cache` in `.init` |
| `RVL_SDK/exi/EXIBios.c` | `.text` 0x80393BE8-0x8039547C, `.data` 0x80506E88-0x80506ED0, `.bss` 0x8057B110-0x8057B1D0, `.sdata` 0x805CC238-0x805CC23C, `.sbss` 0x805CE630-0x805CE634 | Matching, `-schedule off` as in mlab; right after `MSL_C/w_sqrt.c`; `EXIAttach`, `EXIDetach` named by position; `EXIClearInterrupts`, `EXIProbeReset`, `EXIProbe` dead-stripped |
| `RVL_SDK/exi/EXIUart.c` | `.text` 0x8039547C-0x803957B0, `.sbss` 0x805CE638-0x805CE648 | Matching; `ProbeBarnacle` and its four `.sbss` variables named by position |
| `RVL_SDK/exi/EXICommon.c` | `.text` 0x803957B0-0x8039593C | Matching; `EXIWriteReg` named by position; `__EXIFreq` (`.sdata2`) dead-stripped |
| `RVL_SDK/si/SIBios.c` | `.text` 0x8039593C-0x80396944, `.data` 0x80506ED0-0x80506F40, `.bss` 0x8057B1D0-0x8057B3F0, `.sdata` 0x805CC240-0x805CC244, `.sbss` 0x805CE648-0x805CE658 | Matching; same kept functions as mlab (`.text` 0x1008 in both); `CompleteTransfer`, `__SITransfer`, `AlarmHandler`, `__PADFixBits` named by position, `VIGetCurrentLine` (0x8036F8A8) by relocation. `SIGetTypeString` under `#if 0`: dead-stripped, and its strings are in neither this DOL nor mlab's |
| `RVL_SDK/si/SISamplingRate.c` | `.text` 0x80396944-0x80396A24, `.data` 0x80506F40-0x80506FD8, `.sbss` 0x805CE658-0x805CE65C | Matching; `SIRefreshSamplingRate` (0x80396A1C) named by its code (`SISetSamplingRate(SamplingRate)`) |
| `RVL_SDK/vi/vi.c` | `.text` 0x8036D3B8-0x8036FD90, `.data` 0x805018D8-0x80501E30, `.bss` 0x80564C40-0x80564DB0, `.sdata` 0x805CC120-0x805CC140, `.sbss` 0x805CE320-0x805CE3D0 | Matching; mlab's source plus two functions this DOL keeps: `VIGetNextField` (0x8036F80C, tp's body) and `VIGetScanMode` (0x8036F998) as a global function, as in Petari, still inlined into `VIInit` under `-ipa file`. `OnShutdown` (0x8036D3B8) and `__VIResetRFIdle` (0x8036FD80) named by their code; `VIGetCurrentFrameBuffer`, `__VIResetDev0Idle`, `__VIResetSIIdle` dead-stripped |
| `RVL_SDK/vi/i2c.c` | `.text` 0x8036FD90-0x803707AC, `.sdata` 0x805CC140-0x805CC148, `.sbss` 0x805CE3D0-0x805CE3D8 | Matching |
| `RVL_SDK/vi/vi3in1.c` | `.text` 0x803707AC-0x80371E50, `.data` 0x80501E30-0x805023C0, `.bss` 0x80564DB0-0x80564DD0, `.sdata` 0x805CC148-0x805CC160, `.sbss` 0x805CE3D8-0x805CE3F0 | Matching; `VISetRGBModeImm` (0x803719CC) named by its code; `__VISetGamma`, `VISetGamma` dead-stripped. dtk's relocation at 0x80501FA0 (gamma table halfwords 0x8000, 0xA000) blocked in `config.yml` |
| `RVL_SDK/mtx/mtx.c` | `.text` 0x80364660-0x80364A58, `.sdata` 0x805CC0D8-0x805CC0E0, `.sdata2` 0x805D2730-0x805D2738 | Matching; right after `os/__ppc_eabi_init.cpp`; same kept functions as mlab (`.text` 0x3F8 in both) |
| `RVL_SDK/mtx/mtxvec.c` | `.text` 0x80364A58-0x80364AAC | Matching; `PSMTXMultVec` only |
| `RVL_SDK/mtx/mtx44.c` | `.text` 0x80364AAC-0x80364B44, `.sdata2` 0x805D2738-0x805D2748 | Matching; `C_MTXOrtho` only. `C_MTXPerspective` under `#if 0`: dead-stripped, and its two float constants are not in `.sdata2` |
| `RVL_SDK/dvd/dvdfs.c` | `.text` 0x80364B44-0x8036545C, `.data` 0x804FFE98-0x804FFFD0, `.sdata` 0x805CC0E0-0x805CC0F0, `.sbss` 0x805CE208-0x805CE228 | Matching; mlab's source with `DVDReadPrio` and `cbForReadSync` under `#if 0` (dead-stripped, with the assertion string of `DVDReadPrio`); `DVDGetCurrentDir` dead-stripped too |
| `RVL_SDK/dvd/dvd.c` | `.text` 0x8036545C-0x80369F30, `.data` 0x804FFFD0-0x80500340, `.bss` 0x8055FB40-0x805647F0, `.sdata` 0x805CC0F0-0x805CC108, `.sbss` 0x805CE240-0x805CE2D8 | Matching; same code as mlab |
| `RVL_SDK/dvd/dvdqueue.c` | `.text` 0x80369F30-0x8036A188, `.bss` 0x805647F0-0x80564810 | Matching |
| `RVL_SDK/dvd/dvderror.c` | `.text` 0x8036A188-0x8036AA8C, `.data` 0x80500340-0x80500370, `.bss` 0x80564820-0x80564A80, `.sbss` 0x805CE2D8-0x805CE2E8 | Matching; the NAND error log of Petari, as in mlab |
| `RVL_SDK/dvd/dvdidutils.c` | `.text` 0x8036AA8C-0x8036AB7C | Matching; `DVDCompareDiskID` only |
| `RVL_SDK/dvd/dvdFatal.c` | `.text` 0x8036AB7C-0x8036ACD4, `.rodata` 0x804C2658-0x804C2690, `.data` 0x80500370-0x80500880, `.sbss` 0x805CE2E8-0x805CE2F0, `.sdata2` 0x805D2748-0x805D2750 | Matching; `.data` start not found by relocation pairing: the 0x6A8 bytes between `dvderror.c` and `dvd_broadway.c` are mlab's `dvdFatal.c` (0x510) and `dvdDeviceError.c` (0x198) `.data` sizes |
| `RVL_SDK/dvd/dvdDeviceError.c` | `.text` 0x8036ACD4-0x8036AF6C, `.rodata` 0x804C2690-0x804C26B0, `.data` 0x80500880-0x80500A18, `.bss` 0x80564A80-0x80564AA0, `.sdata` 0x805CC108-0x805CC110, `.sbss` 0x805CE2F0-0x805CE2F8 | Matching; `__DVDShowDeviceErrorMessage` dead-stripped; dtk's 4-byte `.rodata` symbol at 0x804C26AC was the section's alignment padding (removed, no user) |
| `game/unit_8032E43C.cpp` (IKAnchor) | `.text` 0x8032E43C-0x8032E5E4, `.ctors` 0x804B87FC-0x804B8800, `.data` 0x804F0288-0x804F02F8 (vtable), `.bss` 0x8052E6F0-0x8052E700, `.sbss` 0x805CDF60-0x805CDF68, `.sdata2` 0x805D23E8-0x805D23F0 | Matching. Start: after the `__sinit` of the previous unit (0x8032E3B8, `.ctors` 0x804B87F8); end: its own `__sinit` (0x8032E5A0). RTTI, base list and `vfC` / `vf5C` of IKAnchor are in the unit at 0x80327260 (weak copies, first unit wins) |
| `Runtime.PPCEABI.H/__mem.c` | `.init` 0x80004338-0x8000446C, `.text` 0x8038098C-0x803809A8 (`strlen`) | Matching; same code as mlab |
| `Runtime.PPCEABI.H/__va_arg.c` | `.text` 0x803809A8-0x80380A70 | Matching; same code as mlab |
| `Runtime.PPCEABI.H/global_destructor_chain.c` | `.text` 0x80380A70-0x80380AD0, `.sbss` 0x805CE5F0-0x805CE5F8 | Matching (objdiff 100 %, `main.dol: OK`) |
| `Runtime.PPCEABI.H/New.cpp` | `extab` 0x800064E0-0x80006514, `extabindex` 0x80008B80-0x80008B98, `.text` 0x80380AD0-0x80380BC4, `.rodata` 0x804C26B0-0x804C2708, `.data` 0x805061F8-0x80506220, `.sdata` 0x805CC1E0-0x805CC1F0, `.sbss` 0x805CE5F8-0x805CE600 | NonMatching: code 100 %, `.rodata`, `.sdata`, `.sbss` 100 %; `.data` 70 %, `extab` / `extabindex` 82 % / 80 % (our object also emits the weak `std::exception` vtable, dtor and `what`, and the first `extab` range of `operator new` starts at 0x30 instead of 0x4C). `operator new` (`__nw__FUl`), `std::bad_alloc` dtor, `what`, vtable and RTTI, `std::exception` RTTI; the exception-specification string `"!std::bad_alloc!!"` (0x804C26B0, pointed to by the `extab` of `operator new`) starts the `.rodata`. The functions from 0x80380BC4 belong to `NMWException.cpp` |
| `Runtime.PPCEABI.H/NMWException.cpp` | `extab` 0x80006514-0x8000655C, `extabindex` 0x80008B98-0x80008BD4, `.text` 0x80380BC4-0x803811D0, `.sdata` 0x805CC1F0-0x805CC1F8 | Matching; mlab's code from 0x80380E20, preceded by rb3's `std::dthandler`, `duhandler`, `terminate`, `unexpected` (`set_terminate` / `set_unexpected` dead-stripped), `__throw_catch_compare` and the `thandler` / `uhandler` pointers |
| `Runtime.PPCEABI.H/ptmf.c` | `.text` 0x803811D0-0x80381250 | Matching; `__ptmf_test`, `__ptmf_scall`, `__ptmf_scall4` |
| `Runtime.PPCEABI.H/MWRTTI.cpp` | `extab` 0x8000655C-0x8000656C, `extabindex` 0x80008BD4-0x80008BEC, `.text` 0x80381250-0x803814F8, `.rodata` 0x804C2718-0x804C2770, `.data` 0x80506220-0x80506248, `.sdata` 0x805CC1F8-0x805CC200 | NonMatching: code 100 %; data not (`extab` 57 %, `extabindex` 0 %, `.data` 68 %, `.sdata` 50 %, `.rodata` 85 %): the original object had `__get_typeid`, stripped by the linker with its `extab` entries and weak vtables and RTTI, ours keeps them. `__dynamic_cast` (calls `__throw`, 0x8038331C), `std::bad_cast` dtor and `what`, vtable and RTTI; `std::exception`'s RTTI (0x805CC1E8) sits before, with `New.cpp` |
| `Runtime.PPCEABI.H/runtime.c` | `.text` 0x803814F8-0x80381CE0, `.rodata` 0x804C2770-0x804C2788 | Matching |
| `Runtime.PPCEABI.H/__init_cpp_exceptions.cpp` | `.text` 0x80381CE0-0x80381D50, `.ctors$10` 0x804B7EC0, `.dtors$10` 0x804B88C0, `.dtors$15` 0x804B88C4, `.sdata` 0x805CC200-0x805CC208 | Matching (objdiff 100 %, `main.dol: OK`) |
| `Runtime.PPCEABI.H/Gecko_ExceptionPPC.cpp` | `extab` 0x8000656C-0x800065E0, `extabindex` 0x80008BEC-0x80008C40, `.text` 0x80381D50-0x80383498, `.rodata` 0x804C2788-0x804C27F0, `.data` 0x80506248-0x80506348, `.sdata` 0x805CC208-0x805CC210, `.bss` 0x8057ADA8-0x8057ADB8 | NonMatching: every function 100 % except `ExPPC_UnwindStack` (97.28 %, register allocation); `.bss` 100 %, `.data` 94 %, `.rodata` 74 %, `.sdata` 75 %, `extab` 81 %, `extabindex` 0 %. `__register_fragment` to `__end__catch` plus `std::bad_exception` dtor, `what`, vtable and RTTI; one fragment slot (`fragmentinfo`, 0x10 bytes of `.bss`) |
| `Runtime.PPCEABI.H/GCN_mem_alloc.c` | `.text` 0x80383498-0x80383608, `.rodata` 0x804C27F0-0x804C2860 | Matching; `__sys_alloc`, `__sys_free` with `InitDefaultHeap` inlined (same code as mscharged); string pool 0x6F bytes (dtk said 0x70). Callees named by their place in `OSAlloc.c` / `OSArena.c`, laid out as in mlab: `OSAllocFromHeap`, `OSFreeToHeap`, `OSInitAlloc`, `OSCreateHeap` (ref_match), `OSSetCurrentHeap` (0x80357FBC), `OSSetArenaLo` (0x80358120), `__OSCurrHeap` (0x805CC068) |
| `MSL_C/mem_funcs.c` | `.text` 0x80387070-0x80387340 | Matching; same code as mlab |
| `MSL_C/alloc.c` | `extab` 0x800065E0-0x80006630, `extabindex` 0x80008C40-0x80008CB8, `.text` 0x80383608-0x80384A40, `.rodata` 0x804C2860-0x804C2878, `.bss` 0x8057ADB8-0x8057ADF0, `.sbss` 0x805CE600-0x805CE608 | Matching. mlab's 12 functions plus `calloc` (0x80384980, 0xC0), which this DOL keeps and mlab's does not: it allocates `size * nmemb` from the malloc pool (`protopool`, `init`) and clears it with `memset`, the shape of MSL's `calloc`; it has its own `extabindex` entry and ends the unit (`ansi_files.c` matches from 0x80384A40) |
| `MSL_C/ansi_files.c` | `extab` 0x80006630-0x80006640, `extabindex` 0x80008CB8-0x80008CD0, `.text` 0x80384A40-0x80384B50, `.data` 0x80506348-0x80506488, `.bss` 0x8057ADF0-0x8057B0F0 | Matching; `__close_all`, `__flush_all` of mlab's five functions. `__files` (0x140) holds the three console `FILE`s, whose buffer pointers give `stdin_buff` (0x8057AFF0), `stdout_buff` (0x8057AEF0), `stderr_buff` (0x8057ADF0) and whose callbacks give `__read_console`, `__write_console`, `__close_console` (same code as mlab's) |
| `MSL_C/ansi_fp.c` | `extab` 0x80006640-0x80006678, `extabindex` 0x80008CD0-0x80008D24, `.text` 0x80384B50-0x803864C0, `.rodata` 0x804C2878-0x804C2958, `.data` 0x80506488-0x805065F0, `.sdata2` 0x805D2920-0x805D2958 | Matching; same code and data sizes as mlab |
| `MSL_C/scanf.c` | `extab` 0x80006730-0x80006748, `extabindex` 0x80008E38-0x80008E5C, `.text` 0x80389940-0x8038AEAC, `.rodata` 0x804C2E90-0x804C2EB8, `.data` 0x80506A38-0x80506B58 | Matching; same code and data sizes as mlab |
| `MSL_C/buffer_io.c` | `extab` 0x80006678-0x80006680, `extabindex` 0x80008D24-0x80008D30, `.text` 0x803864C0-0x803865A0 | Matching; `__prep_buffer`, `__flush_buffer` |
| `MSL_C/direct_io.c` | `extab` 0x80006680-0x80006688, `extabindex` 0x80008D30-0x80008D3C, `.text` 0x803865A0-0x803868A8 | Matching; `__fwrite` |
| `MSL_C/file_io.c` | `extab` 0x80006688-0x80006698, `extabindex` 0x80008D3C-0x80008D54, `.text` 0x803868A8-0x80386A98 | Matching; `fclose`, `fflush` |
| `MSL_C/FILE_POS.c` | `extab` 0x80006698-0x800066A0, `extabindex` 0x80008D54-0x80008D60, `.text` 0x80386A98-0x80386D08 | Matching; `_ftell`, `ftell`, `_fseek` (only `_fseek` has an `extabindex` entry) |
| `MSL_C/mbstring.c` | `extab` 0x800066A0-0x800066B0, `extabindex` 0x80008D60-0x80008D78, `.text` 0x80386D08-0x80386F00 | Matching; `mbtowc`, `__mbtowc_noconv`, `__wctomb_noconv`, `mbstowcs` (0x80386D88, absent from mlab's DOL), `wcstombs` |
| `MSL_C/mem.c` | `extab` 0x800066B0-0x800066B8, `extabindex` 0x80008D78-0x80008D84, `.text` 0x80386F00-0x80387070 | Matching; same code as mlab. `extab` / `extabindex` bounds of these MSL_C units: the `extabindex` entries (function, size, `extab` pointer) of the unit's functions |
| `MSL_C/math_api.c` | `extab` 0x800066B8-0x800066C8, `extabindex` 0x80008D84-0x80008D9C, `.text` 0x80387340-0x803873D8 | Matching; same code as mlab |
| `MSL_C/rand.c` | `.text` 0x80389920-0x80389940, `.sdata` 0x805CC218-0x805CC220 | Matching; `rand` (`srand` dead-stripped); `random_next` 4 bytes, dtk said 8 |
| `MSL_C/misc_io.c` | `.text` 0x803873D8-0x803873E8 | Matching; `__stdio_atexit` (`clearerr` dead-stripped) |
| `MSL_C/printf.c` | `extab` 0x800066C8-0x80006728, `extabindex` 0x80008D9C-0x80008E2C, `.text` 0x803873E8-0x803897B0, `.rodata` 0x804C2E60-0x804C2E90, `.data` 0x805067E8-0x80506A38, `.sdata` 0x805CC210-0x805CC218, `.sdata2` 0x805D2970-0x805D2978 | Matching; mlab's functions without `printf` and `fprintf`, same data sizes. `__lconv` (0x805065F0, referenced here, in data not split yet, as in mlab) is named by the run of data sizes it shares with mlab before `_current_locale` |
| `MSL_C/qsort.c` | `extab` 0x80006728-0x80006730, `extabindex` 0x80008E2C-0x80008E38, `.text` 0x803897B0-0x80389920 | Matching; same code as mlab |
| `MSL_C/string.c` | `extab` 0x80006750-0x80006758, `extabindex` 0x80008E68-0x80008E74, `.text` 0x8038AF5C-0x8038B43C, `.sdata` 0x805CC220-0x805CC228, `.sdata2` 0x805D2978-0x805D2980 | Matching; mlab's functions plus `strrchr` (0x8038B264, 0x48), between `strchr` and `strtok`: it scans with `lbzu`, keeps the last match of `chr & 0xFF` and returns the end of the string when `chr` is 0, the shape of MSL's `strrchr`. `.sdata` holds `strtok_null` / `strtok_ptr`, both pointing to `""` (`.sdata2`, 1 byte; dtk said 8) |
| `MSL_C/signal.c` | `extab` 0x80006748-0x80006750, `extabindex` 0x80008E5C-0x80008E68, `.text` 0x8038AEAC-0x8038AF5C, `.bss` 0x8057B0F0-0x8057B110 | Matching; `signal_funcs` has 7 entries (`raise` tests `sig > 7`), so 0x1C bytes plus padding |
| `MSL_C/strtold.c` | `extab` 0x80006758-0x80006760, `extabindex` 0x80008E74-0x80008E80, `.text` 0x8038B43C-0x8038C830, `.rodata` 0x804C2EB8-0x804C2EC8, `.sdata2` 0x805D2980-0x805D29A0 | Matching; `__strtold` (`atof` dead-stripped, so two doubles fewer in `.sdata2` than mlab). `"INFINITY"` is 9 bytes (dtk said 0x10). `lbl_805D29A0` belongs to the code at 0x8038DCB8, not to this unit. `__double_huge` (0x805CC230) named by its place after `__float_huge`, as in mlab |
| `MSL_C/strtoul.c` | `extab` 0x80006760-0x80006778, `extabindex` 0x80008E80-0x80008EA4, `.text` 0x8038C830-0x8038D1E8, `.data` 0x80506B58-0x80506BE0 | Matching (GC/3.0a5, as in mlab); `__strtoul`, `__strtoull`, `atoi` (0x8038D124; `strtoul` and `strtol` absent, `strtol` inlined into `atoi`) |
| `MSL_C/wmem.c` | `.text` 0x8038D1E8-0x8038D218 | Matching; `wmemcpy`, `wmemchr`; same code as mscharged |
| `MSL_C/wprintf.c` | `extab` 0x80006778-0x800067B0, `extabindex` 0x80008EA4-0x80008EF8, `.text` 0x8038D218-0x8038F3D4, `.rodata` 0x804C34C8-0x804C34D0, `.data` 0x80506BE0-0x80506E88, `.sdata2` 0x805D29A0-0x805D29A8 | Matching; mscharged's functions (same sizes) plus `long2str` (0x234) and `swprintf` (0x8038F2F8, 0xDC: `vswprintf` inlined, the shape of `snprintf` in `printf.c`); `vswprintf` absent. Wide string pool `lbl_80506E30` 0x56 bytes (dtk said 0x58), `lbl_804C34C8` 1 byte (dtk said 8) |
| `MSL_C/wstring.c` | `.text` 0x8038F3D4-0x8038F4B0 | Matching; `wcslen`, `wcscpy`, `wcsncpy`, `wcscmp`, `wcschr` (mlab's DOL lacks `wcscpy` and `wcschr`) |
| `MSL_C/wchar_io.c` | `.text` 0x8038F4B0-0x8038F534 | Matching; `fwide` (`__fwide` dead-stripped) |
| `MSL_C/uart_console_io_gcn.c` | `extab` 0x800067B0-0x800067B8, `extabindex` 0x80008EF8-0x80008F04, `.text` 0x8038F534-0x8038F60C, `.sbss` 0x805CE610-0x805CE618 | Matching; `__write_console`, `__close_console`; `initialized` 4 bytes (dtk said 8). Callees named from mlab matches: `__TRK_write_console` (0x8039B1B0), `InitializeUART` (0x8039DA5C), `WriteUARTN` (0x8039DAA4) |
| `MSL_C/abort_exit_ppc_eabi.c` | `extab` 0x800067B8-0x800067C0, `extabindex` 0x80008F04-0x80008F10, `.text` 0x8038F60C-0x8038F640, `.sbss` 0x805CE618-0x805CE620 | Matching; `__aborting`, `__stdio_exit` |
| `MSL_C/math_sun.c` | `extab` 0x800067C0-0x800067C8, `extabindex` 0x80008F10-0x80008F1C, `.text` 0x8038F640-0x8038F680 | Matching; `scalbn` |
| `MSL_C/extras.c` | `.text` 0x8038F8A4-0x8038F9A4 | Matching; `stricmp` (same code as mlab) and, before it, `strlwr` (0x8038F8A4, 0x58), absent from mlab: it lowers each byte in place through `_current_locale`'s `lower_map_ptr`, as `stricmp` does, the shape of MSL's `strlwr`. Written for this project |
| `MSL_C/e_acos.c` … `MSL_C/s_tan.c`, `MSL_C/e_sqrt.c` (21 fdlibm units) | `.text` 0x8038F9A4-0x80393BE0 with gaps; `.rodata`, `.sbss`, `.sdata2` per unit (see `splits.txt`) | Matching; same code and sizes as mlab |
| `MSL_C/e_exp.c` | `.text` 0x80390170-0x803903A4, `.rodata` 0x804C34D0-0x804C3500, `.sdata2` 0x805D2B10-0x805D2B88 | Matching (GC/3.0a5); fills the gap after `e_atan2.c`; `__ieee754_exp`, called by `exp` (`w_exp.c`). Absent from mlab; source from tp |
| `MSL_C/w_acos.c` … `MSL_C/w_pow.c` (8 units) | `.text` 0x80393978-0x80393998, 4 bytes each: `acos`, `asin`, `atan2`, `exp`, `fmod`, `log`, `log10`, `pow` | Matching; each is a `b __ieee754_<name>` (`-D_IEEE_LIBM`), fills the gap after `s_tan.c` |
| `MSL_C/math_ppc.c`, `MSL_C/w_sqrt.c` | `.text` 0x80393BE0-0x80393BE4 (`nan`), 0x80393BE4-0x80393BE8 (`sqrt`) | Matching; same order as mlab after `e_sqrt.c` |
