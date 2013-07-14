# -*- coding: utf-8 -*-

import os

import werobot
import werobot.utils
import werobot.testing


def remove_file_session():
    try:
        os.remove("werobot_session.db")
    except:
        pass


def test_session():
    remove_file_session()
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
    assert tester.send(message_1) == tester.send(message_2) == 'ss'
