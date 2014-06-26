import os.path, math

''' Returns a version of string str in which all letters have been
    converted to lowercase and punctuation characters have been stripped 
    from both ends. Inner punctuation is left untouched. '''
def clean_up(s):

    punctuation = '''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result

''' Returns the average length of all words in text. Does not
    include surrounding punctuation in words. 
    text is a non-empty list of strings each ending in \n.
    At least one line in text contains a word.'''
def average_word_length(text):
    
    string = " "
    for i in text:
        string = string + " " + i
    fstr = clean_up(string)
    words = fstr.split()
    
    count = 0
    sum = 0
    for token in words:
        count += 1
        sum += len(token)
    return sum / float(count)
 
''' Return the type token ratio (TTR) for this text.
    TTR is the number of different words divided by the total number of words.
    text is a non-empty list of strings each ending in \n.
    At least one line in text contains a word. '''
def type_token_ratio(text):

    string = ""
    for i in text:
        string = string + " " + i
    fstr = clean_up(string)
    word_list = fstr.split()
    
    ls = []
    for i in word_list:
        ls.append(word_list.count(i))

    MAX = -1
    for j in ls:
        if j > MAX:
            MAX = j

    k = 1
    kdiff = 0
    while k <= MAX:
        kdiff = kdiff + (ls.count(k)/k)
        k = k+1

    return (float(kdiff)/float(len(word_list)))
    
''' Returns the hapax_legomana ratio for this text.
    This ratio is the number of words that occur exactly once divided
    by the total number of words.
    text is a list of strings each ending in \n.
    At least one line in text contains a word.'''               
def hapax_legomana_ratio(text):
    
    uqwords = dict()
    words = 0
    for line in text:
        line = line.strip().split()
        for word in line:
            words += 1
            word = word.replace(',', '').strip()
            if word in uqwords:
                uqwords[word] -= 1
            else:
                uqwords[word] = 1
                
    unique_count = 0
    for x in uqwords:
        if uqwords[x] == 1:
            unique_count += 1
      
    HLR = float(unique_count)/float(words)
    return HLR
    
''' Returns a list of non-empty, non-blank strings from the original string
    determined by splitting the string on any of the separators.
    separators is a string of single-character separators.'''
def split_on_separators(original, separators):
    
    result = []
    nstr = ''
    for index, char in enumerate(original):
        if char in separators or index==len(original) -1:
            result.append(nstr)
            nstr=''
            if '' in result:
                result.remove('')
        else:
            nstr+=char
    return result     

''' Returns the average number of words per sentence in text.
    text is guaranteed to have at least one sentence.
    Terminating punctuation defined as !?.
    A sentence is defined as a non-empty string of non-terminating
    punctuation surrounded by terminating punctuation
    or beginning or end of file. '''    
def average_sentence_length(text):
    words=0
    sentences=0
    string = ""
    
    for i in text:
        string = string + " " + i
        
    for line in string.split():
        words+=1
    
    sentence = split_on_separators(text,'?!.')
    for sep in sentence:
        sentences+=1

    average_length = float(words)/float(sentences)
    return average_length

'''Returns the average number of phrases per sentence.
    Terminating punctuation defined as !?.
    A sentence is defined as a non-empty string of non-terminating
    punctuation surrounded by terminating punctuation
    or beginning or end of file.
    phrases are substrings of a sentences separated by
    one or more of the following delimiters ,;: '''
def avg_sentence_complexity(text):
    
    sentences = 0
    phrases = 0 
    sentence=split_on_separators(text,'?!.')
    
    for sep in sentence:
        sentences+=1
    p = split_on_separators(text, ',;:')
    
    for n in p:
        phrases+=1
    asc = phrases/sentences
    return asc  

    
    
'''Use prompt (a string) to ask the user to type the name of a file. If
   the file does not exist, keep asking until they give a valid filename.
   Return the name of that file.'''    
def get_valid_filename(prompt):

    filename = raw_input(prompt)
    while os.path.isfile(filename) == False:
        print ("That file does not exist.")
        filename = raw_input(prompt)

    return filename
 
'''Uses prompt to ask the user to type the name of a directory. If
    the directory does not exist, keep asking until they give a valid directory.
    ''' 
def read_directory_name(prompt):
    
    dirname = raw_input(prompt)
    while os.path.exists(dirname)== False:
        print ("That directory does not exist.")
        dirname = raw_input(prompt)
    return dirname
    
'''Returns a non-negative real number indicating the similarity of two 
    linguistic signatures. The smaller the number the more similar the 
    signatures. Zero indicates identical signatures.
    sig1 and sig2 are 6 element lists with the following elements
    0  : author name (a string)
    1  : average word length (float)
    2  : TTR (float)
    3  : Hapax Legomana Ratio (float)
    4  : average sentence length (float)
    5  : average sentence complexity (float)
    weight is a list of multiplicative weights to apply to each
    linguistic feature. weight[0] is ignored.
    '''   
def compare_signatures(sig1, sig2, weight):
    
    i = 1
    result = 0
    while i <= 5:
        result +=(abs(sig1[i]-sig2[i]))*weight[i]
        i+=1
    return result

'''Read a linguistic signature from filename and return it as 
    list of features. '''
def read_signature(filename):
    
    file = open(filename, 'r')
    # the first feature is a string so it doesn't need casting to float
    result = [file.readline()]
    # all remaining features are real numbers
    for line in file:
        result.append(float(line.strip()))
    return result

def run(): 
    prompt = 'File with unknown author: '
    mystery_filename = get_valid_filename(prompt)

    # readlines gives us a list of strings one for each line of the file
    text = open(mystery_filename, 'r').readlines()
    
    # calculate the signature for the mystery file
    mystery_signature = [mystery_filename]
    mystery_signature.append(average_word_length(text))
    mystery_signature.append(type_token_ratio(text))
    mystery_signature.append(hapax_legomana_ratio(text))
    mystery_signature.append(average_sentence_length(text))
    mystery_signature.append(avg_sentence_complexity(text))
    
    weights = [0, 11, 33, 50, 0.4, 4]
    
    prompt = 'Directory that contains signature files: '
    dir = read_directory_name(prompt)
    # every file in this directory must be a linguistic signature
    files = os.listdir(dir)

    # we will assume that there is at least one signature in that directory
    this_file = files[0]
    signature = read_signature('%s/%s'%(dir,this_file))
    best_score = compare_signatures(mystery_signature, signature, weights)
    best_author = signature[0]
    for this_file in files[1:]:
        signature = read_signature('%s/%s'%(dir, this_file))
        score = compare_signatures(mystery_signature, signature, weights)
        if score < best_score:
            best_score = score
            best_author = signature[0]
    print "best author match: %s with score %s"%(best_author, best_score)        
