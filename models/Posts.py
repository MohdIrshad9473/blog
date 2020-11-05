from View import db


class Posts(db.Model):
#  sno,tittle,content,date
    sno = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(100),      nullable=False)
    Description = db.Column(db.String(500),  nullable=False)
    date = db.Column(db.String(100),  nullable=True)