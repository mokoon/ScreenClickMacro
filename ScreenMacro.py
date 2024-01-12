import cv2
import numpy as np
import pyautogui
import keyboard
from PIL import ImageGrab
import time
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
import threading
import random

#일반 매크로

#화면 처리
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

#멀티스레싱용
def run_macro_in_thread(macro_function):
    macro_thread = threading.Thread(target=macro_function)
    macro_thread.start()

# 화면 크롭용 전역 변수
cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
cropped = False

# 화면 크롭용 함수
def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, cropped

    # 마우스 왼쪽 버튼 눌렀을 때
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    # 마우스 이동, 크롭 영역 그리기
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            x_end, y_end = x, y

    # 마우스 왼쪽 버튼 땠을 때
    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        cropped = True  # 크롭 끝, 이미지 저장 및 창 닫기
# 크롭된 이미지 저장 함수
def save_cropped_image(crop_img):
    root = tk.Tk()
    root.withdraw()  # Tk 창을 숨김
    file_path = filedialog.asksaveasfilename(
        initialdir="img/",
        title="Save as",
        filetypes=(("PNG files", "*.png"), ("All files", "*.*")),
        defaultextension=".png"
    )

    if file_path:  # 사용자가 파일명을 입력하고 "저장"을 눌렀을 때
        cv2.imwrite(file_path, crop_img)
    root.destroy()

#매크로
def macro(image):
    position = find_image_on_screen(image)
    if position:
        # 현재 마우스 위치 저장
        current_mouse_x, current_mouse_y = pyautogui.position()

        # 이미지 크기에 따른 오프셋 계산
        template = cv2.imread(image, 0)
        w, h = template.shape[::-1]
        random_offset_x = random.randint(-int(w * 0.5), int(w * 0.5))
        random_offset_y = random.randint(-int(h * 0.5), int(h * 0.5))

        new_position = (position[0] + random_offset_x, position[1] + random_offset_y)

        print("이미지 찾음:", new_position)
        pyautogui.click(new_position)

        # 마우스를 원래 위치로 이동
        pyautogui.moveTo(current_mouse_x, current_mouse_y)
    else:
        print("이미지를 찾을 수 없음")

    random_delay = random.uniform(0, 0.5)
    time.sleep(0.1 + random_delay)

# 이미지가 화면에 나타나는지 확인하는 함수
def Img_appear(image):
    position = find_image_on_screen(image)
    return position is not None

#닫힐 때
def on_closing():
    global running, macro1_running
    running = False
    macro1_running = False
    root.destroy()
    print("프로그램 종료")

#창 생성
def create_tray_icon():
    global root, macro1_state_label, macro2_state_label, image_change_label, daily_q_label
    root = tk.Tk()
    root.title("매크로 프로그램")
    #root.iconbitmap('icon\M_icon.ico') #아이콘 설정

    menu = Menu(root, tearoff=0)
    menu.add_command(label="종료", command=on_closing)
    root.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))
    # macro1 관련 UI 구성 예시
    macro1_state_label = tk.Label(root, text="전투 매크로 준비 상태")
    macro1_state_label.pack()

    macro1_button = tk.Button(root, text="승률 버튼", command=button1_action)
    macro1_button.pack()

    # 이미지 변경 관련 UI 구성
    image_change_label = tk.Label(root, text="찾을 이미지 변경")
    image_change_label.pack()

    image_change_button = tk.Button(root, text="이미지 변경", command=image_change_action)
    image_change_button.pack()

    # 창 닫기 이벤트 핸들러 설정
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

#매크로 1번째 버튼 이벤트
def button1_action():
    global macro1_running, macro1_state_label
    macro1_running = not macro1_running
    if macro1_running:
        macro1_state_label.config(text="전투 매크로 실행 상태")
    else:
        macro1_state_label.config(text="전투 매크로 중지 상태")


#이미지 변경 버튼 이벤트
def image_change_action():
    global x_start, y_start, x_end, y_end, cropping, cropped

    # 스크린샷 캡쳐
    screen = np.array(ImageGrab.grab())
    screen_copy = screen.copy()

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)

    while True:
        i = screen_copy.copy()

        if cropping:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)

        cv2.imshow("image", i)

        # 'q'를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q') or cropped:
            break

    if cropped and x_start != x_end and y_start != y_end:
        if x_start > x_end: # 좌표 정렬
            x_start, x_end = x_end, x_start
        if y_start > y_end:
            y_start, y_end = y_end, y_start

        # 선택 영역 저장
        crop_img = screen[y_start:y_end, x_start:x_end]
        save_cropped_image(crop_img)  # 사용자가 파일을 저장할 수 있도록 함

    cv2.destroyAllWindows()

#승률 딸깍
def BattleM():
    # 매크로 실행
    macro('img\winrate.png')
    macro('img\winr.png')
    time.sleep(2)

# 전투 중 인격 사망시 루틴
def DefeatM():
    image = 'img\winrate.png'  # 인격 사망 이미지 경로
    # if Img_appear(image):
    #     macro(image) #설정창
    #     macro(image) #전투 나가기
    #     macro(image) #전투 다시하기
    time.sleep(2)


# 매크로 실행 상태
macro1_running = False


def main():
    global macro1_running, running, macro1_state_label
    running = True

    tray_thread = threading.Thread(target=create_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()

    while running:
        
        # if keyboard.is_pressed('-'):
        #     macro1_running = not macro1_running
        #     if macro1_running:
        #         macro1_state_label.config(text="매크로 실행 상태")
        #     else:
        #         macro1_state_label.config(text="매크로 중지 상태")
        #     time.sleep(1)  # 키 반복 방지 대기 시간
        #     keyboard.wait('-')

        if macro1_running:
            run_macro_in_thread(BattleM())  # 스레드에서 매크로 실행
            run_macro_in_thread(DefeatM())  # 스레드에서 매크로 실행

if __name__ == "__main__":
    main()