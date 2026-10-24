// Unit 0x8032E43C-0x8032E5E4: IKAnchor methods, then the static initializer.
// Bounds: starts after the __sinit of the previous unit (0x8032E3B8, .ctors
// 0x804B87F8) and ends with its own __sinit (0x8032E5A0, .ctors 0x804B87FC).
// Real file name unknown.
// Flags: -opt nopeephole (see notes/COMPILER.md, game-code compiler test).

#include "game/IKAnchor.h"

// Small object built from two floats, constructed by about 180 static
// initializers with (-1.0f, -1.0f): probably a static object of a shared header.
class UnkFloat2 {
public:
    UnkFloat2(float x, float y);
    ~UnkFloat2();

    float x;
    float y;
};

extern "C" void fn_8000CF50(UnkStream* stream, void* data);
extern "C" void fn_80012684(UnkStream* stream, void* data, int size);

static UnkFloat2 lbl_805CDF60(-1.0f, -1.0f);

IKAnchor::IKAnchor() {}

IKAnchor::~IKAnchor() {}

void IKAnchor::vf14() { IKSerializable::vf14(); }

int IKAnchor::vf28() {
    IKSerializable::vf28();
    return 1;
}

int IKAnchor::vf2C() {
    IKSerializable::vf2C();
    return 1;
}

int IKAnchor::vf30(UnkStream* stream, int mode) {
    IKSerializable::vf30(stream, mode);
    switch (mode) {
    case 0:
        fn_8000CF50(stream, &m4);
        fn_80012684(stream, &m8, 1);
        break;
    }
    return 1;
}

int IKAnchor::vf1C() { return 0x184; }

int IKAnchor::vf18() { return 0xc; }
