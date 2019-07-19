# coding: utf-8

import json
import os
import re
import shutil
import sys

from PyQt5.QtWidgets import *

from FontResourcepackGenerator_GUI import *


orginal_mcmeta = '''
{
  "pack": {
    "pack_format": 4,
    "description":"!DESCRIPTION"
  }
}
'''

orginal_defaultjson = '''
{
     "providers": [
         {
             "type": "ttf",
             "file": "minecraft:thefont.ttf",
 			"shift": [!SHIFT1, !SHIFT2],
 			"size": !SIZE,
 			"oversample": !OVERSAMPLE
         }
 	]
}
'''


class mainWindow(Ui_MainWindow):
    def init(self):
        self.hasCover = True
        self.mySep = os.sep
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.name = "FontResourcepack"
        self.packpic_path = None
        self.font_path = "C:\\Windows\\Fonts\\simhei.ttf"
        self.save_path = "C:\\Generated packs"
        self.description = "Create by FontResourcepack Generator"
        self.mcmeta = orginal_mcmeta
        self.defaultjson = orginal_defaultjson
        self.font_name = "simhei.ttf"
        self.num_lateraloffset = 0
        self.num_longitudinaloffset = 0
        self.num_fontsize = 11
        self.num_resolution = 2
        # 设置各个按钮的绑定事件
        self.chosefile_button_1.clicked.connect(self.GoToChoosePackpic)
        self.chosefile_button_2.clicked.connect(self.GoToChooseFont)
        self.savefile_button.clicked.connect(self.GoToSave)
        self.submit.clicked.connect(self.StartGenerating)

    # 获取具体数值

    def GetName(self):
        if not str(self.name_input.text()) == '':
            return str(self.name_input.text())
        else:
            return "FontResourcepack"

    def GetPackpic(self):
        return str(self.packpic_input.text())

    def GetDescription(self):
        if not str(self.description_input.text()) == '':
            return str(self.description_input.text())
        else:
            return "Create by FontResourcepack Generator"

    def GetFont(self):
        if not str(self.font_input.text()) == '':
            return str(self.font_input.text())
        else:
            return "C:\\Windows\\Fonts\\simhei.ttf"

    def GetLateraloffset(self):
        if not str(self.lateraloffset_input.text()) == '':
            return int(self.lateraloffset_input.text())
        else:
            return 0

    def GetLongitudinaloffset(self):
        if not str(self.longitudinaloffset_input.text()) == '':
            return int(self.longitudinaloffset_input.text())
        else:
            return 0

    def GetFontsize(self):
        if not str(self.fontsize_input.text()) == '':
            return int(self.fontsize_input.text())
        else:
            return 11

    def GetResolution(self):
        if not str(self.resolution_input.text()) == '':
            return int(self.resolution_input.text())
        else:
            return 2

    def GoToChoosePackpic(self):
        filepath = QFileDialog.getOpenFileName(
            None, "选取pack.png文件", self.cwd, "pack.png (*.png)")
        if not filepath[0] == '':
            self.hasCover = True
            self.packpic_path = filepath[0]
            self.packpic_input.setText(filepath[0])
        else:
            self.hasCover = False

    def GoToChooseFont(self):
        filepath = QFileDialog.getOpenFileName(
            None, "选取TrueType字体文件", self.cwd, "TrueType字体文件 (*.ttf)")
        if not filepath[0] == '':
            self.font_path = filepath[0]
            self.font_input.setText(filepath[0])
        else:
            self.font_path = "C:\\Windows\\Fonts\\simhei.ttf"
            self.font_input.setText("C:\\Windows\\Fonts\\simhei.ttf")

    def GoToSave(self):
        filepath = QFileDialog.getExistingDirectory(None, "保存位置", self.cwd)
        if not filepath == '':
            self.save_path = str(filepath)
            self.save_input.setText(self.save_path)
        else:
            self.save_path = "C:\\Generated packs"
            self.save_input.setText("C:\\Generated packs")

    def StartGenerating(self):
        # 更新名称
        self.task_output.setText("更新名称中...")
        self.name = self.GetName()
        self.progressBar.setProperty("value", 5)
        # 更新封面
        self.task_output.setText("更新封面中...")
        self.packpic_path = self.GetPackpic()
        if self.packpic_path == '':
            self.hasCover = False
        self.progressBar.setProperty("value", 10)
        # 更新描述
        self.task_output.setText("更新描述中...")
        self.description = self.GetDescription()
        self.progressBar.setProperty("value", 15)
        # 更新字体
        self.task_output.setText("更新字体中...")
        self.font_path = self.GetFont()
        self.progressBar.setProperty("value", 20)
        # 更新横向偏移量
        self.task_output.setText("更新横向偏移量中...")
        self.num_lateraloffset = self.GetLateraloffset()
        self.progressBar.setProperty("value", 25)
        # 更新纵向偏移量
        self.task_output.setText("更新纵向偏移量中...")
        self.num_longitudinaloffset = self.GetLongitudinaloffset()
        self.progressBar.setProperty("value", 30)
        # 更新字母大小
        self.task_output.setText("更新字母大小中...")
        self.num_fontsize = self.GetFontsize()
        self.progressBar.setProperty("value", 35)
        # 更新解析度
        self.task_output.setText("更新解析度中...")
        self.num_resolution = self.GetResolution()
        self.progressBar.setProperty("value", 40)
        # 更新mcmeta
        self.task_output.setText("更新pack.mcmeta内容中...")
        self.mcmeta = self.mcmeta.replace("!DESCRIPTION", self.description)
        self.progressBar.setProperty("value", 45)
        # 更新字体名称
        self.task_output.setText("更新字体名称中...")
        self.font_name = "thefont.ttf"
        self.progressBar.setProperty("value", 50)
        # 更新default.json
        self.task_output.setText("更新default.json内容中...")
        self.defaultjson = self.defaultjson.replace(
            "!SHIFT1", str(self.num_lateraloffset))
        self.defaultjson = self.defaultjson.replace(
            "!SHIFT2", str(self.num_longitudinaloffset))
        self.defaultjson = self.defaultjson.replace(
            "!SIZE", str(self.num_fontsize))
        self.defaultjson = self.defaultjson.replace(
            "!OVERSAMPLE", str(self.num_resolution))
        self.progressBar.setProperty("value", 55)
        # 创建目录层级
        self.task_output.setText("创建目录中...")
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        if not os.path.exists(self.save_path+self.mySep+self.name):
            os.mkdir(self.save_path+self.mySep+self.name)
        if not os.path.exists(self.save_path+self.mySep+self.name+self.mySep+"assets"):
            os.mkdir(self.save_path+self.mySep+self.name+self.mySep+"assets")
        if not os.path.exists(self.save_path+self.mySep+self.name+self.mySep+"assets"+self.mySep+"minecraft"):
            os.mkdir(self.save_path+self.mySep+self.name +
                     self.mySep+"assets"+self.mySep+"minecraft")
        if not os.path.exists(self.save_path+self.mySep+self.name+self.mySep+"assets"+self.mySep+"minecraft"+self.mySep+"font"):
            os.mkdir(self.save_path+self.mySep+self.name+self.mySep +
                     "assets"+self.mySep+"minecraft"+self.mySep+"font")
        self.progressBar.setProperty("value", 75)
        # 生成pack.mcmeta文件
        self.task_output.setText("生成pack.mcmeta文件中...")
        mcmetafile = open(self.save_path+self.mySep +
                          self.name+self.mySep+"pack.mcmeta", "w+")
        mcmetafile.write(self.mcmeta)
        mcmetafile.close()
        self.progressBar.setProperty("value", 80)
        if self.hasCover:
            # 复制封面
            self.task_output.setText("复制封面中...")
            shutil.copyfile(self.packpic_path, self.save_path +
                            self.mySep+self.name + self.mySep+"pack.png")
            self.progressBar.setProperty("value", 85)
        # 生成default.json
        self.task_output.setText("生成default.json文件中...")
        jsonfile = open(
            self.save_path+self.mySep+self.name+self.mySep+"assets"+self.mySep+"minecraft"+self.mySep+"font"+self.mySep+"default.json", "wb+")
        jsonfile.write(str.encode(self.defaultjson))
        self.progressBar.setProperty("value", 90)
        # 复制字体文件
        self.task_output.setText("复制字体文件中...")
        shutil.copyfile(self.font_path, self.save_path+self.mySep+self.name + self.mySep+"assets" +
                        self.mySep+"minecraft"+self.mySep+"font"+self.mySep+"thefont.ttf")
        self.progressBar.setProperty("value", 95)
        # 完成
        self.task_output.setText("完成！")
        self.progressBar.setProperty("value", 100)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = mainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    ex.init()
    w.show()
    sys.exit(app.exec_())
