
#!/usr/bin/env python3
# TigerGui

# imports for Tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

# other imports
import fnmatch
import os
import time
import random
import filecmp
from multiprocessing import Process
import shutil
import subprocess
import platform
import math

IgnoreWhiteSpaceMode = True

def withoutwhite(str) : # changes to list of non-white blocks
	res = ""
	norm = True
	for char in str :
		if not char.isspace() :
			res = res + char
			norm = True
		else :
			if norm :
				res = res + '@'
			norm = False
	#print("res=",res)
	return res.strip('@')
			

def fcompare(filename1, filename2) : # file comparing
	try :
		if IgnoreWhiteSpaceMode == True or platform.system() != 'Linux' :
			f1 = open(filename1,"r")
			f2 = open(filename2,"r")
			f1s = f1.read()
			f2s = f2.read()
			f1.close()
			f2.close()
			f1g = withoutwhite(f1s)
			f2g = withoutwhite(f2s)
			return f1g == f2g		
		else :
			#print("Jestem Tutaj")
			#os.system("leafpad " + filename1)
			#os.system("leafpad " + filename2)
			return filecmp.cmp(filename1,filename2)
	except:
		print("[FCOMPARE] - ERROR!")
		

def wykonaj(program,test,maxtime) : # status : WA,OK,RE
	if os.path.isfile(".temporary") :
		os.remove(".temporary")
	if os.path.isfile(".temporary2") :
		os.remove(".temporary2")

	out = test[:-2] + "out"
	myout = test[:-2] + "myout"
	#print("program:", program)
	#print("test:", test)
	#print("out:", out)
	#os.system("leafpad " + test)
	#os.system("leafpad " + out)
	try:
		ts = time.time()
		q=subprocess.call(program, stdin=open(test, "r"), stdout=open(mout,"w"), timeout=maxtime)
		te = time.time()
		elapsed_time = te - ts
	except subprocess.TimeoutExpired :
		return "TLE"
	except:
		return "RE"
	if os.path.isfile(myout) == False :
		return "RE-NOFILE"
	if q!=0 :
		print("RE : program returned status " + str(q) + " on test:" + test)
		return "RE" + q
	"""
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
	"""
	#print("porównuje ",mout,out)
	if fcompare(myout,out) :
		return "OK",elapsed_time
	else :
		return "WA",elapsed_time
	if os.path.isfile(".temporary") :
        	os.remove(".temporary")
	if os.path.isfile(".temporary2") :
		os.remove(".temporary2")


random.seed()
def generuj(generator,brut,zrodlo,test,out,maxtime) :
	try :
		if os.path.isfile(".temporary") :
			os.remove(".temporary")
		shutil.copyfile(zrodlo,".temporary")
		open(".temporary",'a').write(str(random.randint(1,1000000)))
		open(".temporary",'a').close()
		try:
			q=subprocess.call(generator, stdin=open(".temporary", "r"), stdout=open(test,"w"), timeout=maxtime)
			if brut != "NONE" :
				q=subprocess.call(brut, stdin=open(test, "r"), stdout=open(out,"w"), timeout=maxtime)
		except:
			return "RE_GEN"
		#os.system("leafpad " + out)
		if os.path.isfile(out) == False :
			return "RE_GOU"
		if q!=0 :
			return "RE" + str(q)

		if os.path.isfile(".temporary") :
			os.remove(".temporary")
		return "OK"
	except:
		return "RE_GEN"

def buildGui() :
	class Data(object) :
		def __init__ (self) : # initial constructor 
			self.stn = ""
			self.sourceCodeName = ""
			self.binaryCodeName = ""
			self.checker = "diff"
			self.testFolder = "./"
			self.workingFolder = "./"
			self.generator = ""
			self.tryb = 0 # 0 - sprawdzanie, 1 - generowanie
			self.generatorSource = ""
			self.prefix = ""
			self.brut = ""
			self.only_save_tests_which_failed = 1 # 0 - no, 1 yes
			self.N=30
			self.saveOption="wa"
		def defaultInit(self,stn) :
			if stn=="" : 
				return
			self.stn = stn
			self.sourceCodeName = stn + self.workingFolder + ".cpp"
			self.binaryCodeName = self.workingFolder + stn
			self.checker = self.workingFolder + stn + "checker"
			self.prefix = stn
			self.generator = self.workingFolder + stn + "gen"
			self.brut = self.workingFolder + stn + "brut"
			self.generatorSource = self.workingFolder + stn + "source"
			if platform.system() == 'Windows':
				self.binaryCodeName = self.binaryCodeName + '.exe'
				self.generator = self.generator + '.exe'
				self.brut = self.brut + '.exe'
				self.checker = self.checker + '.exe'
			binaryButton.config(text=get_button_text(self.binaryCodeName))
			brutButton.config(text=get_button_text(self.brut))
			generatorButton.config(text=get_button_text(self.generator))
			generatorSourceButton.config(text=get_button_text(self.generatorSource))
		def checkBasicData(self) :
			#binary
			if self.binaryCodeName ==  "":
				messagebox.showinfo(\
				message='Binary was not specified'\
				, icon='error')

				return False
			if not os.path.isfile(self.binaryCodeName) :
				messagebox.showinfo(\
				message='Binary which was specified doesn\'t exist.'\
				, icon='error')
				return False
			return True
		def checkGenData(self) :
			if self.checkBasicData == False :
				return False
			#generator
			if self.generator == "":
				messagebox.showinfo(\
				message='Generator was not specified'\
				, icon='error')
				return False
			if not os.path.isfile(self.generator) :
				messagebox.showinfo(\
				message='Generator which was specified doesn\'t exist.'\
				, icon='error')
				return False
			#brut
			if self.brut == "":
				messagebox.showinfo(\
				message='Brute-force was not specified'\
				, icon='error')
				return False
			if not os.path.isfile(self.brut) :
				messagebox.showinfo(\
				message=\
				'Brute-force program which was specified doesn\'t exist.'\
				, icon='error')
				return False
			#generatorSource
			if self.generatorSource == "":
				messagebox.showinfo(\
				message='Seed was not specified'\
				, icon='error')
				return False
			if not os.path.isfile(self.generatorSource) :
				messagebox.showinfo(\
				message='Seed which was specified doesn\'t exist.'\
				, icon='error')
				return False
			return True
	data = Data()

	#usun wszystko do pierwszego znaku / (włącznie)
	def get_button_text(plik) :
		a = len(plik)-1
		res = ""
		while (a != -1 and plik[a] != '/'):
			res = plik[a] + res
			a = a - 1
		return res

	#definipwanie i inicjalizowanie okienka
	root = Tk()
	root.wm_title('TigerGui (by Stanisław Szcześniak) ')


	def makeOkInformation(string) :
		infoWin = Toplevel(root)
		label = ttk.Label(infoWin, text=string)
		label.pack(side=TOP)
		def killmyself() :
			infoWin.destroy()
		button = ttk.Button(infoWin, text="Ok", command=killmyself)
		button.pack(side=TOP)
	#makeOkInformation("udalo sie")
	#img = PhotoImage(file='/home/administrator/Obrazy/tigericon.jpg')
	#root.tk.call('wm', 'iconphoto', root._w, img)

	content = ttk.Frame(root,padding=(5,5,8,8))
	content.grid(column=0,row=0)

	#<lewaramka>
	#<def>
	bigleftframe = ttk.Frame(content, borderwidth=5, relief="flat")
	bigleftframe.grid(column=0,row=0)
	imagelabel = ttk.Label(bigleftframe,text="") 
	#"                       ___......----:'"":--....(\           \n"
	#"               .-':'\"\":   :  :  :   :  :  :.(1\.`-.       \n"
	#"             .'`.  `.  :  :  :   :   : : : : : :  .';       \n"
	#"            :-`. :   .  : :  `.  :   : :.   : :`.`. a;      \n"
	#"            : ;-. `-.-._.  :  :   :  ::. .' `. `., =  ;     \n"
	#"            :-:.` .-. _-.,  :  :  : ::,.'.-' ;-. ,'''\"     \n"
	#"          .'.' ;`. .-' `-.:  :  : : :;.-'.-.'   `-'         \n"
	#"   :.   .'.'.-' .'`-.' -._;..:---'''''._.-/                 \n"
	#"   :`--'.'  : :'     ;`-.;            :.`.-'`.              \n"
	#"    `'''    : :      ;`.;             :=; `.-'`.            \n"
	#"            : '.    :  ;              :-:   `._-`.          \n"
	#"             `'\"'    `. `.            `--'     '._'        \n"
	#"                       `'\"'                                \n"
	#)
	imagelabel.pack(side=TOP)
	leftframe = ttk.Labelframe(
		bigleftframe,
		borderwidth=5,
		relief="ridge",
		width=180,
		height=400,
		text='Data:',
		padding=(5,5,8,8)
	)
	leftframe.pack(side=TOP)
	#<\def>

	#<STN>
	stnLabel = ttk.Label(leftframe, text='Short Task Name (ex.\'cow\'):')
	stnLabel.pack(side = TOP)
	stnVar = StringVar("")
	stnEntry = ttk.Entry(leftframe, textvariable=stnVar)
	stnEntry.pack(side = TOP)
	stnEntry.focus()
	def changeStn(*args) :
		#print("Jestem tu, stn=",stnVar.get())
		data.defaultInit(stnVar.get())
	stnButton = ttk.Button(leftframe, text='Change', command=changeStn);
	root.bind('<Return>', changeStn)
	stnButton.pack(side = TOP)
	#<\STN>
	
	#<TestFolder>
	folderLabel = ttk.Label(leftframe, text='Directory with tests:')
	folderLabel.pack(side = TOP)

	def getFolder() :
		data.testFolder = askdirectory()
		folderButton.config(text=get_button_text(data.testFolder))
	folderButton = ttk.Button(leftframe, text='./',command=getFolder)
	folderButton.pack( side = TOP)
	#<\TestFolder>
	
	#<WorkingFolder>
	workingFolderLabel = ttk.Label(leftframe, text=\
	'Def. programs directory')
	workingFolderLabel.pack(side = TOP)
	def getWorkingFolder() :
		data.workingFolder = askdirectory()
		workingFolderButton.config(text=get_button_text(data.workingFolder))
	workingFolderButton = ttk.Button(leftframe, text='./',command=getWorkingFolder)
	workingFolderButton.pack( side = TOP)
	#<\WorkingFolder>


	#<Binary>
	binaryLabel = ttk.Label(leftframe, text='Binary:')
	binaryLabel.pack(side = TOP)
	def getBinary() :
		data.binaryCodeName = askopenfilename()
		print("wybrano ", data.binaryCodeName)
		binaryButton.config(text=get_button_text(data.binaryCodeName))
	binaryButton = ttk.Button(leftframe, text='-',command=getBinary)
	binaryButton.pack( side = TOP)
	#<\Binary>


	#<Generator>
	generatorLabel = ttk.Label(leftframe, text='Generator:')
	generatorLabel.pack(side = TOP)
	def getGenerator() :
		data.generator = askopenfilename()
		generatorButton.config(text=get_button_text(data.generator))
	generatorButton = ttk.Button(leftframe, text='-', command=getGenerator)
	generatorButton.pack(side = TOP)
	#<\Generator>

	#<GeneratorSource>
	generatorSourceLabel = ttk.Label(leftframe, text='Seed:')
	generatorSourceLabel.pack(side = TOP)
	def getGenerator() :
		data.generatorSource = askopenfilename()
		generatorSourceButton.config(text=get_button_text(data.generatorSource))
	generatorSourceButton = ttk.Button(leftframe, text='-', command=getGenerator)
	generatorSourceButton.pack(side = TOP)

	#<\GeneratorSource>


	#<Brut>
	brutLabel = ttk.Label(leftframe, text='Brute-force:')
	brutLabel.pack(side = TOP)
	def getBrut() :
		data.brut = askopenfilename()
		brutButton.config(text=get_button_text(data.brut))
	brutButton = ttk.Button(leftframe, text='-', command=getBrut)
	brutButton.pack(side = TOP)
	#<\Brut>
	
	#<checkFrame>
	checkFrame = ttk.Frame(leftframe, borderwidth=5, relief="flat")
	checkFrame.pack(side = TOP)
	saveop = StringVar()
	saveall = ttk.Radiobutton(checkFrame, text='Save all tests', variable=saveop, value='saveall')
	savewa = ttk.Radiobutton(checkFrame, text='Save only tests with WA', variable=saveop, value='savewa')
	savenothing = ttk.Radiobutton(checkFrame, text='Don\'t save anything', variable=saveop, value='savenothing')
	saveop.set("saveall")
	saveall.pack(side = TOP)
	savewa.pack(side = TOP)
	savenothing.pack(side = TOP)
	brutecheckVar = StringVar()
	bruteforceCheckButton = ttk.Checkbutton(\
	leftframe, text='Check with brute-force',  variable=brutecheckVar,\
	onvalue='True', offvalue='False', )
	brutecheckVar.set('True')
	bruteforceCheckButton.pack(side=TOP)
	chceokienko = BooleanVar()
	waShowCheckButton = ttk.Checkbutton(\
	leftframe, text='Show WA-window',  variable=chceokienko,\
	onvalue=True, offvalue=False, )
	chceokienko.set(True)
	waShowCheckButton.pack(side=TOP)
	
	chceczas = BooleanVar()
	showTimeCheckButton = ttk.Checkbutton(\
	leftframe, text='Show execution time',  variable=chceczas,\
	onvalue=True, offvalue=False)
	chceokienko.set(True)
	showTimeCheckButton.pack(side=TOP)
	chceczas.set(False)

	#<\checkFrame>

	#<maxtime>
	mtlabel = ttk.Label(leftframe,text='Max execution time:')
	mtlabel.pack(side=TOP)
	mtVar = StringVar("")
	mtEntry = ttk.Entry(leftframe, textvariable=mtVar)
	mtEntry.pack(side = TOP)
	mtVar.set("5")

			
	#<\maxtime>

	#<\lewaramka>

	#<separator>
	#s = ttk.Separator(content, orient=HORIZONTA)
	#s.grid(column=1,row=0)
	#<\separator>

	#<prawaramka>

	rightframe = ttk.Labelframe(\
	content, borderwidth=5, relief="ridge",width=500,height=400,text='Results:',padding=(5,5,8,8))
	rightframe.grid(column=2,row=0)

	def setAll(ilet, wa, re) :
		allLabel.config(text = 'All tests : ' + str(ilet))
		okLabel.config(text = \
		'Ok : ' + str(ilet - wa - re))
		waLabel.config(text = 'Wa : ' + str(wa))
		reLabel.config(text = 'Re : ' + str((re)))
	
	run_lock = BooleanVar()
	run_lock.set(False)

	class atributes(object) :
		def __init__(self) :
			self.aktpos = 0
			self.ile_testow = 0
			self.testy_z_wa=[]
			self.testy_z_re=[]
			self.continueRunning = BooleanVar()
			self.continueRunning.set(True)
			self.jestokienko = BooleanVar()
			self.jestokienko.set(False)
	
	def resize_text(text) :
		while len(text) < 25:
			if len(text)+1 < 25:
				text = ' ' + text + ' '
			else :
				text = text + ' '
		return text

	def run_test(test,info) :
		text_on = test
		text_on = resize_text(text_on)
	
		testLabelList[info.aktpos].config(text = text_on, bg = 'white')
		root.update()

		wynik,czasf = wykonaj(data.binaryCodeName,test,float(mtVar.get()))
		if chceczas.get() :
			czasf *= 1000
			czas = (math.floor(czasf)+1)/1000

		bgcolor = 'white'
		info.ile_testow += 1
		text_on=""
		if wynik == "OK"  :
			retval="OK"

			text_on = "OK " + test
				
			if chceczas.get() :
				text_on += " t:" + str(czas) 
			if info.ile_testow%2 == 0:
				bgcolor = 'palegreen'
			else :
				bgcolor = 'lightgreen'
		elif wynik == "WA" :
			text_on = "WA " + test
			bgcolor = 'red'
			info.testy_z_wa.append(test)
			if (info.jestokienko.get() == False and chceokienko.get() == True) :
				info.jestokienko.set(True)
				global ErrorsRoot
				ErrorsRoot = Toplevel(root)
				if(data.stn != "") :
					ErrorsRoot.wm_title(\
					"Wa tests from " + data.stn)
				else :
					ErrorsRoot.wm_title(\
					"Wa tests " + data.binaryCodeName)
				global l
				l = Listbox(ErrorsRoot, height=30, bg = 'red')
				l.grid(column=0, row=0, sticky=(N,W,E,S))
				s = ttk.Scrollbar(\
				ErrorsRoot, orient=VERTICAL, command=l.yview)
				s.grid(column=1, row=0, sticky=(N,S))
				l['yscrollcommand'] = s.set
				ttk.Sizegrip().grid(\
				column=1, row=1, sticky=(S,E))

				ErrorsRoot.grid_columnconfigure(0, weight=1)
				ErrorsRoot.grid_rowconfigure(0, weight=1)
				def ErrorsRoothandler():
					info.jestokienko.set(False)
					chceokienko.set(False)
					ErrorsRoot.destroy()
				ErrorsRoot.protocol("WM_DELETE_WINDOW", ErrorsRoothandler)
				def onListDoubleClicked(*args, **selfargs) :
					sel = l.curselection()
					tescik = data.testFolder + l.get(sel[0])
					p = Process(target=os.system, args=\
					("leafpad " + tescik,))
					p.start()
					p2 = Process(target=os.system, args=\
					("leafpad " + tescik[:-2] + "out",))
					p2.start()
				if platform.system() == 'Linux' :
					l.bind("<Double-Button-1>", onListDoubleClicked)
			if info.jestokienko.get() :
				l.insert('end',test)
				ErrorsRoot.update()
			retval="WA"
		else :
			text_on = wynik + get_button_text(test)
			if wynik != 'TLE' :
				bgcolor = 'sienna1'
			else :
				bgcolor = 'salmon1'
			info.testy_z_re.append(test)
			retval="RE"
		text_on=resize_text(text_on)
		testLabelList[info.aktpos].config(text = text_on, bg = bgcolor)
		setAll(info.ile_testow, len(info.testy_z_wa), len(info.testy_z_re))
		root.update()
		return retval
	
	jestokienko = BooleanVar()
	def run() :
		if run_lock.get() == True:
			return
		run_lock.set(True)
		try :
			ErrorsRoot.destroy()
		except:
			run_lock.set(False)
			pass
		if not data.checkBasicData() :
			run_lock.set(False)
			return
		runButton.config(state=DISABLED)
		root.wm_title('Tiger (' + data.stn + ')')
		global A
		A = atributes()
		
		for test in os.listdir(data.testFolder) :
			if not A.continueRunning.get() :
				break
			if fnmatch.fnmatch(test, data.prefix + '*.in') :
				run_test(test,A)
				#print("ile_testow=",A.ile_testow)
				A.aktpos = A.aktpos + 1
				A.aktpos = A.aktpos % data.N
			
		messagebox.showinfo(message="Succsesfully ended testing.\n"\
		"Thank You for using Tiger")
		runButton.config(state=NORMAL)
		run_lock.set(False)
	def remFile(filename1) :
		try :
			if os.path.isfile(filename1) :
				os.remove(filename1)
		except :
			print("[remFile] failed to remove : " + filename1)
	def runGen() :
		try :
			ErrorsRoot.destroy()
		except:
			pass

		if run_lock.get() == True:
			return
		run_lock.set(True)
		if not data.checkGenData() :
			return
		global A
		A = atributes()
		data.saveOption = saveop.get()
		genRunButton.config(state=DISABLED)
		numer=0
		root.wm_title('Tiger - test generating - ' + data.stn + '')
		while True:
			if not A.continueRunning.get() :
				break
			numer+=1
			test=data.testFolder+data.stn+str(numer)+".in"
			if os.path.isfile(test) :
				continue
			genwynik = generuj(data.generator,data.brut,data.generatorSource,test,test[:-2]+"out",5)
			if genwynik == 'OK':
				wyn = run_test(test,A) 
			else :
				wyn = "NaN"
				text_on = wynik + " " + test
				text_on = resize_text(text_on)
				testLabelList[A.aktpos].config(text = text_on, bg = 'sienna1')
				A.testy_z_re.append(test)
				A.ile_testow+=1
				setAll(A.ile_testow, len(A.testy_z_wa), len(A.testy_z_re))
				root.update()
			if saveop.get() == 'savenothing' or (saveop.get() == 'savewa' and wyn=='OK'):
				remFile(test)
				remFile(test[:-2]+"out")
				remFile(test[:-2]+"myout")
			A.aktpos = A.aktpos+1
			A.aktpos = A.aktpos% data.N
		genRunButton.config(state=NORMAL)
		run_lock.set(False)
	#<runsFrame>
	runsFrame = ttk.Frame(rightframe, borderwidth=5, relief="flat")
	runsFrame.pack(side = TOP)
	runButton = Button(runsFrame, text='Run tests from the disk.',command=run, bg='goldenrod1')
	runButton.pack( side = LEFT)
	genRunButton = Button(runsFrame, text="Run tests made by the generator",command=runGen,bg='goldenrod2')
	genRunButton.pack(side = LEFT)
	#<\runsFrame>

	#<testsframe>
	#<def>
	testsFrame = ttk.Frame(rightframe, borderwidth=5,relief="ridge",width=300,height=300)
	testsFrame.pack(side = TOP)
	#<\def>
	
	testLabelList = []
	for x in range(data.N) :
		label = Label(testsFrame, text='-'*25, bg = 'mediumpurple')
		label.pack(side = TOP)
		testLabelList.append(label)
	
	#<\testsframe>-
	
	#<allFrame>
	#<def>
	allFrame = ttk.Labelframe(rightframe, borderwidth=5,relief="ridge",width=400, height=30,text="All:")
	allFrame.pack( side = TOP )
	#<\def>
	allLabel = Label(allFrame,text='All tests :  ')
	allLabel.pack(side = LEFT)
	
	okLabel = Label(allFrame,text='OK :  ',bg='lightgreen')
	okLabel.pack(side = LEFT)

	waLabel = Label(allFrame,text='WA :  ',bg='red')
	waLabel.pack(side = LEFT)

	reLabel = Label(allFrame,text='RE :  ',bg='sienna1')
	reLabel.pack(side = LEFT)

	#<\allFrame>
	#<stopButton>
	def onstopButtonClicked(*args) :
		A.continueRunning.set(False)
	stopButton = Button(rightframe, text='Stop', bg='red', command=onstopButtonClicked)
	stopButton.pack(side = TOP)
	#<\stopButton>
	#<\prawaramka>
		
	#konfiguracja rozciągania okienka
	root.columnconfigure(0,weight=1)
	root.rowconfigure(0,weight=1)
	for i in range(3) :
		content.columnconfigure(i,weight=1)
	content.rowconfigure(0,weight=0)

	root.mainloop()

buildGui()
