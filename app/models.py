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
        return '<Package %r>' % self.productname

class Comic(db.Model):
    __tablename__ = 'comic'
    id = db.Column(db.Integer, primary_key=True)
    packageid = db.Column(db.Integer)
    comicname = db.Column(db.String(50))
    brief = db.Column(db.String(255))
    author = db.Column(db.String(50))
    category = db.Column(db.String(30))
    hits = db.Column(db.String(10))
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
    ordertime = db.Column(db.String(14))
    canceltime = db.Column(db.String(14))

    def __repr__(self):
        return '<OrderRelation %r>' % self.productid

    def to_json(self):
        json_post = {
            'id':self.id,
            'productid':self.productid,
            'phonenum':self.phonenum,
            'status':self.status,
            'ordertime':self.ordertime,
            'canceltime':self.canceltime
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

class Reading(db.Model):
    __tablename__ = 'reading'
    id = db.Column(db.Integer,primary_key=True)
    bookid = db.Column(db.String(30))
    packageid = db.Column(db.Integer)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    state = db.Column(db.String(1))
    hits = db.Column(db.Integer)
    brief = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    curchapter = db.Column(db.Integer)
    freechapter = db.Column(db.Integer)
    createtime = db.Column(db.String(14))
    recentupdatetime = db.Column(db.String(14))
    modifiedtime = db.Column(db.String(14))

    category = db.Column(db.String(255))

    def __repr__(self):
        return '<Reading %r>' % self.name

    def to_json(self):
        json_post = {
            'id':self.id,
            'bookid':self.bookid,
            'packageid':self.packageid,
            'name':self.name,
            'author':self.author,
            'state':self.state,
            'hits':self.hits,
            'brief':self.brief,
            'category':self.category,
            'cover':self.cover,
            'curchapter':self.curchapter,
            'freechapter':self.freechapter,
            'createtime':self.createtime,
            'recentupdatetime':self.recentupdatetime,
            'modifiedtime':self.modifiedtime
        }
        return json_post

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True)
    chapterid = db.Column(db.Integer)
    chaptername = db.Column(db.String(255))
    bookid = db.Column(db.String(30))
    content = db.Column(db.TEXT)
    createtime = db.Column(db.String(14))

    def __repr__(self):
        return '<Chapter %r>' % self.chapterid

    def to_json(self):
        json_post = {
            'id':self.id,
            'chapterid':self.chapterid,
            'chaptername':self.chaptername,
            'bookid':self.bookid,
            'content':self.bookid,
            'createtime':self.createtime
        }
        return json_post

class History(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(1))
    cid = db.Column(db.Integer)
    chapter = db.Column(db.Integer)
    uid = db.Column(db.String(15))
    createtime = db.Column(db.String(14))
    updatetime = db.Column(db.String(14))

    def __repr__(self):
        return '<History %r>' % self.uid

    def to_json(self):
        json_post = {
            'id':self.id,
            'type':self.type,
            'cid':self.cid,
            'chapter':self.chapter,
            'uid':self.uid,
            'createtime':self.createtime,
            'updatetiem':self.updatetime
        }
        return json_post














