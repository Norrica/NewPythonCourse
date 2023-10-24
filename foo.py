import time

import pyautogui
import pyperclip
from pynput import keyboard, mouse

pyautogui.PAUSE = 0.2
pyautogui.move

def make_border():
    pyautogui.click(1489, 241)
    pyautogui.click(1396, 286)
    pyautogui.click(1480, 364)
    pyautogui.click(1454, 280)
    pyautogui.click(1487, 341)
    pyautogui.click(1488, 233)
    pyautogui.hotkey('ctrl', 'right')


def copy_slide_text():
    time.sleep(0.2)
    pyautogui.PAUSE = 0.2
    pyautogui.hotkey('ctrl', 'shift', 'tab')
    pyautogui.press('esc')
    pyautogui.press('esc')
    pyautogui.press('esc')
    for i in range(3): # Выбирается в порядке редактирования.
        pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('apps')  # pyautogui.hotkey('ctrl','c')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 'tab')
    pyautogui.press('esc')
    pyautogui.press('up')
    pyautogui.press('end')
    pyautogui.press('enter')
    pyautogui.press('backspace')
    pyautogui.press('backspace')
    pyautogui.press('esc')
    pyautogui.press('apps')  # pyautogui.hotkey('ctrl','shift','v')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.click(176, 810)
    pyautogui.hotkey('ctrl', 'tab')


def copy_slide_to_doc():
    # pyautogui.press('down')
    # pyautogui.press('down')
    pyautogui.hotkey('ctrl', 'shift', 'tab')
    pyautogui.press('esc')
    pyautogui.press('esc')
    pyautogui.press('esc')
    pyautogui.press('down')
    pyautogui.press('apps')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'tab')
    pyautogui.press('esc')
    pyautogui.press('apps')
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter')
    pyautogui.hotkey('shift', 'left')


def make_8cm_wide():
    pyautogui.hotkey('shift', 'left')
    pyautogui.click(1490, 225)
    time.sleep(0.2)
    pyautogui.click(1705, 279)
    time.sleep(0.2)
    pyautogui.doubleClick(1507, 431)
    pyautogui.write('8')
    pyautogui.PAUSE = 0.05
    for i in range(5):
        pyautogui.click(1559, 435)
    pyautogui.PAUSE = 0.2
    pyautogui.click(1795, 235)
    pyautogui.press('right')


def remove_old_slide_names():
    time.sleep(0.2)
    pyautogui.press('down')
    pyautogui.press('down')
    with pyautogui.hold('shift'):
        pyautogui.press('end')
    pyautogui.press('backspace')


# Определение горячей клавиши
def test():
    pyautogui.hotkey('shift', 'left')
    # pyautogui.doubleClick(1503, 435)
    # for i in [(1499, 242), (1688, 293), (1487, 448), (1487, 448), (1797, 238)]:
    pyautogui.click(1499, 242)
    pyautogui.click(1688, 293)
    pyautogui.doubleClick(1487, 448)
    pyautogui.write('8.5')
    pyautogui.click(1797, 238)
    pyautogui.press('right')


def change_layout(text):
    # Словари для смены раскладки
    eng_to_rus = {
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г',
        'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы',
        'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д',
        ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и',
        'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.',
        'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г',
        'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ', 'A': 'Ф', 'S': 'Ы',
        'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д',
        ':': 'Ж', '"': 'Э', 'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И',
        'N': 'Т', 'M': 'Ь', '<': 'Б', '>': 'Ю', '?': ','
    }

    rus_to_eng = {v: k for k, v in eng_to_rus.items()}  # инвертируем словарь

    # Определение раскладки по первому символу
    if text[0] in eng_to_rus:
        translator = eng_to_rus
    else:
        translator = rus_to_eng

    return ''.join([translator.get(i, i) for i in text])


def replace_text():
    time.sleep(0.1)

    # Копируем выделенный текст
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)

    # Получаем текст из буфера обмена
    copied_text = pyperclip.paste()

    # Меняем раскладку
    new_text = change_layout(copied_text)

    # Вставляем текст обратно
    pyperclip.copy(new_text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    pyautogui.hotkey('alt', 'shift')

    # Даем небольшой таймаут, чтобы избежать многократного срабатывания
    time.sleep(0.5)


hotkey = keyboard.GlobalHotKeys({
    '<ctrl>+<shift>': replace_text,
    '<alt>+8': remove_old_slide_names
})


def caller(key):
    if key == keyboard.Key.pause:
        x, y = pyautogui.position()
        make_border()
        time.sleep(0.5)
        make_8cm_wide()
        pyautogui.moveTo(x, y)
    if key == keyboard.Key.scroll_lock:
        copy_slide_to_doc()
    if key == keyboard.Key.f9:
        copy_slide_text()
    if key == keyboard.Key.ctrl_r:
        remove_old_slide_names()


# - pause - f9   - scroll_lock

l = keyboard.Listener(on_press=caller)
# hotkey.run()
l.run()
# Запуск слушателя
