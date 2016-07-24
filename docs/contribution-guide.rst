贡献指南
==========
欢迎所有人为 WeRoBot 贡献。如果你打算为 WeRoBot 项目贡献代码, 请仔细阅读这份贡献指南。

贡献流程
----------
若要贡献代码, 请注意使用 Github 的 workflow 。

标准的做法应该先 Fork 这个项目到自己的 Repo, 然后从 ``develop`` 分支创建一个新的分支。
当一切开发完成之后, 可以发 Pull Request 到 develop 分支, 我们会为你的代码做 Review。同时 CI 也会为合并之后的分支运行测试。

如果一切没有问题, 我们将合并你的代码到 develop 分支, 并最终发布在 master 分支的稳定版本。

环境搭建
----------
建议使用 virtualenv 创建虚拟环境进行开发, 然后安装开发环境需要的 packages。
关于 Python 版本, 推荐使用 Python 3.5 进行开发。 ::

    # virtualenv is highly recommended.
    virtualenv venv
    # Activate virtualenv.
    source venv/bin/activate
    # Install dev packages.
    pip install -r dev-requirements.txt

代码风格
----------
请遵循 PEP8 标准进行代码书写。

https://www.python.org/dev/peps/pep-0008/

为了统一代码风格我们强制使用 flake8 进行检查。 ::

    # Install git hook for flake8.
    flake8 --install-hook
    # flake8 will automatically run before commit.

添加钩子之后会在每次代码提交时运行 flake8 进行检查。

测试
----------
在代码提交之前, 请先运行本地的测试。每次提交之后会有在线的CI运行更多版本兼容性的测试, 请密切关注测试结果。 ::

    # Run tests locally.
    python setup.py test

当然也可以使用 tox 在本地运行多版本的兼容性测试。 ::

    # Run multi-version tests locally.
    tox

另外请为自己新添加的模块或者功能编写测试代码, 所有的测试文件都在 tests 文件夹下。


