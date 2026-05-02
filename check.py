from models import db, License,  Notification
from datetime import date
from app import app

with app.app_context():
    today = date.today()

    licenses = License.query.all()

    for l in licenses:
        days_left = (l.expiry_date - today).days

        if days_left <= l.notify_days_before and not l.notified_flag:
            msg = f"{l.employee_name} の {l.license_name} が期限間近（残り{days_left}日)"

            n = Notification(message=msg)
            db.session.add(n)

            l.notified_flag = True

    db.session.commit()