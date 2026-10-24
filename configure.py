#!/usr/bin/env python3

###
# Generates build files for the project.
# This file also includes the project configuration,
# such as compiler flags and the object matching status.
#
# Usage:
#   python3 configure.py
#   ninja
#
# Append --help to see available options.
###

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

from tools.project import (
    Object,
    ProgressCategory,
    ProjectConfig,
    calculate_progress,
    generate_build,
    is_windows,
)

# Game versions
# The index is passed to the compiler as BUILD_VERSION; keep it in sync with
# include/version.h and only append new versions.
DEFAULT_VERSION = 0
VERSIONS = [
    "RO8P7D",  # 0: Europe (En,Fr,De,Es,It,Nl)
    "RO8X7D",  # 1: Scandinavia (En,Sv,No,Da,Fi)
    "RO8E7D",  # 2: USA (En,Fr,Es)
]

# Versions to disable until properly configured
DISABLED_VERSIONS = [
    1,  # Scandinavia
    2,  # USA
]

# Version groups for MatchingFor
ALL_PAL = ["RO8P7D", "RO8X7D"]
ALL_USA = ["RO8E7D"]
ALL = ALL_PAL + ALL_USA

parser = argparse.ArgumentParser()
parser.add_argument(
    "mode",
    choices=["configure", "progress"],
    default="configure",
    help="script mode (default: configure)",
    nargs="?",
)
parser.add_argument(
    "-v",
    "--version",
    choices=VERSIONS,
    type=str.upper,
    default=VERSIONS[DEFAULT_VERSION],
    help="version to build",
)
parser.add_argument(
    "--build-dir",
    metavar="DIR",
    type=Path,
    default=Path("build"),
    help="base build directory (default: build)",
)
parser.add_argument(
    "--binutils",
    metavar="BINARY",
    type=Path,
    help="path to binutils (optional)",
)
parser.add_argument(
    "--compilers",
    metavar="DIR",
    type=Path,
    help="path to compilers (optional)",
)
parser.add_argument(
    "--map",
    action="store_true",
    help="generate map file(s)",
)
parser.add_argument(
    "--debug",
    action="store_true",
    help="build with debug info (non-matching)",
)
if not is_windows():
    parser.add_argument(
        "--wrapper",
        metavar="BINARY",
        type=Path,
        help="path to wibo or wine (optional)",
    )
parser.add_argument(
    "--dtk",
    metavar="BINARY | DIR",
    type=Path,
    help="path to decomp-toolkit binary or source (optional)",
)
parser.add_argument(
    "--objdiff",
    metavar="BINARY | DIR",
    type=Path,
    help="path to objdiff-cli binary or source (optional)",
)
parser.add_argument(
    "--sjiswrap",
    metavar="EXE",
    type=Path,
    help="path to sjiswrap.exe (optional)",
)
parser.add_argument(
    "--ninja",
    metavar="BINARY",
    type=Path,
    help="path to ninja binary (optional)",
)
parser.add_argument(
    "--verbose",
    action="store_true",
    help="print verbose output",
)
parser.add_argument(
    "--non-matching",
    dest="non_matching",
    action="store_true",
    help="builds equivalent (but non-matching) or modded objects",
)
parser.add_argument(
    "--warn",
    dest="warn",
    type=str,
    choices=["all", "off", "error"],
    help="how to handle warnings",
)
parser.add_argument(
    "--no-progress",
    dest="progress",
    action="store_false",
    help="disable progress calculation",
)
args = parser.parse_args()

config = ProjectConfig()
config.version = str(args.version)
version_num = VERSIONS.index(config.version)

if version_num in DISABLED_VERSIONS:
    sys.exit(f"Version {config.version} is disabled until it is configured (DISABLED_VERSIONS)")

# Apply arguments
config.build_dir = args.build_dir
config.dtk_path = args.dtk
config.objdiff_path = args.objdiff
config.binutils_path = args.binutils
config.compilers_path = args.compilers
config.generate_map = args.map
config.non_matching = args.non_matching
config.sjiswrap_path = args.sjiswrap
config.ninja_path = args.ninja
config.progress = args.progress
if not is_windows():
    config.wrapper = args.wrapper
# Don't build asm unless we're --non-matching
if not config.non_matching:
    config.asm_dir = None

# Tool versions
config.binutils_tag = "2.42-2"
config.compilers_tag = "20251118"
config.dtk_tag = "v1.8.4"
config.objdiff_tag = "v3.6.1"
config.sjiswrap_tag = "v1.2.2"
config.wibo_tag = "1.0.3"

# Project
config.config_path = Path("config") / config.version / "config.yml"
config.check_sha_path = Path("config") / config.version / "build.sha1"
config.asflags = [
    "-mgekko",
    "--strip-local-absolute",
    "-I include",
    f"-I build/{config.version}/include",
    f"--defsym BUILD_VERSION={version_num}",
]
config.ldflags = [
    "-fp hardware",
    "-nodefaults",
]
if args.debug:
    config.ldflags.append("-g")  # Or -gdwarf-2 for Wii linkers
if args.map:
    config.ldflags.append("-mapunused")
    # config.ldflags.append("-listclosure") # For Wii linkers

# Use for any additional files that should cause a re-configure when modified
config.reconfig_deps = []

# Optional numeric ID for decomp.me preset
# Can be overridden in libraries or objects
config.scratch_preset_id = None

# Base flags, common to most GC/Wii games.
# Generally leave untouched, with overrides added below.
cflags_base = [
    "-nodefaults",
    "-proc gekko",
    "-align powerpc",
    "-enum int",
    "-fp hardware",
    "-Cpp_exceptions off",
    "-O4,p",
    "-inline auto",
    '-pragma "cats off"',
    '-pragma "warn_notinlined off"',
    "-maxerrors 1",
    "-nosyspath",
    "-RTTI off",
    "-fp_contract on",
    "-str reuse",
    "-multibyte",  # For Wii compilers, replace with `-enc SJIS`
    "-i include",
    f"-i build/{config.version}/include",
    "-i libs/Runtime/include",
    "-i libs/MSL_C/include",
    "-i libs/MetroTRK/include",
    "-i libs/MSL_C++/include",
    f"-DBUILD_VERSION={version_num}",  # compare with the names in include/version.h
]

# Debug flags
if args.debug:
    # Or -sym dwarf-2 for Wii compilers
    cflags_base.extend(["-sym on", "-DDEBUG=1"])
else:
    cflags_base.append("-DNDEBUG=1")

# Warning flags
if args.warn == "all":
    cflags_base.append("-W all")
elif args.warn == "off":
    cflags_base.append("-W off")
elif args.warn == "error":
    cflags_base.append("-W error")

# Metrowerks library flags
cflags_runtime = [
    *cflags_base,
    "-use_lmw_stmw on",
    "-str reuse,pool,readonly",
    "-gccinc",
    "-common off",
    "-inline auto",
]

# MSL_C flags (as in mlab-decomp, from mscharged-decomp: SDK flags with -ipa file)
cflags_msl = [
    *(flag for flag in cflags_base if flag != "-fp_contract on"),
    "-fp_contract off",
    "-inline auto",
    "-ipa file",
]

# Game code flags (GC/3.0a5.2, see notes/COMPILER.md); vtables carry RTTI pointers
cflags_game = [
    *cflags_base,
    "-RTTI on",
]

# REL flags
cflags_rel = [
    *cflags_base,
    "-sdata 0",
    "-sdata2 0",
]

config.linker_version = "GC/3.0a5.2"


# Helper function for Dolphin libraries
def DolphinLib(lib_name: str, objects: List[Object]) -> Dict[str, Any]:
    return {
        "lib": lib_name,
        "mw_version": "GC/1.2.5n",
        "cflags": cflags_base,
        "progress_category": "sdk",
        "objects": objects,
    }


# Helper function for REL script objects
def Rel(lib_name: str, objects: List[Object]) -> Dict[str, Any]:
    return {
        "lib": lib_name,
        "mw_version": "GC/1.3.2",
        "cflags": cflags_rel,
        "progress_category": "game",
        "objects": objects,
    }


Matching = True                   # Object matches and should be linked
NonMatching = False               # Object does not match and should not be linked
Equivalent = config.non_matching  # Object should be linked when configured with --non-matching


# Object is only matching for specific versions (IDs or groups such as ALL_PAL)
def MatchingFor(*versions) -> bool:
    fullset = set()
    for vers in versions:
        if isinstance(vers, (list, tuple, set)):
            fullset.update(vers)
        else:
            fullset.add(vers)

    return config.version in fullset


config.warn_missing_config = True
config.warn_missing_source = False
config.libs = [
    {
        "lib": "game",
        "mw_version": "GC/3.0a5.2",
        "cflags": cflags_game,
        "progress_category": "game",
        "objects": [
            Object(Matching, "game/unit_8032E43C.cpp", extra_cflags=["-opt nopeephole"]),
        ],
    },
    {
        "lib": "Runtime.PPCEABI.H",
        "mw_version": config.linker_version,
        "cflags": cflags_runtime,
        "progress_category": "sdk",  # str | List[str]
        "objects": [
            Object(Matching, "Runtime.PPCEABI.H/__mem.c"),
            Object(Matching, "Runtime.PPCEABI.H/__va_arg.c"),
            Object(Matching, "Runtime.PPCEABI.H/global_destructor_chain.c"),
            Object(NonMatching, "Runtime.PPCEABI.H/New.cpp", extra_cflags=["-Cpp_exceptions on", "-RTTI on"]),
            Object(Matching, "Runtime.PPCEABI.H/NMWException.cpp", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "Runtime.PPCEABI.H/ptmf.c"),
            Object(NonMatching, "Runtime.PPCEABI.H/MWRTTI.cpp", extra_cflags=["-Cpp_exceptions on", "-RTTI on"]),
            Object(Matching, "Runtime.PPCEABI.H/runtime.c"),
            Object(Matching, "Runtime.PPCEABI.H/__init_cpp_exceptions.cpp"),
            Object(Matching, "Runtime.PPCEABI.H/GCN_mem_alloc.c"),
        ],
    },
    {
        "lib": "MSL_C",
        # Same sources and per-file flags as mlab-decomp (see notes/PROVENANCE.md)
        "mw_version": "GC/3.0a5.2",
        "cflags": cflags_msl,
        "progress_category": "sdk",
        "objects": [
            Object(Matching, "MSL_C/alloc.c", extra_cflags=["-Cpp_exceptions on", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/ansi_files.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "MSL_C/ansi_fp.c", extra_cflags=["-Cpp_exceptions on", "-rostr", "-use_lmw_stmw on"], mw_version="GC/3.0a5"),
            Object(Matching, "MSL_C/buffer_io.c", extra_cflags=["-Cpp_exceptions on", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/direct_io.c", extra_cflags=["-Cpp_exceptions on", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/file_io.c", extra_cflags=["-Cpp_exceptions on", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/FILE_POS.c", extra_cflags=["-Cpp_exceptions on", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/mbstring.c", extra_cflags=["-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/mem.c"),
            Object(Matching, "MSL_C/mem_funcs.c"),
            Object(Matching, "MSL_C/math_api.c"),
            Object(Matching, "MSL_C/misc_io.c"),
            Object(Matching, "MSL_C/printf.c", extra_cflags=["-Cpp_exceptions on", "-str reuse,pool,readonly", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/qsort.c", extra_cflags=["-Cpp_exceptions on", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/rand.c"),
            Object(Matching, "MSL_C/scanf.c", extra_cflags=["-Cpp_exceptions on", "-str reuse,pool,readonly", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/signal.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "MSL_C/string.c", extra_cflags=["-Cpp_exceptions on", "-str reuse,pool,readonly"]),
            Object(Matching, "MSL_C/strtold.c", extra_cflags=["-Cpp_exceptions on", "-str reuse,pool,readonly", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/strtoul.c", extra_cflags=["-Cpp_exceptions on", "-use_lmw_stmw on"], mw_version="GC/3.0a5"),
            Object(Matching, "MSL_C/wmem.c"),
            Object(Matching, "MSL_C/wprintf.c", extra_cflags=["-Cpp_exceptions on", "-str reuse,pool,readonly", "-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/wstring.c"),
            Object(Matching, "MSL_C/wchar_io.c"),
            Object(Matching, "MSL_C/uart_console_io_gcn.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "MSL_C/abort_exit_ppc_eabi.c", extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "MSL_C/math_sun.c", cflags=cflags_runtime, extra_cflags=["-Cpp_exceptions on"]),
            Object(Matching, "MSL_C/extras.c"),
            Object(Matching, "MSL_C/e_acos.c"),
            Object(Matching, "MSL_C/e_asin.c", mw_version="GC/3.0a5"),
            Object(Matching, "MSL_C/e_atan2.c"),
            Object(Matching, "MSL_C/e_exp.c", mw_version="GC/3.0a5"),
            Object(Matching, "MSL_C/e_fmod.c"),
            Object(Matching, "MSL_C/e_log.c"),
            Object(Matching, "MSL_C/e_log10.c"),
            Object(Matching, "MSL_C/e_pow.c", mw_version="GC/3.0a5"),
            Object(Matching, "MSL_C/e_rem_pio2.c", mw_version="GC/3.0a5"),
            Object(Matching, "MSL_C/k_cos.c"),
            Object(Matching, "MSL_C/k_rem_pio2.c", extra_cflags=["-use_lmw_stmw on"]),
            Object(Matching, "MSL_C/k_sin.c"),
            Object(Matching, "MSL_C/k_tan.c", mw_version="GC/3.0a5"),
            Object(Matching, "MSL_C/s_atan.c", mw_version="GC/3.0a5"),
            Object(Matching, "MSL_C/s_copysign.c"),
            Object(Matching, "MSL_C/s_cos.c"),
            Object(Matching, "MSL_C/s_floor.c"),
            Object(Matching, "MSL_C/s_frexp.c"),
            Object(Matching, "MSL_C/s_ldexp.c"),
            Object(Matching, "MSL_C/s_sin.c"),
            Object(Matching, "MSL_C/s_tan.c"),
            Object(Matching, "MSL_C/w_acos.c", extra_cflags=["-D_IEEE_LIBM"]),
            Object(Matching, "MSL_C/w_asin.c", extra_cflags=["-D_IEEE_LIBM"]),
            Object(Matching, "MSL_C/w_atan2.c", extra_cflags=["-D_IEEE_LIBM"]),
            Object(Matching, "MSL_C/w_exp.c", extra_cflags=["-D_IEEE_LIBM"]),
            Object(Matching, "MSL_C/w_fmod.c", extra_cflags=["-D_IEEE_LIBM"]),
            Object(Matching, "MSL_C/w_log.c", extra_cflags=["-D_IEEE_LIBM"]),
            Object(Matching, "MSL_C/w_log10.c", extra_cflags=["-D_IEEE_LIBM"]),
            Object(Matching, "MSL_C/w_pow.c", extra_cflags=["-D_IEEE_LIBM"]),
            Object(Matching, "MSL_C/e_sqrt.c"),
            Object(Matching, "MSL_C/math_ppc.c"),
            Object(Matching, "MSL_C/w_sqrt.c", extra_cflags=["-D_IEEE_LIBM"]),
        ],
    },
]


# Optional callback to adjust link order. This can be used to add, remove, or reorder objects.
# This is called once per module, with the module ID and the current link order.
#
# For example, this adds "dummy.c" to the end of the DOL link order if configured with --non-matching.
# "dummy.c" *must* be configured as a Matching (or Equivalent) object in order to be linked.
def link_order_callback(module_id: int, objects: List[str]) -> List[str]:
    # Don't modify the link order for matching builds
    if not config.non_matching:
        return objects
    if module_id == 0:  # DOL
        return objects + ["dummy.c"]
    return objects


# Uncomment to enable the link order callback.
# config.link_order_callback = link_order_callback


# Optional extra categories for progress tracking
# Adjust as desired for your project
config.progress_categories = [
    ProgressCategory("game", "Game Code"),
    ProgressCategory("sdk", "SDK Code"),
]
config.progress_each_module = args.verbose
# Optional extra arguments to `objdiff-cli report generate`
config.progress_report_args = [
    # Marks relocations as mismatching if the target value is different
    # Default is "functionRelocDiffs=none", which is most lenient
    # "--config functionRelocDiffs=data_value",
]

if args.mode == "configure":
    # Write build.ninja and objdiff.json
    generate_build(config)
elif args.mode == "progress":
    # Print progress information
    calculate_progress(config)
else:
    sys.exit("Unknown mode: " + args.mode)
