# -*- coding:utf-8 -*-
import os

"""
使用pandoc生成HTML, PDF, EPUB电子书
"""

file = r'D:\FF120\workspace\book\bookroot\心理学\记忆方法\代码记忆法.md'
out_file = 'D:\FF120\workspace\book\bookroot\心理学\记忆方法\代码记忆法.html'

cur_path = os.path.abspath(__file__)
cur_folder = os.path.dirname(cur_path)
stylesheet_folder = os.path.join(cur_folder, 'stylesheet')
stylesheet_file = os.path.join(stylesheet_folder, 'github-markdown.css')

cmd = "pandoc {} --self-contained -c {} -V mainfont=\"SimSun\" -o {}".format(file, stylesheet_file, out_file)

os.system(cmd)

end = 10