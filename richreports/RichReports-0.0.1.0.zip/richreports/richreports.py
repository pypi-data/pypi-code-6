#####################################################################
## 
## richreports.py
##
##   A library that supports the manual and automated assembly of
##   modules for building interactive HTML reports consisting of
##   abstract syntax trees as concrete syntax annotated with the
##   results of static analysis and abstract interpretation
##   algorithms.
##
##   Web:     richreports.org
##   Version: 0.0.1.0
##
##

#####################################################################
## Rich report data structure definitions.
##

import uxadt
_ = None

uxadt._({

  # Highlight
  'HighlightUnbound': [],
  'HighlightUnreachable': [],
  'HighlightDuplicate': [],
  'HighlightError': [],
  'Highlight': [_],

  # Category
  'Keyword': [],
  'Literal': [],
  'Constant': [],
  'Variable': [],
  'Error': [],

  # Entity
  'Lt': [],
  'Gt': [],
  'Space': [],
  'Ampersand': [],

  # Report
  'Text': [_],
  'C': [_,_,_,_],
  'Conc': [_],
  'Entity': [_],
  'Field': [_],
  'Row': [_],
  'Table': [_],
  'Indent': [_],
  'Line': [_,_],
  'LineIfFlat': [_,_],
  'Atom': [_,_,_],
  'Span': [_,_,_],
  'Block': [_,_,_],
  'BlockIndent': [_,_,_],
  'Intersperse': [_,_],
  'Finalize': [_]
  })

#####################################################################
## Interactive HTML report rendering functions.
##

def entity(e):
  return e\
    ._(Lt(),        lambda: '&lt;')\
    ._(Gt(),        lambda: '&gt;')\
    ._(Space(),     lambda: '&nbsp;')\
    ._(Ampersand(), lambda: '&amp;')\
    .end


def highlight(h):
  return h\
    ._(HighlightUnbound(),     lambda: ['RichReports_Highlight_Unbound'])\
    ._(HighlightUnreachable(), lambda: ['RichReports_Highlight_Unreachable'])\
    ._(HighlightDuplicate(),   lambda: ['RichReports_Highlight_Duplicate'])\
    ._(HighlightError(),       lambda: ['RichReports_Highlight_Error'])\
    ._(Highlight(_),           lambda hs: hs)\
    .end


def messageToAttr(ms):
  def conv(m):
    return '\''+html(m)\
      .replace('"', '&quot;')\
      .replace('\'', '\\\'')\
      .replace('\n', '')\
      .replace('\r', '')\
      + '\''
  return 'onclick=msg(this, ['+ ','.join([conv(m) for m in ms]) +']);'


def html(r):
  def html0(rs):
    return ''.join([html(r) for r in rs])
  return r\
    ._(Text(_), lambda s: s)\
    ._(C(_,_,_,_), lambda c,hs,ms,s:
      '<span class="RichReports_"'+c\
      + (' RichReports_Clickable' if hs else '')\
      + (' RichReports_Highlightable' if ms else '')\
      + ' '.join([highlight(h) for h in hs])\
      + '" ' + (messageToAttr(ms) if ms else '')\
      + '>' + s + '</span>'\
      )\
    ._(Conc(_), html0)\
    ._(Entity(_), entity)\
    ._(Field(_), lambda rs: '<td>'+ html0(rs) + '</td>')\
    ._(Row(_), lambda rs: '<tr>' + html0(rs) + '</tr>')\
    ._(Table(_), lambda rs: '<table>' + html0(rs) + '</table>')\
    ._(Line(_,_), lambda _,rs: '<div>' + html0(rs) + '</div>')\
    ._(Atom(_,_,_), lambda hs,ms,rs:\
      '<span><span class="RichReports_Clickable" '+messageToAttr(ms)+'><span class="'+ ''.join([highlight(h) for h in hs]) +'">' + html0(rs) + '</span></span></span>'\
      if ms\
      else '<span class="'+ ''.join([highlight(h) for h in hs]) +'">' + html0(rs) + '</span>'\
      )\
    ._(Span(_,_,_), lambda hs,ms,rs:\
      '<span><span class="RichReports_Clickable RichReports_Clickable_Exclamation" '+messageToAttr(ms)+'>!</span><span class="'+ ''.join([highlight(hs) for h in hs]) +'">' + html0(rs) + '</span></span>'\
      if ms\
      else '<span class="'+ ''.join([highlight(hs) for h in hs]) +'">' + html0(rs) + '</span>'\
      )\
    ._(Block(_,_,_), lambda _0,_1,rs: '<div>' + html0(rs) + '</div>')\
    ._(BlockIndent(_,_,_), lambda _0,_1,rs: '<div class="RichReports_BlockIndent">' + html0(rs) + '</div>')\
    ._(Intersperse(_,_), lambda r,rs: html(r).join([html(r0) for r0 in rs]))\
    ._(Finalize(_), lambda r: '''
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {
              font-family: "Courier", monospace;
              font-size: 12px;
            }
            table {
              font-family: "Courier", monospace;
              font-size: 12px;
            }
            #RichReports_Message {
              background-color: yellow;
              padding: 3px;
              border: 1px solid black;
              font-family: "Courier", monospace;
              font-size: 12px;
              cursor: pointer;
            }
            .RichReports_Clickable {
              cursor: pointer;
            }
            .RichReports_Clickable_Exclamation {
              background-color: yellow;
              border: 1px solid black;
              margin: 0px 5px 1px 5px;
              padding: 0px 2px 0px 2px;
              font-size: 9px;
            }
            .RichReports_Clickable:hover {
              background-color: yellow;
            }
            .RichReports_Keyword {
              font-weight: bold;
              color: blue;
            }
            .RichReports_Variable {
              font-style: italic;
              color: green;
            }
            .RichReports_Literal {
              font-weight: bold;
              color: firebrick;
            }
            .RichReports_Error {
              font-weight: bold;
              color: red;
              text-decoration: underline;
            }
            .RichReports_Highlight             { margin:           2px;       }
            .RichReports_Highlight_Unbound     { background-color: orange;    }
            .RichReports_Highlight_Unreachable { background-color: orange;    }
            .RichReports_Highlight_Duplicate   { background-color: yellow;    }
            .RichReports_Highlight_Error       { background-color: lightpink; }
            .RichReports_BlockIndent           { margin-left:      10px;      }
          </style>
          <script type="text/javascript", src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
          <script type="text/javascript">
            funciton msg (obj, msgs) {
              var html = '';
              for (var i = 0; i < msgs.length; i++)
                html += '<div class="RichReports_MessagePortion">' + msgs[i] + '</div>';
              document.getElementById('RichReports_Message').innerHTML = html;
              document.getElementById('RichReports_Message').style.display = 'inline-block';
              var top = $(obj).offset().top;
              var left = $(obj).offset().left;
              $('#RichReports_Message').offset({top:top + 15, left:left + 15});
            }     
          </script>
        </head>
        <body>
          ''' + html(r) + '''
          <div id="RichReports_Message" style="display:none;" onclick="this.style.display='none';"></div>
        </body>
        </html>
      ''')\
    .end

##eof
