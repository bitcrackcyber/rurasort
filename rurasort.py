#!/usr/bin/python

"""
  rurasort.py 1.8 

    author: Dimitri Fousekis (@rurapenthe0)

    Licensed under the GNU General Public License Version 2 (GNU GPL v2),
        available at: http://www.gnu.org/licenses/gpl-2.0.txt

    (C) 2015 Dimitri Fousekis (@rurapenthe0)

    TODO:
    Please send a tweet to @rurapenthe0 with any suggestions or comments.
    
    THANKS:
    Assistance with certain operations or input provided by: @m3g4tr0n, g0tmi1k, and atom (@hashcat)

To use this script, simply call it from the command-line with your relevant option.
NOTE : *** IT IS RECOMMENDED YOU RUN ONLY ONE ENGINE/PARAM AT A TIME, ENSURE OUTPUT IS CORRECT THEN USE THE NEXT ONE. **
"""


#import our required libraries
import sys, io, argparse,re,unicodedata
from bs4 import BeautifulSoup

filelist=[]

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
cmdparams.add_argument("--dup-sense", help="Senses if more than <specified>%% of a word is duplicate chars and removes the word", dest="sense",type=int)
cmdparams.add_argument("--hash-remove", help="Filters word candidates that are actually hashes", dest="hashfilter", action="store_true")
cmdparams.add_argument("--email-sort",help="Converts email addresses to username and domain as separate words", dest="emailsort", action="store_true")
cmdparams.add_argument("--email-split",nargs=2, help="Extracts email addresses to username and domain and appends to <user wordlist> and <domain wordlist>",dest="emailsplit",metavar='<user/domain.txt>')
cmdparams.add_argument("--dewebify",action="store_true",help="Extracts words from an HTML specified by --infile and outputs a plain wordlist.", dest="dewebify")
cmdparams.add_argument("--noutf8",help="Only output non UTF-8 characters. Works with --dewebify only",dest="noutf8",action="store_true")
args = cmdparams.parse_args()

# Hash Detection Engine. These engines are from hashfind.py, and detect various hash types
# this engine checks the string candidate for a match to valid hash types and filters it out.

def Hashfilter(inputstring):
#Init values
	hash_present = False
	hash_done = False
	# We want the loop to end immediately if we find a match, otherwise its wasting resources. 
	while (not hash_present) or (not hash_done):
	# MD5 Check (includes NTLM, MD4, MD2)
		results = re.search(r'(^|[^a-fA-F0-9])[a-fA-F0-9]{32}([^a-fA-F0-9]|\$)',inputstring,re.M|re.I)
		if results: hash_present = True
	# mySQL (old hashes)
		results = re.search(r'[0-7][0-9a-f]{7}[0-7][0-9a-f]{7}',inputstring,re.M|re.I)
		if results: hash_present = True
	# Joomla Check
		results = re.search(r'([0-9a-zA-Z]{32}):(\w{32})',inputstring)
		if results: hash_present = True
	# vBulletin Check
		results = re.search(r'([0-9a-zA-Z]{32}):(\S{3,32})',inputstring,re.M|re.I)
		if results: hash_present = True
	# PHBB3 Check
		results = re.search(r'\$H\$\S{31}',inputstring,re.M|re.I)
		if results: hash_present = True
	# Wordpress MD5
		results = re.search('\$P\$\S{31}',inputstring,re.M)
		if results: hash_present = True
	# Drupal Check
		results = re.search(r'\$S\$\S{52}',inputstring,re.M|re.I)
		if results: hash_present = True
	# Unix MD5 old Check
		results = re.search(r'\$1\$\w{8}\S{22}',inputstring,re.M|re.I)
		if results: hash_present = True
	# SHA512Crypt Check
		results = re.search(r'\$6\$\w{8}\S{86}',inputstring,re.M|re.I)
		if results: hash_present = True
	# SHA1 Check
		results = re.search(r'(^|[^a-fA-F0-9])[a-fA-F0-9]{40}([^a-fA-F0-9]|$)',inputstring,re.M|re.I)
		if results: hash_present = True
	# SHA512 check
		results = re.search(r'(^|[^a-fA-F0-9])[a-fA-F0-9]{128}([^a-fA-F0-9]|$)',inputstring,re.M|re.I)
		if results: hash_present = True
	# SHA256 Check
		results = re.search(r'(^|[^a-fA-F0-9])[a-fA-F0-9]{64}([^a-fA-F0-9]|$)',inputstring,re.M|re.I)
		if results: hash_present = True
	# SHA384 Check
		results = re.search(r'(^|[^a-fA-F0-9])[a-fA-F0-9]{96}([^a-fA-F0-9]|$)',inputstring,re.M|re.I)
		if results: hash_present = True
	# Blowfish Check
		results = re.search(r'\$2a\$10\$\S{53}',inputstring,re.M|re.I)
		if results: hash_present = True
	# MD5 APR Check
		results = re.search(r'\$apr1\$\w{8}\S{22}',inputstring,re.M|re.I)
		if results: hash_present = True
	# Sun MD5 Check
		results = re.search(r'\$md5\$rounds\=904\$\w{16}\S{23}',inputstring,re.M|re.I)
		if results: hash_present = True
	# SHA256Unix Check
		results = re.search(r'\$5\$\w{8}\$\S{43}',inputstring,re.M|re.I)
		if results: hash_present = True
	# AIX SHA256 Check
		results = re.search(r'\{ssha256\}06\$\S{16}\$\S{43}',inputstring,re.M|re.I)
		if results: hash_present = True
	# AIX SHA512 Check
		results = re.search(r'\{ssha512\}06\$\S{16}\$\S{86}',inputstring,re.M|re.I)
		if results: hash_present = True
	# AIX SHA1 Check
		results = re.search(r'\{ssha1\}06\$\S{16}\$\S{27}',inputstring,re.M|re.I)
		if results: hash_present = True
	# OSX Hash Check
		results = re.search(r'\$ml\$\w{5}\$\w{64}\$\w{128}',inputstring,re.M|re.I)
		if results: hash_present = True
	# HMAC SHA1 Check
		results = re.search(r'([0-9a-fA-F]{130}):(\w{40})',inputstring,re.M|re.I)
		if results: hash_present = True
	# Cisco 8  Check
		results = re.search(r'\$8\$\S{14}\$\S{43}',inputstring,re.M|re.I)
		if results: hash_present = True
	# Cisco 9 Check
		results = re.search(r'\$9\$\S{14}\$\S{43}',inputstring,re.M|re.I)
		if results: hash_present = True
	# DJango SHA256 Check
		results = re.search(r'pbkdf2_sha256\$20000\$\S{57}',inputstring,re.M|re.I)
		if results: hash_present = True
	# DJango SHA1 Check
		results = re.search(r'sha1\$\w{5}\$\w{40}',inputstring,re.M|re.I)
		if results: hash_present = True
	# MSSQL 2005 Check 
		results = re.search(r'(0x\w{52})',inputstring,re.M|re.I)
		if results: hash_present = True
	# MSSQL 2000 Check
		results = re.search(r'(0x\w{92})',inputstring,re.M|re.I)
		if results: hash_present = True
	# IP Address Check
		results = re.search(r'([0-9]{1,3}[\.]){3}[0-9]{1,3}',inputstring)
		if results: hash_present = True

		hash_done = True
	if hash_present: return ""
	else: return inputstring
  


# Filter Engines. The Engines process a particular string, depending on whether the command-line requested such or not.

#Email filter engine
def Emailsort(inputstring):
	resultset = []
	results = re.search('[a-zA-Z0-9.#?$*_-]+@[a-zA-Z0-9.#?$*_-]+',inputstring,re.M|re.I)
	if results:
		find_positional = inputstring.find('@')
		resultset.append(inputstring[0:find_positional])
		resultset.append(inputstring[find_positional+1:len(inputstring)])
		return resultset
	else: 
		resultset.append(inputstring)
		return resultset

#Email split engine
def Emailsplit(inputstring):
	global user_file_handler
	global domain_file_handler
	resultset = []
	results = re.search('[a-zA-Z0-9.#?$*_-]+@[a-zA-Z0-9.#?$*_-]+',inputstring,re.M|re.I)
	if results:
		find_positional = inputstring.find('@')
		user_file_handler.write(inputstring[0:find_positional]+'\r\n')
		domain_file_handler.write(inputstring[find_positional+1:len(inputstring)].rstrip()+'\r\n')
		return ""
	else: return inputstring
		
# De-Webify Engine
def Dewebify(filename):
	try:
		filehandler = open('rurasort.jnk','r')
		junklist2 = filehandler.read().rstrip().split()
	except: 
		sys.stderr.write('[-] Error! I cannot open the junkfile - is it there? \r\n')
		sys.exit(-1)

	filehandler = open(filename,'r')
	htmls = filehandler.read()
   	response =  ''.join(BeautifulSoup(htmls,"html.parser").findAll(text=True))
	sys.stderr.write('[+] Parsing complete next phase: Removing whitespace...\r\n')
	wordlist = []
	templist = []
	wordlist = response.lower().split()
	for items in wordlist:
		templist.append(items.lstrip().rstrip())
	sys.stderr.write('[+] Whitespace removal complete. Next phase: Ignoring > Length 20...\r\n')
	wordlist = []
	wordlist = templist
	templist= []
	for items in wordlist:
		if len(items) < 21: templist.append(items)
	sys.stderr.write('[+] Length check complete. Removing duplicates...\r\n')
	wordlist = []
	wordlist = templist
	templist = []
	for items in wordlist:
		if items not in templist: templist.append(items)
	sys.stderr.write('[+] Duplicates removed. Removing special chars...\r\n')
	wordlist = []
	wordlist = templist
	templist = []
	for items in wordlist:
		templist.append(Special_Trim(items))
	sys.stderr.write('[+] Special chars removed. Removing known junk from junkfile...\r\n')
	wordlist = []
	wordlist = templist
	templist = []
	for items in wordlist:
		canaccept = True
		for checkitem in junklist2:
			if checkitem in items.lower(): canaccept=False
		if canaccept: templist.append(items)
	sys.stderr.write('[+] Junk removed. Ignoring < Length 4 ...\r\n')
	wordlist = []
        wordlist = templist
        templist = []
        for items in wordlist:
                if len(items.rstrip()) > 3: templist.append(items)
	sys.stderr.write('[+] All done, printing output...\r\n')
	for items in templist:
		if args.noutf8:
			if (unicodedata.category(items[1]) != 'Ll') and (unicodedata.category(items[1]) != 'Nd'): print items.encode('utf-8')
		else: print items.encode('utf-8')
	sys.stderr.write('[+] All done.\r\n')
	
	#print response
		
#Duplicate sense engine
def Sense(inputstring):
	if args.sense < 50:
		print "[-] Warning, 50% or less duplicate sensing may produce unsatisfactory results. Edit the code if you want to override"
		sys.exit(1)
	keepstring = True
	sense_dict=[]
	total_chars = len(inputstring)
	sense_dict = list(inputstring)
	for candidate in sense_dict:
		char_count = inputstring.count(candidate)
		average = (char_count / float(total_chars)) * 100
		if average >= args.sense:
			keepstring = False
			break
	if keepstring: return inputstring

#De-Tab Engine
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
	if args.dewebify:
		Dewebify(args.infile)
		sys.exit(0)
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
			if args.sense: words = Sense(words)
			if args.hashfilter: words = Hashfilter(words)
			if args.emailsplit: words = Emailsplit(words)

        
      	 	 	if args.wordify:
                    		for items in Wordify(words): print items
        	        if args.emailsort:
        	        		for items in Emailsort(words): print items

                 	try:	
			 if len(words) > 0:
           			if (not args.wordify) and (not args.emailsort):
                		 print words
	      		except: continue


	except IOError, error: print error.args[1]+" : "+args.infile


try:
	if args.emailsplit:
		user_file_handler = open(args.emailsplit[0],'a')
		domain_file_handler = open(args.emailsplit[1],'a')
			
except IOError, error: print"[-] Problem during Email Split file handling:" +error.args[1]
if __name__ == "__main__":
	main()



