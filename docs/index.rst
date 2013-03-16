WeRoBot
=======


WeRoBot是一个微信机器人框架，采用MIT协议发布。


Hello World
------------

最简单的Hello World， 会给收到的每一条信息回复 `Hello World` ::

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
目前WeRoBot共有以下几种Message： `TextMessage` ， `ImageMessage` ， `LocationMessage` ， `EventMessage` 和 `UnknownMessage` 。他们都继承自 WeChatMessage 。

TextMessage
~~~~~~~~~~~~

TextMessage的属性：


======== ===================================
name      value
======== ===================================
id        消息id，64位整型 [3]_
type      'text' 或 'hello' [1]_
target    信息的目标用户。通常是机器人用户。
source    信息的来源用户。通常是发送信息的用户。
time      信息发送的时间，一个UNIX时间戳。
content   信息的内容
======== ===================================

ImageMessage
~~~~~~~~~~~~~

ImageMessage的属性：

======= ==================================
name     value
======= ==================================
id       消息id，64位整型 [3]_
type     'image'
target   信息的目标用户。通常是机器人用户。
source   信息的来源用户。通常是发送信息的用户。
time     信息发送的时间，一个UNIX时间戳。
img      图片网址。你可以从这个网址下到图片
======= ==================================

LinkMessage
~~~~~~~~~~~~
============    ==================================
name             value
============    ==================================
id               消息id，64位整型 [3]_
type             'link'
target           信息的目标用户。通常是机器人用户。
source           信息的来源用户。通常是发送信息的用户。
time             信息发送的时间，一个UNIX时间戳。
title            消息标题
description      消息描述
url              消息链接
============    ==================================


LocationMessage
~~~~~~~~~~~~~~~~

LocationMessage的属性：

========= ===================================
name       value
========= ===================================
id         消息id，64位整型 [3]_
type       'location'
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。
location   一个元组。(纬度, 经度)
scale      地图缩放大小
label      地理位置信息
========= ===================================

EventMessage
~~~~~~~~~~~~~~

EventMessage的属性：

========= ===================================
name       value
========= ===================================
type       'enter' 或 'location' [2]_
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。
location   一个元组。(纬度, 经度)。 type 为 'location' 时存在。
precision  地理位置精度。 type 为 'location' 时存在。
========= ===================================

UnknownMessage
~~~~~~~~~~~~~~~

UnknownMessage的属性：

========= =====================================
name       value
========= =====================================
type       'unknown'
content    请求的正文部分。标准的XML格式。
========= =====================================

.. note:: 如果你不为 WeRoBot 贡献代码，你完全可以无视掉 UnknownMessage 。在正常的使用中，WeRoBot应该不会收到 `UnknownMessage` ——除非 WeRoBot 停止开发。

.. [1] 当有用户关注你的时候，你会收到一条来自该用户的、内容为 `Hello2BizUser` 的 TextMessage 。WeRoBot 会将其的type设为 `hello` 。
.. [2] 有两种时间推送： 如果是用户进入会话， type 为 `enter` ； 如果是地理位置， type 为 `location` 。
.. [3] 截至目前（ 2013.03.16 ），微信机器人所收到的消息中都不包含 MsgID.

类型过滤
--------------
在大多数情况下， 一个 Handler 并不能处理所有类型的消息。幸运的是， WeRoBot 可以帮你过滤收到的消息。

只想处理被新用户关注的消息？::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.hello
    def hello(message):
        return 'Hello My Friend!'

    robot.run()

或者，你的 handler 只能处理文本？ ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.text
    def echo(message):
        return message.content

    robot.run()

你也可以使用 ``robot.image`` 修饰符来只接受图像信息；
``robot.location`` 修饰符来只接受位置信息；
``robot.enter`` 修饰符来只接受进入会话信息。

.. note:: `robot.location` 修饰符会让你的 handler 接受到两类消息——位置信息和事件推送中的地理位置。

当然，还有 `robot.unknown` —— 如果你想收到未知属性的信息的话。

额，这个 handler 想处理文本信息和地理位置信息？ ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.text
    @robot.location
    def handler(message):
        # Do what you love to do
        pass

    robot.run()

当然，你也可以用 `add_handler` 函数添加handler，就像这样::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    def handler(message):
        # Do what you love to do
        pass

    robot.add_handler(handler, types=['text', 'location'])

    robot.run()

.. note:: 通过 `robot.handler` 添加的 handler 将收到所有信息。

Replies
--------------

目前WeRoBot共有三种Reply： `TextReply` ， `ArticlesReply` 和 `MusicReply` 。他们都继承自 `WeChatReply` 。

TextReply
~~~~~~~~~~~

`TextReply` 是简单的文本消息，构造函数的参数如下：

========= ===================================
name       value
========= ===================================
content    信息正文。
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
flag       如果是True， WeRoBot会对这条消息进行星标。你可以在公众平台后台看到所有的星标消息。
========= ===================================

你可以在构建Reply时传入一个合法的 `Message` 对象来自动生成 `source` 和 `target` ::

    reply = TextReply(message=message, content='Hello!')

.. note:: 如果你的handler返回了一个字符串， WeRoBot会自动将其转化为一个文本消息。

ArticlesReply
~~~~~~~~~~~~~~~

`ArticlesReply` 是图文消息，构造函数的参数如下：

========= ===================================
name       value
========= ===================================
content    信息正文。**可为空**。
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
flag       如果是True， WeRoBot会对这条消息进行星标。你可以在公众平台后台看到所有的星标消息。
========= ===================================

你需要给 `ArticlesReply` 添加 `Article` 来增加图文。
`Article` 类位于 `werobot.reply.Article` 。

`Article` 的构造函数的参数如下：

============ ===================================
name          value
============ ===================================
title         标题
description   描述
img           图片链接
url           点击图片后跳转链接
============ ===================================

注意，微信公众平台对图片链接有特殊的要求，详情可以在
`消息接口使用指南 <http://mp.weixin.qq.com/cgi-bin/readtemplate?t=wxm-callbackapi-doc&lang=zh_CN>`_ 里看到。

在构造完一个 `Article` 后， 你需要通过 `ArticlesReply` 的 `add_article` 参数把它添加进去。就像这样： ::

    from werobot.reply import ArticlesReply, Article
    reply = ArticlesReply(message=message)
    article = Article(
        title="WeRoBot",
        desription="WeRoBot是一个微信机器人框架",
        img="https://github.com/apple-touch-icon-144.png",
        url="https://github.com/whtsky/WeRoBot"
    )
    reply.add_article(article)

.. note:: 每个ArticlesReply中 **最多添加10个Article** 。

你也可以让你的 handler 返回一个列表， 里面每一个元素都是一个长度为四的列表，
 WeRoBot 会将其自动转为 ArticlesReply 。就像这样： ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.text
    def articles(message):
        return [
            [
                "title",
                "description",
                "img",
                "url"
            ],
            [
                "whtsky",
                "I wrote WeRoBot",
                "https://secure.gravatar.com/avatar/0024710771815ef9b74881ab21ba4173?s=420",
                "http://whouz.com/"
            ]
        ]

    robot.run()


MusicReply
~~~~~~~~~~~

`MusicReply` 是音乐消息，构造函数的参数如下：

=============    ======================================================================
name              value
=============    ======================================================================
target            信息的目标用户。通常是机器人用户。
source            信息的来源用户。通常是发送信息的用户。
time              信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
title             标题
description       描述
url               音乐链接
hq_url            高质量音乐链接，WIFI环境优先使用该链接播放音乐。可为空 [3]_
flag              如果是True， WeRoBot会对这条消息进行星标。你可以在公众平台后台看到所有的星标消息。
=============    ======================================================================

你也可以让你的 handler 返回一个长度为三或四的列表， [3]_
 WeRoBot 会将其自动转为 MusicReply 。就像这样： ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.text
    def music(message):
        return [
            "title",
            "description",
            "music_url",
            "hq_music_url"
            ]

    @robot.text
    def music2(message):
        return [
            "微信你不懂爱",
            "龚琳娜最新力作",
            "http://weixin.com/budongai.mp3",
            ]

    robot.run()


.. [3] 如果你省略了高质量音乐链接的地址， WeRoBot 会自动将音乐链接的地址用于高质量音乐链接。

部署
---------------------
在独立服务器上部署
~~~~~~~~~~~~~~~~~~~~~~
当你运行 `werobot.run` 的时候，你可以通过传递 `server` 参数来手动指定使用的服务器 ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.handler
    def echo(message):
        return 'Hello World!'

    robot.run(server='tornado')

server 支持以下几种：

+ cgi
+ flup
+ wsgiref
+ waitress
+ cherrypy
+ paste
+ fapws3
+ tornado
+ gae
+ twisted
+ diesel
+ meinheld
+ gunicorn
+ eventlet
+ gevent
+ rocket
+ bjoern
+ auto

当 server 为 auto 时， WeRoBot 会自动依次尝试以下几种服务器：

+ Waitress
+ Paste
+ Twisted
+ CherryPy
+ WSGIRef

所以，只要你安装了相应的服务器软件，就可以使用 ``werobot.run`` 直接跑在生产环境下。

.. note:: server 的默认值为 ``auto``

使用 Supervisor 管理守护进程
##################################

请注意， ``werobot.run`` 是跑在 **非守护进程模式下** 的——也就是说，一旦你关闭终端，进程就会自动退出。

我们建议您使用 `Supervisor <http://supervisord.org/>`_ 来管理 WeRoBot 的进程。

配置文件样例： ::

    [program:wechat_robot]
    command = python /home/whtsky/robot.py
    user = whtsky
    redirect_stderr = true
    stdout_logfile = /home/whtsky/logs/robot.log

使用 Nginx 进行反向代理
################################

微信服务器只支持80端口的机器人——显然，你的服务器上不会只跑着一个微信机器人。对于这种情况，我们建议您使用 Nginx 来进行反向代理。

配置文件样例： ::

    server {
        server_name example.com;
        listen 80;

        location / {
            proxy_pass_header Server;
            proxy_redirect off;
            proxy_pass http://127.0.0.1:8888;
        }
    }

.. note:: 在这个例子中， WeRoBot 的端口号为8888。你应该在微信管理后台中将服务器地址设为 ``http://example.com`` 。

在SAE上部署
~~~~~~~~~~~~~~~~~

``werobot.app`` 是一个标准的 WSGI Application 。 如果你想在 SAE 上部署 WeRoBot ，可以参考以下代码 ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.handler
    def echo(message):
        return 'Hello World!'

    application = sae.create_wsgi_app(robot.app)


不知道该用什么Token?
----------------------
WeRoBot帮你准备了一个Token生成器： ::

    import werobot.utils

    print(werobot.utils.generate_token())


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

Changelog
-----------

Version 0.3.3
~~~~~~~~~~~~~~~~
+ Add `host` param in werobot.run

Version 0.3.2
~~~~~~~~~~~~~~~~
+ Convert all arguments to unicode in Python 2 ( See issue `#1 <https://github.com/whtsky/WeRoBot/pull/1>`_ )

Version 0.3.1
~~~~~~~~~~~~~~~~
+ Add `server` param in werobot.run

Version 0.3.0
~~~~~~~~~~~~~~~~

+ Add new messages and replies support for WeChat 4.5