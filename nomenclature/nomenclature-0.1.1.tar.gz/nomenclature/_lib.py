import pkgutil

from cffi import FFI

ffi = FFI()
ffi.cdef(pkgutil.get_data('nomenclature', 'c/cdef.h').decode('ascii'))
lib = ffi.verify(
    pkgutil.get_data('nomenclature', 'c/verify.h').decode('ascii'),
    ext_package='nomenclature',
    extra_compile_args=['-D_GNU_SOURCE']
    )

__all__ = ('lib', 'ffi')
