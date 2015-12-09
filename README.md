# rurasort
RuraSort - A utility to sort and streamline wordlists.

Copyright (c) 2015 Dimitri Fousekis, released under GNU General Public License.

A recent update was pushed at PasswordsCon15. 

This utility is used to help you streamline your worldlists by performing tasks on them. Note that output is made to STDOUT 
and you have to pipe data to where you want it to go. Usually to a file with > myfile.txt 

This program CANNOT read from STDIN, it requires a file for input.

To get help, simply run the script with --help. If you cannot execute it try chmod +x rurasort.py and make sure Python is in the correct environment paths. . 

Please ensure you have argparse and beautifulsoup installed, or install it with : easy_install argparse OR pip install argparse and easy_install beautifulsoup4
