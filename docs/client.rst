``WeRoBot.Client`` —— 微信 API 操作类
=====================================

.. module:: werobot.client

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

获取用户列表
``````````````````````````````
详细请参考 http://mp.weixin.qq.com/wiki/12/54773ff6da7b8bdc95b7d2667d84b1d4.html

.. automethod:: Client.get_followers
