"""
Book name and number information; common to all translation data
"""

book_names = {
    1:("GEN","Genesis","Gn"),
    2:("EXO","Exodus","Ex"),
    3:("LEV","Leviticus","Lv"),
    4:("NUM","Numbers","Nm"),
    5:("DEU","Deuteronomy","Dt"),
    6:("JOS","Joshua","Jos"),
    7:("JDG","Judges","Jgs"),
    8:("RUT","Ruth","Ru"),
    9:("1SA","1 Samuel","1 Sm"),
    10:("2SA","2 Samuel","2 Sm"),
    11:("1KI","1 Kings","1 Kgs"),
    12:("2KI","2 Kings","2 Kgs"),
    13:("1CH","1 Chronicles","1 Chr"),
    14:("2CH","2 Chronicles","2 Chr"),
    15:("EZR","Ezra","Ezr"),
    16:("NEH","Nehemiah","Neh"),
    17:("EST","Esther","Est"),
    18:("JOB","Job","Jb"),
    19:("PSA","Psalms","Ps"),
    20:("PRO","Proverbs","Prv"),
    21:("ECC","Ecclesiastes","Eccl"),
    22:("SOS","Song of Solomon","Sg"),
    23:("ISA","Isaiah","Is"),
    24:("JER","Jeremiah","Jer"),
    25:("LAM","Lamentations","Lam"),
    26:("EZE","Ezekiel","Ez"),
    27:("DAN","Daniel","Dn"),
    28:("HOS","Hosea","Hos"),
    29:("JOE","Joel","Jl"),
    30:("AMO","Amos","Am"),
    31:("OBA","Obadiah","Ob"),
    32:("JON","Jonah","Jon"),
    33:("MIC","Micah","Mi"),
    34:("NAH","Nahum","Na"),
    35:("HAB","Habakkuk","Hb"),
    36:("ZEP","Zephaniah","Zep"),
    37:("HAG","Haggai","Hg"),
    38:("ZEC","Zechariah","Zec"),
    39:("MAL","Malachi","Mal"),
    40:("MAT","Matthew","Mt"),
    41:("MAR","Mark","Mk"),
    42:("LUK","Luke","Lk"),
    43:("JOH","John","Jn"),
    44:("ACT","Acts","Acts"),
    45:("ROM","Romans","Rom"),
    46:("1CO","1 Corinthians","1 Cor"),
    47:("2CO","2 Corinthians","2 Cor"),
    48:("GAL","Galatians","Gal"),
    49:("EPH","Ephesians","Eph"),
    50:("PHP","Philippians","Phil"),
    51:("COL","Colossians","Col"),
    52:("1TH","1 Thessalonians","1 Thes"),
    53:("2TH","2 Thessalonians","2 Thes"),
    54:("1TI","1 Timothy","1 Tm"),
    55:("2TI","2 Timothy","2 Tm"),
    56:("TIT","Titus","Ti"),
    57:("PHM","Philemon","Phlm"),
    58:("HEB","Hebrews","Heb"),
    59:("JAM","James","Jas"),
    60:("1PE","1 Peter","1 Pt"),
    61:("2PE","2 Peter","2 Pt"),
    62:("1JO","1 John","1 Jn"),
    63:("2JO","2 John","2 Jn"),
    64:("3JO","3 John","3 Jn"),
    65:("JDE","Jude","Jude"),
    66:("REV","Revelation","Rv") }
    
#Creating reverse dictionary of book_names data (i.e. keyed to book name and returning corresponding book number)
book_numbers = {}
for book, names in book_names.items():
   for name in names:
      book_numbers[name.upper()] = book
