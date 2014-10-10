# Apple plist parsing
import sys
sys.path.append('.')
import dum


# Document object model
class Dict:
    class dum:
        pass

    def dum_projection(self):
        return dict(zip(self.entries[::2], self.entries[1::2]))


class Array:
    def dum_projection(self):
        return self.objects


class Plist:
    class dum:
        objects = dum.group(dict=Dict, array=Array, integer=int, string=str)

    def dum_projection(self):
        return self.objects[0]

# forward declarations
Array.dum = Plist.dum
Dict.dum.entries = dum.group(key=str, dict=Dict, array=Array, integer=int,
                             string=str)


# Document object model
def plist(s):
    return dum.xmls(Plist, s)

# https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/PropertyLists/UnderstandXMLPlist/UnderstandXMLPlist.html
if __name__ == "__main__":
    SAMPLE = """<plist version="1.0">
<dict>
    <key>Author</key>
    <string>William Shakespeare</string>
    <key>Lines</key>
    <array>
        <string>It is a tale told by an idiot,</string>
        <string>Full of sound and fury, signifying nothing.</string>
    </array>
    <key>Birthdate</key>
    <integer>1564</integer>
</dict>
</plist>"""
    print(plist(SAMPLE))
