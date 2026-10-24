#ifndef GAME_IKSERIALIZABLE_H
#define GAME_IKSERIALIZABLE_H

// Class names come from RTTI: "IKBaseClass" (.rodata 0x804B8920), "IKSerializable"
// (0x804B8910). Methods are unknown: virtual functions are named after their vtable
// offset, parameter and return types are guesses that only have to give the same code.
// The real header name is unknown.

class UnkStream;

// vtable lbl_804C8308
class IKBaseClass {
public:
    IKBaseClass();
    virtual ~IKBaseClass();
    virtual int vfC(unsigned long id);
    virtual void vf10();
    virtual void vf14();
    virtual int vf18() = 0;
    virtual int vf1C() = 0;
    virtual int vf20();
    virtual int vf24();
};

// vtable lbl_804C82A8
class IKSerializable : public IKBaseClass {
public:
    IKSerializable();
    virtual ~IKSerializable();
    virtual int vfC(unsigned long id);
    virtual void vf14();
    virtual int vf28();
    virtual int vf2C();
    virtual int vf30(UnkStream* stream, int mode);
    virtual int vf34();
    virtual int vf38();
    virtual void vf3C();
    virtual int vf40();
    virtual int vf44();
    virtual int vf48();
    virtual void vf4C();
    virtual void vf50();
};

#endif
