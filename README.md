# bilibili_score简单说明
爬取b站2000-2018年内所有番剧分数并保存到mysql数据库中
新增支持数据导出csv文件功能
在线地址 ||
http://45.32.14.42:8002/index/
更新番剧分数
htttp://45.32.14.42:8002/collect
...



运行步骤

1.新建mysql用户及密码

```
mysql -u root -p
# 以root账户登录会提示你输入密码
create user wzg@'%' identified by 'password';
# 新建用户wzg 密码password
```

本次新建用户民是wzg

2.新建bangumi数据库

```
create database bangumi;
```

3.将bangumi权限赋予wzg

```
grant all privileges on bangumi.* to wzg;
```

4.开启80端口

```
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload
```

5.生成表

```
python manage.py makemigrations
python manage.py migrate
```

