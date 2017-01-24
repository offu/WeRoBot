Config
=====================

WeRoBot 使用 ``WeRoBot.Config`` 类来存储配置信息。  ``WeRoBot`` 类实例的 ``config`` 属性是一个 :class:`WeRobot.config.Config` 实例。

:class:`WeRobot.config.Config` 继承自 `dict` 。因此， 你可以像使用普通 dict 一样使用它 ::

    from werobot import WeRoBot
    robot = WeRoBot(token='2333')

    robot.config.update(
        HOST='0.0.0.0',
        PORT=80
    )

与普通 `dict` 不同的是， 你可以先把配置文件保存在一个对象或是文件中， 然后在 :class:`WeRoBot.config.Config` 中导入配置 ::

    from werobot import WeRoBot
    robot = WeRoBot(token='2333')

    class MyConfig(object):
        HOST = '0.0.0.0'
        PORT = 80

    robot.config.from_object(MyConfig)
    robot.config.from_pyfile("config.py")


默认配置
----------

.. code:: python

    dict(
        TOKEN=None,
        SERVER="auto",
        HOST="127.0.0.1",
        PORT="8888",
        SESSION_STORAGE=None,
        APP_ID=None,
        APP_SECRET=None,
        ENCODING_AES_KEY=None
    )


API
----------

.. module:: werobot.config
.. autoclass:: Config
    :members:
