# -*- coding: utf-8 -*-

import werobot
import werobot.utils
import werobot.testing
from werobot.session import filestorage, mongodbstorage, redisstorage

import pymongo
import redis


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
        robot.session_storage = session_storages
        assert tester.send(message_1) == tester.send(message_2) == 'ss'
        remove_session(session_storage)
