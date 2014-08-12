from cffi import FFI
ffi = FFI()

ffi.cdef("""
void set_callback( void(*)() );
void callmeback();
""")


lib = ffi.verify("""
void (*_callback)() = 0;

void set_callback( void(*callback)() )
{
   _callback = callback;
}

void callmeback() {
    _callback();
}
""")


_callback = None

@ffi.callback('void(*)()')
def callback_py():
    print 'ff'
    @ffi.callback('void(*)()')
    def callback():
        print 'd'
    return callback

lib.set_callback(callback_py())

#callback_py(None)

lib.callmeback()
