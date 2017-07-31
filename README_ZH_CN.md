# 概览

一个简单的dashboard,集成了[cobbler](http://cobbler.github.io/manuals/quickstart/) && [saltstalk](https://github.com/saltstack), 使用了flask + bootstrap技术栈。

dashboard的前端模板部分来自[salimhamed/dashboard](https://github.com/salimhamed/dashboard)。


# 安装

1. Clone the repository

  ```
  git clone https://github.com/salimhamed/dashboard.git
  ```

2. Create a virtualenv in the project directory

  ```
  cd dashboard
  virtualenv venv
  source venv/bin/activate
  ```

3. Install dependencies

  ```
  pip install -r requirements.txt
  ```

4. Create database

  ```
  ./manage db_rebuild
  ```

5. Run tests

  ```
  ./manage.py test
  ```

6. Start development server

  ```
  ./manage.py runserver
  ```