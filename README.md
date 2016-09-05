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

第三步：


      先说解决办法，首先给你的weapp账户配置几个自营平台（也可以就一个），记住这几个账户的user_id;
      并且决定好哪个账户是微众家，哪个是商城等。

第四部：

        因为panda是把自己的账户（供货商）和对应供货商的商品同步到weapp，所以一定要保持zeus的启动。
已经决定好了哪个账户分别是什么商城了，记录好你的user_id,查看下边对应关系，在表
self_username_webapp_account中添加几条记录（你决定同步到几个平台就加几条，测试环境，建议1-3个就可以了），
这个表的weapp_account_id字段就是刚才记录的user_id.
sql 例子如下：
insert into self_username_weapp_account (self_user_name, weapp_account_id) values('weizoom_jia', 123)

weizoom_jia      微众家

weizoom_mama      微众妈妈

weizoom_xuesheng  微众学生

weizoom_baifumei  微众白富美

weizoom_shop      微众商城

weizoom_club      微众俱乐部

感兴趣可以看下下边的解释


      第一步中所有的商品同步之后都挂在第一部中的那个账号下，我们把这个webapp_type=2的账户简单看做商品池。
      那么我们同步的商品在其他自营平台显示是怎么映射的啊？请看weapp库的product_pool中间表；
      就是说商品池的商品同步到哪个平台，不同步到哪个平台都是这个表来控制的。
      你也看到了，这个表里有一个woid，这个id是干嘛的啊？就是自应平台对应账户的user_id,那我panda怎么知道这个平台的woid?
       带着问题看panda里边这个表，self_username_webapp_account,这个表是用来映射用户名和woid（weapp的id）的。
       那么为什么会有self_user_name这个字段？这个是什么鬼？是这样的历史遗留问题：前端拿self_user_name这个字段的值，
       匹配的哪个平台，就是说每个平台对应一个slef_username然后，这个平台的user_id(woid)是多少。
