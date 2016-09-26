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

       将init_store_name.sql导入mysql或者直接复制到数据库即可，需要使用数据库的root账户登陆数据库。
       更新结果，是将guo这个云伤痛账号更新成商品池特殊账号，jobs更新成自营平台。

如果start_service.bat/sh启动不起来，请检查是否安装MySQLdb（pip install MySQLdb)
