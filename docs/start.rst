入门
=============


Hello World
-------------
最简单的Hello World， 会给收到的每一条信息回复 `Hello World` ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.handler
    def hello(message):
        return 'Hello World!'

    robot.run()

消息处理
--------------
WeRoBot 会解析微信服务器发来的消息， 并将消息转换成成 :ref:`Message` 或者是 :ref:`Event` 。
:ref:`Message` 表示用户发来的消息，如文本消息、图片消息； :ref:`Event` 则表示用户触发的事件， 如关注事件、扫描二维码事件。
在消息解析、转换完成后， WeRoBot 会讲消息转交给 :ref:`Handler` 进行处理，并将 :ref:`Handler` 的返回值返回给微信服务器。

在刚才的 Hello World 中， 我们编写的 ::

    @robot.handler
    def hello(message):
        return 'Hello World!'

就是一个简单的 :ref:`Handler` ， `@robot.handler` 意味着 `robot` 会将所有接收到的消息（ 包括 :ref:`Message` 和 :ref:`Event` ） 都转交给这个 :ref:`Handler` 来处理。
当然， 你也可以编写一些只能处理特定消息的 :ref:`Handler` ::

    # @robot.text 修饰的 Handler 只处理文本消息
    @robot.text
    def echo(message):
        return message.content

    # @robot.image 修饰的 Handler 只处理图片消息
    @robot.image
    def img(message):
        return message.img


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

