**customer_manage**

# FAQ

### 如何准备NodeJS环境？ ###

如果没有安装cnpm，安装cnpm：
```
npm install -g cnpm --registry=https://registry.npm.taobao.org 
```

安装必要的包：
```
cnpm install supervisor -g
cnpm install -g bunyan
cnpm install
```

### 如何在本地开发调试？ ###

答：初次搭建环境，按如下步骤：
1. 在mysql中创建`panda`数据库: `create database panda default character set utf8 `;
1. 将`panda`数据库授权给`panda`用户：`grant all on panda.* to 'panda'@localhost identified by 'weizoom'`
1. 执行 `rebuild.bat`，初始化数据库
1. 启动 `start_bundle_server.bat`
1. 启动 `start_service.bat | bunyan`
1. 访问 `http://127.0.0.1:4180/account/login/`
1. 以 `manager:test`登陆系统



### 运行起来后，想系统正常使用，请看如下内容 ###
第一步：

       首先将weapp库的一个账户(account_user_profile表)其中某一条记录的webapp_type字段修改成2，
       注意这条记录的user_id

第二步：

       打开panda的配置文件panda/settings.py找到PRODUCT_POOL_OWNER_ID配置，将'develop' == MODE
       的配置中这个变量配置成第一步中的user_id
