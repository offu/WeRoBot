# -*- coding: utf-8 -*-

import werobot
import werobot.utils
import werobot.testing
from werobot.session import filestorage, mongodbstorage, redisstorage
from werobot.session import SessionStorage

import pymongo
import redis
from nose.tools import raises


def remove_session(session):
    del session['test']


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
    def second(message, session):
        return session['last']

    tester = werobot.testing.WeTest(robot)
    message_1 = werobot.testing.make_text_message('ss')
    message_2 = werobot.testing.make_text_message('dd')

    session_storages = [
        filestorage.FileStorage(),
        mongodbstorage.MongoDBStorage(pymongo.MongoClient().t.t),
        redisstorage.RedisStorage(redis.Redis()),
    ]

    for session_storage in session_storages:
        robot.session_storage = session_storage
        assert tester.send(message_1) == tester.send(message_2) == 'ss',\
            session_storage
        remove_session(session_storage)


@raises(NotImplementedError)
def test_session_storage_get():
    session = SessionStorage()
    session.get('s')


@raises(NotImplementedError)
def test_session_storage_set():
    session = SessionStorage()
    session.set('s')


@raises(NotImplementedError)
def test_session_storage_delete():
    session = SessionStorage()
    session.delete('s')
