# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import os
import shutil
import subprocess
import sys
import tkinter.messagebox
import zipfile
from time import sleep

import requests
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from lib.share import SI


class Update:
    def __init__(self):
        CURRENT_DIRECTORY = os.path.dirname(os.path.realpath('main.py'))
        filename = os.path.join(CURRENT_DIRECTORY, "UI/update.ui")
        self.ui = QUiLoader().load(filename)

        self.ui.progressBar.setRange(0, 4)
        self.ui.progressBar.setValue(0)

        self.ui.button.clicked.connect(self.updateFile)
        self.ui.textBrowser.append(f'{self.dowVersion()}')

    def updateFile(self):
        # 重置倒退进度条的进度
        self.ui.progressBar.reset()
        # 当代码执行至此，进读条为：0%
        self.ui.textBrowser.append("正在下载压缩包...............")
        # setValue(0):表示完成了 0/4
        self.ui.progressBar.setValue(0)
        # 睡眠一秒，方便看到进度条加载样式

        # 当代码执行至此，进读条为：25%
        self.dowZip()
        self.ui.textBrowser.append("下载完成")
        # setValue(1):表示完成了 2/4
        self.ui.progressBar.setValue(1)
        # 睡眠一秒，方便看到进度条加载样式

        # 当代码执行至此，进读条为：50%
        sleep(1)
        self.ui.textBrowser.append("正在解压文件.....................")
        sleep(1)
        # def run():
        res = self.extract_files('./EdgeBanding.zip')
        sleep(1)
        self.ui.progressBar.setValue(2)
        # 睡眠一秒，方便看到进度条加载样式
        sleep(1)
        if res:
            self.ui.textBrowser.append("解压完成")
        self.ui.progressBar.setValue(3)
        os.remove('EdgeBanding.zip')

        self.ui.textBrowser.append("正在替换......................")
        sleep(1)
        res = self.do_replace_files()
        sleep(1)
        if res:
            self.ui.textBrowser.append("替换完成")
        shutil.rmtree('EdgeBanding')
        sleep(1)
        self.ui.textBrowser.append("等待重启")
        self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)
        self.ui.progressBar.setValue(4)
        # sleep(5)
        subprocess.Popen("./EdgeBanding.exe")
        sleep(1)
        sys.exit()

    @staticmethod
    def dowZip():
        url = 'http://192.168.10.16:220/EdgeBanding.zip'
        file = 'EdgeBanding.zip'
        response = requests.get(url)
        with open(file, 'wb') as f:
            f.write(response.content)
        # 打开文本文件

    @staticmethod
    def dowVersion():
        url = 'http://192.168.10.16:220/Version.txt'
        file = 'Version.txt'
        response = requests.get(url)
        with open(file, 'wb') as f:
            f.write(response.content)
        # 打开文本文件
        file = open(f"Version.txt", "r")
        # 读取第一行
        first_line = file.read()
        # 关闭文件
        file.close()
        os.remove('Version.txt')
        # 输出第一行内容
        return str(first_line)

    @staticmethod
    def extract_files(Path):
        file = Path.split('.')[1]
        file = file.split('/')[1]
        print(file)
        if not os.path.exists(file):
            os.mkdir(file)
        with zipfile.ZipFile(Path) as zf:
            zf.extractall(path=file)  # 解压目录
        return True

    def do_replace_files(self):
        extract_dir = 'EdgeBanding'
        for file in os.listdir(extract_dir):
            if not file.endswith('main'):
                try:
                    # print(f'替换文件：{file}')
                    self.copy_files(os.path.join(extract_dir, file), '.')
                except BaseException as e:
                    if os.path.isdir(file):
                        tkinter.messagebox.showwarning(title='错误', message=f'文件夹[{file}]有文件正在使用,更新失败,请关闭文件后重试')
                    else:
                        tkinter.messagebox.showwarning(title='错误', message=f'文件[{file}]正在使用,更新失败,请关闭文件后重试')
                    print(f'替换文件错误{e}')
                    raise e
        return True

    @staticmethod
    def copy_files(src_file, dest_dir):
        file_name = src_file.split(os.sep)[-1]
        if os.path.isfile(src_file):
            shutil.copyfile(src_file, os.path.join(dest_dir, file_name))
        else:
            dest_path = os.path.join(dest_dir, file_name)
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(src_file, os.path.join(dest_dir, file_name))


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QApplication([])
    SI.loginWin = Update()
    SI.loginWin.ui.show()
    sys.exit(app.exec_())

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
