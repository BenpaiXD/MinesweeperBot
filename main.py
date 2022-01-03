from PIL import Image, ImageGrab
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getMap():
    im = ImageGrab.grab(())
    im.convert("RGB")
    print(str(im.width) + " " + str(im.height))
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

    #ImageGrab.grab(tuple(size)).save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

    return tuple(size)


def main():
    PATH = 'C:\\Program Files (x86)\\chromedriver.exe'
    ser = Service(PATH)
    driver = webdriver.Chrome(service=ser)
    driver.maximize_window()
    driver.get("https://minesweeperonline.com/")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "options-link")))
    except():
        print("error, quit")
        driver.quit()

    mapCoords = getMap()
    driver.quit()


if __name__ == '__main__':
    main()

