from flask import Flask, jsonify
from models import db, Notification

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/notifications")
def get_notifications():
    notifs = Notification.query.filter_by(is_read=False).all()

    result = []
    for n in notifs:
        result.append({
            "id": n.id,
            "message": n.message,
            "time": n.created_at
        })

    return jsonify(result)

@app.route("/read/<int:id>")
def read(id):
    n = Notification.query.get(id)
    n.is_read = True
    db.session.commit()

    return {"status": "ok"}