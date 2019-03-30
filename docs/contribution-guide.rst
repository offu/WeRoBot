贡献指南
===========================

有许多种为 WeRoBot 做贡献的方式， 包括但并不仅限于

+ `上报 bug <https://github.com/whtsky/WeRoBot/issues/new?labels=bug>`_
+ `提交 Feature Request <https://github.com/whtsky/WeRoBot/issues/new?labels=Feature Request>`_
+ :ref:`贡献代码`
+ 加入 WeRoBot QQ 群(283206829) 帮助解答问题
+ 把 WeRoBot 安利给你周围的人 :)

贡献代码
----------

如果你希望为 WeRoBot 贡献代码， 请现在 GitHub 上 `Fork <https://github.com/whtsky/WeRoBot>`_ WeRoBot 仓库， 然后在 ``master`` 分支上开一个新的分支。

如果你的贡献的代码是修复 Bug ， 请确认这个 Bug 已经有了对应的 Issue （如果没有， 请先创建一个）； 然后在 Pull Request 的描述里面引用这个 Bug 的 Issue ID ， 就像这样(假设 Issue ID 为 153) ::

    Fix #153

环境搭建
~~~~~~~~~~~
建议使用 ``virtualenv`` 创建虚拟环境进行开发, 然后安装开发环境需要的 packages。
关于 Python 版本, 推荐使用 Python 3.6 进行开发。

如果使用的是 3.x 版本 ::

    # Python 3.5
    python -m venv venv

如果是其他版本 ::

    # virtualenv is highly recommended.
    virtualenv venv
    # Activate virtualenv.
    source venv/bin/activate
    # Install dev packages.
    pip install -r dev-requirements.txt

代码风格
~~~~~~~~~~~
我们使用 `yapf <https://github.com/google/yapf>`_ 进行代码格式化。
在提交代码之前，请格式化一下你的代码 ::

    # Install yapf
    pip install yapf
    # format code
    yapf -i -p -r werobot/ tests/ *.py

你也可以 `安装 yapf Pre-Commit Hook <https://github.com/google/yapf/tree/master/plugins#git-pre-commit-hook>`_ 来自动进行代码格式化工作。

测试
~~~~~~~~~~~
在代码提交之前, 请先运行本地的测试。每次提交之后会有在线的 CI 运行更多版本兼容性的测试, 请密切关注测试结果。 ::

    # Run tests locally.
    python setup.py test

当然也可以使用 tox 在本地运行多版本的兼容性测试。 ::

    # Run multi-version tests locally.
    tox

如果你的 Pull Request 添加了新的模块或者功能，请为这些代码添加必要的测试。 所有的测试文件都在 tests 文件夹下。

当一切开发完成之后, 可以发 Pull Request 到 ``master`` 分支, 我们会为你的代码做 Review。同时 CI 也会自动运行测试。

.. note:: 我们只会 Merge 通过了测试的代码。
