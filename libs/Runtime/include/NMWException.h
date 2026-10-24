#pragma once

#include <cstring>
#include <__ppc_eabi_linker.h>
#include <size_t.h>

typedef void* ctor_dtor_ptr;

// From rb3's NMWException.h (see notes/PROVENANCE.md).
#ifdef __cplusplus
extern "C" {
#endif

typedef short vbase_ctor_arg_type;
typedef char local_cond_type;

typedef struct CatchInfo {
    void* location;
    void* typeinfo;
    void* dtor;
    void* sublocation;
    long pointercopy;
    void* stacktop;
} CatchInfo;

extern void __end__catch(CatchInfo* catchinfo);
extern void __throw(char* throwtype, void* location, void* dtor);
extern void __unexpected(CatchInfo* catchinfo);

#ifdef __cplusplus
}
#endif

extern "C"
{

    void* __construct_new_array(void*, ctor_dtor_ptr, ctor_dtor_ptr, size_t, size_t);
    void __construct_array(void*, ctor_dtor_ptr, ctor_dtor_ptr, size_t, size_t);
    void __destroy_arr(void*, ctor_dtor_ptr, size_t, size_t);
    void __destroy_new_array(void*, ctor_dtor_ptr);

    extern char __throw_catch_compare(const char* throwtype, const char* catchtype, long* offset_result);

    extern int __register_fragment(struct __eti_init_info*, char*);
    extern void __unregister_fragment(int);
};
