#!/usr/bin/env python

import xbob.db.utfvp
import facereclib

utfvp_directory = "[YOUR_UTFVPDB_DIRECTORY]"

database = facereclib.databases.DatabaseXBob(
    database = xbob.db.utfvp.Database(),
    name = 'utfvp',
    original_directory = utfvp_directory,
    original_extension = ".png"
)
