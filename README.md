## 在线教育平台  


## 主要功能：  

* 账号注册、激活、登录、密码找回等功能。
* 个人中心页面支持`个人信息`、`我的课程`、`我的收藏`、`我的消息`管理。
* 首页轮播图、机构、课程展示。
* 支持讲师、课程、机构选项的全局搜索。
* 侧边栏提供热门课程推荐、机构/讲师排名、课程咨询。
* 支持授课机构按类别、按地区筛选，按学习人数、课程数排序。

## 环境

* Python 3.7.2
* Django 2.2(LTS)
* MySQL 5.7.22
* redis64-3.0.501


### 快速启动该项目

1.安装Python 3.7.2 
2.安装MySQL 5.7 并创建mxonline数据库

3.安装redis服务

    mysql -u root -p
    Enter password: 
    mysql> create database online;

3.建立虚拟环境（可省略）

    python3 -m venv venv
    source venv/bin/activate

4.项目下载

    git clone git@github.com:hongcongjin/MxOnline.git
    cd MxOnline

5.安装Django 2.2

    pip install django==2.2

6.安装其他依赖包

    pip install -r requirements.txt 
    # 如有个别包不能安装，请下载源码，放到extra_apps里，并在setting里配置
    # pillow包的版本，需要查看官网根据自己的系统选定版本

7.修改配置

```python
# setting.py
# 将数据库密码换成自己的
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'mxonline',
    'USER': 'root',
    'PASSWORD': '12345',
    'HOST': '127.0.0.1',
    'POST': '3306',
    }
}
```

8.创建数据表

    python manage.py makemigrations
    python manage.py migrate

9.运行项目

    python manage.py runserver

## 生产环境使用的是阿里云(ESC+OOS)实现

部署使用的是centos7+nginx+uWSGI

nginx在处理请求是异步非阻塞的，能支持更多的并发连接。

uWSGI具有超快的性能，低内存和多app管理等优点，能够将用户的访问请求与应用app隔离，实现真正的部署。

## 总结

1，项目在部署的时候虽然使用了高并发的处理，但是在django程序中并未对程序进行优化。没有充分发挥Redis的优点。

2，在某些视图中存在一些耗时操作，例如发送短信验证码等，可以使用异步任务去完成。将耗时任务解耦出来，不影响主任务的进行。(优化点1)

3， 如果Redis服务端需要同时处理多个请求，加上网络延迟，那么服务端利用率不高，大大的降低Redis的效率。使用对队列进行优化。(优化点2)

4，队友一些静态化的图片，存在服务器中，会造成程序内存占用过高，图片安全性，容灾性很低。可以采用FastDFS对静态图片进行存储管理。FastDFS可以帮助我们搭建一套高性能的文件服务器集群，并提供文件的上传，下载服务。(优化点3)

5，在实现商品搜索上使用了like关键字，但是like关键字效率极低，查询多个字段，使用like关键字也不方便。 我们可以引入全文检索的方案和搜索引擎配合来实现商品搜索。 Elasticsearch 是用 Java 实现的，开源的搜索引擎 。在Django使用 Haystack 对接搜索引擎的框架，搭建了用户和搜索引擎之间的沟通桥梁 。 (优化点4)

6，使用容器化方案Docker来实现FastDFS和Elasticsearch 。简化相同而且繁琐的工作。(优化点5)

7，在项目迭代更新之后，带来的用户量不断增加， 首页访问频繁，而且查询数据量大，其中还有大量的循环处理。  用户访问首页会耗费服务器大量的资源，并且响应数据的效率会大大降低。 使用页面静态化来处理。静态化页面: 减少数据库查询次数。  提升页面响应效率。京东使用的就是页面静态化。(优化点6)

8， 对于首页的静态化，考虑到页面的数据可能由多名运营人员维护，并且经常变动，所以将其做成定时任务，即定时执行静态化。使用Django的定时任务，对首页的静态化进行定时更新。(优化7)

9，MySQL的读写分离，随着用户的增加，访问数据也随之增加，考虑到MySQL在性能方面大大的不如redis。 我们选择使用MySQL读写分离实现。涉及内容包括主从同步和Django实现MySQL读写分离。(优化点8)

10， 在日后有条件的情况下对redis和MySQL都进行集群配置，增加用户体验。

