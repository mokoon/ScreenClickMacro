import pyautogui
import time

time.sleep(1)
print("프로그램 실행")
# 미리 만들어놓은 이미지가 화면상 어느 위치에 있는지 찾기
while True:
    print(pyautogui.position())

