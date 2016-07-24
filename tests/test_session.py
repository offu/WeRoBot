# -*- coding: utf-8 -*-

import os
import pymongo
import redis
import pytest

import werobot
import werobot.testing
import werobot.utils
from werobot.session import SessionStorage
from werobot.session import filestorage, mongodbstorage, redisstorage
from werobot.session import sqlitestorage
from werobot.utils import to_binary


def teardown_module():
    try:
        os.remove("werobot_session")
        os.remove("werobot_session.sqlite3")
    except:
        pass


def remove_session(session):
    try:
        del session[to_binary("fromUser")]
    except:
        pass


def test_session():
    storage = filestorage.FileStorage()
    robot = werobot.WeRoBot(token=werobot.utils.generate_token(),
                            enable_session=True,
                            session_storage=storage)

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
        storage,
        mongodbstorage.MongoDBStorage(pymongo.MongoClient().t.t),
        redisstorage.RedisStorage(redis.Redis()),
        sqlitestorage.SQLiteStorage(),
    ]

    for session_storage in session_storages:
        remove_session(session_storage)
        robot.session_storage = session_storage
        reply_1 = tester.send_xml(xml_1)._args['content']
        assert reply_1 == 'ss', (reply_1, session_storage)
        reply_2 = tester.send_xml(xml_2)._args['content']
        assert reply_2 == 'ss', (reply_2, session_storage)
        remove_session(session_storage)
    storage.db.close()


def test_session_storage_get():
    session = SessionStorage()
    with pytest.raises(NotImplementedError):
        session.get('s')


def test_session_storage_set():
    session = SessionStorage()
    with pytest.raises(NotImplementedError):
        session.set('s', {})


def test_session_storage_delete():
    session = SessionStorage()
    session.delete('s')


def test_sqlitestorage():
    storage = sqlitestorage.SQLiteStorage()

    assert storage.get("喵") == {}
    storage.set("喵", "喵喵")
    assert storage.get("喵") == u"喵喵"
    storage.delete("喵")
    assert storage.get("喵") == {}
