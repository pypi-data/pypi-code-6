# -*- coding: utf-8 -*-

qsl = u"""{survey om_psy239460_Chromebook2_130121 title="Umfrage" language="de_DE" widget_all_required=HARD nav_back=0 extrajs="https://umfrage2.yougov.de/static/yg_2012.js" extracss="https://umfrage2.yougov.de/static/yg_2012.css"}

{page einleitung}

{text}
<<div style="font-size:17px; margin-left:10px;">
<p><b>Sehr geehrte Teilnehmerin, sehr geehrter Teilnehmer,  </b></p>
<p>&nbsp;</p>
<p>zuerst möchten wir uns für Ihre Teilnahmebereitschaft an dieser Online-Befragung zum Thema "Computer" herzlich bedanken.</p>
<p>&nbsp;</p>
<p>Die Befragung wird ca. 5 Minuten dauern und Sie bekommen bis zu 250 Punkte gutgeschrieben. Selbstverständlich werden Ihre Angaben vollständig anonym behandelt; der Datenschutz wird strengstens eingehalten.</p>
<p>&nbsp;</p>
<p>Benutzen Sie bitte ausschließlich die Pfeil-Schaltfläche im unteren Teil des Fragebogens, um zur nächsten Seite zu gelangen.</p>
<p>&nbsp;</p>
<p>Sie können die Befragung starten, indem Sie auf den „Pfeil nach rechts“ klicken.</p>
<p>&nbsp;</p>
<p><b>Viel Spaß bei der Umfrage!</b></p>
</div>>
{end text}


{end page einleitung}


{page ms_redirect}

{goto survey mediascale_redirect_20120615 resume=blank_skipped}

{end page ms_redirect}


{page blank_skipped}

{end page blank_skipped}


{text if 0}
All German adults
{end text}


[unaided1] {single} An welche Produkte denken Sie bei tragbaren Computern, die zum Schreiben von E-Mails, zum Surfen im Internet und zum Erstellen von Dokumenten verwendet werden können? Geben Sie Ihre Antwort in das unten stehende Feld ein. Trennen Sie dabei einzelne Angaben mit Semikolons (";") voneinander ab.
<1> [q1_open] {open rows=6 cols=60 prompt=""}
<2 xor> Mir fallen keine ein.

{text if 0}
All German adults
{end text}

[aided] {multiple order=randomize} Welche der folgenden Produkte kennen Sie? Wählen Sie alle zutreffenden Antworten aus – auch Produkte, die Sie gegebenenfalls in der vorherigen Frage genannt haben.
<1>  Chromebook
<2>  Acer Aspire One
<3>  Asus Eee PC
<4>  Apple Macbook Air
<5>  Toshiba Satellite
<6>  Apple iPad
<7>  Samsung Galaxy Tab
<8>  Kindle Fire
<9>  Blackberry Playbook
<10>  Galaxy Note
<11>  HP Envy Spectre
<12>Chromebox
<13>Nexus 7
<14>Microsoft Surface
<15 fixed xor> Ich kenne keines dieser Produkte.

{text if 0}
All German adults
{end text}

[buzz] {multiple} Haben Sie im letzten Monat irgendetwas über Chromebooks gelesen, gehört oder gesehen?
<1> Ja, ich habe etwas Positives über Chromebooks gehört.
<2> Ja, ich habe etwas Negatives über Chromebooks gehört.
<3> Ja, ich habe etwas gehört, das weder positiv noch negativ war.
<4 xor> Nein, ich habe nichts über Chromebooks gehört.



{text if 0}
All German adults who saw, read or heard something positive about Chromebooks in the last month
{end text}

 [buzzopen if 1 in buzz] {open rows=5 cols=50} Was haben Sie letzten Monat _Positives_ über Chromebooks gelesen, gehört oder gesehen? Geben Sie Ihre Antwort im Feld unten ein. Machen Sie möglichst genaue Angaben.



{text if 0}
All German adults who saw, read or heard something negative about Chromebooks in the last month
{end text}

[buzzopen2 if 2 in buzz]  {open rows=5 cols=50} Was haben Sie letzten Monat _Negatives_ über Chromebooks gelesen, gehört oder gesehen? Geben Sie Ihre Antwort im Feld unten ein. Machen Sie möglichst genaue Angaben.


 {text if 0}
All German adults who saw, read or heard something about Chromebooks in the last month
{end text}

 [buzzwhere if buzz.has_any([1,2,3])] {multiple order=randomize} Wo haben Sie etwas zu Chromebooks gehört oder gesehen? Wählen Sie alle zutreffenden Antworten aus.

<1>  In einer Fernsehsendung
<2>  In einem Artikel in einer Zeitschrift oder Zeitung
<3>  Auf einer Nachrichtenseite im Internet oder einem Blog
<4>  Im Fernsehen
<5>  In einer Zeitschrift
<6>  In einer Zeitung
<7>  Im Internet
<8>  Bei Familie oder Freunden
<9>  In sozialen Netzwerken wie Facebook oder Twitter
<10>  In einem Geschäft wie PC World oder John Lewis
<11 fixed>  Andere [buzzwhereother] {open cols=50}


  {text if 0}
All German adults who have heard of Chromebooks
{end text}




 [knowcbook if 1 in aided] Wie viel wissen Sie über das Chromebook?
<1>  Sehr viel
<2>  Viel
<3>  Relativ viel
<4>  Ein bisschen
<5>  Nichts






   {text if 0}
All German adults who have heard of Chromebooks and know about it
{end text}



 [promoter if 1 in aided and not knowcbook==5] Bitte bewerten Sie auf einer Skala von 0 bis 10 (0 für "Eher unwahrscheinlich", 10 für "Sehr wahrscheinlich"), wie wahrscheinlich es ist, dass Sie das Chromebook Ihrer Familie und Freunden empfehlen.
<1>  0 – Eher unwahrscheinlich
<2>  1
<3>  2
<4>  3
<5>  4
<6>  5
<7>  6
<8>  7
<9>  8
<10>  9
<11>  10 – Sehr wahrscheinlich
<12>  Ich weiß es nicht.


    {text if 0}
All German adults
{end text}


[intent] {single} Haben Sie vor, in den kommenden sechs Monaten einen neuen Laptop, ein Netbook oder ein Tablet zu kaufen?
<1>  Das habe ich fest vor
<2>  Das ist recht wahrscheinlich
<3>  Ich weiß es noch nicht
<4>  Das ist eher unwahrscheinlich
<5>  Das habe ich bestimmt nicht vor


 {text if 0}
All German adults who have heard of Chromebooks and plan to buy a a new laptop, netbook, or tablet computer in the next 6 months
{end text}


[likelybuy if 1 in aided and intent in[1,2]] {single} Wie wahrscheinlich ist es, dass Sie sich bei einem Computerneukauf für ein Chromebook entscheiden?
<1> Sehr wahrscheinlich
<2> Wahrscheinlich
<3> Möglich
<4> Eher unwahrscheinlich
<5> Äußerst unwahrscheinlich

 # Segmentation



  {
intent_Text = ""
if intent in [1,2]:
 intent_Text = „Sie haben erwähnt, dass sie planen, im nächsten Jahr einen Laptop, ein Netbook oder einen Tablet-Computer zu kaufen. Wie viel werden Sie dafür höchstens ausgeben?“
elif intent in [3,4,5]:
 intent_Text = „Falls Sie planen würden, im nächsten Jahr einen Laptop, ein Netbook oder einen Tablet-Computer zu kaufen,  wie viel würden Sie dafür höchstens ausgeben? ”
}


#21a.
[budget] {open-intrange 0 10000 left="&pound;"} $intent_Text (Geben Sie Ihre Antwort in Zahlen an.)
#<350€ - Tech attitude questions set #1
#350€-599€ - Tech attitude questions set #2
#>599€ - Tech attitude questions set #3

{
set = 0
if int(budget) < 350:
    set = 1
if int(budget) >= 350 and int(budget) < 599:
    set = 2
if int(budget) >= 599:
    set = 3
}

[segmentation1 if set == 1] {grid roworder=randomize colorder=reverse} Wie sehr stimmen Sie folgenden Äußerungen zu bzw. nicht zu?
 -[trend] Ich schließe mich neuen Trends viel später an als andere.
 -[deal] Ich suche immer nach dem besten Angebot und kaufe meist das kostengünstigste Produkt, das ich finden kann.
 -[simple] Ich brauche nicht unbedingt mehr Funktionen als E-Mails, Internetsurfen und Nachrichten.
 -[social_friends] Ich finde ein erfülltes Privatleben sehr wichtig und gehe häufig mit Freunden aus.
 -[social_networks] Soziale Netzwerke spielen in meinem Alltag eine wichtige Rolle.
 -[social_tool] Mein Computer ist sehr wichtig für mich, um Beziehungen zu meinen Freunden zu pflegen.
 -[cautious] Ich bin vorsichtig beim Kauf eines neuen Produkts. Normalerweise kaufe ich ein Produkt erst, wenn es meines Erachtens sicher ist und ich weiß, dass viele Leute es gerne verwenden.
 -[family] Meine Familie ist mir wichtiger als meine Arbeit und Karriere.
 -[shares] Ich teile meinen Computer mit meiner Familie.

 <1> Ich stimme vollkommen zu.
 <2> Ich stimme teilweise zu.
 <3> Ich bin neutral.
 <4> Ich stimme eher nicht zu.
 <5> Ich stimme nicht zu.
 <6 fixed> Ich habe keine Meinung dazu.

[segmentation2 if set == 2] {grid roworder=randomize colorder=reverse} How strongly do you agree or disagree with the following statements?
 -[brand] Ich glaube, dass eine Marke qualitativ hochwertigere Produkte hat, je berühmter sie ist.
 -[risk_adverse] Ich gehe nicht gerne Risiken ein. Ich kaufe lieber bekannte und sichere Produkte für meine Familie.
 -[follower] Ich kaufe gerne Produkte, die in meinem Umfeld am meisten verwendet werden.
 -[design] Für mich ist beim Kauf eines neuen Produkts das Design wichtiger als die Anzahl der Funktionen.
 -[appearance] Es ist mir wichtig, wie ich auf andere wirke.
 -[expression] Mein Computer ist Ausdruck meiner Persönlichkeit und Individualität.
 -[entertainment] In meiner Freizeit beschäftige ich mich gerne mit Technologie.
 -[functional] Für mich sind beim Kauf eines neuen Produkts die Funktionen wichtiger als das Design.
 -[quickly] Ich möchte einen Computer, mit dem ich schnell auf gespeicherte Dateien zugreifen und gleichzeitig im Internet surfen kann.

  <1> Ich stimme vollkommen zu.
 <2> Ich stimme teilweise zu.
 <3> Ich bin neutral.
 <4> Ich stimme eher nicht zu.
 <5> Ich stimme nicht zu.
 <6 fixed> Ich habe keine Meinung dazu.

[segmentation3 if set == 3] {grid roworder=randomize colorder=reverse} Wie sehr stimmen Sie folgenden Äußerungen zu bzw. nicht zu?
 -[on_the_go] Ich bin ständig unterwegs und muss für meine Arbeit immer erreichbar sein.
 -[basics] Es ist mir egal, was ein Computer kostet, so lange er mir dabei hilft, meine Arbeit effizienter zu gestalten.
 -[syncs] Ich synchronisiere meinen Computer mit anderen Geräten, damit ich meine To-Do-Listen, Kalender, Kontakte und andere Informationen immer zur Hand habe.
 -[risk_taker] Ich probiere gerne neue Dinge aus und gehe Risiken ein.
 -[premium] Ich bin bereit, für die neueste Technologie einen Aufschlag zu bezahlen.
 -[techie] Ich interessiere mich sehr für die neuesten Technologien und verbringe viel Zeit damit.
 -[status] Ich drücke meinen sozialen Status durch hochwertige Produkte aus.
 -[newest] Ich liebe neue Produkte mit brandneuen Funktionen und Designs.
 -[latest] Es ist mir egal, was ein Computer kostet, solange er über die neuesten Funktionen verfügt.
<1> Ich stimme vollkommen zu.
 <2> Ich stimme teilweise zu.
 <3> Ich bin neutral.
 <4> Ich stimme eher nicht zu.
 <5> Ich stimme nicht zu.
 <6 fixed> Ich habe keine Meinung dazu.




{page sozio_start if not pdl.gender or (not pdl.sta or pdl.sta.last > months(12))}

[GESCHL if not pdl.gender] {pdl-update gender}

[BUNDESLAND if (not pdl.sta or pdl.sta.last > months(12))] {pdl-update sta}


{page birthx if (not pdl.birthmonth or not pdl.birthyear or (pdl.birthmonth.last > months(12) or pdl.birthyear.last > months(12)))}


<<style>

#leftgrid .question-text {
width:100%;
float:left
}

#leftgrid .question-cont {
width:50%;
float:left;
}

#rightgrid .question-text {
width:100%;
float:right
}
#rightgrid .question-cont {
width:50%;
float:right;
clear:none
}

</style>>

<<div id="leftgrid">>
[qbirthmonth] {dropdown default_text="- Bitte wählen Sie einen Monat aus -"} Wann sind Sie geboren?
 <1> Januar
 <2> Februar
 <3> März
 <4> April
 <5> Mai
 <6> Juni
 <7> Juli
 <8> August
 <9> September
 <10> Oktober
 <11> November
 <12> Dezember

<</div>>

<<div id="rightgrid">>

[qbirthyear] {open-intrange 1900 2000 cols=4 right="Jahr"} &nbsp;

<</div>>


{

if qbirthmonth:
  pdl.birthmonth.set(str(qbirthmonth.value))

if qbirthyear:pdl.birthyear.set(str(qbirthyear))
}

{end page birthx}



{page sozio_vi if (not pdl.educ or not pdl.housz or not pdl.hinc or (pdl.educ.last > months(12) or pdl.housz.last > months(12) or pdl.hinc.last > months(12)))}

[HHNE if (not pdl.hinc or pdl.hinc.last > months(12))] {pdl-update hinc}

[BILDUNG if (not pdl.educ or pdl.educ.last > months(12))] {pdl-update educ}

[HHGR if (not pdl.housz or pdl.housz.last > months(12))] {pdl-update housz}

{end page sozio_vi}



# [qc_points] {single varlabel="vergebene Punkte"} vergebene Punkte für diese Studie - für QC
# <0> 0 min
# <50> 1 min
# <100> 2 min
# <125> für BIX
# <150> 3 min
# <200> 4 min
# <250> 5 min
# <300> 6 min
# <350> 7 min
# <400> 8 min
# <450> 9 min
# <500> 10 min
# <550> 11 min
# <600> 12 min
# <650> 13 min
# <700> 14 min
# <750> 15 min
# <800> 16 min
# <850> 17 min
# <900> 18 min
# <950> 19 min
# <1000> 20 min
# <1250> 25 min
# <1500> 30 min
# <1750> 35 min
# <2000> 40 min
# <2500> 50 min
#
#[qc_team] {single varlabel="Projektteam"} Projektteam für QC
# <19> Operations Data Collection
# <17> Marketing
# <31> FDL1
# <33> FDL3
# <34> Industry&Telecoms
# <35> FDL2
# <44> Organisational Consulting
# <47> Consumer & Products
# <55> BrandIndex (Products)
# <65> Service Rating
# <66> Recruitment DE

{page QC}
{
if panman.is_panelist: panman.grant()
pdl.qc_team.set(47)
pdl.qc_points.set(250)
}
{end page QC}


{page ende timeout=2}

{text}
<<div style="font-size:16px; margin-left:10px;">
<p>Sie sind am Ende des Fragebogens angekommen.</p>
<p>&nbsp;</p>
<p>Wir möchten uns herzlich bei Ihnen bedanken!</p>
<p>&nbsp;</p>
<p>Wir wünschen Ihnen noch einen schönen Tag!</p>
</div>>
{end text}

{end page ende}
"""
