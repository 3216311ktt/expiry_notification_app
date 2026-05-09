from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class License(db.Model):
    __tablename__ = 'licenses'

    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(100))
    license_name = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)
    notify_days_before = db.Column(db.Integer)
    notified_flag = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer,primary_key=True)
    message = db.Column(db.String(255))
    target = db.Column(db.String(50), default="all")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reads = db.relationship(
        "NotificationRead",
        backref= "notification",
        lazy=True,
        cascade="all, delete-orphan"
    )

class NotificationRead(db.Model):
    __tablename__ = "notification_reads"

    id = db.Column(db.Integer, primary_key=True)

    notification_id = db.Column(
        db.Integer,
        db.ForeignKey("notifications.id"),
        nullable=False
    )

    client_name = db.Column(db.String(50), nullable=False)
    read_at = db.Column(db.DateTime, default=datetime.utcnow)
