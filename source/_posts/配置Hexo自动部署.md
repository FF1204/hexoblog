---
title: 配置Hexo自动部署
date: 2019-06-17 07:29:08
tags:
    - hexo
---

# 配置 Hexo 自动生成并部署到 Github 和 Coding

使用 Hexo 时间长了，总觉得还要自己生成和部署一下很麻烦，于是就想是否有办法只保留Hexo的源码部分，
生成HTML的功能交给CI工具自动完成，这样本地也不必安装 Hexo 的运行环境，之专注写 markdown 格式
的文章就可以了。至于预览，可以交给 VSCode 的 markdown preview enhance 插件去完成。

代码托管工具使用 Github 和 码云，两个都是使用 Git, 而且都支持 Pages 服务。使用外网的时候访问Github
的 Pages 服务， 使用国内网络的时候访问码云的 Pages 服务。

CI工具使用 [travis](https://travis-ci.org/), 它可以关联 Github 代码仓库并且在 Github 仓库有更新的
时候自动触发 CI 任务的执行。

配置完成之后，实现的效果是：本地写完文章之后，push到github或者码云，都会触发CI自动生成博客的HTML网站，
并强制推送到 Github 和 码云的 Pages 仓库中，实现二者的同步更新。

## travis 配置

### 1. 创建文件 `.travis.yml`

在需要触发CI任务的仓库 `.git` 同级的目录下创建 `.travis.yml` 文件， 内容如下：

```shell
language: node_js # 编译语言、环境

sudo: required # 需要管理员权限

dist: xenial # 指定 CI 系统版本为 Ubuntu16.04 LTS

node_js: stable #Node.js 版本

branches:
  only:
    - hexo # 只有hexo分支检出更改才触发CI

before_install: 
  - export TZ='Asia/Shanghai' #配置时区为东八区UTC+8
  - npm install hexo-cli # 安装 hexo
  - sudo apt-get install libpng16-dev # 安装 libpng16-dev CI编译出现相关报错时请取消注释

install:
  - npm install # 安装依赖

script: # 执行脚本，清除缓存，生成静态文件
  - hexo clean
  - hexo generate

after_script:
    - cd ./public
    - git config user.name $GIT_NAME
    - git config user.email $GIT_EMAIL
    - git init .
    - git add .
    - git commit -m "travis auto deploy"
    - git push --force --quiet "https://[username]:[password]@gitee.com/[username]/hexoblog.git" master:master

deploy:
  provider: pages
  skip_cleanup: true # 跳过清理
  local_dir: public # 需要推送到Github的静态文件目录 
  name: $GIT_NAME # 用户名变量
  email: $GIT_EMAIL # 用户邮箱变量
  github_token: $GITHUB_TOKEN # GitHub Token变量
  keep-history: true # 保持推送记录，以增量提交的方式
  target-branch: master # 推送的目标分支 local_dir->>master分支
  on:
    branch: hexo # 工作分支
```

Travis CI 会检测代码仓中的 `.travis.yml` 文件， 检测到就触发构建任务。

### 注册 travis 账号

使用 Github 账号登录 travis 选择需要自动触发CI的代码仓库，将上面脚本中的 `$xxx` 变量名称和值设置成环境变量。
这样就完成了Github 上自动CI的配置。

## 码云上的配置

travis 上可以自动关联 Gihub, 但是无法自动关联码云。 我们使用webhook功能在码云上关联 Travis。
