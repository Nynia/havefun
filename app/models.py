from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask import current_app, request, url_for
from flask_login import UserMixin
class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer,primary_key=True)
    productid = db.Column(db.String(255))
    productname = db.Column(db.String(255))
    type = db.Column(db.String(1))
    price = db.Column(db.Integer)
    description = db.Column(db.String(255))
    createtime = db.Column(db.String(14))
    modifiedtime = db.Column(db.String(14))
    img = db.Column(db.String(255))
    spid = db.Column(db.String(15))
    chargeid = db.Column(db.String(10))
    secret = db.Column(db.String(30))


    def to_json(self):
        json_post = {
            'id':self.id,
            'productid': self.productid,
            'productname': self.productname,
            'type': self.type,
            'price':self.price,
            'description': self.description,
            'createtime': self.createtime,
            'modifiedtime': self.modifiedtime,
            'img':self.img,
            'spid':self.spid,
            'chargeid':self.chargeid,
            'secret':self.secret
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        pass

    def __repr__(self):
        return '<Package %r>' % self.packagename

class Comic(db.Model):
    __tablename__ = 'comic'
    id = db.Column(db.Integer, primary_key=True)
    packageid = db.Column(db.Integer)
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
            'id':self.id,
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

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phonenum = db.Column(db.String(20))
    nickname = db.Column(db.String(200))
    createtime = db.Column(db.String(14))
    password_hash = db.Column(db.String(128))
    integral = db.Column(db.Integer)

    def to_json(self):
        json_post = {
            'id':self.id,
            'phonenum':self.phonenum,
            'nickname':self.nickname,
            'createtime':self.createtime,
            'integral':self.integral
        }
        return json_post

    def __repr__(self):
        return '<User %r>' % self.phonenum

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    column1 = db.Column(db.String(10))
    column2 = db.Column(db.DateTime)


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    packageid = db.Column(db.Integer)
    name = db.Column(db.String(255))
    img_icon = db.Column(db.String(255))
    type = db.Column(db.String(1))
    url = db.Column(db.String(255))
    category = db.Column(db.String(20))
    star = db.Column(db.Integer)
    brief = db.Column(db.String(255))
    size = db.Column(db.String(20))
    createtime = db.Column(db.String(14))

    img_screenshot_1 = db.Column(db.String(255))
    img_screenshot_2 = db.Column(db.String(255))
    img_screenshot_3 = db.Column(db.String(255))
    img_screenshot_4 = db.Column(db.String(255))
    img_screenshot_5 = db.Column(db.String(255))
    img_screenshot_6 = db.Column(db.String(255))

    def __repr__(self):
        return '<Game %r>' % self.name

    def to_json(self):
        json_post = {
            'id':self.id,
            'packageid':self.packageid,
            'name':self.name,
            'img_icon':self.img_icon,
            'type':self.type,
            'url':self.url,
            'category':self.category,
            'star':self.star,
            'brief':self.brief,
            'size':self.size,
            'createtime':self.createtime,
            'img_screenshot_1':self.img_screenshot_1,
            'img_screenshot_2': self.img_screenshot_2,
            'img_screenshot_3': self.img_screenshot_3,
            'img_screenshot_4': self.img_screenshot_4,
            'img_screenshot_5': self.img_screenshot_5,
            'img_screenshot_6': self.img_screenshot_6,
        }
        return json_post

class OrderRelation(db.Model):
    __tablename__ = 'orderrelation'
    id = db.Column(db.Integer,primary_key=True)
    productid = db.Column(db.String(21))
    phonenum = db.Column(db.String(11))
    status = db.Column(db.String(1))
    starttime = db.Column(db.String(14))
    endtime = db.Column(db.String(14))

    def __repr__(self):
        return '<OrderRelation %r>' % self.productid

    def to_json(self):
        json_post = {
            'id':self.id,
            'productnid':self.productid,
            'phonenum':self.phonenum,
            'status':self.status,
            'starttime':self.starttime,
            'endtime':self.endtime
        }
        return json_post

class OrderHistroy(db.Model):
    __tablename__ = 'orderrecord'
    id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.String(21))
    phonenum = db.Column(db.String(11))
    action = db.Column(db.String(1))
    createtime = db.Column(db.String(14))

    def __repr__(self):
        return '<OrderHistroy %r>' % self.phonenum

    def to_json(self):
        json_post = {
            'id':self.id,
            'productid':self.productid,
            'phonenum':self.phonenum,
            'action':self.action,
            'createtime':self.createtime
        }
        return json_post



















