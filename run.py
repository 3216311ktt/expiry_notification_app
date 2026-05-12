import time
from datetime import datetime

from check import run_check

last_run_date = None

while True:

    now = datetime.now()

    # 平日だけ
    if now.weekday() < 5:

        # 9:02
        if now.hour == 9 and now.minute == 2:

            today = now.date()

            if last_run_date != today:

                print("run_check start")

                run_check()

                last_run_date = today

                print("run_check done")

    time.sleep(30)