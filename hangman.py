# SDP_VIDEHI
from tkinter import messagebox
from tkinter import *
import random
import os
import glob

CZECH = {'á': 'a', 'é': 'e', 'ě': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'š': 's',
         'č': 'c', 'ř': 'r', 'ž': 'z', 'ň': 'n', 'ť': 't', 'ĺ': 'l', 'ď': 'd'}


class HangMan:
    def __init__(self):
        self.path = os.getcwd()
        self.currentWords = []
        self.topic = ''
        self.wordList = []
        self.currentWord = ''
        self.alreadyGuessed = []
        self.alreadyGuessedWrong = []
        self.images = []

    def accessOptions(self):
        optionsPath = 'Data\Words\*.txt'
        optionNames = glob.glob(optionsPath)
        self.options = []
        for x in optionNames:
            x = (x.split('\\'))
            x = re.sub(r'.txt$', '', x[len(x)-1])
            self.options.append(x)

    def loadPictures(self):
        path = r'' + self.path + '\Data\Pictures\ '
        os.chdir(path)
        for x in range(1, 12):
            name = str(x)+'.gif'
            self.images.append(PhotoImage(file=name))

    def loadWords(self):
        path = r'' + self.path + '\Data\Words\ '
        os.chdir(path)
        title = self.topic + '.txt'
        wordFile = open(title, 'r')
        wordList = wordFile.read()
        wordFile.close()
        wordList = wordList.split('\n')
        self.wordList = wordList

    def randomWord(self):
        i = random.randint(0, len(self.wordList))
        self.currentWord = (self.wordList[i-1])

    def newWord(self):
        self.checkTopic()
        self.nextWord.config(state='disabled')
        self.entryField.config(state='normal')
        self.alreadyGuessed = []
        self.alreadyGuessedWrong = []
        self.hangmanCanvas.delete(ALL)
        self.randomWord()
        self.drawLetters()

    def runInitialWindow(self):
        startWindow = Tk()
        startWindow.title('Hangman By Videhi')
        frameOptions = LabelFrame(
            startWindow, text='Choose a Topic', labelanchor=N)
        frameOptions.pack()

        self.topicVar = StringVar()
        self.topicVar.set(None)
        for word in self.options:
            Radiobutton(frameOptions, text=word,
                        variable=self.topicVar, value=word).pack()
        confirm = Button(frameOptions, text='OK', bg='black',
                         fg='white', width=7, command=startWindow.destroy)
        confirm.pack()
        geometry = '300x'+str(30+30*len(self.options))
        startWindow.geometry(geometry)
        startWindow.resizable(width=FALSE, height=FALSE)
        startWindow.mainloop()

    def getTopic(self):
        return self.topicVar.get()

    def runMainWindow(self):
        self.mainWindow = Tk()
        self.mainWindow.geometry('800x600')
        self.mainWindow.resizable(width=FALSE, height=FALSE)
        self.mainWindow.title('Hangman by Videhi')

        background = Canvas(self.mainWindow, width=800, height=600,
                            highlightthickness=0, bg='#c4dbf5')
        background.pack(anchor=NW)

        self.hangmanCanvas = Canvas(
            self.mainWindow, width=750, height=400, bg='white', highlightthickness=0)
        self.hangmanCanvas.place(x=20, y=40)

        self.wordField = Canvas(self.mainWindow, width=590, height=120,
                                bg='white', highlightthickness=0)
        self.wordField.place(x=180, y=445)

        self.nextWord = Button(self.mainWindow, text=' Next Word ', command=self.newWord,
                               highlightthickness=0, state='disabled')

        entryFrame = LabelFrame(
            self.mainWindow, text='   Enter a Letter   ', relief=RAISED, bg='#c4dbf5')
        entryFrame.place(x=45, y=485)

        self.entryField = Entry(entryFrame, width=5, relief='sunken',
                                font=('Verdana', 14), state='normal')
        self.entryField.pack()
        self.entryField.focus_set()
        self.entryField.bind('<Return>', self.proceedLetterEvent)

        self.topicVar = StringVar(self.mainWindow)
        self.topicVar.set(self.topic)
        changeTopic = OptionMenu(self.mainWindow, self.topicVar, *self.options)
        changeTopic.config(highlightthickness=0)
        changeTopic.place(x=770, y=12, anchor=NE)

        confirmLetter = Button(entryFrame, text='OK', bg='black',
                               fg='white', command=self.proceedLetter)
        confirmLetter.pack()
        self.mainWindow.protocol("WM_DELETE_WINDOW", self.close)

    def drawLetters(self):
        word = self.currentWord
        self.wordField.delete(ALL)
        y = 70
        l_h = 25
        offset = 20
        space = 10
        lineWidth = 20
        height = 20
        wordcount = 0
        lettercount = 0
        maxlen = 0
        ct = -1
        if len(word) > 18:
            test = word.split(' ')
            for x in test:
                lettercount += len(x)+1
                if lettercount > 18:
                    break
                wordcount += 1
            for x in range(wordcount):
                maxlen += (1+len(test[x]))
            for n in range(maxlen):
                state = 'hidden'
                if (word[n] in self.alreadyGuessed) or (word[n] in "-!,'?;."):
                    state = 'normal'
                if word[n] in " -?!';.,":
                    stateline = 'hidden'
                else:
                    stateline = 'normal'
                y1 = y-30
                self.wordField.create_line(offset+n*(lineWidth+space), y1, offset +
                                           n*(lineWidth+space)+lineWidth, y1, width=1, state=stateline)
                self.wordField.create_text(offset+n*(lineWidth+space)+lineWidth/2,
                                           y1-l_h/2, text=word[n], font=('Times', height), state=state)
            for n in range(maxlen, len(word)):
                ct += 1
                state = 'hidden'
                if (word[n] in self.alreadyGuessed) or (word[n] in "-!,'?;."):
                    state = 'normal'
                if word[n] in " -?!';.,":
                    stateline = 'hidden'
                else:
                    stateline = 'normal'
                y2 = y+20
                self.wordField.create_line(offset+ct*(lineWidth+space), y2, offset +
                                           ct*(lineWidth+space)+lineWidth, y2, width=1, state=stateline)
                self.wordField.create_text(offset+ct*(lineWidth+space)+lineWidth/2,
                                           y2-l_h/2, text=word[n], font=('Times', height), state=state)
        else:
            for n in range(len(word)):
                state = 'hidden'
                if (word[n] in self.alreadyGuessed) or (word[n] in "-!,'?;."):
                    state = 'normal'
                if word[n] in " -?!';.,":
                    stateline = 'hidden'
                else:
                    stateline = 'normal'
                self.wordField.create_line(offset+n*(lineWidth+space), y, offset+n*(
                    lineWidth+space)+lineWidth, y, width=1, state=stateline)
                self.wordField.create_text(offset+n*(lineWidth+space)+lineWidth/2,
                                           y-l_h/2, text=word[n], font=('Times', height), state=state)

    def replaceCzech(self, word):
        word = list(word)
        for x in range(len(word)):
            if word[x] in CZECH:
                word[x] = CZECH[word[x]]
        return ''.join(word)

    def proceedLetterEvent(self, event):
        self.proceedLetter()

    def proceedLetter(self):
        word = self.currentWord
        word_test = word.lower()
        word_test = self.replaceCzech(word_test)
        letter = (self.entryField.get()).lower()
        self.entryField.delete(0, END)
        if (letter in self.alreadyGuessed) or (letter not in 'abcdefghijklmnopqrstuwvxyz0123456789') or ((len(letter)) != 1):
            return
        self.alreadyGuessed += letter
        self.alreadyGuessed += letter.upper()
        for let in CZECH:
            if letter == CZECH[let]:
                self.alreadyGuessed += let
                self.alreadyGuessed += let.upper()
                break
        if letter in word_test:
            self.drawLetters()
            hlp = 0
            for x in list(word):
                if x in self.alreadyGuessed:
                    hlp += 1

            if hlp == len(''.join(re.split("[ -?!;.,]", word))):
                self.youWin()
                self.endGame()
        else:
            self.alreadyGuessedWrong.append(letter.upper())
            self.drawAlreadyGuessed()
            self.drawHangman()
            if len(self.alreadyGuessedWrong) == 11:
                self.youLose()
                self.endGame()
                self.alreadyGuessed.extend(list(word))
                self.drawLetters()

    def drawHangman(self):
        self.hangmanCanvas.create_image(
            0, 0, anchor=NW, image=self.images[len(self.alreadyGuessedWrong)-1])

    def drawAlreadyGuessed(self):
        agprint = ', '.join(self.alreadyGuessedWrong)
        self.hangmanCanvas.create_text(
            20, 375, text=agprint, font=('Verdana,14'), anchor=NW)

    def youWin(self):
        self.hangmanCanvas.create_text(
            375, 350, text='You win! Click on next word to play again', fill='red', font=('Verdana', 15))

    def youLose(self):
        self.hangmanCanvas.create_text(
            375, 350, text='You Loose! Game over. Click on next word to play again', fill='red', font=('Verdana', 15))

    def endGame(self):
        self.nextWord.config(state='active')
        self.entryField.config(state='disabled')

    def checkTopic(self):
        if self.topic != self.getTopic():
            self.topic = self.getTopic()
            self.loadWords()

    def levelwindow(self):
        self.win = Tk()
        var = StringVar()
        v = IntVar()
        self.win.geometry('300x250')
        self.win.resizable(width=FALSE, height=FALSE)
        self.win.title('Hangman by Videhi')
        self.Label = Label(self.win, textvariable=var, relief=FLAT, fg="black",
                           font="Times")
        var.set("Welcome to the hangman game by Videhi ! \nYour objective is to guess a word,\nby guessing one letter at a time .\nIf the letter isn't in the word ,\na man is getting hanged\nNow choose a difficulty")
        self.Label.pack()
        b1 = Radiobutton(self.win, variable=v, text="Easy",
                         value=1, bg="#AED6F1")
        b2 = Radiobutton(self.win, variable=v, text="Medium",
                         value=2, bg="#5DADE2")
        b3 = Radiobutton(self.win, variable=v, text="Hard",
                         value=3, bg="#2874A6")

        confirma = Button(self.win, text='OK', bg='black',
                          fg='white', command=self.win.destroy)
        b1.pack()
        b2.pack()
        b3.pack()
        confirma.pack()
        self.win.mainloop()

    def run(self):
        self.levelwindow()
        self.accessOptions()
        self.runInitialWindow()
        self.topic = self.getTopic()
        if self.topic == "None":
            sys.exit(0)
        self.loadWords()
        self.randomWord()
        self.runMainWindow()
        self.loadPictures()
        self.drawLetters()
        self.mainWindow.mainloop()

    def close(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.mainWindow.destroy()


game = HangMan()
game.run()
