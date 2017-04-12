Config
=====================

WeRoBot 使用 ``WeRoBot.Config`` 类来存储配置信息。  ``WeRoBot`` 类实例的 ``config`` 属性是一个 :class:`werobot.config.Config` 实例。

:class:`~werobot.config.Config` 继承自 `dict` 。因此， 你可以像使用普通 dict 一样使用它 ::

    from werobot import WeRoBot
    robot = WeRoBot(token='2333')

    robot.config.update(
        HOST='0.0.0.0',
        PORT=80
    )

当然， 你也可以先创建一个 Config ，然后在初始化 ``WeRobot`` 的时候传入自己的 Config ::

    from werobot.config import Config
    config = Config(
        TOKEN="token from config!"
    )
    robot = WeRoBot(config=config, token="token from init")
    assert robot.token == "token from config!"

.. note:: 如果你在初始化 ``WeRoBot`` 时传入了 ``config`` 参数， ``WeRoBot`` 会忽略除 ``logger`` 外其他所有的初始化参数。 如果你需要对 ``WeRoBot`` 进行一些配置操作， 请修改 Config 。

与普通 `dict` 不同的是， 你可以先把配置文件保存在一个对象或是文件中， 然后在 :class:`~werobot.config.Config` 中导入配置 ::

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
