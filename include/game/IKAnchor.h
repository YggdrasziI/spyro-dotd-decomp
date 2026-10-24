#ifndef GAME_IKANCHOR_H
#define GAME_IKANCHOR_H

// Class name from RTTI: "IKAnchor" (.rodata 0x804C1BC0), bases IKBaseClass and
// IKSerializable (base list lbl_804EF950). The real header name is unknown.

#include "game/IKSerializable.h"

// vtable lbl_804F0288
class IKAnchor : public IKSerializable {
public:
    IKAnchor();
    virtual ~IKAnchor();
    // vfC and vf5C sit at the end of the unit at 0x80327260 (next to that unit's
    // own weak functions): probably inline in the original header. Declared out of
    // line here so that this unit does not emit copies.
    virtual int vfC(unsigned long id);
    virtual void vf14();
    virtual int vf18();
    virtual int vf1C();
    virtual int vf28();
    virtual int vf2C();
    virtual int vf30(UnkStream* stream, int mode);
    virtual void vf54() = 0;
    virtual void vf58() = 0;
    virtual void vf5C(unsigned char value);
    virtual void vf60() = 0;
    virtual void vf64() = 0;
    virtual void vf68() = 0;
    virtual void vf6C() = 0;

    int m4;
    unsigned char m8;
    bool m9;
};

#endif
