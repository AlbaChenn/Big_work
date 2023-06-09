# big_work System
基于Django的商城管理系统

1. 本系统使用mysql数据库
2. 先进入mysql数据库客户端，创建数据库：dailyfresh_db，数据库编码：utf8
3. settings.py 配置数据库连接参数，将数据库用户名、密码、端口，配置为运行电脑安装的mysql数据库参数
4. 打开命令行窗口，进入工程根目录，运行如下命令，自动创建数据库表
>>>cd big_work
>>>python manage.py makemigrations app
>>>python manage.py migrate
