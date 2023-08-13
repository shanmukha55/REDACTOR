import argparse
import glob
import spacy
import re
import sys
import numpy as np
import ntpath
import os
import en_core_web_sm
import en_core_web_md
import en_core_web_lg
from spacy.matcher import Matcher
global final_data

def get_files (args):
    '''
    To get the list of files with matched pattern.
    Parameter
    ----------
    args : Namespace
        The parameter contains list of passed arguments in CLI.
    Returns
    -------
        list of file names.
    '''
    files = []
    if args.input==[]:
        print ("There is no file to redact.",file = sys.stderr)
        exit(0)
    else:
        files = glob.glob(str(args.input[0]).strip('\''))
    if files == []:
        print ("There is no text file to redact.",file = sys.stderr)
        exit(0)
    return files

def read_text_file (file_to_read):
    '''
    To open a file and read data.
    Parameter
    ----------
    file_to_read : file
        The parameter is a file
    Returns
    -------
        file contents in string
    '''
    with open(file_to_read,'r', encoding='utf-8') as file:
        file_to_read = file.read()
        file.close()
    return file_to_read

def unicode_char (Word):
    '''
    To replace redacted terms with unicode character.
    Parameter
    ----------
    Word : string
        redacted value
    Returns
    -------
        replaced term with unicode character.
    '''
    item = ''
    for i in Word:
        if i  == ' ':
            item  += ' '
        else:
            item  += '\u2588'
    return item

def redact_names(text):
    '''
    To redact names in given text file
    Parameter
    ----------
    text : str
        file contents
    Returns
    -------
    text  : str
        file data after redacting names
    names : dict
        dict of redacted name and their type
    count : int
        no of redacted names
    '''
    names = {}
    nlp = en_core_web_sm.load()
    doc= nlp(text)
    name_entity = ["PERSON", "ORG"]
    only_noun = ["NOUN", "PROPN"]
    count =0
    for token in doc:
        if token.is_punct == False and token.is_space == False and token.is_stop == False:
            if token.ent_type_ in name_entity and token.pos_ in only_noun:
                count += 1
                text = text.replace(str(token), unicode_char(str(token)))
                names[token] = token.ent_type_
    return text,names,count

def redact_dates(text):
    '''
    To redact dates in given text file
    Parameter
    ----------
    text : str
        file contents
    Returns
    -------
    text  : str
        file data after redacting dates
    dates : list
        list of redacted dates
    count : int
        no of redacted dates
    '''
    dates = []
    date_patterns = r'\d{1,2}[-\./\s]\d{1,2}[-\./\s]\d{2,4}|\d{1,2}[-\./\s]\d{1,2}[-\./\s]\d{2,4}|\d{2,4}[-\./\s]\d{1,2}}[-\./\s]\d{1,2}|\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[\s,]*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[th]*[\s,]*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[th]*|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)|\d{1,2}[th]*[\s,]*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{2,4}|\d{1,2}[\s,]*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{2,4}'
    date=re.findall(date_patterns,text)
    for d in date:
        dates.append(d)
    count = 0
    for found_date in dates:
        count += len(re.findall(str(found_date), text))
        text = text.replace(str(found_date), unicode_char(str(found_date)))
    return text,dates,count

def redact_phones(text):
    '''
    To redact phone numbers in given text file
    Parameter
    ----------
    text : str
        file contents
    Returns
    -------
    text  : str
        file data after redacting phone numbers
    phones : list
        list of redacted phone numbers
    count : int
        no of redacted phone numbers
    '''
    phones = []
    phone_patterns = r'\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}'
    phone=re.findall(phone_patterns,text)
    for d in phone:
        phones.append(d)
    count = 0
    for found_phone in phones:
        count += 1
        text = text.replace(str(found_phone), unicode_char(str(found_phone)))
    return text,phones,count

def redact_gender(text):
    '''
    To redact gender revealing words in given text file
    Parameter
    ----------
    text : str
        file contents
    Returns
    -------
    text  : str
        file data after redacting gender revealing words
    gender_list : list
        list of redacted gender revealing words
    count : int
        no of redacted gender revealing words
    '''
    gender = {'he','she','him','her','his','himself','herself','male','female','men','women','ms','mr','miss','mr.','ms.','boy','girl','boys','girls','lady','ladies','gentleman','gentlemen','guy','hero','heroine','spokesman','spokeswoman','boyfriend','boyfriends','girlfriend','girlfriends','brother','brothers','sister','sisters','mother','father','mothers','fathers','grandfather','grandfathers','grandmother','grandmothers','mom','dad','moms','dads','king','kings','queen','queens','aunt','aunts','uncle','uncles','niece','nieces','nephew','nephews','groom','bridegroom','grooms','bridegrooms','son','sons','daughter','daughters','waiter','waitress'}
    gender_list = []
    nlp = en_core_web_sm.load()
    doc= nlp(text)
    for token in doc:
        if token.lower_ in gender:
            gender_list.append(token.text)
    count = len(gender_list)
    for found_gender in gender_list:
        text = re.sub(r"\b{}\b".format(found_gender), unicode_char(str(found_gender)), text)
    return text,gender_list,count

def redact_address(text):
    '''
    To redact address in a given text file
    Parameter
    ----------
    text : str
        file contents
    Returns
    -------
    text  : str
        file data after redacting address
    address_list : list
        list of redacted address
    count : int
        no of redacted address
    '''
    nlp = en_core_web_lg.load()
    doc= nlp(text)
    count = 0
    address_list = []
    for token in doc:
        if token.ent_type_ == "LOC" or token.ent_type_ == "GPE":
            count += 1
            address_list.append(token)
            text = text.replace(str(token.text), unicode_char(str(token.text)))
    return text,address_list,count

def redact_concepts(text, args, temp):
    '''
    To redact address in a given text file
    Parameter
    ----------
    text : str
        file contents
    args : namespace
        arguments passed in CLI
    temp : str
        temporary variable to store file data
    Returns
    -------
    text  : str
        file data after redacting concept
    concepts : list
        list of redacted concept matching sentences.
    count : int
        no of redacted concept sentences
    '''
    nlp = en_core_web_lg.load()
    doc = nlp(temp)
    count = 0
    concepts= []
    sentences=list(doc.sents)
    for concept_word in args.concept:
        simi = []
        word = nlp(str(concept_word).strip('\''))
        for sent in sentences:
            if sent.vector_norm:
                simi.append(word.similarity(sent))
        simi = np.array(simi)
        result = np.where(simi >0.5)
        if result != []:
            concepts += [(str(sentences[sent]), sentences[sent].start_char, sentences[sent].end_char, concept_word) for sent in result[0]]
            count += len(concepts)
    check_val = set()
    res = []
    # handle same lines for multiple concept words
    for i in concepts:
        if i[0] not in check_val:
            res.append(i)
            check_val.add(i[0])
    if len(res):
        count = len(res)
    # sorting to remove lines corectly based on ending index
    res = sorted(res, key=lambda x:x[2])
    for entity in reversed(res):
        if entity[1] !=0:
            start=entity[1]
            end=entity[2]
            text=text[0:start-1]+text[end:]
        else:
            start=entity[2]
            text = text[start+1:]
    return text,concepts,count

def stats(args, text, file):
    '''
    To get stats from redacted terms.
    Parameter
    ----------
    text : str
        file contents
    args : namespace
        arguments passed in CLI
    file : string
        file name
    Returns
    -------
    final_data  : str
        file data after redacting all values.
    '''
    final_data = temp = text
    if args.names:
        final_data,names,name_count = redact_names(final_data)
        if args.stats == 'stdout':
            print("Redacted Names")
            write_stdout(names,name_count)
        elif args.stats != 'stderr':
            write_tostatfile(names,name_count,file,args)
    if args.dates:
        final_data,dates,date_count = redact_dates(final_data)
        if args.stats == 'stdout':
            print("Redacted Dates")
            write_stdout(dates,date_count)
        elif args.stats != 'stderr':
            write_tostatfile(dates,date_count,file,args)
    if args.phones:
        final_data,phones,phones_count = redact_phones(final_data)
        if args.stats == 'stdout':
            print("Redacted Phones")
            write_stdout(phones,phones_count)
        elif args.stats != 'stderr':
            write_tostatfile(phones,phones_count,file,args)
    if args.genders:
        final_data,gender,gender_count = redact_gender(final_data)
        if args.stats == 'stdout':
            print("Redacted Genders")
            write_stdout(gender,gender_count)
        elif args.stats != 'stderr':
            write_tostatfile(gender,gender_count,file,args)
    if args.address:
        final_data,address,address_count = redact_address(final_data)
        if args.stats == 'stdout':
            print("Redacted Address")
            write_stdout(address,address_count)
        elif args.stats != 'stderr':
            write_tostatfile(address,address_count,file,args)
    if args.concept:
        final_data,concepts,concept_count = redact_concepts(final_data, args, temp)
        if args.stats == 'stdout':
            print("Redacted concepts")
            write_stdout(concepts,concept_count)
        elif args.stats != 'stderr':
            write_tostatfile(concepts,concept_count,file,args)
        #print(final_data,concepts,concept_count, file=sys.stdout)
    if args.stats == 'stderr':
        print("No Error Found", file=sys.stderr)
    return final_data

def write_tostatfile(redacted_terms, count, file, args):
    '''
    To write stats to given file.
    Parameter
    ----------
    redacted_terms : any
        redacted values
    count : int
        no of each redacted terms
    args : namespace
        arguments passed in CLI
    file : string
        file name
    Returns
    -------
    writes stats to a file.
    '''
    path=file.split('.')
    cwd = os.getcwd()
    folder_path = os.path.join(cwd,str(args.stats).strip('\''))
    path=ntpath.basename(path[0])+ '.stats'
    complete_path = (str(args.stats).strip('\'') + '\\' + path)
    final_path = os.path.join(cwd,complete_path)
    if os.path.isdir(folder_path):
        final_file = open(final_path, "a" ,encoding="utf-8")
    else:
        os.mkdir(folder_path)
        final_file = open(final_path, "a" ,encoding="utf-8")
    final_file.write("No. of redacted terms = " + str(count)  + '\n')
    final_file.write("Redacted values = " + str(redacted_terms) + '\n')
    final_file.close()

def write_stdout(redacted_terms, count):
    '''
    To write redacted data to stdout.
    Parameter
    ----------
    redacted_terms : any
        redacted values
    count : int
        no of each redacted terms
    Returns
    -------
    prints redacted data.
    '''
    print("No. of redacted terms =", count, file = sys.stdout)
    print("Redacted values =", redacted_terms, '\n' , file = sys.stdout)
    #print(redacted_terms, count, file = sys.stdout)

def output(args, complete_data, files):
    '''
    To write redacted output to a file.
    Parameter
    ----------
    complete_data : any
        redacted data
    count : int
        no of each redacted terms
    args : namespace
        arguments passed in CLI
    Returns
    -------
    writes output after redaction to a file.
    '''
    if args.output == 'stdout':
        print("\n","******* Redacted data output from ", files,"file","*******","\n",complete_data)
    elif args.output != 'stderr':
        cwd = os.getcwd()
        folder_path = os.path.join(cwd,str(args.output).strip('\''))
        path=ntpath.basename(files)+ '.redacted'
        complete_path = (str(args.output).strip('\'') + '\\' + path)
        final_path = os.path.join(cwd,complete_path)
        if os.path.isdir(folder_path):
            final_file = open(final_path, "w" ,encoding="utf-8")
        else:
            os.mkdir(folder_path)
            final_file = open(final_path, "w" ,encoding="utf-8")
        final_file.write(complete_data)
        final_file.close()
    elif args.output == 'stderr':
        print("No Error Found", file = sys.stderr)
def main(parser):
    """
    Command line parsing and redacting everything.
    Parameter
    ---------
    parser : Argumentparser
    """
    args=parser.parse_args()
    list_of_files = get_files(args)
    for file in list_of_files:
        if args.stats == 'stdout':
            print("\n" + "******* Stats after redacting the file", file.split('.')[0] + " *******" + '\n')
        text = read_text_file (file)
        final_data = stats(args, text, file)
        output(args, final_data, file)

if __name__ == "__main__":
    parser =argparse.ArgumentParser()
    parser.add_argument("--input",type=str,required=True,nargs='*',help="It takes the patterns of the input files")
    parser.add_argument("--names",action="store_true",help="It helps in redacting names")
    parser.add_argument("--dates",action="store_true",help="It helps in redacting dates")
    parser.add_argument("--phones",action="store_true",help="It helps in redacting phones")
    parser.add_argument("--genders",action="store_true",help="It helps in redacting genders")
    parser.add_argument("--address",action="store_true",help="It helps in redacting address")
    parser.add_argument("--concept",type=str,action='append',required=True,help="It helps in redacting concepts")
    parser.add_argument("--output",type=str, required=True,help="It takes the output file path")
    parser.add_argument("--stats",help="It provides the stats of the redacted flags")
    main(parser)
