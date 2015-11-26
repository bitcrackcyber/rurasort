#!/usr/bin/python

"""
  rurasort

    author: Dimitri Fousekis (@rurapenthe0)

    Licensed under the GNU General Public License Version 2 (GNU GPL v2),
        available at: http://www.gnu.org/licenses/gpl-2.0.txt

    (C) 2015 Dimitri Fousekis (@rurapenthe0)

    TODO:
    Please send a tweet to @rurapenthe0 with any suggestions.
    

To use this script, simply call it from the command-line with your relevant option.
NOTE : *** IT IS RECOMMENDED YOU RUN ONLY ONE ENGINE/PARAM AT A TIME, ENSURE OUTPUT IS CORRECT THEN USE THE NEXT ONE. **
"""


#import our required libraries
import sys, io, argparse

#command-line parameters
cmdparams = argparse.ArgumentParser(description="RuraSort - Wordlist management tool by RuraPenthe. Output goes to stdout.")
cmdparams.add_argument("--maxlen", help="filter out words over a certain max length",dest="maxlen", type=int)
cmdparams.add_argument("--maxtrim",help="trim words over a certain max length", dest="maxtrim", type=int)
cmdparams.add_argument("--digit-trim", help="trim all digits from beginning and end of words", dest="digit_trim", action="store_true")
cmdparams.add_argument("--special-trim", help="trim all special characters from beginning and end of words", dest="special_trim", action="store_true")
cmdparams.add_argument("--dup-remove", help="remove duplicate words within words eg: hellohello -> hello", dest="dup_remove", action="store_true")
cmdparams.add_argument("--no-sentence", help="de-sentenceify the line by removing allspacesbetweenwords", dest="no_sentence", action="store_true")
cmdparams.add_argument("--lower", help="change word to all lower case", dest="lower", action="store_true")
cmdparams.add_argument("--infile", help="specify the wordlist to be used", dest="infile")
cmdparams.add_argument("--wordify", help="convert all input sentences into separate words", dest="wordify", action="store_true")
cmdparams.add_argument("--no-numbers", help="ignore/delete words that are all numeric", dest="no_numbers", action="store_true")
cmdparams.add_argument("--minlen", help="filter out words below a certain min length",dest="minlen", type=int)
cmdparams.add_argument("--detab", help="remove tabs or space from beginning of words",dest="detab", action="store_true")

args = cmdparams.parse_args()

#Engines. The Engines process a particular string, depending on whether the command-line requested such or not.

def Detab(inputstring):
	return inputstring.lstrip()

#Maxlen Engine
def Maxtrim(inputstring):
    return inputstring[:args.maxtrim]

def Maxlen(inputstring):
    if len(inputstring) > args.maxlen: return ''
    else: return inputstring
#Minlen Engine
def Minlen(inputstring):
    if len(inputstring) > args.minlen: return inputstring

#Digit Trim Engine
def Digit_Trim(inputstring):

	#left-side process
	newstring = inputstring.lstrip('1,2,3,4,5,6,7,8,9,0')
	
	#right-side process
	newstring = newstring.rstrip('1,2,3,4,5,6,7,8,9,0')

	return newstring

#Special Trim Engine
def Special_Trim(inputstring):
    newstring = inputstring.lstrip("!\"#$%&'()*+,-./:;?@[\]^_`{|}~")
    return newstring.rstrip("!\"#$%&'()*+,-./:;?@[\]^_`{|}~")

#Duplicate Remover Engine
def Dup_Remove(inputstring):

    holding = inputstring[:len(inputstring)/2]
    if inputstring.count(holding) > 1: inputstring=inputstring.replace(holding,'')+holding
    return inputstring

#No-Sentence Engine
def DeSentenceify(inputstring):
    return inputstring.replace(' ','')

#Lower-case Engine
def Lower(inputstring):
    return inputstring.lower()

#Date-Remover Engine
#TBA

#Wordify Engine
def Wordify(inputstring):
    return inputstring.split()

#Binary Remove Engine
def Bin_Remove(inputstring):
    print ""

#No Numbers Engine
def No_Numbers(inputstring):
    #First remove any spaces, we dont want them.
    inputstring.replace(' ','')
    if inputstring.isdigit(): return ""
    else: return inputstring

def main():
#Main Starts Here
#Lets get our file open and begin processing
	if not args.infile:
        	print "[-] I need an input file with --infile! or try --help for help."
        	sys.exit()


	try:

   		 for words in open(args.infile):
                 	words=words.rstrip('\n')
        	 	if args.maxlen: words = Maxlen(words)
		 	if args.minlen: words = Minlen(words)
        	 	if args.digit_trim: words = Digit_Trim(words)
                 	if args.special_trim: words = Special_Trim(words)
         	 	if args.dup_remove: words = Dup_Remove(words)
        	 	if args.no_sentence: words = DeSentenceify(words)
        	 	if args.lower: words = Lower(words)
        	 	if args.no_numbers: word = No_Numbers(words)
		 	if args.detab: words = Detab(words)
		 	if args.maxtrim: words = Maxtrim(words)

        
      	 	 	if args.wordify:
                    		for items in Wordify(words): print items

                 	try:	
			 if len(words) > 0:
           			if not args.wordify:
                		 print words
	      		except: continue


	except IOError, error: print error.args[1]+" : "+args.infile




if __name__ == "__main__":
	main()



