#ifndef _RUNTIME_MWCPLUSLIB_H
#define _RUNTIME_MWCPLUSLIB_H

#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

#define CTORARG_TYPE int
#define CTORARG_COMPLETE (1)
#define CTORARG_PARTIAL (0)

#define CTORCALL_COMPLETE(ctor, objptr) (((void (*)(void *, CTORARG_TYPE))ctor)(objptr, CTORARG_COMPLETE))
#define CTORCALL_PARTIAL(ctor, objptr) (((void (*)(void *, CTORARG_TYPE))ctor)(objptr, CTORARG_PARTIAL))

#define DTORARG_TYPE int
#define DTORARG_COMPLETE (-1)
#define DTORARG_PARTIAL (0)

#define DTORCALL_COMPLETE(dtor, objptr) (((void (*)(void *, DTORARG_TYPE))dtor)(objptr, DTORARG_COMPLETE))
#define DTORCALL_PARTIAL(dtor, objptr) (((void (*)(void *, DTORARG_TYPE))dtor)(objptr, DTORARG_PARTIAL))

typedef void *ConstructorDestructor;

typedef struct DestructorChain {
    struct DestructorChain *next;
    void *destructor;
    void *object;
} DestructorChain;

void *__register_global_object(void *object, void *destructor, DestructorChain *regmem);
void __destroy_global_chain(void);
int __register_atexit(void (*)(void));

// The array functions are declared in NMWException.h (mlab's types).



#ifdef __cplusplus
}
#endif

#endif
