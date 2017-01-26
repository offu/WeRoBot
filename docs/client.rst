``WeRoBot.Client`` —— 微信 API 操作类
=====================================

.. module:: werobot.client

.. autoclass:: Client

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