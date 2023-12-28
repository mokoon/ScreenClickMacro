# ScreenClickMacro
스크린 클릭 매크로

파이썬 기반 pyautogui 로 작동
화면 분석은 open cv

1. 프로그램 실행
2. 지정한 키 입력으로 매크로 실행 준비
3. 한번 더 입력 시 매크로 동작
4. 동작 중 해당 키 입력시 동작 종료 준비 상태로 돌아감

기본 키는 - 키로 지정해두고 사용 예정 (수정 가능)

이미지는 직접 연결 해줘야됨 개인 사용용으로 작업하는거라 GUI나 매크로 순서 할당 디테일한 딜레이등 편의성 기능을 추가할지는 미지수

*필수사항
실행파일(exe)가 있는 폴더에 icon폴더와 img폴더를 만들어서 해당 폴더에 이미지와 아이콘을 넣어서 사용할 것


실행파일 뽑는법
ScreenMacro.py
폴더에서 
pyinstaller -w -F ScreenMacro.py

필요한 외부 라이브러리
pip install opencv-python numpy pyautogui keyboard pillow

코드 수정시 고려사항
이미지 명, 이미지 주소 필히 확인
매크로는 원하는만큼 추가해서 사용 가능
macro함수 내부 이미지 좌표 클릭 위치 랜덤값 가중치는 이미지 크기에 맞춰서 설정해줘야됨
