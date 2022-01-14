from tkinter import *
from tkinter import _setit
from time import time

from Bot import Bot


class Menu:
    def __init__(self):
        self._master = Tk()
        self._master.title("Minesweeper Bot")
        self._frame = Frame(self._master)
        self._master.attributes("-topmost", True)
        self._opened = False
        self._bot = Bot(self)

        self._panelButtons = Frame(self._frame)

        self._btnOpen = Button(self._panelButtons, text="Open Minesweeper", command=self.open)
        self._btnOpen.grid(row=0, sticky="we")

        self._difficultyList = ["Beginner", "Intermediate", "Expert", "Custom"]
        self._difficulty = StringVar(self._master)
        self._difficulty.set("Select Difficulty")
        self._difficultyMenu = OptionMenu(self._panelButtons, self._difficulty, *self._difficultyList, command=self.difficultyChange)
        # self._difficultyMenu.grid(row=1)

        self._btnReset = Button(self._panelButtons, text="Reset", command=self.reset, state=DISABLED)
        self._btnReset.grid(row=2, sticky="we")

        self._btnRun = Button(self._panelButtons, text="Run", command=self.run, state=DISABLED)
        self._btnRun.grid(row=3, sticky="we")

        self._btnAbout = Button(self._panelButtons, text="About", command=self.about)
        self._btnAbout.grid(row=4, sticky="we")

        self._btnClose = Button(self._panelButtons, text="Exit", command=self.close)
        self._btnClose.grid(row=5, sticky="we")

        self._panelButtons.grid()

        self._TextBox = Text(self._frame, width=50, height=12, state=DISABLED)
        self._TextBox.grid(row=0, column=1, rowspan=4, columnspan=6)

        self._panelCustom = Frame(self._frame)

        self._lblCustom = Label(self._panelCustom, text="Custom Board Settings")
        self._lblCustom.pack(side=TOP, fill=X, expand=True)

        self._lblH = Label(self._panelCustom, text="H:", width=3)
        self._lblH.pack(side=LEFT)

        self._hVal = StringVar()
        self._SBoxH = Spinbox(self._panelCustom, from_=1, to=50, textvariable=self._hVal, width=3)
        self._SBoxH.pack(side=LEFT)

        self._lblW = Label(self._panelCustom, text="W:", width=3)
        self._lblW.pack(side=LEFT)

        self._wVal = StringVar()
        self._SBoxW = Spinbox(self._panelCustom, from_=8, to=80, textvariable=self._wVal, width=3)
        self._SBoxW.pack(side=LEFT)

        self._lblMines = Label(self._panelCustom, text="Mines:")
        self._lblMines.pack(side=LEFT)

        self._minesVal = StringVar()
        self._SBoxMines = Spinbox(self._panelCustom, from_=1, to=1000, textvariable=self._minesVal, width=3)
        self._SBoxMines.pack(side=LEFT)

        self._panelCustom.grid(column=1)

        self._frame.pack()
        mainloop()

    def open(self):
        self._opened = True
        self._bot.launch()
        self._btnOpen['state'] = DISABLED
        self._difficultyMenu.grid(row=1, sticky="we")

    def difficultyChange(self, diff):
        _setit(self._difficulty, diff)
        self._btnRun['state'] = NORMAL
        self._bot.setDifficulty(diff)
        self._btnReset['state'] = DISABLED

    def reset(self):
        self.difficultyChange(self._difficulty.get())

    def run(self):
        self._btnRun['state'] = DISABLED
        start = time()
        self._bot.run()
        end = time()
        self.print("Time to Run: " + str(round(end - start, 2)))
        self._btnReset['state'] = NORMAL

    def about(self):
        pass

    def close(self):
        self._master.destroy()
        self._bot.destroy()
        quit()

    def print(self, string):
        self._TextBox.config(state=NORMAL)
        self._TextBox.insert('1.0', string + "\n")
        self._TextBox.config(state=DISABLED)
        self._master.update()


def main():
    Menu()


if __name__ == '__main__':
    main()