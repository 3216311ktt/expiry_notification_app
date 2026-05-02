from flask import Flask, jsonify
from models import db, Notification

app = Flask(__name__)
app.json.ensure_ascii = False

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/notifications")
def get_notifications():
    notifs = Notification.query.filter_by(is_read=False).all()

    return jsonify([
        {
            "id": n.id,
            "message": n.message,
            "time": n.created_at
        } for n in notifs
    ])


@app.route("/read/<int:id>")
def read(id):
    n = Notification.query.get(id)
    if n:
        n.is_read = True
        db.session.commit()
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)