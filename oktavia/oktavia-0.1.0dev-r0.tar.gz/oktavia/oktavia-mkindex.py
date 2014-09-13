import sys
import argparse
import snowballstemmer
from . import oktavia
from . import htmlparser
from . import csvparser
from . import textparser
from . import stemmer

def usage():
    print(''.join([
        "usage: oktavia-mkindex-cli [options]",
        "",
        "Common Options:",
        " -i, --input [input folder/file ] : Target files to search. .html, .csv, .txt are available.",
        " -o, --output [outputfolder]      : Directory that will store output files.",
        "                                  : This is a relative path from root.",
        "                                  : Default value is 'search'. ",
        " -t, --type [type]                : Export type. 'index', 'base64', 'cmd', 'js(default)',",
        "                                  : 'commonjs' 'web', are available.",
        "                                  : 'index' is a just index file. 'cmd' is a base64 code with search program.",
        "                                  : Others are base64 source code style output.",
        " -m, --mode [mode]                : Mode type. 'html', 'csv', 'text' are available.",
        " -c, --cache-density [percent]    : Cache data density. It effects file size and search speed.",
        "                                  : 100% become four times of base index file size. Default value is 5%.",
        "                                  : Valid value is 0.1% - 100%.",
        " -n, --name [function]            : A variable name for 'js' output or property name",
        "                                  : for 'js' and 'commonjs'. Default value is 'searchIndex'.",
        " -q, --quiet                      : Hide detail information.",
        " -h, --help                       : Display this message.",
        "",
        "HTML Mode Options:",
        " -r, --root  [document root]      : Document root folder. Default is current. ",
        "                                  : Indexer creates result file path from this folder.",
        " -p, --prefix [directory prefix]  : Directory prefix for a document root from a server root.",
        "                                  : If your domain is example.com and 'manual' is passed,",
        "                                  : document root become http://example.com/manual/.",
        "                                  : It effects search result URL. Default value is '/'.",
        " -u, --unit [search unit]         : 'file', 'h1'-'h6'. Default value is 'file'.",
        " -f, --filter [target tag]        : Only contents inside this tag is indexed.",
        "                                  : Default value is \"article,#content,#main,div.body\".",
        " -s, --stemmer [algorithm]        : Select stemming algorithm.",
        " -w, --word-splitter [splitter]   : Use optional word splitter.",
        "                                  : 'ts' (TinySegmenter for Japanese) is available",
        "",
        "Text Mode Options:",
        " -r, --root  [document root]      : Document root folder. Default is current. ",
        "                                  : Indexer creates result file path from this folder.",
        " -s, --stemmer [algorithm]        : Select stemming algorithm.",
        " -w, --word-splitter [splitter]   : Use optional word splitter.",
        "                                  : 'ts' (TinySegmenter for Japanese) is available",
        " -u, --unit [search unit]         : file, block, line. Default value is 'file'.",
        "",
        "Supported Stemmer Algorithms:",
        "  danish, dutch, english, finnish, french german, hungarian italian",
        "  norwegian, porter, portuguese, romanian, russian, spanish, swedish, turkish"
    ]))

def main():
    print("Search Engine Oktavia - Index Generator\n")

    parser = argparse.ArgumentParser(description='Search Engine Oktavia - Index Generator')
    inputs = [] : string[]
    root = process.cwd()
    prefix = '/'
    output : Nullable.<string> = null
    showhelp = false
    notrun = false
    unit = 'file'
    type = 'js'
    mode = ''
    verbose = true
    filter = [] : string[]
    algorithm : Nullable.<string> = null
    //wordsplitter : Nullable.<string> = null
    cacheDensity : number = 5.0
    name = null : Nullable.<string>
    validModes = ['html', 'csv', 'text']
    validUnitsForHTML = ['file', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    validUnitsForText = ['file', 'block', 'line']
    validStemmers = [
        'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian',
        'italian', 'norwegian', 'porter', 'portuguese', 'romanian', 'russian',
        'spanish', 'swedish', 'turkish'
    ]
    validTypes = ['index', 'base64', 'cmd', 'js', 'commonjs', 'web']
    //validWordSplitters = ['ts']

    optstring = "n:(name)q(quiet)m:(mode)i:(input)r:(root)p:(prefix)o:(output)h(help)u:(unit)f:(filter)s:(stemmer)w:(word-splitter)t:(type)c:(cache-density)"
    parser = BasicParser(optstring, args)
    opt = parser.getopt()
    while (opt)
    {
        switch (opt.option)
        {
        case "m":
            if (validModes.indexOf(opt.optarg) == -1)
            {
                console.error("Option m/mode should be 'html', 'csv', 'text'.")
                notrun = true
            }
            mode = opt.optarg
            break
        case "i":
            inputs.push(opt.optarg)
            break
        case "r":
            root = node.path.resolve(opt.optarg)
            break
        case "p":
            prefix = opt.optarg
            break
        case "n":
            name = opt.optarg
            break
        case "o":
            output = opt.optarg
            if (output.slice(0, 1) == '/')
            {
                output = output.slice(1)
            }
            break
        case "h":
            showhelp = true
            break
        case "q":
            verbose = false
            break
        case "u":
            unit = opt.optarg
            break
        case "f":
            items = opt.optarg.split(',')
            for (i in items)
            {
                filter.push(items[i])
            }
            break
        case "t":
            if (validTypes.indexOf(opt.optarg) == -1)
            {
                console.error('Option -t/--type is invalid.')
                notrun = true
            }
            else
            {
                type = opt.optarg
            }
            break
        case "s":
            if (validStemmers.indexOf(opt.optarg) == -1)
            {
                console.error('Option -s/--stemmer is invalid.')
                notrun = true
            }
            else
            {
                algorithm = opt.optarg
            }
            break
        /*case "w":

            break*/
        case "c":
            match = /(\d+\.?\d*)/.exec(opt.optarg)
            if (match)
            {
                tmpValue = match[1] as number
                if (0.1 <= tmpValue && tmpValue <= 100)
                {
                    cacheDensity = tmpValue
                }
                else
                {
                    console.error('Option -c/--cache-density should be in 0.1 - 100.')
                    notrun = true
                }
            }
            else
            {
                console.error('Option -c/--cache-density is invalid.')
                notrun = true
            }
            break
        case "?":
            notrun = true
            break
        }
        opt = parser.getopt()
    }
    inputTextFiles = [] : string[]
    inputHTMLFiles = [] : string[]
    inputCSVFiles = [] : string[]
    if (filter.length == 0)
    {
        filter = ['article', '#content', '#main', 'div.body']
    }
    for (i in inputs)
    {
        input = inputs[i]
        if (!node.fs.existsSync(input))
        {
            console.error("Following input folder/file doesn't exist: " + input)
            notrun = true
        }
        else
        {
            stat = node.fs.statSync(input)
            if (stat.isFile())
            {
                _Main._checkFileType(node.path.resolve(input), inputTextFiles, inputHTMLFiles, inputCSVFiles)
            }
            else if (stat.isDirectory())
            {
                _Main._checkDirectory(input, inputTextFiles, inputHTMLFiles, inputCSVFiles)
            }
            else
            {
                console.error("Following input is not folder or file: " + input)
                notrun = true
            }
        }
    }
    if (inputTextFiles.length == 0 && inputHTMLFiles.length == 0 && inputCSVFiles.length == 0 || !mode)
    {
        showhelp = true
    }
    if (showhelp)
    {
        _Main.usage()
    }
    else if (!notrun)
    {
        stemmer : Nullable.<Stemmer> = null
        if (algorithm)
        {
            stemmer = _Main._createStemmer(algorithm)
        }
        dump = null : Nullable.<string>
        switch (mode)
        {
        case 'html':
            unitIndex = validUnitsForHTML.indexOf(unit)
            if (unitIndex == -1)
            {
                console.error('Option -u/--unit should be file, h1, h2, h3, h4, h5, h6. But ' + unit)
            }
            else
            {
                htmlParser = HTMLParser(unitIndex, root, prefix, filter, stemmer)
                for (i = 0 i < inputHTMLFiles.length i++)
                {
                    htmlParser.parse(inputHTMLFiles[i])
                }
                console.log('generating index...')
                if (verbose)
                {
                    console.log('')
                }
                dump = htmlParser.dump(cacheDensity, verbose)
            }
            break
        case 'csv':
            csvParser = CSVParser(root, stemmer)
            for (i in inputCSVFiles)
            {
                csvParser.parse(inputCSVFiles[i])
            }
            break
        case 'text':
            if (validUnitsForText.indexOf(unit) == -1)
            {
                console.error('Option u/unit should be file, block, line. But ' + unit)
            }
            else
            {
                textParser = TextParser(unit, root, stemmer)
                for (i in inputTextFiles)
                {
                    textParser.parse(inputTextFiles[i])
                }
                dump = textParser.dump(cacheDensity, verbose)
            }
            break
        }
        if (dump)
        {
            indexFilePath = ""
            switch (type)
            {
            case 'index':
                if (output == null)
                {
                    output = 'search'
                }
                indexFilePath = node.path.resolve(root, output, 'searchindex.okt')
                dirPath = node.path.dirname(indexFilePath)
                _Main._mkdirP(dirPath)
                console.log("writing index in binary...", indexFilePath)
                node.fs.writeFileSync(indexFilePath, dump, "utf16le")
                break
            case 'base64':
                if (output == null)
                {
                    output = 'search'
                }
                indexFilePath = node.path.resolve(root, output, 'searchindex.okt.b64')
                dirPath = node.path.dirname(indexFilePath)
                _Main._mkdirP(dirPath)
                console.log("writing index in base64...", indexFilePath)
                node.fs.writeFileSync(indexFilePath, Base64.btoa(dump), "utf8")
                break
            case 'cmd':
                if (output == null)
                {
                    output = 'index-search-cli'
                }
                srcLines = node.fs.readFileSync(node.path.join(node.__dirname, 'oktavia-cli-runtime.js'), 'utf8').split('\n')
                latinString = Base64.to8bitString(dump)
                base64String = Base64.btoa(latinString)
                indexContent = 'searchIndex = "' + base64String + '"'
                srcLines.splice(1, 0, indexContent)
                console.log("writing index for cli...", output)
                node.fs.writeFileSync(output, srcLines.join('\n'), 'utf8')
                node.fs.chmodSync(output, '0755')
                break
            case 'web':
                if (output == null)
                {
                    output = 'searchindex.js'
                }
                srcLines = node.fs.readFileSync(node.path.join(node.__dirname, "web", 'oktavia-web-runtime.js'), 'utf8').split('\n')
                latinString = Base64.to8bitString(dump)
                base64String = Base64.btoa(latinString)
                indexContent = 'searchIndex = "' + base64String + '"'
                srcLines.splice(0, 0, indexContent)
                console.log("writing index for web...", output)
                node.fs.writeFileSync(output, srcLines.join('\n'), 'utf8')
                break
            case 'js':
                if (output == null)
                {
                    output = 'search'
                }
                indexFilePath = node.path.resolve(root, output, 'searchindex.js')
                dirPath = node.path.dirname(indexFilePath)
                _Main._mkdirP(dirPath)
                if (name == null)
                {
                    name = 'searchIndex'
                }
                contents = [
                    '// Oktavia Search Index',
                    '' + name + ' = "' + Base64.btoa(dump) + '"', ''
                ]
                console.log("writing index in js...", indexFilePath)
                node.fs.writeFileSync(indexFilePath, contents.join('\n'), "utf8")
                break
            case 'commonjs':
                if (output == null)
                {
                    output = 'search'
                }
                indexFilePath = node.path.resolve(root, output, 'searchindex.js')
                dirPath = node.path.dirname(indexFilePath)
                _Main._mkdirP(dirPath)
                if (name == null)
                {
                    name = 'searchIndex'
                }
                contents = [
                    '// Oktavia Search Index',
                    'exports.' + name + ' = "' + Base64.btoa(dump) + '"', ''
                ]
                console.log("writing index in js...", indexFilePath)
                node.fs.writeFileSync(indexFilePath, contents.join('\n'), "utf8")
                break
            }
        }
    }
}

def _checkFileType (path : string, texts : string[], HTMLs : string[], CSVs : string[]) : void
{
    match = path.match(/(.*)\.(.*)/)
    if (match && match[1])
    {
        switch (match[2].toLowerCase())
        {
        case 'html':
        case 'htm':
            HTMLs.push(path)
            break
        case 'csv':
            CSVs.push(path)
            break
        default:
            texts.push(path)
        }
    }
}

def checkDirectory (path : string, texts : string[], HTMLs : string[], CSVs : string[]) : void
{
    files = node.fs.readdirSync(path)
    for (j in files)
    {
        filepath = node.path.resolve(path, files[j])
        stat = node.fs.statSync(filepath)
        if (stat.isFile())
        {
            _Main._checkFileType(filepath, texts, HTMLs, CSVs)
        }
        else if (stat.isDirectory())
        {
            _Main._checkDirectory(filepath, texts, HTMLs, CSVs)
        }
    }
}

def mkdirP (path : string) : void
{
    if (node.fs.existsSync(path))
    {
        return
    }
    _Main._mkdirP(node.path.dirname(path))
    node.fs.mkdirSync(path)
}

def createStemmer(algorithm):
    stemmer : Stemmer
    switch (algorithm.toLowerCase())
    {
    case "danish":
        stemmer = DanishStemmer()
        break
    case "dutch":
        stemmer = DutchStemmer()
        break
    case "english":
        stemmer = EnglishStemmer()
        break
    case "finnish":
        stemmer = FinnishStemmer()
        break
    case "french":
        stemmer = FrenchStemmer()
        break
    case "german":
        stemmer = GermanStemmer()
        break
    case "hungarian":
        stemmer = HungarianStemmer()
        break
    case "italian":
        stemmer = ItalianStemmer()
        break
    case "norwegian":
        stemmer = NorwegianStemmer()
        break
    case "porter":
        stemmer = PorterStemmer()
        break
    case "portuguese":
        stemmer = PortugueseStemmer()
        break
    case "romanian":
        stemmer = RomanianStemmer()
        break
    case "russian":
        stemmer = RussianStemmer()
        break
    case "spanish":
        stemmer = SpanishStemmer()
        break
    case "swedish":
        stemmer = SwedishStemmer()
        break
    case "turkish":
        stemmer = TurkishStemmer()
        break
    default:
        stemmer = EnglishStemmer()
        break
    }
    return stemmer
