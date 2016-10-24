错误页面
==========
``WeRoBot`` 自带了一个错误页面，它将会在 Signature 验证不通过的时候返回错误页面。

定制错误页面
------------
如果你想为 ``WeRoBot`` 指定 Signature 验证不通过时显示的错误页面，可以这么做: ::

    @robot.error_page
    def make_error_page(url):
        return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url
