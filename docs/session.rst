Session
==========

WeRoBot 0.4.0 中增加了功能强大的 Session 系统，你可以通过 Session 轻松实现用户状态的记录，享受如同 Web 开发般的便捷。

一个简单的使用 Session 的 Demo ::

    robot = werobot.WeRoBot(token=werobot.utils.generate_token(),
                            enable_session=True)

    @robot.text
    def first(message, session):
        if 'last' in session:
            return
        session['last'] = message.content
        return message.content

    robot.run()

开启 Session
----------------

想要开启 Session ，在实例化 :class:`WeRoBot` 的时候需要传入 ``enable_session`` 和 ``session_storage`` 两个参数：

+ ``enable_session`` ： 必须为 True （打开 Session ）
+ ``session_storage`` ： 可选，一个 Session Storage 实例。默认是 :class:`werobot.session.filestorage.FileStorage` 。

修改 Handler 以使用 Session
--------------------------------

没有打开 Session 的时候，一个标准的 WeRoBot Handler 应该是这样的 ::

    @robot.text
    def hello(message):
        return "Hello!"

而在打开 Session 之后， 这个 Handler 需要修改为接受第二个参数： ``session`` ::

    @robot.text
    def hello(message, session):
        count = session.get("count", 0) + 1
        session["count"] = count
        return "Hello! You have sent %s messages to me" % count

传入的 ``session`` 参数是一个标准的 Python 字典。

在修改完 Handler 之后， 你的微信机器人就拥有 Session 系统了 :)

可用的 Session Storage
-----------------------

.. module:: werobot.session.filestorage

.. autoclass:: FileStorage

.. module:: werobot.session.mongodbstorage

.. autoclass:: MongoDBStorage

.. module:: werobot.session.redisstorage

.. autoclass:: RedisStorage