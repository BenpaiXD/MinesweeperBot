from PIL import Image, ImageGrab
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Bot:
    def __init__(self):
        self._PATH = 'C:\\Program Files (x86)\\chromedriver.exe'
        self._ser = Service(self._PATH)
        self._driver = None
        self._options = None
        self._mapCoords = ()

    def launch(self):
        self._driver = webdriver.Chrome(service=self._ser)
        self._driver.maximize_window()
        self._driver.get("https://minesweeperonline.com/")
        try:
            self._options = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "options-link")))
        except():
            print("error, quit")
            self._driver.quit()

    def setDifficulty(self, diff):
        self._options.click()
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "options-close")))
        except():
            print("error, quit")
            self._driver.quit()

        if diff == "Beginner":
            self._driver.find_element(By.ID, "beginner").click()
        elif diff == "Intermediate":
            self._driver.find_element(By.ID, "intermediate").click()
        elif diff == "Expert":
            self._driver.find_element(By.ID, "expert").click()

        self._driver.find_element(By.CLASS_NAME, "dialogText").click()

    def run(self):
        self.getMap()


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


    def destroy(self):
        self._driver.quit()

if __name__ == '__main__':
    bot = Bot()
    bot.launch()
