// From mlab-decomp; OSAllocFromMEM1ArenaLo from tp (see notes/PROVENANCE.md).
#include <revolution/os.h>

// From tp's include/global.h (CC0).
#define ROUND(n, a) (((u32)(n) + (a)-1) & ~((a)-1))

void* __OSArenaLo = (void*)-1;
void* __OSArenaHi = NULL;

static void* s_mem2ArenaLo = (void*)-1;
static void* s_mem2ArenaHi = NULL;

void* OSGetMEM1ArenaHi(void) {
    return __OSArenaHi;
}

void* OSGetMEM2ArenaHi(void) {
    return s_mem2ArenaHi;
}

void* OSGetArenaHi(void) {
    return OSGetMEM1ArenaHi();
}

void* OSGetMEM1ArenaLo(void) {
    return __OSArenaLo;
}

void* OSGetMEM2ArenaLo(void) {
    return s_mem2ArenaLo;
}

void* OSGetArenaLo(void) {
    return OSGetMEM1ArenaLo();
}

void OSSetMEM1ArenaHi(void* hi) {
    __OSArenaHi = hi;
}

void OSSetMEM2ArenaHi(void* hi) {
    s_mem2ArenaHi = hi;
}

void OSSetArenaHi(void* hi) {
    OSSetMEM1ArenaHi(hi);
}

void OSSetMEM1ArenaLo(void* lo) {
    __OSArenaLo = lo;
}

void OSSetMEM2ArenaLo(void* lo) {
    s_mem2ArenaLo = lo;
}

void OSSetArenaLo(void* lo) {
    OSSetMEM1ArenaLo(lo);
}

// From tp (CC0), libs/revolution/src/os/OSArena.c: mlab's version adds the operands of
// the second rounding in the other order.
void* OSAllocFromMEM1ArenaLo(u32 size, u32 align) {
    void* ptr;
    u8* arenaLo;

    ptr = OSGetMEM1ArenaLo();
    arenaLo = ptr = (void*)ROUND(ptr, align);
    arenaLo += size;
    arenaLo = (u8*)ROUND(arenaLo, align);
    OSSetMEM1ArenaLo(arenaLo);
    return ptr;
}

void* OSAllocFromMEM2ArenaLo(u32 size, u32 align) {
    u8* begin = PTR_ROUNDUP(OSGetMEM2ArenaLo(), align);
    u8* end = begin + size;
    end = PTR_ROUNDUP(end, align);

    OSSetMEM2ArenaLo(end);

    return begin;
}
