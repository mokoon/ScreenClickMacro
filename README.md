# ScreenClickMacro
## 스크린 클릭 매크로

파이썬 기반 pyautogui 로 작동
화면 분석은 open cv

## 사용방법
1. 프로그램 실행
2. 이미지 변경 버튼으로 자신화면의 이미지 캡처
3. 매크로 실행 버튼으로 실행


~~기본 키는 - 키로 지정해두고 사용 예정 (수정 가능)~~
ui 버튼 클릭으로 매크로 동작 결정

*필수사항
실행파일(exe)가 있는 폴더에 icon폴더와 img폴더를 만들어서 해당 폴더에 이미지와 아이콘을 넣어서 사용할 것


## 실행파일 뽑는법
ScreenMacro.py
폴더에서 
pyinstaller -w -F ScreenMacro.py

pyinstaller -w -F --icon=icon\caron.ico lim1bus.py

## 필요한 외부 라이브러리
pip install opencv-python numpy pyautogui keyboard pillow

코드 수정시 고려사항
매크로는 원하는만큼 원하는 동작으로 추가해서 사용
멀티스레싱으로 구현해두었지만 각 동작의 연산량이 크게 늘어난다면 멀티 프로세싱으로 구현하는것도 고려해볼것

가급적이면 직접 코드를 수정하고 필요한 이미지를 자신의 환경에서 딴 뒤에 프로그램을 exe로 직접 따는걸 추천

# exe 파일 생성 이후 windowsdefender에서 트로이목마로 검진할수도 있음
해당 경우 실행 파일 검진 예외 설정이 필요함.
