# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask import Flask, request
import config
from flask_script import Manager
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class City(db.Model):
    __tablename__ = 'City'

    C_id = db.Column(db.Integer, primary_key=True)
    C_Name = db.Column(db.String(30))
    C_ProvinceId = db.Column(db.ForeignKey('Province.P_id'), index=True)

    Province = db.relationship('Province', primaryjoin='City.C_ProvinceId == Province.P_id', backref='cities')


class Friend(db.Model):
    __tablename__ = 'Friends'

    F_id = db.Column(db.Integer, primary_key=True)
    F_FriendId = db.Column(db.ForeignKey('User.U_id'), index=True)
    F_UserId = db.Column(db.ForeignKey('User.U_id'), index=True)
    F_Name = db.Column(db.String(30))

    User = db.relationship('User', primaryjoin='Friend.F_FriendId == User.U_id', backref='user_friends')
    User1 = db.relationship('User', primaryjoin='Friend.F_UserId == User.U_id', backref='user_friends_0')


class GMToUser(db.Model):
    __tablename__ = 'GMToUser'

    GMTU_Id = db.Column(db.Integer, primary_key=True)
    GMTU_UserId = db.Column(db.ForeignKey('User.U_id'), index=True)
    GMTU_GMId = db.Column(db.ForeignKey('Group_Message.GM_id'), index=True)

    Group_Message = db.relationship('GroupMessage', primaryjoin='GMToUser.GMTU_GMId == GroupMessage.GM_id', backref='gm_to_users')
    User = db.relationship('User', primaryjoin='GMToUser.GMTU_UserId == User.U_id', backref='gm_to_users')


class GroupMessage(db.Model):
    __tablename__ = 'Group_Message'

    GM_id = db.Column(db.Integer, primary_key=True)
    GM_Content = db.Column(db.String)
    GM_FromId = db.Column(db.ForeignKey('User.U_id'), index=True)
    GM_FromName = db.Column(db.String(30))
    GM_CreateTime = db.Column(db.DateTime)
    GM_ContentTypeId = db.Column(db.ForeignKey('MessagesType.MT_id'), index=True)
    GM_GroupId = db.Column(db.ForeignKey('Groups.G_id'), index=True)

    MessagesType = db.relationship('MessagesType', primaryjoin='GroupMessage.GM_ContentTypeId == MessagesType.MT_id', backref='group_messages')
    User = db.relationship('User', primaryjoin='GroupMessage.GM_FromId == User.U_id', backref='group_messages')
    Group = db.relationship('Group', primaryjoin='GroupMessage.GM_GroupId == Group.G_id', backref='group_messages')


class GroupUser(db.Model):
    __tablename__ = 'Group_User'

    GU_id = db.Column(db.Integer, primary_key=True)
    GU_UserId = db.Column(db.ForeignKey('User.U_id'), index=True)
    GU_JoinTime = db.Column(db.DateTime)
    GU_NickName = db.Column(db.String(30))
    GU_GroupId = db.Column(db.ForeignKey('Groups.G_id'), index=True)

    Group = db.relationship('Group', primaryjoin='GroupUser.GU_GroupId == Group.G_id', backref='group_users')
    User = db.relationship('User', primaryjoin='GroupUser.GU_UserId == User.U_id', backref='group_users')


class Group(db.Model):
    __tablename__ = 'Groups'

    G_id = db.Column(db.Integer, primary_key=True)
    G_Name = db.Column(db.String(30))
    G_CreateTime = db.Column(db.DateTime)
    G_AdminId = db.Column(db.ForeignKey('User.U_id'), index=True)

    User = db.relationship('User', primaryjoin='Group.G_AdminId == User.U_id', backref='groups')


class Message(db.Model):
    __tablename__ = 'Messages'

    M_id = db.Column(db.Integer, primary_key=True)
    M_Content = db.Column(db.String)
    M_Time = db.Column(db.DateTime)
    M_TypeId = db.Column(db.ForeignKey('MessagesType.MT_id'), index=True)
    M_FromUserId = db.Column(db.ForeignKey('User.U_id'), index=True)
    M_ToUserId = db.Column(db.ForeignKey('User.U_id'), index=True)

    User = db.relationship('User', primaryjoin='Message.M_FromUserId == User.U_id', backref='user_messages')
    User1 = db.relationship('User', primaryjoin='Message.M_ToUserId == User.U_id', backref='user_messages_0')
    MessagesType = db.relationship('MessagesType', primaryjoin='Message.M_TypeId == MessagesType.MT_id', backref='messages')


class MessagesType(db.Model):
    __tablename__ = 'MessagesType'

    MT_id = db.Column(db.Integer, primary_key=True)
    MT_Name = db.Column(db.String(20))


class Nation(db.Model):
    __tablename__ = 'Nation'

    N_id = db.Column(db.Integer, primary_key=True)
    N_Name = db.Column(db.String(30))


class Province(db.Model):
    __tablename__ = 'Province'

    P_id = db.Column(db.Integer, primary_key=True)
    P_Name = db.Column(db.String(30))
    P_NationId = db.Column(db.ForeignKey('Nation.N_id'), index=True)

    Nation = db.relationship('Nation', primaryjoin='Province.P_NationId == Nation.N_id', backref='provinces')


class User(db.Model):
    __tablename__ = 'User'

    U_id = db.Column(db.Integer, primary_key=True)
    U_LoginId = db.Column(db.String(20))
    U_LoginName = db.Column(db.String(20))
    U_Password = db.Column(db.String(128))
    U_Signature = db.Column(db.String(150))
    U_NationId = db.Column(db.ForeignKey('Nation.N_id'), index=True)
    U_ProvinceId = db.Column(db.ForeignKey('Province.P_id'), index=True)
    U_CityId = db.Column(db.ForeignKey('City.C_id'), index=True)

    City = db.relationship('City', primaryjoin='User.U_CityId == City.C_id', backref='users')
    Nation = db.relationship('Nation', primaryjoin='User.U_NationId == Nation.N_id', backref='users')
    Province = db.relationship('Province', primaryjoin='User.U_ProvinceId == Province.P_id', backref='users')

    def hash_password(self, password):  # 给密码加密方法
        self.U_Password = pwd_context.encrypt(password)

    def verify_password(self, password):  # 验证密码方法
        return pwd_context.verify(password, self.U_Password)

    # def __init__(self, U_LoginName, U_Password):
    #     self.U_LoginName = U_LoginName
    #     self.U_Password = U_Password

    def __repr__(self):
        return '<User %r>' % self.U_LoginName

    def __str__(self):
        return '<User %s>' % self.U_LoginName