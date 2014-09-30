"""
Sanity tests for Builder
"""

import builder.builder

def test_builder():
    import _sdl.cdefs
    assert len(list(builder.builder.iter_declarations(_sdl.cdefs.ffi)))
