#include "extras.h"
#include "file_io.h"
#include "locale.h"

inline int tolower_inline(int c)
{
    return ((c < 0) || (c >= 0x100)) ? c : (int)(_current_locale.ctype_cmpt_ptr->lower_map_ptr[c]);
}

// strlwr: written for this project from the DOL (0x8038F8A4); mlab's DOL lacks it.
char* strlwr(char* str)
{
    char* p = str;

    while (*p)
    {
        *p = tolower_inline(*p);
        p++;
    }

    return str;
}

int stricmp(const char* s1, const char* s2)
{
    char c1, c2;

    while (1)
    {
        c1 = tolower_inline(*s1++);
        c2 = tolower_inline(*s2++);

        if (c1 < c2)
        {
            return -1;
        }

        if (c1 > c2)
        {
            return 1;
        }

        if (c1 == 0)
        {
            return 0;
        }
    }
}

#if 0 // Not present in this game's DOL (dead-stripped by the original link).
// strnicmp: from zeldaret/tp (CC0-1.0); present in this game's DOL.
int strnicmp(const char* str1, const char* str2, int n) {
    return __msl_strnicmp(str1, str2, n);
}
#endif

#if 0 // Not present in this game's DOL (dead-stripped by the original link).
int strncasecmp(const char* s1, const char* s2, size_t n)
{
    return __msl_strnicmp(s1, s2, n);
}
#endif

int strcmpi(const char* str1, const char* str2)
{
    return stricmp(str1, str2);
}

int strcasecmp(const char* s1, const char* s2)
{
    return stricmp(s1, s2);
}

#if 0 // Not present in this game's DOL (dead-stripped by the original link).
char* itoa(int value, char* str, int base)
{
    return __msl_itoa(value, str, base);
}
#endif
