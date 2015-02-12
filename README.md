# rurasort
RuraSort - A utility to sort and streamline wordlists.
(c) 2015 Dimitri Fousekis & Telspace Systems www.telspace.co.za

This utility is used to help you streamline your worldlists by performing tasks on them. Note that output is made to STDOUT and you have
to pipe data to where you want it to go. Usually to a file with > myfile.txt etc
This program CANNOT read from STDIN. 

Here is the help page:
usage: rurasort.py [-h] [--maxlen MAXLEN] [--maxtrim MAXTRIM] [--digit-trim]
                   [--special-trim] [--dup-remove] [--no-sentence] [--lower]
                   [--infile INFILE] [--wordify] [--no-numbers]
                   [--minlen MINLEN] [--detab]

RuraSort - Wordlist management tool by RuraPenthe. Output goes to stdout.

optional arguments:
  -h, --help         show this help message and exit
  --maxlen MAXLEN    filter out words over a certain max length
  --maxtrim MAXTRIM  trim words over a certain max length
  --digit-trim       trim all digits from beginning and end of words
  --special-trim     trim all special characters from beginning and end of
                     words
  --dup-remove       remove duplicate words within words eg: hellohello ->
                     hello
  --no-sentence      de-sentenceify the line by removing allspacesbetweenwords
  --lower            change word to all lower case
  --infile INFILE    specify the wordlist to be used
  --wordify          convert all input sentences into separate words
  --no-numbers       ignore/delete words that are all numeric
  --minlen MINLEN    filter out words below a certain min length
  --detab            remove tabs or space from beginning of words
