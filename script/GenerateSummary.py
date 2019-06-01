# -*- coding:utf-8 -*-
import os
import sys

# 配置文件
book_name = 'bookroot'              # 书籍名称
summary_name = 'summary.markdown'   # 目录文件名称

"""
生成gitbook使用的summary.md文件
"""
cur_path = os.path.abspath(__file__)
cur_folder = os.path.dirname(cur_path)
root_folder = os.path.dirname(cur_folder)
book_folder = os.path.join(root_folder, book_name)
summary_path = os.path.join(book_folder, summary_name)
out_console = sys.stdout
out_file = open(summary_path,'w')
sys.stdout = out_file
 
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        dir_indent = "    " * (level-1) + "* "
        file_indent = "    " * level + "* "
        if level and not len(dirs) == 0:
            print('{}{}'.format(dir_indent, os.path.basename(root)))
        exts = [os.path.splitext(f)[1] for f in files]
        if '.md' in exts:
            for f in files:
                f_name = os.path.splitext(f)[0]
                f_path = os.path.join(root,f).replace(startpath,'').lstrip('\\')
                print('{}[{}]({})'.format(file_indent, f_name, f_path))
 
list_files(book_folder)
out_file.close()
sys.stdout = out_console

end = 10
