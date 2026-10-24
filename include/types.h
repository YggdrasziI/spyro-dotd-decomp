#ifndef TYPES_H
#define TYPES_H

#ifndef REVOLUTION_TYPES_H
typedef signed char s8;
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
typedef signed long long s64;
typedef unsigned long long u64;

typedef float f32;
typedef double f64;
#endif

#ifndef __cplusplus
typedef int bool;
#ifndef true
#define true 1
#endif
#ifndef false
#define false 0
#endif
#endif

#endif // TYPES_H
