#!/usr/bin/env python3

import subprocess
import os.path
import sys
import fnmatch
import filecmp
import argparse
import textwrap
import signal
import tigergui
from multiprocessing import Pool
from multiprocessing import Process

class bcolors :
	INFO = '\033[95m'
	INFO_LOW = '\033[94m'
	SUCCES = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

parser = argparse.ArgumentParser(
formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent(
"Lion is a command-line tool for input-output tasks.\nOn default it reads the tests from the disk\n\n" 

"                       ___......----:'"":--....(\           \n"
"               .-':'\"\":   :  :  :   :  :  :.(1\.`-.       \n"
"             .'`.  `.  :  :  :   :   : : : : : :  .';       \n"
"            :-`. :   .  : :  `.  :   : :.   : :`.`. a;      \n"
"            : ;-. `-.-._.  :  :   :  ::. .' `. `., =  ;     \n"
"            :-:.` .-. _-.,  :  :  : ::,.'.-' ;-. ,'''\"     \n"
"          .'.' ;`. .-' `-.:  :  : : :;.-'.-.'   `-'         \n"
"   :.   .'.'.-' .'`-.' -._;..:---'''''._.-/                 \n"
"   :`--'.'  : :'     ;`-.;            :.`.-'`.              \n"
"    `'''    : :      ;`.;             :=; `.-'`.            \n"
"            : '.    :  ;              :-:   `._-`.          \n"
"             `'\"'    `. `.            `--'     '._'        \n"
"                       `'\"'                                \n"
))

parser.add_argument(
	"ShortTaskName",
	help="Short Task Name (for example : swo for task Swords) "
	"Default setting require : (for Swords) "
	"Tests in form swoX.in and swoX.out, binary code in swo or source in swo.cpp"
)

parser.add_argument(
	"-gui",
	"-graphicaluserinterface",
	action="store_true", 
	help="Open graphical user interface. If this option is used all other options are ignored."
)

binarySourceGroup = parser.add_mutually_exclusive_group() # grupa do binary i sourcecode
binarySourceGroup.add_argument(
	"-b",
	"--binarycode", 
	help="Exceptional binary code to run against the common one",
	default=""
)

binarySourceGroup.add_argument(
	"-s",
	"--sourcecode",
	help="Exceptional source code to compile and run against the common one",
	default=""
)

generateGroup = parser.add_mutually_exclusive_group()
generateGroup.add_argument(
	"-g",
	"--generate",
	action="store_true", 
	help="Generate and run tests but save only those on which the program failed."
)

generateGroup.add_argument(
	"-gs",
	"--generateandsave",
	action="store_true", 
	help="Generate, run tests and save all tests."
)

generateGroup.add_argument(
	"-tf",
	"--testfolder",
	help="Change the folder with tests which will be executed",
	default=""
)
parser.add_argument(
	"-op",
	"--otherprefix",
	help="Change the default prefix for tests",
	default=""
)


checkerGroup = parser.add_mutually_exclusive_group()
checkerGroup.add_argument(
	"-c",
	"--checker",
	help="For tasks, which have several acceptable answers (checker gets the input and the output - joined in one file) "
	"This chcecker needs to get the input from stdin and return OK or WA to stdout",
	default=""
)

checkerGroup.add_argument(
	"-cb",
	"--checkerbruteforce",
	help="For tasks, which have several acceptable answers (checker gets the input, bruteforceprogram output, the output - joined in one file)\n"
	"This chcecker needs to get the input from stdin and return OK or WA to stdout",
	default=""
)

parser.add_argument(
	"-mt",
	"--maxtime",
	help="Change the time after the program will be killed",
	default="5"
)


args = parser.parse_args()

if(args.gui) :
	tigergui.buildGui()
	sys.exit()

STN = args.ShortTaskName


checker = ""

#def wykonaj(program,test,maxtime) :
#	if __name__ == '__main__' :
#		p = Process(target=wykonaj, args=(program,test,maxtime,)) 
#		p.start()
#		p.join()


PID=0

def handler(signum, frame) :
	#print (bcolors.FAIL + "TimeLimitExceeded - Aborting" + bcolors.ENDC)
	#print ("Zabijam ", os.getppid(), " i ", os.getpid())
	print(bcolors.INFO + "Za chwilę zabiję te procesy, pamiętaj o zabiciu jeszcze wykonywanego programu." + bcolors.ENDC)
	os.system("kill " + str(os.getpid()))
	os.system("kill " + str(os.getppid()))


def shell(string,maxextime) : 
	if __name__ == '__main__' :
		signal.signal(signal.SIGALRM, handler)
		p = Process(target=os.system, args=(string,))
		PID = os.getpid()
		#print(PID)
		#asystem(string)
		signal.alarm(int(maxextime))
		p.start()
		p.join()
		#print("procesid = ", p.pid)
	signal.alarm(0)


def wykonaj(program,test,maxtime) : # statusy : WA,OK,RE
	
	if os.path.isfile(".temporary") :
		os.remove(".temporary")
	if os.path.isfile(".temporary2") :
		os.remove(".temporary2")

	out = test[:-2] + "out"
	#print("test:", test)
	#print("out:", out)
	
	if os.path.isfile(out) == False :
		print((bcolors.WARNING + "{0:20} "+ ": RE - Can't find the out file" + bcolors.ENDC).format(test))
		return "RE"
	shell("./" + program + " < " + test + " > "  + ".temporary", maxtime)
	if os.path.isfile(".temporary") == False:
		print(bcolors.FAIL + "Your program ended, but didn't return the answer for : " + test + bcolors.ENDC)
		return "RE"
	if args.checker != "" :
		shell("cat" + test + "  > .temporary2; echo >> .temporary2; cat .temporary >> .temporary2",maxtime)
		shell("./" + checker + " < .temporary2 > .temporary3",maxtime)
		with open('.temporary3', 'r') as f:
			first_line = f.readline()
			return first_line
	elif args.checkerbruteforce != "" :
		shell("cat" + test + "  > .temporary2; echo >> .temporary2;",maxtime)
		shell("cat" + out + "  > .temporary2; echo >> .temporary2;",maxtime)
		shell("cat .temporary >> .temporary2",maxtime)
		shell("./" + checker + " < .temporary2 > .temporary3",maxtime)
		with open('.temporary3', 'r') as f:
			first_line = f.readline()
			return first_line
	elif filecmp.cmp(out,".temporary") :
		print((bcolors.SUCCES + "{0:20} "+ ": OK" + bcolors.ENDC).format(test))
		return "OK"
	else :
		print((bcolors.FAIL + "{0:20} "+ ": WA" + bcolors.ENDC).format(test))
		return "WA"


sourceCodeName = ""
binaryCodeName = ""

if args.binarycode != "" :
	binaryCodeName = args.binarycode
else :
	binaryCodeName = STN

if os.path.isfile(binaryCodeName) :
	 print (bcolors.INFO + "Succesfully read the binary file : " + bcolors.INFO_LOW + binaryCodeName +  bcolors.ENDC)
else : 
	print (bcolors.WARNING + "Couldn't find the binary file : " + bcolors.INFO_LOW + binaryCodeName + bcolors.ENDC)
	if args.sourcecode != "" :
		sourceCodeName = args.sourcecode;	
	else :
		sourceCodeName = STN + ".cpp"
	if os.path.exists(sourceCodeName) :
		print (bcolors.INFO + "Succsesfully read the source file : " + bcolors.INFO_LOW + sourceCodeName + bcolors.ENDC)
	else :
		print (bcolors.FAIL + "Couldn't find the source file: " + bcolors.INFO_LOW + sourceCodeName + ", ani nie podano innego " + bcolors.ENDC)
		sys.exit()
	
	print (bcolors.INFO + "So let's try to compile your program (C++) : " + bcolors.INFO_LOW + sourceCodeName + bcolors.ENDC) 
	shell("g++" + " -o " + STN + " " + sourceCodeName +" -O2" + " -Wall" + " -static" + " -std=c++11"+ " -g")
	binaryCodeName = STN
	if os.path.exists(binaryCodeName) :
		print(bcolors.SUCCES + "Compiled succsesfully." + bcolors.ENDC)
	else :
		print(bcolors.FAIL + "There were some errors during the compilation process." + bcolors.ENDC)
		sys.exit()



#print(bcolors.INFO + "Czy chcesz generować testy generatorem(0), czy sprawdzić testy już zapisane na dysku(1) ? (0/1) " + bcolors.ENDC)
#tryb = input()
if(args.generate or args.generateandsave) :
	print(bcolors.WARNING + "Ta opcja jescze w pełni nie działa." + bcolors.ENDC)
	generator = nazwa_programu + "gen"
	zrodlo = nazwa_programu + "zrodlo"
	brut = nazwa_programu + "brut"
	nr = 1
	wa = 0
	ac = 0
	while True :
		shell("cp " + zrodlo + " zrodlo2",10) # poprawić
		shell("echo " + str(nr) + " >> " +  "zrodlo2",10)
		test = nazwa_programu + str(nr) + ".in"
		testout = nazwa_programu + str(nr) + ".in"
		shell("./" + generator + " <  zrodlo2 " + " > " + test, 10);
		shell("./" + brut + " < " + test + " > " + testout, 10);
		wynik = wykonaj(nazwa_programu,test,args.maxtime)
		if(wynik == "OK") :
			ac+=1
		if(wynik == "WA") :
			wa+=1
		print("ac:",ac," wa:",wa," nr:", nr)
		nr+=1
		
else :
	print (bcolors.INFO + "Reading tests from the disk." + bcolors.ENDC)
	ile_testow = 0
	testy_z_wa = []
	testy_z_re = []
	katalog = "."
	if args.testfolder != "":
		katalog = args.testfolder
	#print("katalog=" + katalog);
	if not os.path.isdir(katalog) :
		print (bcolors.FAIL + "Folder " + katalog + " doesn't exist" + bcolors.ENDC)
		sys.exit()
	prefix=STN
	if args.otherprefix != "" :
		prefix = args.otherprefix
	for test in os.listdir(katalog) :
		if fnmatch.fnmatch(test,prefix +'*.in') :
			wynik = wykonaj(binaryCodeName,katalog+"/" + test,args.maxtime)
			if wynik == "WA" :
				testy_z_wa.append(test)
			elif wynik == "RE" :
				testy_z_re.append(test)
			ile_testow += 1
	ile_z_ok = ile_testow - len(testy_z_wa) - len(testy_z_re)
	print()
	if ile_testow > 0 :
		print(bcolors.INFO + "Udało się zrobić ", ile_z_ok, "/" ,ile_testow ," ~ ", ile_z_ok*100//ile_testow, "%", bcolors.ENDC)
	if len(testy_z_wa) > 0 : 
		print(bcolors.FAIL + "WA na testach : ");
		print(testy_z_wa)
	if len(testy_z_re)>0 :
		print(bcolors.WARNING + "RE na testach : ");
		print(testy_z_re, bcolors.ENDC)

print(bcolors.INFO + "Ending..." + bcolors.ENDC)
if os.path.isfile(".temporary") :
	os.remove(".temporary")
if os.path.isfile(".temporary2") :
	os.remove(".temporary2")
if os.path.isfile(".temporary3") :
	os.remove(".temporary3")

