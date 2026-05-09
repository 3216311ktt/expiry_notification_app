from flask import Flask, jsonify, render_template, request, redirect
from models import db, Notification, NotificationRead, License
from datetime import date, datetime

app = Flask(__name__)
# app.json.ensure_ascii = False

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():

    client = request.args.get("client", "common")

    if client:
        notifs = Notification.query.all()

        for n in notifs:
            exists = NotificationRead.query.filter_by(
                notification_id=n.id,
                client_name=client
            ).first()

            if not exists:
                r = NotificationRead(
                    notification_id=n.id, # type: ignore
                    client_name=client # type: ignore
                )
                db.session.add(r)

        db.session.commit()

    licenses = License.query.all()

    today = date.today()

    alert_licenses = []
    normal_licenses = []

    for l in licenses:

        days_left = (l.expiry_date - today).days

        if days_left <= l.notify_days_before:
            alert_licenses.append(l)
        else:
            normal_licenses.append(l)

    return render_template(
        "index.html",
        alert_licenses=alert_licenses,
        normal_licenses=normal_licenses,    
        today=today
    )


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    license = License.query.get(id)

    if request.method == "POST":

        license.employee_name = request.form["employee_name"] # type: ignore
        license.license_name = request.form["license_name"] # type: ignore
        license.expiry_date = datetime.strptime(request.form["expiry_date"], "%Y-%m-%d").date() # type: ignore
        license.notify_days_before = int(request.form["notify_days_before"]) # type: ignore
        license.notified_flag = False # type: ignore

        Notification.query.filter_by(
            target=f"license:{license.id}" # type: ignore
        ).delete()

        db.session.commit()

        return redirect("/")
    
    return render_template("edit.html", license=license)

@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        license = License()

        license.employee_name = request.form["employee_name"]
        license.license_name = request.form["license_name"]

        license.expiry_date = datetime.strptime(request.form["expiry_date"], "%Y-%m-%d").date()
        license.notify_days_before = int(request.form["notify_days_before"])

        db.session.add(license)
        db.session.commit()

        return redirect("/")
    
    return render_template("add.html")


@app.route("/notifications")
def get_notifications():

    client = request.args.get("client", "common")

    notifs = Notification.query.order_by(Notification.created_at.desc()).all()

    unread = []

    for n in notifs:
        already_read = NotificationRead.query.filter_by(
            notification_id=n.id,
            client_name=client
        ).first()

        if not already_read:
            unread.append({
                "id": n.id,
                "message": n.message,
                "time": n.created_at
            })

    return jsonify(unread)


@app.route("/read/<int:id>")
def read(id):

    client = request.args.get("client", "common")

    exists = NotificationRead.query.filter_by(
        notification_id=id,
        client_name=client
    ).first()

    if not exists:
        r = NotificationRead(
            notification_id=id, # type: ignore
            client_name=client # type: ignore
        )
        db.session.add(r)
        db.session.commit()
        
    return {"status": "ok"}




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)