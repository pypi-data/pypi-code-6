"""
babel.bin is an executable only module, and runs automatically on import.
"""

# Check args and import other important functions
from babel.bin.base import args, fail

# Expand args.TO if it matches an alias
import babel.bin.aliases

# Delegate sending based on recipient type
import re
if re.match(r"https?://.*", args.TO):
    import babel.bin.http
elif re.match(r"(\+\d{1,3})?\d{10}|\d{3}-\d{3}-\d{4}", args.TO):
    import babel.bin.sms
else:
    fail("Couldn't parse recipient address.")