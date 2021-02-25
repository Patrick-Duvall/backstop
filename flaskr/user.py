from flask_login import UserMixin

from flaskr.db import get_db


class User(UserMixin):
    def __init__(self, id_, username, email):
        self.id = id_
        self.username = username
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], username=user[1], email=user[2]
        )
        return user

    @staticmethod
    def create(id_, name, email):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, username, email) "
            "VALUES (?, ?, ?)",
            (id_, name, email,),
        )
        db.commit()
