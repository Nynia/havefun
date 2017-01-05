from app import db

class Package(db.Model):
    __tablename__ = 'packageinfo'
    packageid = db.Column(db.String(255), primary_key=True)
    packagename = db.Column(db.String(255))
    type = db.Column(db.String(1))
    price = db.Column(db.Integer)
    description = db.Column(db.String(255))
    createtime = db.Column(db.DateTime)
    modifiedtime = db.Column(db.DateTime)

    def to_json(self):
        json_post = {
            'packageid': self.packageid,
            'packagename': self.packagename,
            'type': self.type,
            'price':self.price,
            'description': self.description,
            'createtime': self.createtime,
            'modifiedtime': self.modifiedtime
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        pass

    def __repr__(self):
        return '<Package %r>' % self.packagename

class Comic(db.Model):
    __tablename__ = 'comicinfo'
    comicid = db.Column(db.String(15), primary_key=True)
    packageid = db.Column(db.String(15))
    comicname = db.Column(db.String(50))
    brief = db.Column(db.String(255))
    author = db.Column(db.String(50))
    category = db.Column(db.String(30))
    hits = db.Column(db.Integer)
    state = db.Column(db.String(1))
    cover = db.Column(db.String(255))
    curchapter = db.Column(db.Integer)
    freechapter = db.Column(db.Integer)
    createtime = db.Column(db.DateTime)
    recentupdatetime = db.Column(db.DateTime)
    modifiedtime = db.Column(db.DateTime)

    def to_json(self):
        json_post = {
            'comicid':self.comicid,
            'packageid':self.packageid,
            'comicname':self.comicname,
            'brief':self.brief,
            'author':self.author,
            'category':self.category,
            'hits':self.hits,
            'state':self.state,
            'cover':self.cover,
            'curchapter':self.curchapter,
            'freechapter':self.freechapter,
            'createtime':self.createtime,
            'modifiedtime':self.modifiedtime,
            'recentupdatetime':self.recentupdatetime
        }
        return json_post
    def __repr__(self):
        return '<Comic %r>' % self.comicname

class User(db.Model):
    __tablename__ = 'userinfo'
    userid = db.Column(db.Integer, primary_key=True)
    phonenum = db.Column(db.String(20))
    nickname = db.Column(db.String(200))
    createtime = db.Column(db.DateTime)
    password = db.Column(db.String(50))
    integral = db.Column(db.Integer)

    def to_json(self):
        json_post = {
            'userid':self.userid,
            'phonenum':self.phonenum,
            'nickname':self.nickname,
            'createtime':self.createtime,
            'password':self.password,
            'integral':self.integral
        }
        return json_post

    def __repr__(self):
        return '<User %r>' % self.phonenum
