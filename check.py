from models import db, License,  Notification
from datetime import date
from app import app

def run_check():
    with app.app_context():
        today = date.today()
        licenses = License.query.all()

        for l in licenses:
            if not l.expiry_date:
                continue

            days_left = (l.expiry_date - today).days

            if days_left <= l.notify_days_before and not l.notified_flag:

                target_key = f"license_{l.id}"

                exists = Notification.query.filter_by(
                    target=target_key
                ).first()

                if not exists:
                    msg = (
                        f"{l.employee_name} の "
                        f"{l.license_name} が期限間近（残り{days_left}日）"
                    )

            
                    n = Notification(
                        message=msg, # type: ignore
                        target=target_key # type: ignore
                    )
                    

                    db.session.add(n)

                l.notified_flag = True
    
        db.session.commit()
        

if __name__ == "__main__":
    run_check()