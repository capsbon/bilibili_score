# bilibili_score简单说明
爬取b站所有番剧分数并保存到mysql数据库中
新增支持数据导出csv文件功能
在线地址 ||
http://score.wangzhigang.org/index/
更新番剧分数
htttp://score.wangzhigang.org/collect
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
python3 manage.py makemigrations
python3 manage.py migrate
```

6.安装所需库

```
pip3 install -r requirements.txt
```

7.修改settings.py添加要部署的主机地址

找到ALLOWED_HOST改为

```
ALLOWED_HOSTS = ['127.0.0.1','45.32.14.42','localhost','score.wangzhigang.org']
```

8.以守护进程运行在80端口

```
nohup python3 manage.py runserver 0:80 &
```

ps.

git本地仓库强行覆盖远程仓库

```
git push origin master -f
```

远程仓库强行覆盖本地

```
git fetch --all  
git reset --hard origin/master 
git pull origin master
```

