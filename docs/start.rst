入门
=============


Hello World
-------------
最简单的Hello World， 会给收到的每一条信息回复 `Hello World` ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.handler
    def echo(message):
        return 'Hello World!'

    robot.run()


