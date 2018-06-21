# [中文版本](https://github.com/zhangchenchen/supervisors/blob/master/README_ZH_CN.md)

# Overview

This is a simple dashboarding application integrated with [cobbler](http://cobbler.github.io/manuals/quickstart/) && [saltstalk](https://github.com/saltstack), built using Flask and Bootstrap.

The dashboard template is from [salimhamed/dashboard](https://github.com/salimhamed/dashboard).


# Installation

1. Clone the repository

  ```
  git clone git@github.com:zhangchenchen/supervisors.git
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


