``WeRoBot.Client`` —— 微信 API 操作类
=====================================
有部分接口暂未实现，可自行调用微信接口。

.. module:: werobot.client

开始开发
------------

获取 access token
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/14/9f9c82c1af308e3b14ba9b973f99a8ba.html

.. automethod:: Client.grant_token
.. automethod:: Client.get_access_token

.. note:: Client 的操作都会自动进行 `access token` 的获取和过期刷新操作，如果有特殊需求（如多进程部署）可重写 ``get_access_token``。

获取微信服务器IP地址
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/4/41ef0843d6e108cf6b5649480207561c.html

.. automethod:: Client.get_ip_list

自定义菜单
------------

自定义菜单创建接口
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/10/0234e39a2025342c17a7d23595c6b40a.html

.. automethod:: Client.create_menu

自定义菜单查询接口
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/5/f287d1a5b78a35a8884326312ac3e4ed.html

.. automethod:: Client.get_menu

自定义菜单删除接口
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/3/de21624f2d0d3dafde085dafaa226743.html

.. automethod:: Client.delete_menu

个性化菜单接口
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/0/c48ccd12b69ae023159b4bfaa7c39c20.html

.. automethod:: Client.create_custom_menu
.. automethod:: Client.delete_custom_menu
.. automethod:: Client.match_custom_menu

获取自定义菜单配置接口
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/14/293d0cb8de95e916d1216a33fcb81fd6.html

.. automethod:: Client.get_custom_menu_config

消息管理
------------

客服接口
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html
发送卡券接口暂时未支持。可自行实现。

.. automethod:: Client.add_custom_service_account
.. automethod:: Client.update_custom_service_account
.. automethod:: Client.delete_custom_service_account
.. automethod:: Client.upload_custom_service_account_avatar
.. automethod:: Client.get_custom_service_account_list
.. automethod:: Client.get_online_custom_service_account_list
.. automethod:: Client.send_text_message
.. automethod:: Client.send_image_message
.. automethod:: Client.send_voice_message
.. automethod:: Client.send_video_message
.. automethod:: Client.send_music_message
.. automethod:: Client.send_article_message
.. automethod:: Client.send_news_message
.. automethod:: Client.send_miniprogrampage_message

用户管理
------------

用户分组管理
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/8/d6d33cf60bce2a2e4fb10a21be9591b8.html

.. automethod:: Client.create_group
.. automethod:: Client.get_groups
.. automethod:: Client.get_group_by_id
.. automethod:: Client.update_group
.. automethod:: Client.move_user
.. automethod:: Client.move_users
.. automethod:: Client.delete_group

设置备注名
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/16/528098c4a6a87b05120a7665c8db0460.html

.. automethod:: Client.remark_user

获取用户基本信息
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/1/8a5ce6257f1d3b2afb20f83e72b72ce9.html

.. automethod:: Client.get_user_info
.. automethod:: Client.get_users_info

账户管理
------------
长链接转短链接接口和微信认证事件推送暂未添加，可自行实现。

生成带参数的二维码
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/18/167e7d94df85d8389df6c94a7a8f78ba.html

.. automethod:: Client.create_qrcode
.. automethod:: Client.show_qrcode

获取用户列表
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/12/54773ff6da7b8bdc95b7d2667d84b1d4.html

.. automethod:: Client.get_followers

素材管理
------------

新增临时素材
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/15/2d353966323806a202cd2deaafe8e557.html

.. automethod:: Client.upload_media

获取临时素材
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/9/677a85e3f3849af35de54bb5516c2521.html

.. automethod:: Client.download_media

新增永久素材
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/10/10ea5a44870f53d79449290dfd43d006.html

.. automethod:: Client.add_news
.. automethod:: Client.upload_news_picture
.. automethod:: Client.upload_permanent_media
.. automethod:: Client.upload_permanent_video

获取永久素材
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/12/3c12fac7c14cb4d0e0d4fe2fbc87b638.html

.. automethod:: Client.download_permanent_media

删除永久素材
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/7/2212203f4e17253b9aef77dc788f5337.html

.. automethod:: Client.delete_permanent_media

修改永久图文素材
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/10/c7bad9a463db20ff8ccefeedeef51f9e.html

.. automethod:: Client.update_news

获取素材总数
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/5/a641fd7b5db7a6a946ebebe2ac166885.html

.. automethod:: Client.get_media_count

获取素材列表
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/15/8386c11b7bc4cdd1499c572bfe2e95b3.html

.. automethod:: Client.get_media_list

用户标签管理
------------
详细请参考 https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140837

创建标签
``````````````````````````````
.. automethod:: Client.create_tag

获取公众号已创建的标签
``````````````````````````````
.. automethod:: Client.get_tags

编辑标签
``````````````````````````````
.. automethod:: Client.update_tag

删除标签
``````````````````````````````
.. automethod:: Client.delete_tag

获取标签下粉丝列表
``````````````````````````````
.. automethod:: Client.get_users_by_tag

批量为用户打标签
``````````````````````````````
.. automethod:: Client.tag_users

批量为用户取消标签
``````````````````````````````
.. automethod:: Client.untag_users

获取用户身上的标签列表
``````````````````````````````
.. automethod:: Client.get_tags_by_user

模板消息
------------
.. automethod:: Client.send_template_message


返回码都是什么意思？
--------------------------

参考 https://mp.weixin.qq.com/wiki/10/6380dc743053a91c544ffd2b7c959166.html

48001 -- API Unauthorized
---------------------------

如果你遇到了这个错误，请检查你的微信公众号是否有调用该接口的权限。
参考： https://mp.weixin.qq.com/wiki/13/8d4957b72037e3308a0ca1b21f25ae8d.html
