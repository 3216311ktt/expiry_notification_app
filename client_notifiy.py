import requests
import time
from plyer import notification
import platform
import os

SERVER_URL = "http://127.0.0.1:5000/notifications"

# # 音を鳴らす（5分ごとに分岐）
# def play_sound():
#     if platform.system() == "Windows":
#         import winsound
#         winsound.Beep(1000, 500)
#     elif platform.system() == "Darwin":  # Mac
#         os.system('afplay /System/Library/Sounds/Ping.aiff')
#     else: # Linux
#         os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')


# # 通知表示
# def show_notification(title, message):
#     notification.notify(
#         title=title,
#         message=message,
#         timeout=10
#     )

def play_sound():
    os.system('afplay /System/Library/Sounds/Ping.aiff')

def show_notification(title, message):
    os.system(f'''
    osascript -e 'display notification "{message}" with title "{title}"'
    ''')

# メインループ
def main():
    seen_ids = set()

    while True:
        try:
            res = requests.get(SERVER_URL)
            data = res.json()

            for n in data:
                if n["id"] not in seen_ids:
                    show_notification("資格更新通知", n["message"])
                    play_sound()
                    seen_ids.add(n["id"])

        except Exception as e:
            print("エラー:", e)

        time.sleep(10)  # 10秒ごとにチェック


if __name__ == "__main__":
    main()