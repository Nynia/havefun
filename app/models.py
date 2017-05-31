from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask import current_app, request, url_for
from flask_login import UserMixin


class Package(db.Model):
    __tablename__ = 'package'
    productid = db.Column(db.String(255), primary_key=True)
    productname = db.Column(db.String(255))
    type = db.Column(db.String(1))
    price = db.Column(db.Integer)
    description = db.Column(db.String(255))
    createtime = db.Column(db.String(14))
    modifiedtime = db.Column(db.String(14))
    img = db.Column(db.String(255))
    bannerimg = db.Column(db.String(255))
    spid = db.Column(db.String(15))
    chargeid = db.Column(db.String(10))
    secret = db.Column(db.String(30))
    img2 = db.Column(db.String(30))
    copyright = db.Column(db.String(255))
    def to_json(self):
        json_post = {
            'productid': self.productid,
            'productname': self.productname,
            'type': self.type,
            'price': self.price,
            'description': self.description,
            'createtime': self.createtime,
            'modifiedtime': self.modifiedtime,
            'img': self.img,
            'bannerimg': self.bannerimg,
            'spid': self.spid,
            'chargeid': self.chargeid,
            'secret': self.secret,
            'img2': self.img2,
            'copyright':self.copyright
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
    packageid = db.Column(db.String(21))
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
            'id': self.id,
            'packageid': self.packageid,
            'comicname': self.comicname,
            'brief': self.brief,
            'author': self.author,
            'category': self.category,
            'hits': self.hits,
            'state': self.state,
            'cover': self.cover,
            'curchapter': self.curchapter,
            'freechapter': self.freechapter,
            'createtime': self.createtime,
            'modifiedtime': self.modifiedtime,
            'recentupdatetime': self.recentupdatetime
        }
        return json_post

    def __repr__(self):
        return '<Comic %r>' % self.comicname


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phonenum = db.Column(db.String(20))
    nickname = db.Column(db.String(200))
    createtime = db.Column(db.String(14))
    password_hash = db.Column(db.String(128))
    integral = db.Column(db.Integer)
    lastcheckin = db.Column(db.String(14))
    continus_checkin = db.Column(db.Integer)
    lastlogin = db.Column(db.String(14))
    continus_login = db.Column(db.Integer)

    def to_json(self):
        json_post = {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'createtime': self.createtime,
            'integral': self.integral,
            'lastcheckin':self.lastcheckin,
            'continus_checkin':self.continus_checkin,
            'lastlogin':self.lastlogin,
            'continus_login':self.continus_login
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


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    packageid = db.Column(db.String(21))
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
            'id': self.id,
            'packageid': self.packageid,
            'name': self.name,
            'img_icon': self.img_icon,
            'type': self.type,
            'url': self.url,
            'category': self.category,
            'star': self.star,
            'brief': self.brief,
            'size': self.size,
            'createtime': self.createtime,
            'img_screenshot_1': self.img_screenshot_1,
            'img_screenshot_2': self.img_screenshot_2,
            'img_screenshot_3': self.img_screenshot_3,
            'img_screenshot_4': self.img_screenshot_4,
            'img_screenshot_5': self.img_screenshot_5,
            'img_screenshot_6': self.img_screenshot_6,
        }
        return json_post


class OrderRelation(db.Model):
    __tablename__ = 'orderrelation'
    id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.String(21))
    phonenum = db.Column(db.String(11))
    status = db.Column(db.String(1))
    ordertime = db.Column(db.String(14))
    canceltime = db.Column(db.String(14))

    def __repr__(self):
        return '<OrderRelation %r>' % self.productid

    def to_json(self):
        json_post = {
            'id': self.id,
            'productid': self.productid,
            'phonenum': self.phonenum,
            'status': self.status,
            'ordertime': self.ordertime,
            'canceltime': self.canceltime
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
            'id': self.id,
            'productid': self.productid,
            'phonenum': self.phonenum,
            'action': self.action,
            'createtime': self.createtime
        }
        return json_post


class Reading(db.Model):
    __tablename__ = 'reading'
    id = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.String(30))
    packageid = db.Column(db.String(21))
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
            'id': self.id,
            'bookid': self.bookid,
            'packageid': self.packageid,
            'name': self.name,
            'author': self.author,
            'state': self.state,
            'hits': self.hits,
            'brief': self.brief,
            'category': self.category,
            'cover': self.cover,
            'curchapter': self.curchapter,
            'freechapter': self.freechapter,
            'createtime': self.createtime,
            'recentupdatetime': self.recentupdatetime,
            'modifiedtime': self.modifiedtime
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
            'id': self.id,
            'chapterid': self.chapterid,
            'chaptername': self.chaptername,
            'bookid': self.bookid,
            'content': self.bookid,
            'createtime': self.createtime
        }
        return json_post


class ViewInfo(db.Model):
    __tablename__ = 'view_info'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(1))
    comicid = db.Column(db.Integer)
    recentchapter = db.Column(db.Integer)
    userid = db.Column(db.String(15))
    createtime = db.Column(db.String(14))
    updatetime = db.Column(db.String(14))

    def __repr__(self):
        return '<History %r>' % self.uid

    def to_json(self):
        json_post = {
            'id': self.id,
            'type': self.type,
            'comicid': self.chapterid,
            'recentchapter': self.recentchapter,
            'userid': self.userid,
            'createtime': self.createtime,
            'updatetiem': self.updatetime
        }
        return json_post

class ComicChapterInfo(db.Model):
    __tablename__ = 'comicchapterinfo'
    id = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.Integer)
    chapterid = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    createtime = db.Column(db.String(14))
    updatetime = db.Column(db.String(14))

    def __repr__(self):
        return '<ComicChapterInfo %r>' % self.id

    def to_json(self):
        json_post = {
            'id': self.id,
            'bookid':self.bookid,
            'chapterid':self.chapterid,
            'quantity':self.quantity,
            'createtime': self.createtime,
            'updatetiem': self.updatetime
        }
        return json_post

class AccessLog(db.Model):
    __tablename__ = 'access_log'
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.String(20))
    remoteip = db.Column(db.String(50))
    useragent = db.Column(db.String(255))
    addr = db.Column(db.String(255))
    timestamp = db.Column(db.String(14))

    def __repr__(self):
        return '<AccessLog %r>' % self.url

    def to_json(self):
        json_post = {
            'id': self.id,
            'uid':self.uid,
            'remoteip':self.remoteip,
            'useragent':self.useragent,
            'addr':self.addr,
            'timestamp':self.timestamp
        }
        return json_post

class IntegralStrategy(db.Model):
    __tablename__ = 'integral_strategy'
    id = db.Column(db.Integer,primary_key=True)
    value = db.Column(db.Integer)
    description = db.Column(db.String(255))
    createtime = db.Column(db.String(14))
    updatetime = db.Column(db.String(14))

    def __repr__(self):
        return '<IntetralRecord %r>' % self.description

    def to_json(self):
        json_post = {
            'id':self.id,
            'value':self.value,
            'description':self.description,
            'createtime':self.createtime,
            'updatetime':self.updatetime
        }
        return json_post

class IntegralRecord(db.Model):
    __tablename__ = 'integral_record'
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer)
    action = db.Column(db.Integer)
    change = db.Column(db.Integer)
    timestamp = db.Column(db.String(14))

    def __repr__(self):
        return '<IntegralRecord %r>' % self.action

    def to_json(self):
        json_post = {
            'id':self.id,
            'uid':self.uid,
            'action':self.action,
            'change':self.change,
            'timestamp':self.timestamp
        }
        return json_post

class CheckinRecord(db.Model):
    __tablename__ = 'checkin_record'
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer)
    timestamp = db.Column(db.String(14))

    def __repr__(self):
        return '<CheckinRecord %r>' % self.id

    def to_json(self):
        json_post = {
            'id':self.id,
            'uid':self.uid,
            'timestamp':self.timestamp,
        }
        return json_post

class LoginRecord(db.Model):
    __tablename__ = 'login_record'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    timestamp = db.Column(db.String(14))
    continusdays = db.Column(db.Integer)

    def __repr__(self):
        return '<LoginRecord %r>' % self.id

    def to_json(self):
        json_post = {
            'id': self.id,
            'uid': self.uid,
            'timestamp': self.timestamp,
            'continusdays': self.continusdays
        }
        return json_post

class FavorInfo(db.Model):
    __tablename__ = 'favor_info'
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(1))
    uid = db.Column(db.Integer)
    cid = db.Column(db.Integer)
    state = db.Column(db.String(1))
    updatetime = db.Column(db.String(14))
    firstfavortime = db.Column(db.String(14))
    def __repr__(self):
        return '<FavorInfo %d %d>' %(self.uid, self.cid)

    def to_json(self):
        json_post = {
            'id':self.id,
            'type':self.type,
            'uid':self.uid,
            'cid':self.cid,
            'state':self.state,
            'updatetime':self.updatetime,
            'firstfavortime':self.firstfavortime
        }
        return json_post