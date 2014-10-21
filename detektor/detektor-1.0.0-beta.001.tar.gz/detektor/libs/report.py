import os


class ReportGen:
    def __init__(self, rdir, dir, filename):
        self.f = open(os.path.join(rdir, filename), 'w')
        self.directory = dir
        self.items = []
        
    def header(self):
        import time
        from datetime import datetime
        curtime = time.gmtime()
        curtime = datetime(curtime[0], curtime[1], curtime[2],
                           curtime[3], curtime[4], curtime[5]).ctime()
        self.f.write("""
<HTML>
<HEAD>
<TITLE>Detector Report</TITLE>

<STYLE>
BODY {
  background: #ABABAB;
}
TABLE {
  margin: 20px 60px 10px 100px;
  padding: 40px 40px 20px 40px;
  width: 80%%;
  border: 1px solid #898989;
  background: #EEE;
  text-size: %%90;
}
TR {
  border-bottom: 1px
}
TH {
  text-align: left;
  text-weight: bold
}
TD {
  vertical-align: top;
}
.foot {
  margin: 30px 0 10px 0;
  text-align: center;
  text-size: %%70;
}
</STYLE>
</HEAD>
<BODY>
<CENTER>
<H1 ALIGN='CENTER'>Detector Report</H1>
<p>Comparing files at %s
</p>

</CENTER>
<TABLE align='center'>
<TR><TH>Assignment</TH><TH>Student 1</TH><TH>Student 2</TH>
<TH>Summary</TH>
<TH>Points (avg)</TH>
<TH>View</TH>
</TR>
<TR><TD COLSPAN=6><hr></TD></TR>
        """  % curtime )

    def report(self, tuples):
        for t in tuples:
            ass = t[0]
            stud1 = t[1]
            stud2 = t[2]
            summary = t[3]
            points = t[4]
            avg = t[5]
            link = "<a href='" + t[6] + "'>go</a>"
            if summary[:10] == 'Programs v':
                s = ("""
                <TR> <TD>%s</TD> <TD BGCOLOR='red'>%s</TD> <TD BGCOLOR='red'>%s</TD>
                <TD>%s</TD><TD>%s (%s)</TD> <TD>%s</TD></TR>
                """ % (ass, stud1, stud2, summary, points, avg, link) )
            else:
                s = ("""
                <TR> <TD>%s</TD> <TD>%s</TD> <TD>%s</TD>
                <TD>%s</TD><TD>%s (%s)</TD> <TD>%s</TD></TR>
                """ % (ass, stud1, stud2, summary, points, avg, link) )
            self.f.write(s)
        
    def footer(self):
        self.f.write("""
</TABLE>
<DIV CLASS='foot'>
The Detector was implemented by Magne Westlie (magnew@simula.no)
</BODY>
</HTML>
        """)
        self.f.close()

    def make_diff_page(self, file, s1, s2):
        fp = open(os.path.join(self.directory, s1, file), 'r')
        s1_lines = fp.readlines()
        fp.close()
        fp = open(os.path.join(self.directory, s2, file), 'r')
        s2_lines = fp.readlines()
        fp.close()
        self.f.write("""
        <html>
        <body>
        <table width='100%' border='1px'>
        <tr>
        <td width='50%' valign='top'>
        <pre>\n""")
        for l in s1_lines:
            self.f.write(l)
        self.f.write("</pre></td><td width='50%' valign='top'><pre>\n")
        for l in s2_lines:
            self.f.write(l)
        self.f.write("</pre></td></tr></table></body></html>")
        self.f.close()
