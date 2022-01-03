from tkinter import *
from Bot import Bot


class Menu:
    def __init__(self):
        self._master = Tk()
        self._master.title("Minesweeper Bot")
        self._frame = Frame(self._master)
        self._master.attributes("-topmost", True)
        self._opened = False
        self._bot = Bot()

        self._btnOpen = Button(self._frame, text="Open Minesweeper", command=self.open)
        self._btnOpen.pack()

        self._difficultyList = ["Beginner", "Intermediate", "Expert"]
        self._difficulty = StringVar(self._master)
        self._difficulty.set("Select Difficulty")
        self._difficultyMenu = OptionMenu(self._master, self._difficulty, *self._difficultyList, command=self.difficultyChange)
        # self._difficultyMenu.pack()

        self._btnRun = Button(self._frame, text="Run", command=self.run, state=DISABLED)
        self._btnRun.pack()

        self._btnClose = Button(self._frame, text="Exit", command=self.close)
        self._btnClose.pack()

        self._frame.pack()
        mainloop()

    def open(self):
        self._opened = True
        self._bot.launch()
        self._btnOpen['state'] = DISABLED
        self._difficultyMenu.pack()

    def difficultyChange(self, diff):
        self._btnRun['state'] = NORMAL
        self._bot.setDifficulty(diff)

    def run(self):
        self._bot.run()

    def close(self):
        self._master.destroy()
        self._bot.destroy()
        quit()


def main():
    Menu()


if __name__ == '__main__':
    main()