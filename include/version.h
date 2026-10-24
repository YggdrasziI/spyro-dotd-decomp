#ifndef VERSION_H
#define VERSION_H

/* Game versions. BUILD_VERSION is the index of the version in configure.py VERSIONS. */
#define VERSION_EUR 0 /* RO8P7D, Europe (En,Fr,De,Es,It,Nl) */
#define VERSION_SCA 1 /* RO8X7D, Scandinavia (En,Sv,No,Da,Fi) */
#define VERSION_USA 2 /* RO8E7D, USA (En,Fr,Es) */

#define REGION_PAL (BUILD_VERSION == VERSION_EUR || BUILD_VERSION == VERSION_SCA)
#define REGION_USA (BUILD_VERSION == VERSION_USA)

#endif
