#include <new>
#include <stdlib.h>

// Written for this project from the DOL (0x80380AD0): this DOL keeps the library's
// operator new, which rb3's DOL does not have.
static std::new_handler __new_handler;

void* operator new(std::size_t size) throw(std::bad_alloc) {
    void* ptr;

    if (size == 0) {
        size = 4;
    }

    for (;;) {
        if ((ptr = malloc(size)) != NULL) {
            break;
        }

        if (__new_handler) {
            __new_handler();
        } else {
            throw std::bad_alloc();
        }
    }

    return ptr;
}
