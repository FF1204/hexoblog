# -*- coding: utf-8 -*-
import os
import re

# 配置文件    
book_name = r'bookroot'
hexo2github = True
backup_folder = 'backup_book'


"""
把markdown里面的图片链接由 hexo 格式转换成 github 格式

hexo 格式： !(a.png)[a.png]
github 格式： !(a.png)[title/a.png]

主要区别是相差一个目录名称
"""
def checkHexoFolder(root, dirs, files):
    """
    检查是否符合Hexo博客中每个.md文件都对应有一个同名的文件夹存放对应的资源
    如果有不对应的，创建一个与文件名同名的文件夹
    """
    for file in files:
        file_name = file.rstrip('.md')
        if file_name not in dirs:
            os.mkdir(os.path.join(root,file_name))
    
    return

def toHexo(root, file):
    """
    把内容中的图片链接换成Hexo格式
    """
    fd = open(os.path.join(root, file), 'r', encoding='utf-8')
    content = fd.readlines()
    fd.close()
    img_pattern = r'^(!\[.*\])\s*(\()(.*)(\))'
    pattern = re.compile(img_pattern)
    for i, line in enumerate(content):
        line = line.lstrip()
        match = re.match(pattern, line)
        if match:
            edit_line = match.group(3)
            file_name = file.rstrip('.md')
            if edit_line.count(file_name) > 0:
                edit_line = edit_line.lstrip().lstrip(file_name).lstrip('\\')
                new_line = match.group(1) + \
                        match.group(2) + \
                        edit_line + \
                        match.group(4) + '\n'
            content[i] = new_line
    fd = open(os.path.join(root, file), 'w', encoding='utf-8')
    fd.writelines(content)
    fd.close()

def toGitHub(root, file):
    """
    把内容中的图片链接换成Github格式
    """
    fd = open(os.path.join(root, file), 'r', encoding='utf-8')
    content = fd.readlines()
    fd.close()

    img_pattern = r'^(!\[.*\])\s*(\()(.*)(\))'
    pattern = re.compile(img_pattern)
    for i, line in enumerate(content):
        line = line.lstrip()
        match = re.match(pattern, line)
        if match:
            edit_line = match.group(3)
            file_name = file.rstrip('.md')
            if edit_line.count(file_name) > 0:
                continue
            else:
                new_line = match.group(1) + \
                        match.group(2) + \
                        file_name + '\\' + match.group(3) + \
                        match.group(4) + '\n'
            print(content[i])
            content[i] = new_line
    fd = open(os.path.join(root, file), 'w', encoding='utf-8')
    fd.writelines(content)
    fd.close()

def backupDir(dst, src):
    """
    备份文件夹
    """
    import shutil
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return

cur_path = os.path.abspath(__file__)
cur_folder = os.path.dirname(cur_path)
root_folder = os.path.dirname(cur_folder)
book_folder = os.path.join(root_folder, book_name)

# 备份文件
dst = os.path.join(root_folder, backup_folder)
backupDir(dst, book_folder)

# 开始处理
for root, dirs, files in os.walk(book_folder):
    if files and files[0].endswith('.md'): # 有.md文件的视为叶子节点
        checkHexoFolder(root, dirs, files)
        for file in files:
            if hexo2github:
                toGitHub(root, file)
            else:
                toHexo(root, file)

end = 10