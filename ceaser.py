#!/usr/bin/python3.6

import is_english
import sys
import string

"""A class to handle encrypting and decrypting a Ceaser Cypher"""

ALPHALIST = string.ascii_lowercase


def encrypt(stringtoencrypt, shift, alphalist= ALPHALIST):
    """Encypts stringtoencypt using the int(shift), pass alphalist to override the standard english list"""

    # Send the string off for prep
    stringtoencrypt, nonletterlist = _stringprep(stringtoencrypt)

    # Apply the shift to each letter
    output = ''
    for letter in stringtoencrypt:
        if letter in alphalist:
            letterindex = alphalist.index(letter) + shift
            letterindex %= len(alphalist)
            if letterindex < 0:
                letterindex += len(alphalist)

            output += alphalist[letterindex]

    # Send the encryption off for rebuilding with spaces
    output = _stringrebuild(output,nonletterlist)

    return output


def decrypt(stringtodecrypt, shift, alphalist= ALPHALIST):
    """Decrypts stringtodecrypt using the int(shift), pass alphalist to override the standard english list"""

    output = ''

    # Send the string off for prep
    stringtodecrypt, nonletterlist = _stringprep(stringtodecrypt)

    for letter in stringtodecrypt:
        if letter in alphalist:
            letterindex = alphalist.index(letter) + shift
            letterindex %= len(alphalist)
            if letterindex < 0:
                letterindex += len(alphalist)

            output += alphalist[letterindex]

    output = _stringrebuild(output, nonletterlist)
    return output


def read_file_to_decrypt(file_name):
    with open(file_name, 'r') as f:
        file_contents = ''
        for line in f:
            file_contents += line

    return file_contents
def write_file_to_encrypt(file_name, file_contents):
    with open(file_name, 'w') as f:
        f.write(file_contents)

def autodecrypt(stringtodecrypt,englishpercent):
    possiblelist = []
    for i in range(26):
        processedstring = decrypt(stringtodecrypt,i)
        x = is_english.is_english(processedstring, 0,englishpercent)
        if x[0]:
            possiblelist.append([x[1], i, processedstring])
    return possiblelist


def _stringprep(stringtoprep):
    """This preps strings by making them lowercase, then tracking and removing spaces"""
    stringtoprep = stringtoprep.lower()
    formatedstring = ''

    # Find spaces and make a list of where they are for rebuilding
    nonletterlist = []
    for i in range(len(stringtoprep)):
        if not stringtoprep[i].isalpha():
            nonletterlist.append([i, stringtoprep[i]])

    # Build a new string without spaces
    for letter in stringtoprep:
       if letter.isalpha():
           formatedstring += letter

    return formatedstring, nonletterlist


def _stringrebuild(stringtorebuild, nonletterlist):
    """This rebuilds the string adding spaces back in"""
    rebuiltstring = ''
    rebuildlist = []

    # Turn the string into a list
    for i in range(len(stringtorebuild)):
        rebuildlist.append(stringtorebuild[i])
    # Insert non letters back where they belong
    for i in nonletterlist:
        rebuildlist.insert(i[0], i[1])
    # Rebuild string from list
    for i in range(len(rebuildlist)):
        rebuiltstring += rebuildlist.pop(0)

    return rebuiltstring


def argsdict():
    options = {}
    for i in range(3, len(argv), 2):
        try:
            options[argv[i]] = argv[i+1]
        except IndexError:
            argserr()
    return options


def argserr():
    print('Must use as ceaser.py encrypt/decrypt shift/auto')
    print('Use -f or --file, -t or --text optionally')
    print('File must be in the same folder to work')
    print("When using -t or --text use '' around your string")
    sys.exit()

if __name__ == '__main__':
    from sys import argv
    options = argsdict()
    print(options.keys())
    if '-f' in options.keys() or '--file' in options.keys():
        try:
            file = options['-f']
        except KeyError:
            print('Here?')
            file = options['--file']
    elif '-t' in options.keys() or '--text' in options.keys():
        try:
            file = options['-t']
            print('here')
        except KeyError:
            file = options['--text']
    else:
        print('What would you like to encrypt or decrypt?')
        file = input(':')
    try:
        if argv[1] == 'encrypt':
            try:
                shift = int(argv[2])
                output = encrypt(file, shift)
            except ValueError:
                argserr()
        elif argv[1] == 'decrypt':
            try:
                shift = int(argv[2])
                output = decrypt(file, shift)
            except ValueError:
                if argv[2] == 'auto':
                    output = autodecrypt(file, .375)

                else:
                    argserr()
    except IndexError:
        print('index error')
        argserr()

    print(output)
