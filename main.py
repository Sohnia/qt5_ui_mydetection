#-*- coding:utf-8 -*-
import sys
from functools import partial

from qtpy import QtWidgets
from view import main_window
from controler import main_window_ctl
Ui_MainWindow = main_window.Ui_mainWindow#指定Ui_MainWindow 为main_menu文件下的Ui_MainWindow对象。

class CoperQt(QtWidgets.QMainWindow,Ui_MainWindow):
    #创建一个Qt对象
    #这里的第一个变量是你该窗口的类型，第二个是该窗口对象。
    #这里是主窗口类型。所以设置成当QtWidgets.QMainWindow。
    #你的窗口是一个会话框时你需要设置成:QtWidgets.QDialog
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)  # 创建主界面对象
        Ui_MainWindow.__init__(self)#主界面对象初始化
        self.setupUi(self)  #配置主界面对象
        self.setFixedSize(self.width(), self.height())
        self.action_list = [self.actionDenseNet121,
                            self.actionInceptionV3,
                            self.actionResNet50,
                            self.actionSqueezeNet]
        self.ctl = main_window_ctl(self)
        self.ctl.init_model()
        self.version.triggered.connect(self.ctl.version)
        self.about_author.triggered.connect(self.ctl.about_author)
        self.open_image.triggered.connect(self.ctl.open_image)
        instance = [i.triggered.connect(partial(self.ctl.change_model, n)) for n,i in enumerate(self.action_list)]

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            e.acceptProposedAction()
            # 遍历输出拖动进来的所有文件路径
            if len(e.mimeData().urls())==1:
                for url in e.mimeData().urls():
                    url = str(url.toLocalFile())
                    content = self.ctl.detect_image(url)
                    self.ctl.showMsgbox("识别信息",content)
            else:
                content = ''
                for url in e.mimeData().urls():
                    url = str(url.toLocalFile())
                    if(self.is_image_file(url)):
                        content += url + "\n\n"
                        content += self.ctl.detect_image(url) + "\n\n\n\n"
                self.ctl.save_log(content)
                self.ctl.showMsgbox("结果提示","请到log文件夹下面查看结果！")
        else:
            e.ignore()

    def dropEvent(self, e):
        position = e.pos()
        e.accept()
        # print(position)

    def is_image_file(self,url):
        if url.split('.')[-1].lower() in ['jpg','png','jpeg','bmp','tif','ppm']:
            return True
        else:
            return False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoperQt()#创建QT对象
    window.show()#QT对象显示
    sys.exit(app.exec_())
