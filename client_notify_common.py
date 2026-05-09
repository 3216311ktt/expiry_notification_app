import requests
import time
from plyer import notification
import platform
import os
import webbrowser
from datetime import datetime, timedelta
from win10toast_click import ToastNotifier

toaster = ToastNotifier()

SERVER_HOST = "KTTminiPC"
CLIENT_NAME = "common"
SERVER_URL = f"http://{SERVER_HOST}/notifications?client={CLIENT_NAME}"

def open_index():
    webbrowser.open(f"http://{SERVER_HOST}/?client={CLIENT_NAME}")
    return 0

# 音を鳴らす（5分ごとに分岐）
def play_sound():

    for _ in range(2):

        if platform.system() == "Windows":
            import winsound
            winsound.PlaySound(
                "sounds/093518ec.wav",
                winsound.SND_ALIAS
        )
        elif platform.system() == "Darwin":  # Mac
            os.system('afplay /System/Library/Sounds/Ping.aiff')
        else: # Linux
            os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')

        time.sleep(0.1)

# 通知表示
def show_notification(title, message):
    if platform.system() == "Windows":
        toaster.show_toast(
            title,
            message,
            duration=10,
            threaded=True,
            callback_on_click=open_index   
        ) # type: ignore

        time.sleep(12)

    elif platform.system() == "Darwin":  # Mac
        os.system(f'''
        osascript -e 'display notification "{message}" with title "{title}"'
        ''')

    else:
        print(f"{title}: {message}")

# メインループ
def main():

    last_notified = {}

    while True:
        try:
            res = requests.get(SERVER_URL, timeout=3)
            data = res.json()

            now = datetime.now()

            for n in data:

                notify_id = n["id"]

                should_notify = False

                if notify_id not in last_notified:
                    should_notify = True

                else:
                    elapsed = (
                        now - last_notified[notify_id]
                    )

                    if elapsed >= timedelta(minutes=10):
                        should_notify = True

                if should_notify:

                    show_notification(
                        "資格更新通知",
                        n["message"]
                    )

                    play_sound()

                    last_notified[notify_id] = now

        except Exception as e:
            print("エラー:", e)

        time.sleep(10)  # 10秒ごとにチェック


if __name__ == "__main__":
    main()