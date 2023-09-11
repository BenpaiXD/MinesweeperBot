import os

from PIL import Image, ImageGrab
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from Mouse import *
from colorama import Fore
import timeit


class Bot:
    def __init__(self, menu):
        self._menu = menu
        self._PATH = 'C:\\Program Files (x86)\\chromedriver.exe'
        self._ser = Service(self._PATH)
        self._driver = None
        self._options = None
        self._mapCoords = ()
        self._size = ()
        self._board = []
        self._tileSize = 0
        self._LClickMoves = set()
        self._RClickMoves = set()
        self._checkedBoard = list()
        self._constrainedTiles = list()
        self._constrNumTiles = list()
        self._possibleMines = list()
        self._probabilities = list()
        self._numMines = 0
        self._guesses = 0
        self._cap = 10

    def launch(self):
        options = Options()
        options.add_argument("--disable-notifications")
        self._driver = webdriver.Chrome(service=self._ser, options=options)
        self._driver.maximize_window()
        self._driver.get("https://minesweeperonline.com/")
        try:
            self._options = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.ID, "options-link")))
        except():
            print("error, quit")
            self._driver.quit()

    def setDifficulty(self, diff):
        self._menu.print("Difficulty set to: " + diff)
        if not self._menu._opened:
            return

        self._options.click()
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "options-close")))
        except():
            print("error, quit")
            self._driver.quit()

        if diff == "Beginner":
            self._driver.find_element(By.ID, "beginner").click()
            self._size = (9, 9)
            self._numMines = 10
        elif diff == "Intermediate":
            self._driver.find_element(By.ID, "intermediate").click()
            self._size = (16, 16)
            self._numMines = 40
        elif diff == "Expert":
            self._driver.find_element(By.ID, "expert").click()
            self._size = (16, 30)
            self._numMines = 99
        else:
            self._driver.find_element(By.ID, "custom").click()
            self._driver.find_element(By.ID, "custom_height").clear()
            self._driver.find_element(By.ID, "custom_height").send_keys(self._menu._SBoxH.get().strip())
            self._driver.find_element(By.ID, "custom_width").clear()
            self._driver.find_element(By.ID, "custom_width").send_keys(self._menu._SBoxW.get().strip())
            self._driver.find_element(By.ID, "custom_mines").clear()
            self._driver.find_element(By.ID, "custom_mines").send_keys(self._menu._SBoxMines.get().strip())
            self._size = (int(self._menu._SBoxH.get().strip()), int(self._menu._SBoxW.get().strip()))
            self._numMines = int(self._menu._SBoxMines.get().strip())

        self.initializeBoard()
        self._driver.find_element(By.CLASS_NAME, "dialogText").click()


    def simpleCheck(self, board) -> list:
        # loop through each tile on the board
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                # skip if tile is empty
                if not (board[i][j] == 0 or board[i][j] == 9 or board[i][j] == -1 or
                        self._checkedBoard[i][j]):
                    self.checkTile(board, (i, j))


    def run(self):
        self.getMap()
        
        # Click in center of the board so we can start the game
        mousePos(self.mouseCoords((self._size[0] - 1, 0)))
        leftClick()
        
        self.getBoard()

        while any(9 in sublist for sublist in self._board):
            self._RClickMoves.clear()
            self._LClickMoves.clear()
            self._constrainedTiles.clear()
            self._constrNumTiles.clear()
            self._possibleMines.clear()
            self._probabilities.clear()
            
            
            self.getBoard()
            
            if (any(-69 in sublist for sublist in self._board)):
                break

            self.simpleCheck(self._board)

            for move in self._RClickMoves:
                mousePos(self.mouseCoords(move))
                self._numMines -= 1
                rightClick()

            for move in self._LClickMoves:
                mousePos(self.mouseCoords(move))
                leftClick()

            if not (len(self._RClickMoves) == len(self._LClickMoves) == 0):
                continue

            #self._menu.print("Calculating possible mine configurations\n"
            #                 "This may take a moment, please wait...")
            
            # Loop through each tile
            for i in range(self._size[0]):
                for j in range(self._size[1]):
                    # skip if tile is empty
                    if not (self._board[i][j] == 0 or self._board[i][j] == 9 or self._board[i][j] == -1 or self._checkedBoard[i][j]):
                        if not any((i, j) in subset for subset in self._constrNumTiles):
                            self._constrainedTiles.append(set())
                            self._constrNumTiles.append(set())
                            self.getConstrainedTiles((i, j), self._constrainedTiles[-1], self._constrNumTiles[-1])
                            if set() in self._constrainedTiles:
                                self._constrainedTiles.remove(set())
                            if set() in self._constrNumTiles:
                                self._constrNumTiles.remove(set())

            for k in range(len(self._constrainedTiles)):
                # converting the sets of constrained tiles and constrained number tiles to lists 
                self._constrNumTiles[k] = list(self._constrNumTiles[k])
                self._constrainedTiles[k] = list(self._constrainedTiles[k])
                
                self._possibleMines.append(list())
                self._probabilities.append([0] * len(self._constrainedTiles[k]))
                self.possibleCombinations(self._constrainedTiles[k], self._constrNumTiles[k], [False] * len(self._constrainedTiles[k]), 0)
                for l in range(len(self._probabilities[k])):
                    try:
                        self._probabilities[k][l] /= len(self._possibleMines[k])
                    except ZeroDivisionError:
                        print(self._guesses)
                        return

            maxProb = (0, 0)
            for i in range(len(self._constrainedTiles)):
                for j in range(len(self._constrainedTiles[i])):
                    if self._probabilities[i][j] == 1:
                        self._RClickMoves.add(self._constrainedTiles[i][j])
                    elif self._probabilities[i][j] == 0:
                        self._LClickMoves.add(self._constrainedTiles[i][j])
                    else:
                        if self._probabilities[i][j] < self._probabilities[maxProb[0]][maxProb[1]] or 1 - self._probabilities[i][j] < self._probabilities[maxProb[0]][maxProb[1]]:
                            maxProb = (i, j)

            if len(self._RClickMoves) == len(self._LClickMoves) == 0 and not len(self._probabilities) == 0:
                self._guesses += 1
                self._menu.print("All remaining tiles have a chance of being a mine,")
                if self._probabilities[maxProb[0]][maxProb[1]] <= 0.5:
                    self._menu.print("Opening a tile which has a " + str(round(self._probabilities[maxProb[0]][maxProb[1]] * 100, 2)) + "% chance of being a mine")
                    self._LClickMoves.add(self._constrainedTiles[maxProb[0]][maxProb[1]])
                else:
                    self._menu.print("Flagging a tile which has a " + str(self._probabilities[maxProb[0]][maxProb[1]]) + "% chance of being a mine")
                    self._RClickMoves.add(self._constrainedTiles[maxProb[0]][maxProb[1]])

            # self.printConstrBoard()
            for move in self._RClickMoves:
                mousePos(self.mouseCoords(move))
                self._numMines -= 1
                rightClick()

            for move in self._LClickMoves:
                mousePos(self.mouseCoords(move))
                leftClick()
        print(self._guesses)


    def countSurroundingTiles(self, coords: tuple) -> tuple:
        # first index is for number of mines, second is for number of closed tiles
        counts = [0, 0]
        
        for i in range(coords[0] - 1, coords[0] + 2):
            for j in range(coords[1] - 1, coords[1] + 2):
                # ensure not looking out of bounds
                if 0 <= i < self._size[0] and 0 <= j < self._size[1]:
                    if self._board[i][j] == -1:
                        counts[0] += 1
                    elif self._board[i][j] == 9:
                        counts[1] += 1
        return tuple(counts)
        

    def possibleCombinations(self, constrTilesArr: list, numTilesArr: list, TFarr: list, index: int):
        """_summary_

        Args:
            constrTilesArr (list): _description_
            numTilesArr (list): _description_
            TFarr (list): _description_
            index (int): _description_
        """
        
        # early exit check
        for coords in numTilesArr:
            surroundingCount = self.countSurroundingTiles(coords)
            numMines = surroundingCount[0]
            numClosedTiles = surroundingCount[1]
            
            if numMines > self._board[coords[0]][coords[1]]:
                # self._menu.print("early exit")
                return
            elif self._board[coords[0]][coords[1]] - numMines > numClosedTiles:
                # self._menu.print("early exit")
                return
        
        if index == len(constrTilesArr):
            valid = True
            for coords in numTilesArr:
                numMines = self.countSurroundingTiles(coords)[0]

                valid = valid and numMines == self._board[coords[0]][coords[1]]

            if valid:
                self._possibleMines[-1].append(list(TFarr))
                for i in range(len(TFarr)):
                    if TFarr[i]:
                        self._probabilities[-1][i] += 1
            return

        self._board[constrTilesArr[index][0]][constrTilesArr[index][1]] = 0
        TFarr[index] = False
        self.possibleCombinations(constrTilesArr, numTilesArr, TFarr, index + 1)

        self._board[constrTilesArr[index][0]][constrTilesArr[index][1]] = -1
        TFarr[index] = True
        self.possibleCombinations(constrTilesArr, numTilesArr, TFarr, index + 1)

        self._board[constrTilesArr[index][0]][constrTilesArr[index][1]] = 9

    def getConstrainedTiles(self, coords, constrTiles, constrNumTiles):
        # blank tile case
        if self._board[coords[0]][coords[1]] == 9:
            if coords in constrTiles:
                return
            constrTiles.add(coords)
            for i in range(coords[0] - 1, coords[0] + 2):
                for j in range(coords[1] - 1, coords[1] + 2):
                    if 0 <= i < self._size[0] and 0 <= j < self._size[1] and 1 <= self._board[i][j] <= 8:
                        self.getConstrainedTiles((i, j), constrTiles, constrNumTiles)

        else:
            if coords in constrNumTiles:
                return
            constrNumTiles.add(coords)
            for i in range(coords[0] - 1, coords[0] + 2):
                for j in range(coords[1] - 1, coords[1] + 2):
                    if 0 <= i < self._size[0] and 0 <= j < self._size[1] and self._board[i][j] == 9:
                        self.getConstrainedTiles((i, j), constrTiles, constrNumTiles)


    def checkTile(self, board, coords: tuple):
        """
        Checks the tiles around the provided numbered tile, 
        puts surrounding tiles which must be mines in the rClickMoves array and tiles which cannot be mines in the LClickMoves array
        uncertain tiles are left unchanged
        
        Args:
            coords (tuple): coorinates of tile to check
        """
        
        # Raise exception if tile being checked is not a numbered tile
        if 9 < board[coords[0]][coords[1]] or board[coords[0]][coords[1]] < 1:
            raise Exception(f"checkTile Exception: Can only check numbered tiles (tile at ({coords[0], coords[1]}) id {self._board[coords[0]][coords[1]]})")
        
        blankTiles = list()
        numMines = 0
        
        # look at tiles 1 chessboard unit away
        h = len(board)
        w = len(board[0])
        for i in range(coords[0] - 1, coords[0] + 2):
            for j in range(coords[1] - 1, coords[1] + 2):
                # skip if attemping to obsever tile out of bounds
                if 0 <= i < h and 0 <= j < w:
                    
                    if self._board[i][j] == 9:
                        blankTiles.append((i, j))
                    elif self._board[i][j] == -1:
                        numMines += 1

        # if the number of blank tiles surrounding the current tile is equal to the current tile number minus the number of mines tounching the tile, the blank tiles must be mines so they are set to be flagged
        if len(blankTiles) == board[coords[0]][coords[1]] - numMines:
            for tile in blankTiles:
                self._RClickMoves.add(tile)
            self._checkedBoard[coords[0]][coords[1]] = True
        elif numMines == board[coords[0]][coords[1]]: # if the number of mines surrounding the current tile is equal to its number, all other blank tiles can be uncovered
            for tile in blankTiles:
                self._LClickMoves.add(tile)
            self._checkedBoard[coords[0]][coords[1]] = True




    def getBoard_v2(self):
        boardDiv = self._driver.find_element(By.ID, 'game')
        tiles = boardDiv.find_elements(By.XPATH, '*')
        
        for element in tiles:
            elemID = element.get_attribute("id")
            if elemID == "" or not elemID[:6] == "square":
                continue
            coords = elemID.split("_")
            coords = [int(x) for x in coords]
            
            elemClass = element.get_attribute("class")
            if elemClass== "square blank":
                self._board[coords[0]][coords[1]] = 9
            elif elemClass == "square bombflagged":
                self._board[coords[0]][coords[1]] = -1
            elif elemClass == "square bombrevealed" or elemClass == "square bombdeath":
                self._board[coords[0]][coords[1]] = -69
            else:
                self._board[coords[0]][coords[1]] = int(elemClass[-1])
                


    def getBoard(self):
        """
        Loads the _board 2D list attribute from the browser such that numbers 1-8 are labeled as such, 
        mines are labled as -1, unflipped tiles are nine and blank tiles are 0
        
        """
        
        im = ImageGrab.grab(self._mapCoords)
        # im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
        im.convert("RGB")
        for j in range(self._size[1]):
            for i in range(self._size[0]):
                rgb = im.getpixel(self.tileCoords((i, j)))
                
                # non numeric tiles
                if rgb == (189, 189, 189):
                    coords = list(self.tileCoords((i, j)))
                    coords[0] -= 1
                    if im.getpixel(tuple(coords)) == (0, 0, 0):
                        self._board[i][j] = -1
                        continue
                    coords[0] -= 7
                    if im.getpixel(tuple(coords)) == (255, 255, 255):
                        self._board[i][j] = 9
                    else:
                        self._board[i][j] = 0
                # 1
                elif rgb == (0, 0, 255):
                    self._board[i][j] = 1
                # 2
                elif rgb == (0, 123, 0):
                    self._board[i][j] = 2
                # 3
                elif rgb == (255, 0, 0):
                    self._board[i][j] = 3
                # 4
                elif rgb == (0, 0, 123):
                    self._board[i][j] = 4
                # 5
                elif rgb == (123, 0, 0):
                    self._board[i][j] = 5
                # 6
                elif rgb == (0, 123, 123):
                    self._board[i][j] = 6
                # 7
                elif rgb == (0, 0, 0):
                    self._board[i][j] = 7
                # 8
                elif rgb == (123, 0, 0):
                    self._board[i][j] = 8
                else:
                    self._board[i][j] = -69

    def initializeBoard(self):
        self._board = list()
        self._checkedBoard = list()
        for i in range(self._size[0]):
            arr = list()
            arr2 = list()
            for j in range(self._size[1]):
                arr.append(-1)
                arr2.append(False)
            self._board.append(arr)
            self._checkedBoard.append(arr2)

    def getMap(self):
        im = ImageGrab.grab(())
        im.convert("RGB")
        # print(str(im.width) + " " + str(im.height))
        size = [0, 0, 0, 0]
        for j in range(int(round(im.height * 0.0833)), im.height - int(round(im.height * 0.02778))):
            for i in range(im.width):
                if im.getpixel((i, j)) == (189, 189, 189) and im.getpixel((i + 1, j)) == (189, 189, 189):
                    size[0] = i
                    size[1] = j
                    break
            else:
                continue
            break

        for i in range(size[0], im.width):
            if im.getpixel((i, size[1])) == (255, 255, 255):
                size[2] = i
                break

        for i in range(size[1], im.height):
            if im.getpixel((size[0], i)) == (255, 255, 255):
                size[3] = i
                break

        size[0] += 8
        size[1] += 50
        size[2] -= 10
        size[3] -= 10

        # ImageGrab.grab(tuple(size)).save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

        self._mapCoords = tuple(size)
        self._tileSize = round((self._mapCoords[2] - self._mapCoords[0]) / self._size[1])

    def mouseCoords(self, coords):
        newCoords = list()
        newCoords.append(coords[1] * self._tileSize + 9 + self._mapCoords[0])
        newCoords.append(coords[0] * self._tileSize + 8 + self._mapCoords[1])
        return tuple(newCoords)

    def tileCoords(self, coords):
        newCoords = list()
        newCoords.append(coords[1] * self._tileSize + 9)
        newCoords.append(coords[0] * self._tileSize + 8)
        return tuple(newCoords)

    def printConstrBoard(self):
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if any((i, j) in subset for subset in self._constrainedTiles):
                    print(Fore.RED + str(self._board[i][j]), end='\t')
                else:
                    print(Fore.WHITE + str(self._board[i][j]), end='\t')

            print()

    def destroy(self):
        if self._driver is not None:
            self._driver.quit()


def testConstrainedTiles():
    bot = Bot(None)
    bot._board = [[-1, 2, 1, 1, 1, 2, 9, 9, 9],
                  [1, 2, -1, 2, 2, -1, 9, 9, 9],
                  [1, 2, 2, 2, -1, 3, 9, 9, 9],
                  [1, -1, 2, 2, 2, 2, 9, 9, 9],
                  [3, 2, 2, -1, 1, 1, 9, 9, 9],
                  [-1, 2, 1, 1, 2, 2, 9, 9, 9],
                  [-1, 2, 0, 0, 1, -1, 3, 9, 9],
                  [2, 2, 1, 0, 1, 2, 3, 9, 9],
                  [2, -1, 2, 0, 0, 2, -1, 9, 9],
                  [2, -1, 2, 0, 0, 3, -1, 9, 9],
                  [1, 1, 2, 1, 1, 2, -1, 9, 9],
                  [1, 2, 3, -1, 2, 3, 4, 9, 9],
                  [1, -1, -1, 2, 3, -1, -1, 9, 9],
                  [1, 2, 2, 1, 2, -1, 4, 9, 9],
                  [0, 0, 0, 0, 1, 2, 9, 9, 9],
                  [0, 0, 0, 0, 0, 1, 9, 9, 9]]
    bot._size = [len(bot._board), len(bot._board[1])]

    for i in range(bot._size[0]):
        for j in range(bot._size[1]):
            # skip if tile is empty
            if not (bot._board[i][j] == 0 or bot._board[i][j] == 9 or bot._board[i][j] == -1):
                if not (i, j) in bot._constrNumTiles:
                    bot._constrainedTiles.append(set())
                    bot.getConstrainedTiles((i, j), bot._constrainedTiles[-1])

    print(bot._constrainedTiles)
    bot.printConstrBoard()
    quit()

    bot._constrainedTiles.append(set())
    bot.getConstrainedTiles((0, 5), bot._constrainedTiles[-1])
    print(bot._constrainedTiles)
    bot.printConstrBoard()


def print2DList(arr):
    for x in arr:
        print(*x, sep=' ')


def testAdvancedAlgo():
    bot = Bot(None)
    
    bot._board = [[9, 9, 9, 9, 9, 9, 9, 9, 9, 2, 1, 0, 1, -1, 1, 0, 0, 1, -1, 2, 2, 2, 2, 1, 1, 0, 0, 1, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, -1, 2, 0, 1, 1, 1, 0, 0, 2, 2, 3, -1, -1, 4, -1, 1, 0, 0, 1, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, -1, 3, 0, 1, 1, 1, 0, 0, 1, -1, 2, 3, -1, -1, 2, 1, 0, 0, 1, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 5, -1, 3, 1, 2, -1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 0, 1, 1, 2, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, -1, 3, 3, -1, 3, 1, 2, -1, 1, 0, 1, 2, 2, 1, 0, 0, 0, 1, -1, 3, 9, 9],
[9, 9, 9, 9, 9, 9, 3, 3, -1, 3, 4, -1, 3, 0, 1, 1, 1, 1, 2, -1, -1, 2, 1, 0, 0, 1, 2, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 2, 1, 1, 2, -1, -1, 3, 1, 1, 0, 0, 1, -1, 4, 4, -1, 1, 1, 1, 1, 1, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 2, 0, 1, 3, 4, 3, 2, -1, 1, 0, 0, 1, 1, 2, -1, 3, 3, 3, -1, 3, 2, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 1, 1, 2, -1, -1, 1, 2, 2, 2, 0, 1, 1, 1, 1, 3, -1, 3, -1, -1, 9, 9, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 2, 1, 2, -1, 2, 1, 2, -1, 1, 0, 2, -1, 4, 3, 3, 9, 9, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 1, 0, 2, -1, 2, 2, -1, 5, 3, 1, 1, 3, -1, 3, 1, 9, 9, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, -1, 1, 0, 1, 1, 2, 3, -1, -1, -1, 2, 1, 3, -1, 9, 9, 9, 9, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 1, 0, 0, 1, 2, -1, 4, 5, -1, 3, 2, -1, 4, 9, 9, 9, 9, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 0, 0, 0, 1, -1, 2, 2, -1, 3, -1, 2, 2, -1, 9, 9, 9, 9, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 9, 9, 9, 9, 9, 9, 9],
[9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 1, 1, 9, 9, 9, 9, 9, 9, 9]]
    
    
    

if __name__ == '__main__':
    testConstrainedTiles()
