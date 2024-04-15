from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    User class for each registered user
    """

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    debtors = db.relationship('Debtor', backref='user', lazy=True)


class Debtor(db.Model):
    """
    A debtor table corresponding to each user
    """

    __tablename__ = 'debtor'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    purchase = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Float)
    collected_on = db.Column(db.Date)
    settled_on = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
