import time

import pyautogui
import pynput.keyboard
from pynput.keyboard import Listener

pyautogui.PAUSE = 0.2

def do(key):
    print(key)
    if key == pynput.keyboard.Key.pause:
        pyautogui.click(1489, 241)
        pyautogui.click(1396, 286)
        pyautogui.click(1480, 364)
        pyautogui.click(1454, 280)
        pyautogui.click(1487, 341)
        pyautogui.click(1488, 233)
        pyautogui.hotkey('ctrl', 'right')
    if key == pynput.keyboard.Key.scroll_lock:
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        pyautogui.press('down')
        pyautogui.press('apps')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'tab')
        pyautogui.press('apps')
        pyautogui.press('down')
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        pyautogui.hotkey('shift', 'left')
    if key ==pynput.keyboard.Key.ctrl_r:
        pyautogui.hotkey('shift','left')
        pyautogui.doubleClick(1503, 435)
        pyautogui.write('8.5')
        pyautogui.press('esc')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('right')

def do_a(x,y,m,v):
    if v:
        print(x,y)

l = Listener(on_press=do)
l.run()
