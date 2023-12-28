import cv2
import numpy as np
import pyautogui
import keyboard
from PIL import ImageGrab
import time
import tkinter as tk
from tkinter import Menu
import threading



def find_image_on_screen(image_path, confidence=0.8):
    # 화면 캡쳐
    screen = np.array(ImageGrab.grab())
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # 이미지 로드
    template = cv2.imread(image_path, 0)
    w, h = template.shape[::-1]

    # 이미지 매칭
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)

    for pt in zip(*loc[::-1]):
        return pt[0] + w//2, pt[1] + h//2

    return None

def macro(image):
    position = find_image_on_screen(image)
    if position:
        print("이미지 찾음:", position)
        pyautogui.click(position)
    else:
        print("이미지를 찾을 수 없음")
    time.sleep(0.5)

def on_closing():
    global running, macro_running
    running = False
    macro_running = False
    root.destroy()
    print("프로그램 종료")

def create_tray_icon():
    global root, macro_state_label
    root = tk.Tk()
    root.title("매크로 프로그램")
    root.iconbitmap('icon\M_icon.ico')

    menu = Menu(root, tearoff=0)
    menu.add_command(label="종료", command=on_closing)
    root.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))

    macro_state_label = tk.Label(root, text="매크로 준비 상태")
    macro_state_label.pack()

    # 창 닫기 이벤트 핸들러 설정
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


# 매크로 실행 상태
macro_running = False

def main():
    global macro_running, running, macro_state_label
    running = True

    tray_thread = threading.Thread(target=create_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()

    while running:
        if keyboard.is_pressed('-'):
            macro_running = not macro_running
            if macro_running:
                macro_state_label.config(text="매크로 실행 상태")
            else:
                macro_state_label.config(text="매크로 중지 상태")
            time.sleep(1)  # 키 반복 방지 대기 시간
            keyboard.wait('-')

        if macro_running:
            # 매크로 실행
            macro('img\winrate.png')
            macro('img\winr.png')
            time.sleep(2)

if __name__ == "__main__":
    main()