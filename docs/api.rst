API
==========

.. module:: werobot

应用对象
------------

.. module:: werobot.robot
.. autoclass:: BaseRoBot
    :members:
.. autoclass:: WeRoBot
    :members:

配置对象
------------

.. module:: werobot.config
.. autoclass:: Config
    :members:

Session 对象
------------
.. module:: werobot.session.sqlitestorage
.. autoclass:: SQLiteStorage

.. module:: werobot.session.filestorage
.. autoclass:: FileStorage

.. module:: werobot.session.mongodbstorage
.. autoclass:: MongoDBStorage

.. module:: werobot.session.redisstorage
.. autoclass:: RedisStorage

.. module:: werobot.session.saekvstorage
.. autoclass:: SaeKVDBStorage

.. module:: werobot.session.mysqlstorage
.. autoclass:: MySQLStorage

.. module:: werobot.session.postgresqlstorage
.. autoclass:: PostgreSQLStorage

log
------------
.. module:: werobot.logger
.. autofunction:: enable_pretty_logging
