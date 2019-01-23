回复
==============


你可以在构建Reply时传入一个合法的 `Message` 对象来自动生成 `source` 和 `target` ::

    reply = TextReply(message=message, content='Hello!')


TextReply
-----------

`TextReply` 是简单的文本消息，构造函数的参数如下：

========= ===================================
name       value
========= ===================================
content    信息正文。
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
========= ===================================

.. note:: 如果你的handler返回了一个字符串， WeRoBot会自动将其转化为一个文本消息。

ImageReply
-----------

`ImageReply` 为回复图片消息，构造函数的参数如下：

========= ===================================
name       value
========= ===================================
media_id   通过素材管理接口上传多媒体文件，得到的id。
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
========= ===================================

VoiceReply
----------

`VoiceReply` 为回复语音消息，构造函数的参数如下：

========= ===================================
name       value
========= ===================================
media_id   通过素材管理接口上传多媒体文件，得到的id。
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
========= ===================================

VideoReply
----------

`VideoReply` 为回复视频消息，构造函数的参数如下：

============ ===================================
name          value
============ ===================================
media_id      通过素材管理接口上传多媒体文件，得到的id。
title         视频消息的标题。可为空。
description   视频消息的描述。可为空。
target        信息的目标用户。通常是机器人用户。
source        信息的来源用户。通常是发送信息的用户。
time          信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
============ ===================================


ArticlesReply
---------------

`ArticlesReply` 是图文消息，构造函数的参数如下：

========= ===================================
name       value
========= ===================================
content    信息正文。**可为空**。
target     信息的目标用户。通常是机器人用户。
source     信息的来源用户。通常是发送信息的用户。
time       信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
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

    from werobot.replies import ArticlesReply, Article
    reply = ArticlesReply(message=message)
    article = Article(
        title="WeRoBot",
        description="WeRoBot是一个微信机器人框架",
        img="https://github.com/apple-touch-icon-144.png",
        url="https://github.com/whtsky/WeRoBot"
    )
    reply.add_article(article)

.. note:: 根据微信公众平台的 `最新公告 <https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncement&announce_id=115383153198yAvN&lang=zh_CN>`_，每个ArticlesReply中 **最多添加1个Article** 。

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
-----------

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

TransferCustomerServiceReply
-----------------------------

将消息转发到多客服,构造函数的参数如下:

=============    ======================================================================
name              value
=============    ======================================================================
target            信息的目标用户。通常是机器人用户。
source            信息的来源用户。通常是发送信息的用户。
time              信息发送的时间，一个UNIX时间戳。默认情况下会使用当前时间。
account           指定会话接入的客服账号，可以没有此参数，没有时会自动分配给可用客服。
=============    ======================================================================

SuccessReply
---------------
给微信服务器回复 "success"。
假如服务器无法保证在五秒内处理并回复，需要回复 `SuccessReply` ，这样微信服务器才不会对此作任何处理，并且不会发起重试。
