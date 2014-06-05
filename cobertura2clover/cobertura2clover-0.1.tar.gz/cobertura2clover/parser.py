from bs4 import BeautifulSoup
import sys

def main(argv=sys.argv):
    def writetofile(output):
        output.write('<?xml version="1.0"?>\n')
        output.write('<coverage generated="'+ result['timestamp'] +'" clover="3.3">\n')
        output.write('<project timestamp="'+ result['timestamp'] +'">\n')
        output.write(
            '<metrics packages="1" files="'+ result['files'] +'" classes="'+ result['files'] +'" \
    complexity="0" loc="'+ result['loc'] +'" ncloc="'+ result['loc'] +'" \
    elements="'+ result['loc'] +'" statements="'+ result['loc'] +'" \
    coveredelements="'+ result['coveredelements'] +'" coveredstatements=\
    "'+ result['coveredelements'] +'" coveredconditionals="0" \
    conditionals="0" methods="0" coveredmethods="0"/>\n'
            )
        output.write('</project>\n')
        output.write('</coverage>')

        
    file_in = open(sys.argv[1], 'r')
    soup = BeautifulSoup(file_in, "xml")

    result = {}
    result['timestamp'] = soup.coverage['timestamp']
    result['files'] = str(len(soup.find_all('class')))
    result['loc'] = str(len(soup.find_all('line')))
    result['coveredelements'] = str(len(soup.find_all('line', hits=1)))

    output = open(sys.argv[2], 'a')
    writetofile(output)
    output.close()

