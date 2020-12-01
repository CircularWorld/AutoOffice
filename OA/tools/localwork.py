import os
import shutil
import zipfile
from tkinter import *
from tkinter import ttk
# from tkinter.filedialog import askdirectory
from tkinter import filedialog

import tkinter.messagebox


def selectStartPath():
    path_ = filedialog.askdirectory()
    start_path.set(path_)
    print(path_)


def selectEndPath():
    path_ = filedialog.askdirectory()
    end_path.set(path_)
    print(path_)


def run_function():
    # 获取 起始目录  文件类型 和放置目录
    start = start_path.get()
    # print('>>>', start)
    type_ = type.get()
    # print('>>', type_)
    end = end_path.get()
    # print('>>', end)
    files = get_files(start, type_)
    if not files:
        # 没有找到对应文件结束本次点击
        return
    # 功能获取 移动复制删除解压缩
    func = functions.get()
    if func == 'move':
        # print(func)
        move_files(start, type_, end, files)
    elif func == 'copy':
        copy_files(start, type_, end, files)
    elif func == 'delete':
        del_files(start, type_, files)
    elif func == 'unzip':
        unzip_file(start, type_, end, files)
    else:
        tkinter.messagebox.showinfo(title='提示', message='请选择功能')
        print('没有选择功能')


def move_files(start, type_, end, files):
    # 可迭代对象
    # files = get_files(start, type_)
    for file in files:
        print(file)
        try:
            shutil.move(file, end)
        except shutil.Error as e:
            print('文件已存在')
    tkinter.messagebox.showinfo(title='提示', message='所有文件移动成功')


def copy_files(start, type_, end, files):
    # files = get_files(start, type_)
    for file in files:
        print(file)
        shutil.copy(file, end)
    tkinter.messagebox.showinfo(title='提示', message='所有文件复制成功')


def del_files(start, type_, files):
    # files = get_files(start, type_)
    for file in files:
        print(file)
        os.remove(file)
    tkinter.messagebox.showinfo(title='提示', message='所有文件删除成功')


def unzip_file(start, type_, end, files):
    # files = get_files(start, type_)
    for file in files:
        try:
            zip_file = zipfile.ZipFile(file)
        except Exception as e:
            print('此文件不是zip文件')
            continue
        zip_file.extractall(end)
    tkinter.messagebox.showinfo(title='提示', message='所有文件已解压成功')


# 获取当前文件夹下文件
def get_files(start_file, file_type):
    # 获取当前目录下的文件
    if tree.get():
        print(tree.get())
        try:
            files = os.listdir(start_file)
        except Exception as e:
            tkinter.messagebox.showinfo(title='提示', message='没有对应的文件，请确认匹配字符')
            print('>>>>>>', e)
            return None
        files_new = []
        for file in files:
            if file_type in file:
                # print(file)
                file_ = start_file + '/' + file
                # print(root + '/' + file)
                files_new.append(file_)


    else:
        # 遍历文件树
        files_new = []
        for root, dirs, files in os.walk(start_file):
            # print('root_dir:', root)  # 当前目录路径
            # print('sub_dirs:', dirs)  # 当前路径下所有子目录
            # print('files:', files)  # 当前路径下所有非目录子文件
            for file in files:
                if file_type in file:
                    # print(file)
                    file_ = root + '/' + file
                    # print(root + '/' + file)
                    files_new.append(file_)
    if not files_new:
        tkinter.messagebox.showinfo(title='提示', message='没有对应的文件，请确认匹配字符')
        return None
    return files_new


window = Tk()  # 实例化对象 建立window
# 添加背景
# photo = PhotoImage(file='img/bg_picture.gif')
# 关键:设置为背景图片
# bgL = Label(window,image=photo).grid()

start_path = StringVar()
end_path = StringVar()
type = StringVar()
functions = StringVar()
functions.set('move')
tree = IntVar()  # 定义是否遍历所有文件夹
window.title('本地文件工具')  # 窗口名称
window.geometry('430x200')  # 窗口大小

# 1 添加标签
l1 = ttk.Label(window, text="目标路径:").grid(row=0, column=0)
e1 = ttk.Entry(window, textvariable=start_path).grid(row=0, column=1)
btn1 = ttk.Button(window, text="路径选择", command=selectStartPath).grid(row=0, column=2)

# 1 添加标签
l2 = ttk.Label(window, text='匹配文字').grid(row=1, column=0)
e2 = ttk.Entry(window, textvariable=type).grid(row=1, column=1)

#  放置目录
l3 = ttk.Label(window, text="放置路径:").grid(row=2, column=0)
e3 = ttk.Entry(window, textvariable=end_path).grid(row=2, column=1)
btn3 = ttk.Button(window, text="路径选择", command=selectEndPath).grid(row=2, column=2)
# 功能选择
l4 = ttk.Label(window, text="功能:").grid(row=3, column=1)
r1 = ttk.Radiobutton(window, text='移动', variable=functions, value='move').grid(row=3, column=2)
r2 = ttk.Radiobutton(window, text='复制', variable=functions, value='copy').grid(row=3, column=3)
r3 = ttk.Radiobutton(window, text='删除', variable=functions, value='delete').grid(row=3, column=4)
r4 = ttk.Radiobutton(window, text='解压', variable=functions, value='unzip').grid(row=3, column=5)
#

c1 = ttk.Checkbutton(window, text='遍历文件树', variable=tree, onvalue=0, offvalue=1).grid(row=4, column=1)

btn_run = ttk.Button(window, text="执行", command=run_function).grid(row=4, column=2)

# 第6步，主窗口循环显示
window.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
