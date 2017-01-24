部署
=====================

在独立服务器上部署
----------------------
当你运行 `werobot.run` 的时候，你可以通过传递 `server` 参数来手动指定使用的服务器 ::

    import werobot

    robot = werobot.WeRoBot(token='tokenhere')

    @robot.handler
    def echo(message):
        return 'Hello World!'

    robot.run(server='gevent', port=12233)

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

请注意， ``werobot.run`` 是跑在 **非守护进程模式下** 的——也就是说，一旦你关闭终端，进程就会自动退出。

我们建议您使用 `Supervisor <http://supervisord.org/>`_ 来管理 WeRoBot 的进程。

配置文件样例： ::

    [program:wechat_robot]
    command = python /home/whtsky/robot.py
    user = whtsky
    redirect_stderr = true
    stdout_logfile = /home/whtsky/logs/robot.log

使用 Nginx 进行反向代理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

微信服务器只支持80端口的机器人——显然，你的服务器上不会只跑着一个微信机器人。对于这种情况，我们建议您使用 Nginx 来进行反向代理。

配置文件样例： ::

    server {
        server_name example.com;
        listen 80;

        location / {
            proxy_pass_header Server;
            proxy_redirect off;
            proxy_pass http://127.0.0.1:12233;
        }
    }

.. note:: 在这个例子中， WeRoBot 的端口号为 12233。你应该在微信管理后台中将服务器地址设为 ``http://example.com`` 。

在SAE上部署
-----------------
> 新浪云上的 Python 应用的入口为 index.wsgi:application ，也就是 index.wsgi 这个文件中名为 application 的 callable object。

所以，假设你在 `robot.py` 中使用了 WeRoBot ::

    # filename: robot.py
    import werobot

    robot = werobot.WeRoBot(token='tokenhere')


    @robot.handler
    def echo(message):
        return 'Hello World!'

你需要再创建一个 `index.wsgi` 文件， 里面写 ::

    import sae
    from robot import robot


    application = sae.create_wsgi_app(robot.wsgi)

然后按照 SAE 的要求编写好`config.yaml`文件就可以了。
可以参考 `示例仓库 <https://github.com/whtsky/WeRoBot-SAE-demo>`_

如果你希望使用 SAE 提供的 KVDB 存储 Session 数据， 可以选择 :class:`werobot.session.saekvstorage` 作为你的 Session Storage.:w

