Changelog
=============

Version 1.2.0
----------------
+ 增加 :class:`werobot.session.mysqlstorage.MySQLStorage`
+ 增加 :func:`werobot.robot.BaseRoBot.add_filter`
+ :func:`werobot.utils.generate_token` 在 Python 3.6+ 下优先使用 ``secrets.choice`` 来随机生成 token
+ 修复 :func:`werobot.client.Client.get_media_list` 的调用参数错误 (`#208 <https://github.com/whtsky/WeRoBot/issues/208>`_)
+ 修复了某些情况下 Client 中文编码不正确的问题 (`#250 <https://github.com/whtsky/WeRoBot/issues/250>`_)
+ Handler 中的 Exception 现在会以 Error level 记录到 logger 中
+ 在文档中增加了独立的 :doc:`api` 部分
+ 添加了 ``video`` 和 ``shortvideo`` 的修饰器
+ 增加了 :class:`werobot.session.saekvstorage.SaeKVDBStorage` 的测试
+ 抛弃对 Django < 1.8 的支持

Version 1.1.1
----------------

+ 修复 :func:`werobot.client.Client.create_menu` 文档中的错误
+ 在 :func:`werobot.client.Client.send_music_message` 的文档中提示了可能的缩略图不显示的问题

Version 1.1.0
----------------

+ 为 :class:`werobot.robot.BaseRoBot` 增加 ``client`` property
+ 允许在初始化 :class:`werobot.robot.BaseRoBot` 时传入 :doc:`config` 。注意如果传入了 config ， BaseRoBot 会忽略除 ``config`` 与 ``logger`` 外的其他所有的参数。
+ deprecate :class:`werobot.robot.BaseRoBot` 的 ``enable_session`` 参数
+ Session Storage 现在是惰性加载的了； 如果希望关闭 Session ， 请将 :doc:`config` 中的 ``SESSION_STORAGE`` 设为 ``False`` (`#189 <https://github.com/whtsky/WeRoBot/issues/189>`_)
+ 修复了打包时 `error.html` 被忽略导致的默认错误页面错误的问题 (`#194 <https://github.com/whtsky/WeRoBot/issues/194>`_)
+ 允许使用 ``reply.time`` 的方式快速读取 Reply 属性
+ 完善 :doc:`client` 中自定义菜单、消息管理、素材管理、用户管理、账户管理、素材管理部分的 `API`
+ 修复了直接 GET 访问 Robot 主页返回 500 的问题

Version 1.0.0
----------------

+ 增加对消息加解密的支持
+ 重写 werobot.messages, 完善对 Event 的支持
+ 将微信消息的 `id` 属性重命名为 `message_id`
+ 增加 :class:`werobot.reply.SuccessReply`
+ 增加 :class:`werobot.reply.ImageReply`
+ 增加 :class:`werobot.reply.VoiceReply`
+ 增加 :class:`werobot.reply.VideoReply`
+ 删除 :func:`werobot.reply.create_reply`
+ 为 :class:`werobot.reply.WeChatReply` 增加 ``process_args`` 方法
+ 为 :class:`werobot.robot.BaseRoBot` 增加 ``parse_message`` 方法
+ 为 :class:`werobot.robot.BaseRoBot` 增加 ``get_encrypted_reply`` 方法
+ 删去了 Reply 中过时的 flag
+ 修复 :class:`werobot.session.filestorage.FileStorage` 在 PyPy 下的兼容性问题
+ 增加 :class:`werobot.session.sqlitestorage.SQLiteStorage`
+ 将默认的 SessionBackend 切换为 :class:`werobot.session.sqlitestorage.SQLiteStorage`
+ 将图文消息单个消息的渲染函数放到 :class:`werobot.replies.Article` 内
+ 取消对 Python2.6, Python3.3 的支持
+ 增加与 Django 1.6+, Flask, Bottle, Tornado 集成的支持
+ 替换 `inspect.getargspec()` 

Version 0.6.1
----------------

+ Fix wrong URL in ``upload_media``
+ Add VideoMessage

Version 0.6.0
----------------

+ Add ``@werobot.filter``
+ Add :class:`werobot.session.saekvstorage`
+ Add support for Weixin Pay ( :class:`werobot.pay.WeixinPayClient` )
+ Add ``werobot.reply.TransferCustomerServiceReply``
+ Fix FileStorage's bug

Version 0.5.3
----------------

+ Fix: can't handle request for root path

Version 0.5.2
----------------

+ Fix Python 3 support

Version 0.5.1
----------------

+ Fix typo

Version 0.5.0
----------------

+ Add ``werobot.client``
+ Add ``werobot.config``
+ Add ``werobot.logger``
+ Add ``@werobot.key_click`` (Thanks @tg123)
+ Support Location Event
+ Use smart args
+ Friendly 403 page
+ Improved server support
+ Enable session by default.
+ Drop ``werobot.testing.make_text_message``
+ Drop ``werobot.testing.make_image_message``
+ Drop ``werobot.testing.make_location_message``
+ Drop ``werobot.testing.make_voice_message``
+ Drop ``werobot.testing.WeTest.send``
+ Rewrite ``werobot.message``
+ Rewrite testing case

Version 0.4.1
----------------
+ Add VoiceMessage
+ Add ``message.raw``: Raw XML of message
+ Rename ``UnknownMessage.content`` to ``UnknownMessage.raw``
+ Fix a bug when signature is invalid.
+ Ignore session when receive UnknownMessage

Version 0.4.0
----------------
+ Add session support
+ Add logging support
+ Rename ``werobot.test`` to ``werobot.testing``
+ Handlers added by ``@robot.handler`` will have the lowest priority.

Version 0.3.5
----------------
+ Bug fix: Make ``BaseRoBot`` importable

Version 0.3.4
----------------
+ Rename ``WeRoBot.app`` to ``WeRoBot.wsgi``
+ Add ``BaseRoBot`` class. It's useful for creating extensions.
+ Reorganized documents.

Version 0.3.3
----------------
+ Add ``host`` param in werobot.run
+ Update EventMessage
+ Add LinkMessage

Version 0.3.2
----------------
+ Convert all arguments to unicode in Python 2 ( See issue `#1 <https://github.com/whtsky/WeRoBot/pull/1>`_ )

Version 0.3.1
----------------
+ Add ``server`` param in werobot.run

Version 0.3.0
----------------
+ Add new messages and replies support for WeChat 4.5
