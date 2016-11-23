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

消息加密
--------------

WeRoBot 支持对消息的加密，即微信公众号的安全模式。
为 WeRoBot 开启消息加密功能，首先需要安装 ``cryptography`` ::

    pip install cryptography

之后需要在微信公众平台的基本配置中将消息加解密方式选择为安全模式，随机生成 `EncodingAESKey`，并且把它传给 WeRoBot 或者 WeRoBot 实例的 config 或者创建相对应的 Config 类 ::

    from werobot import WeRoBot
    robot = WeRoBot(token='2333',
                    encoding_aes_key='your_encoding_aes_key',
                    app_id='your_app_id')

