WeRoBot
=======

.. image:: https://secure.travis-ci.org/whtsky/WeRoBot.png?branch=master
    :target: https://travis-ci.org/whtsky/WeRoBot


WeRoBot是一个微信机器人框架，采用MIT协议发布。


Hello World
------------

最简单的Hello World， 会给收到的每一条信息回复`Hello World` ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.handler
    def echo(message):
        return 'Hello World!'

    robot.run()


Handlers
-----------

WeRoBot会将合法的请求发送给handlers依次执行。

如果某一个Handler返回了非空值，WeRoBot就会根据这个值创建回复，后面的handlers将不会被执行。

你可以通过两种方式添加handler ::

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


Messages
---------
目前WeRoBot共有三种Message：`TextMessage`， `ImageMessage`和`LocationMessage`。他们都继承自WeChatMessage。

TextMessage的属性：


======== ===================================
name      value
======== ===================================
type      'text'
target    信息的目标用户。通常是机器人用户。
source    信息的来源用户。通常是发送信息的用户。
time      信息发送的时间，一个UNIX时间戳。
content   信息的主题内容
======== ===================================

ImageMessage的属性：

======= ==================================
name     value
======= ==================================
type     'image'
target   信息的目标用户。通常是机器人用户。
source   信息的来源用户。通常是发送信息的用户。
time     信息发送的时间，一个UNIX时间戳。
img      图片网址。你可以从这个网址下到图片
======= ==================================

LocationMessage的属性：

========= ===================================
name       value
========= ===================================
type       'location'
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。
location   一个元组。(纬度,    经度)
scale      地图缩放大小
label      地理位置信息
========= ===================================



Replies
--------------

目前WeRoBot共有三种Reply：`TextReply`， `ArticlesReply`。WeChatReply。

你可以在构建Reply时传入一个合法的`Message`类来自动生成`source`和`target`。

若handler返回的是一个字符串，WeRoBot会自动将其转化成一个TextReply.

不知道该用什么Token?
----------------------
WeRoBot帮你准备了一个Token生成器： ::

    import werobot.util

    print(werobot.util.generate_token())


贡献代码
-----------
WeRoBot欢迎每个人贡献代码。

在提交Pull Request前请注意，我有pep8强迫症。。请确定自己的代码通过flake8检测。

另外，不能自动merge的和不能通过测试的代码不会被接受。你可以在安装nose（`pip install nose`）之后运行`nosetests`来进行测试。

捐助
--------

Buy me a cup of coffee :)

Via Alipay（支付宝） ::
    "whtsky#gmail.com".replace("#", "@")