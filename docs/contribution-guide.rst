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

如果你希望为 WeRoBot 贡献代码， 请现在 GitHub 上 `Fork <https://github.com/whtsky/WeRoBot>`_ WeRoBot 仓库， 然后在 ``develop`` 分支上开一个新的分支。

.. note:: ``master`` 分支存放着 WeRoBot 最新 release 版本的代码。 所有的开发工作都应该在 ``develop`` 分支上展开

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
请遵循 ``PEP8`` 标准进行代码书写。

https://www.python.org/dev/peps/pep-0008/

为了统一代码风格我们推荐使用 ``flake8`` 进行代码风格检查, 并为代码提交添加钩子。 ::

    # Install git hook for flake8.
    flake8 --install-hook
    # flake8 will automatically run before commit.

添加钩子之后会在每次代码提交时运行 ``flake8`` 进行检查。

若要单独运行 ``flake8``。 ::

    # Run flake8 immediately.
    flake8 werobot

测试
~~~~~~~~~~~
在代码提交之前, 请先运行本地的测试。每次提交之后会有在线的 CI 运行更多版本兼容性的测试, 请密切关注测试结果。 ::

    # Run tests locally.
    python setup.py test

当然也可以使用 tox 在本地运行多版本的兼容性测试。 ::

    # Run multi-version tests locally.
    tox

如果你的 Pull Request 添加了新的模块或者功能，请为这些代码添加必要的测试。 所有的测试文件都在 tests 文件夹下。

当一切开发完成之后, 可以发 Pull Request 到 ``develop`` 分支, 我们会为你的代码做 Review。同时 CI 也会自动运行测试。

.. note:: 我们只会 Merge 通过了测试的代码。

如果一切没有问题, 我们将合并你的代码到 ``develop`` 分支, 并最终发布在 ``master`` 分支的稳定版本。
