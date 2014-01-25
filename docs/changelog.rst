Changelog
=============

Version 0.5.0
----------------

+ Add ``werobot.client``
+ Add ``werobot.config``
+ Rewrite ``werobot.message``
+ Friendly 403 page
+ Improved server support
+ Drop ``werobot.testing.make_text_message``
+ Drop ``werobot.testing.make_image_message``
+ Drop ``werobot.testing.make_location_message``
+ Drop ``werobot.testing.make_voice_message``
+ Drop ``werobot.testing.WeTest.send``
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
