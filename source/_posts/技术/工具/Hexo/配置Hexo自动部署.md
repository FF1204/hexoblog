---
title: Hexo博客配置攻略
date: 2019-06-17 07:29:08
toc: true
copyright: true
tags:
    - hexo
---

## 基础知识

- **站点配置文件**位于：`hexoblog/_config.yml`

- **主题配置文件**位于：`hexoblog/themes/theme_name/_config.yml`

- **安装依赖** : 在`hexoblog/package.json`中添加要安装的依赖，然后在站点根目录执行`npm install`

- **自定义站点配置文件** : 使用`--config config_file.yml`可以使用自己定义的站点配置文件启动

<!-- more -->

## 自动构建

> 要实现的功能
> - 博客源代码托管在Github平台和Gitee平台
> - 利用Github, Gitee的Pages服务托管生成的HTML网页
> - 每当提交到Github的时候触发自动构建，自动生成Hexo博客部署到Github和Gitee
> - Github和Gitee部署不同主题的网页

代码托管网站使用[Github]()和[Gitee](), 二者都提供`Pages`服务。自动构建工具选择[travis](), 它可以自动关联到Github中的仓库上。

我本地博客路径为`hexoblog`, Github仓库为`hexoblog`, 共有两个分支，`hexo`为主分支，托管博客源码, `master`为`pages`分支，托管博客生成的HTML文件。 Gitee的布局和Github一样，也有一个`hexoblog`仓库，两个分支。我在Github上部署主题为wikitten的博客，在Gitee上部署主题为next的博客。

要实现上述功能，只需要配置好几个配置文件就可以了。

在站点根目录新增`.travis.yml`文件，内容如下：

```shell
language: node_js # 编译语言、环境

sudo: required # 需要管理员权限

dist: trusty # 指定 CI 系统版本为 Ubuntu16.04 LTS

node_js: 
    - '8' #Node.js 版本

branches:
  only:
    - hexo # 只有hexo分支检出更改才触发CI

before_install: 
  - export TZ='Asia/Shanghai' #配置时区为东八区UTC+8
  - npm install hexo-cli > /dev/null # 安装 hexo
  - git config user.name $GIT_NAME
  - git config user.email $GIT_EMAIL
  - sed -i'' "s~xxx_gitee_xxx~${GITEE_TOKEN}~" _config.next.yml # 配置部署用到的TOKEN
  - sed -i'' "s~xxx_github_xxx~${GITHUB_TOKEN}~" _config.wikitten.yml
  #  - sudo apt-get install libpng16-dev # 安装 libpng16-dev CI编译出现相关报错时请取消注释

install:
  - npm install # 安装依赖

script: # 执行脚本，清除缓存，生成静态文件
  - hexo clean
  - hexo g -d --config _config.next.yml
  - hexo clean
  - hexo g -d --config _config.wikitten.yml
```
以上脚本是travis自动构建需要读取的脚本，里面使用的GIT_NAME, GIT_EMAIL, GITEE_TOKEN, GITHUB_TOKEN是环境变量，可以在travis的网站中配置具体的值，如果你不介意暴露这些信息，也可以直接写具体的值。

`xxx_gitee_xxx` 是占位符，`sed -i'' "s~xxx_gitee_xxx~${GITEE_TOKEN}~" _config.next.yml`的含义是替换`_config.next.yml`中的`xxx_gitee_xxx`为在travis网站中设置的环境变量GITEE_TOKEN, 这样可以避免自己的密码暴露在脚本中。Github 和 Gitee 生成 Token的方法可以参考官方文档。

`hexo g -d --config _config.next.yml`是使用`_config.next.yml`生成网站并部署，通过使用这样的命令，我们可以生成多个主题的网站。

复制**站点配置文件**重命名为`_config.next.yml`并修改如下配置：

```
theme: next
# theme: Wikitten

# Deployment
## Docs: https://hexo.io/docs/deployment.html
deploy:
    type: git
    repo: https://FF1204:xxx_gitee_xxx@gitee.com/FF1204/hexoblog.git
    branch: master
    message: travis-ci commit
```

指定主题为`next`主题，deploy 为部署到Giteee的hexoblog仓库的master分支。

复制**站点配置文件**重命名为`_config.wikitten.yml`并修改如下配置：

```
theme: Wikitten

# Deployment
## Docs: https://hexo.io/docs/deployment.html

deploy:
    type: git
    repo: https://xxx_github_xxx@github.com/FF1204/hexoblog.git
    branch: master
    message: travis-ci commit    
```

指定主题为`Wikitten`主题，deploy 为部署到 Github 的 hexoblog 仓库的 master 分支。

使用Github账号登陆travis网站，打开hexoblog仓库的自动构建选项，即可开始自动构建。(上面提到的主题的安装可以搜索对应的官网)

## 高级功能

熟悉主题的构造之后，可以直接更改主题文件实现一些主题本来不具备的功能。

### 添加聊天功能

DaoVoice提供了一个功能不错的在线聊天功能，只需要到网站中添加一段代码，便可生成一个聊天图标，你使用微信便可以直接和浏览你网页的人互动。

注册Daovice网站，开通自己的账户，你会获得自己的一段代码和一个appid.

以next主题为例，在themes/next/layout/_partials/head.swig最后添加

```script
{% if theme.daovoice %}
  <script>
  (function(i,s,o,g,r,a,m){i["DaoVoiceObject"]=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;a.charset="utf-8";m.parentNode.insertBefore(a,m)})(window,document,"script",('https:' == document.location.protocol ? 'https:' : 'http:') + "//widget.daovoice.io/widget/0f81ff2f.js","daovoice")
  daovoice('init', {
      app_id: "{{theme.daovoice_app_id}}"
    });
  daovoice('update');
  </script>
{% endif %}
```

然后在next的主题配置文件中添加

```
# Online contact
daovoice: true
daovoice_app_id: xxxxxx
```

把注册账户的时候获得的app_id填在配置文件中。

### 网站底部字数统计

安装插件：

```
npm install hexo-wordcount --save
```

在`hexoblog/themes/next/layout/_partials/footer.swig`尾部添加：

```
<div class="theme-info">
  <div class="powered-by"></div>
  <span class="post-count">博客全站共{{ totalcount(site) }}字</span>
</div>
```

## 主题推荐

### next

next 是一个极简的主题，使用人数多，教程丰富，各种DIY非常多，建议使用这个主题，有问题容易解决，而且现在还在更新。

### wikitten

Wikitten是一个可以自动按照文件夹层次分类的主题，而且展示的时候也是按照文件夹的层次分类展示的，比较符合我的多级分类的需要。

### Maupassant

非常简单的一个模板，简单到渣，但是很优秀

## hexo 博客推荐

推荐一些值得参考的博客样例。

- next 主题配置大全：https://www.jianshu.com/p/f054333ac9e6
