#!/usr/bin/env python
# -*- coding: utf-8 -*-


import werobot

robot = werobot.WeRoBot(token='helloworld')
robot.settings.PORT = 8123


@robot.text
def echo(message):
    return 'Hello World!'


if __name__ == '__main__':
    robot.run()
