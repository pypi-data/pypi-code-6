from transit.transit_types import true, false
                                    

if true:
    print("ok")
if not true:
    print("not ok")
if false:
    print("not ok")
if not false:
    print("ok")
if true and false:
    print("not ok")
if true or false:
    print("ok")
