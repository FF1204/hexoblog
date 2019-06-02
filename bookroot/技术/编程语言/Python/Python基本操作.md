---
title: Python基本操作
toc: true
tags:
  - Python
date: 2019-06-02 15:40:32
---

## 常用内置方法

```python
string.split(sep, count)               # 以sep分割string最多count次
string.strip(sep)                      # 删除string开始和结束的sep
string.lstrip(sep)
string.rstrip(sep)
string.count(pattern)                  # pattern 在 string 中出现的次数
string.find(pattern start, end)        # pattern 第一次在string出现的位置,没有找到返回-1
```
## OS

os 模块提供了非常丰富的方法用来处理文件和目录

```python
import os

os.chdir(path)          # 改变当前工作目录

os.path.exists(path)    # 是否存在
os.path.abspath(path)   # 绝对路径
os.apth.basename(path)  # path的最后一级
os.path.dirname(path)   # path的上一级
os.path.isfile(path)    # 是否文件
os.path.isdir(path)     # 是否文件夹
os.path.splitext(path)  # 分割成路径和文件扩展名
```

## shutil

shutil 是对 OS 模块中文件和文件夹操作的增强，提供了很多高级功能

```python
import shutil

shutil.rmtree(path)             # 删除目录
shutil.copytree(src, dst)       # 拷贝文件夹，dst必须是不存在的目录
shutil.move(src, dst)           # 递归的移动文件, dst必须是不存在的目录
```

## pickle

python 变量的持久化存储，例如存储一个深度学习模型。

```python
import pickle

fd = open(path, 'wb')
pickle.dump(var, fd)        # 保存 var 到文件

fd = open(path, 'rb')
var = pickle.load(fd)             # 从文件中加载变量
```

## 函数式编程

**map(function, list)**

在list中对每个元素应用函数function**, 相当于
`[function(i) for i in list]`

**reduce(function, list)**

在list中的每两个元素递归应用function，例如求一个数列的和
`reduce(add(a,b),[1.2.3.4.5])`