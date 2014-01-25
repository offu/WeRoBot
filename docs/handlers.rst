Handlers
==========


WeRoBot会将合法的请求发送给 handlers 依次执行。

如果某一个 Handler 返回了非空值， WeRoBot 就会根据这个值创建回复，后面的 handlers 将不会被执行。

你可以通过两种方式添加 handler ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    # 通过修饰符添加handler
    @robot.handler
    def echo(message):
        return 'Hello World!'

    # 通过`add_handler`添加handler
    def echo(message):
        return 'Hello World!'
    robot.add_handler(echo)


类型过滤
------------

在大多数情况下， 一个 Handler 并不能处理所有类型的消息。幸运的是， WeRoBot 可以帮你过滤收到的消息。

只想处理被新用户关注的消息？::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.subscribe
    def subscribe(message):
        return 'Hello My Friend!'

    robot.run()

或者，你的 handler 只能处理文本？ ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.text
    def echo(message):
        return message.content

    robot.run()

==================  =================
修饰符                类型
==================  =================
robot.text           文本
robot.image          图像
robot.location       位置
robot.link           链接
robot.subscribe      被关注
robot.unsubscribe    被取消关注
robot.click          自定义菜单时间
robot.voice          语音
robot.unknown        未知类型
==================  =================

额，这个 handler 想处理文本信息和地理位置信息？ ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.text
    @robot.location
    def handler(message):
        # Do what you love to do
        pass

    robot.run()

当然，你也可以用 ``add_handler`` 函数添加handler，就像这样::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    def handler(message):
        # Do what you love to do
        pass

    robot.add_handler(handler, types=['text', 'location'])

    robot.run()

.. note:: 通过 ``robot.handler`` 添加的 handler 将收到所有信息；只有在其他 handler 没有给出返回值的情况下， 通过 ``robot.handler`` 添加的 handler 才会被调用。

robot.key_click 修饰符
-------------------------

``@robot.key_click`` 是对 ``@robot.click`` 修饰符的改进。

如果你在自定义菜单中定义了一个 Key 为 ``abort`` 的菜单，响应这个菜单的 handler 可以写成这样 ::

    @robot.key_click("abort")
    def abort():
        return "I'm a robot"

当然，如果你不喜欢用 ``@robot.key_click`` ，也可以写成这样 ::

    @robot.click
    def abort(message):
        if message.key == "abort":
            return "I'm a robot"
两者是等价的。
