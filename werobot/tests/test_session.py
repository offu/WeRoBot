# -*- coding: utf-8 -*-

import werobot
import werobot.utils
import werobot.testing
from werobot.session import filestorage, mongodbstorage, redisstorage
from werobot.session import SessionStorage
from werobot.utils import to_binary

import pymongo
import redis
from nose.tools import raises


def remove_session(session):
    del session[to_binary("fromUser")]


def test_session():
    robot = werobot.WeRoBot(token=werobot.utils.generate_token(),
                            enable_session=True)

    @robot.text
    def first(message, session):
        if 'last' in session:
            return
        session['last'] = message.content
        return message.content

    @robot.text
    def second(_, session):
        return session['last']

    tester = werobot.testing.WeTest(robot)
    xml_1 = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[ss]]></Content>
        <MsgId>1234567890123456</MsgId>
        </xml>
    """
    xml_2 = """
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[dd]]></Content>
        <MsgId>1234567890123456</MsgId>
        </xml>
    """

    session_storages = [
        filestorage.FileStorage(),
        mongodbstorage.MongoDBStorage(pymongo.MongoClient().t.t),
        redisstorage.RedisStorage(redis.Redis()),
    ]

    for session_storage in session_storages:
        robot.session_storage = session_storage
        assert tester.send_xml(xml_1) == tester.send_xml(xml_2) == 'ss',\
            session_storage
        remove_session(session_storage)


@raises(NotImplementedError)
def test_session_storage_get():
    session = SessionStorage()
    session.get('s')


@raises(NotImplementedError)
def test_session_storage_set():
    session = SessionStorage()
    session.set('s', {})


@raises(NotImplementedError)
def test_session_storage_delete():
    session = SessionStorage()
    session.delete('s')
