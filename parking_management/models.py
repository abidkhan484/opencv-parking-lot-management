from parking_management import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class CameraDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_url = db.Column(db.String(80), unique=True, nullable=False)
    coordinates = db.Column(db.String(80), unique=True, nullable=True)

    def __repr__(self):
        return f'CameraId {self.id}'
