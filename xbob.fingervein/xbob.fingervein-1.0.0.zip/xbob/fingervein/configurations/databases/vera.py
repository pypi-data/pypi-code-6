#!/usr/bin/env python

import xbob.db.vera
import facereclib

vera_directory = "[YOUR_VERADB_DIRECTORY]"

database = facereclib.databases.DatabaseXBob(
    database = xbob.db.vera.Database(),
    name = 'vera',
    original_directory = vera_directory,
    original_extension = ".png",    
)
