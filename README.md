SharpLite
=========

a light weight desktop app scaffold with C# + SQLite + PetaPoco + django


## 使用 C# + SQLite + PetaPoco + django 快速打造桌面应用程序

### 为什么是 SQLite?
在以前的程序中, 我通常会使用 MySQL. 
如果使用你程序的用户是一个软件小白, 而且远在另一个城市, 那么让她安装和部署 MySQL 将是一场噩梦:
她需要配置服务, 面对一系列莫名其妙的参数, 端口, 环境变量, 等等.
她需要启动服务, 这个过程非常漫长, 而且很可能服务无法启动. 尤其是重装了 MySQL 之后, 服务死活起不来的情况很常见.
她需要执行你的脚本初始化数据库, 而这个脚本很可能因为环境等问题没法运行.
她可能需要导出数据, 便于给你定位错误.
她需要迁移数据, 如果数据库规格发生变化的话.就算是你给她编写了迁移工具, 要正确运行通常也不简单.
...
而使用 SQLite, 上述这些问题都不存在:
不需要安装, 也没有服务, 就是一个文件而已.
不需要初始化数据库, 你可以将做好之后再发布给她.
不需要导出数据, 直接把文件发给你就可以了.
不需要让用户自己迁移数据, 你可以让她把数据库文件发给你, 迁移好之后再发回去.

### 为什么是 PetaPoco?
http://www.toptensoftware.com/petapoco/
用过 NHibernate 的人都会被它的配置感到厌恶吧, 而且因为框架庞太复杂, 学习的成本也比较高.
而 PetaPoco 是一个轻量级的 ORM 框架. 真的很轻量: 它只有PetaPoco.cs一个文件. 
不需要复杂的配置, 不需要安装, 只需要将 PetaPoco.cs 加入到你的项目中即可.
它没有对数据库的访问作过多的包装, 你可以很方便的执行原生 SQL 语句, 然后得到你要的类对象.
因此你可以很自由的使用它, 并且效率相当优异.

### 为什么还有 django?
是的, 你没有看错, 我说的是 python 的 web 开发框架 django.
它和C#以及桌面开发没有半毛钱关系. 使用它是因为它优秀的ORM, 以及内置的 SQLite 支持.
PetaPoco 没有自动生成数据库表格的功能, 而手工创建表格,添加字段的方式,效率实在太低下.
借助 django, 你可以定义数据模型, 然后 manage.py syncdb 一下, 就可以得到对应的数据库表格了.
后期的开发中, 你也可以使用 python 方便的对数据进行各种操作.

### 一点小麻烦
现在, 你可以用django轻松的得到建立好的sqlite数据库. 
PetaPoco 可以支持通过执行 T4 模版, 从数据库表格来生成对应的 C# 类. 
但很遗憾, 目前支持的数据库中还没有 SQLite.
现在, 你需要手工建立类.

### 注意事项

#### 自定义表名
在django中定义models时, 默认的表名是app_model的格式. 这不太符合 C# 的命名习惯, 你可以通过 Meta 自定义:

# -*- coding: utf-8 -*-
from django.db import models
class User(models.Model):
    username = models.CharField()
    password = models.CharField()
    class Meta:
        db_table = 'User'

#### 在开发环境中使用 SQLite     
在 C# 中使用 SQLite, 你需要安装 SQLite 的 .NET 驱动.
这里我使用的是 dotConnect for SQLite Standard (Free)
http://www.devart.com/dotconnect/sqlite/download.html
安装了它之后, 当你在 Properties 的 Settings 中设置连接字符串时, 就可以找到 SQLite Database (dotConnect for SQLite) 的数据提供程序了.        
此外, 你需要在 Preferences 中添加对 Devert.Data 以及 Devert.Data.SQLite 的引用.

#### SQLite 的部署
在用户的电脑上, 你可以让她安装dotConnect for SQLite Standard (Free)来支持 SQLite
不过, 让用户安装东西通常会带来反感或麻烦. 你也可以什么都不用装, 只需要:
将下列 dll 与你的 exe 放在一起:
Devart.Data.SQLite.dll
Devart.Data.dll
antlr.runtime.dll
sqlite3.dll
在你的 app.config 中添加数据提供程序配置:

<?xml version="1.0" encoding="utf-8" ?>
<configuration>
    <configSections>
    </configSections>
    <connectionStrings>
        <add name="SharpLite.Properties.Settings.SQLite" connectionString="Data Source=sqlite.db"
            providerName="Devart.Data.SQLite" />
    </connectionStrings>
    
    <system.data>
    <DbProviderFactories>
      <remove invariant="Devart.Data.SQLite" />
      <add name="dotConnect for SQLite" invariant="Devart.Data.SQLite" description="Devart dotConnect for SQLite" type="Devart.Data.SQLite.SQLiteProviderFactory, Devart.Data.SQLite" />
    </DbProviderFactories>
    </system.data>
    
</configuration>

这个配置很关键, 它能让你的程序找到上述 dll 中的数据提供程序.
如果你没有配置它, 用户点击了你的exe后, 你的程序将运行不起来, 也没有任何错误提示. 
如果不知道原因, 这会是一件相当让人抓狂的事. 
我今天就遇到了, 折腾了好久都没找到原因:( 
最后不得已, 我在需要部署的电脑上安装了 vs2008, 并运行代码, 这才发现问题. 真是欲哭无泪啊T_T!!!

#### 建立数据连接
你可以建立如下的类作为数据库的全局入口:

using PetaPoco;

namespace SharpLite
{
    class DbAccess
    {
        private static Database m_instance = null;

        public static Database GetInstance()
        {
            if (m_instance == null)
            {
                m_instance = new Database("SharpLite.Properties.Settings.SQLite");
            }
            return m_instance;
        }
    }
}

这里用到了 app.config 中定义的连接字符串属性, 也就要用到 System.configuration 模块.
你需要在 Preferences 添加对它的应用, 否则编译会无法通过.

#### PetaPoco 的编译条件
PetaPoco 中用到了 C# 的动态特性, 例如 var 关键字(C# 3.0 引入), 以及 Dynamic 空间(C# 4.0 引入).
像我使用的是 .NET 3.5, 支持 var 关键字没问题, Dynamic 空间则不行. 编译时出现如下错误:
Error	1	The type or namespace name 'Dynamic' does not exist in the namespace 'System' (are you missing an assembly reference?)	
D:\workspace\SharpLite\SharpLite\PetaPoco.cs	1535	45	SharpLite

好在我并不需要为此升级到 .NET 4, PetaPoco 代码中提供了条件编译开关, 用以避免使用 Dynamic 特性.
你只需在项目属性 -> Build -> General -> Confitional compilation symbols 后面的文本框中加入 PETAPOCO_NO_DYNAMIC 即可.
注意 Debug 和 Release 要分别设置.

如果你仍然在使用 .NET 2.0, 那么很遗憾, var 关键字都不支持, PetaPoco 没法使用了. 
这个方案也不适用于你了. 不过, 我还是真诚的建议你: 升级吧:)

### Demo项目
我已将SharpLite项目托管到github, 你可以前去参考: https://github.com/guoqiao/SharpLite
这个项目我也会逐步改进, 作为我采用此种架构的程序的框架代码.
