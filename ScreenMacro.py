import cv2
import numpy as np
import pyautogui
import keyboard
from PIL import ImageGrab
import time

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

def main():
    running = False

    while True:
        # 특정 키 ('s' 예시)를 누르면 매크로 시작/종료
        if keyboard.is_pressed('-'):
            running = not running
            if running:
                print("매크로 시작")
            else:
                print("매크로 종료")
                time.sleep(2)
            keyboard.wait('-')

        if running:
            position = find_image_on_screen('img\8.png') # 이미지 경로
            if position:
                print("이미지 찾음:", position)
                pyautogui.click(position)
            else:
                print("이미지를 찾을 수 없음")
            time.sleep(0.5)

if __name__ == "__main__":
    main()