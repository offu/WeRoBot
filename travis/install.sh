#!/usr/bin/env bash

brew install pyenv
brew outdated pyenv || brew upgrade pyenv
brew install libffi
brew install ncurses
brew install zlib
eval "$(pyenv init -)"
for version in $PYTHON_VERSION
  do
    pyenv install $version -s
  done
pyenv local $PYTHON_VERSION

pip install --upgrade pip wheel

brew install redis
brew services start redis
# New mongodb's dependency on python@2 can cause conflicts.
# So let's fallback to mongodb@3.4.
brew install mongodb@3.4
brew services start mongodb@3.4
brew install mysql
brew services start mysql

brew install openssl
python --version
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include -I$(xcrun --show-sdk-path)/usr/include" pip install -r dev-requirements.txt
export DATABASE_MYSQL_USERNAME="root"
export DATABASE_MYSQL_PASSWORD=""
mysql -u $DATABASE_MYSQL_USERNAME -e "CREATE DATABASE IF NOT EXISTS werobot;"
