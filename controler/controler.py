#-*- coding:utf-8 -*-
import time
from imageai.Prediction import ImagePrediction
from qtpy import QtWidgets
import os
import configparser


class main_window_ctl():
    def __init__(self,ui_instance):
        self.ui = ui_instance
        self.conf = configparser.ConfigParser()
        self.__author_about__ = '----- ***** ------\n-\n'\
            'By: Sohnia Zhu\n-\n' \
            'github: https://github.com/sohnia\n-\n'\
            '----- ***** ------'
        self.__version_content__ = '--------- ***** ----------\n-\n' \
                           'ALPHA V1.0\n-\n' \
                           '--------- ***** ----------'
        self.detector = ImagePrediction()
        self.model_list = ["DenseNet.h5", "inception.h5","resnet50.h5", "squeezenet.h5"]
        self.model_dict = {self.model_list[0]:self.detector.setModelTypeAsDenseNet,
                           self.model_list[1]:self.detector.setModelTypeAsInceptionV3,
                           self.model_list[2]:self.detector.setModelTypeAsResNet,
                           self.model_list[3]:self.detector.setModelTypeAsSqueezeNet
        }

        self.execution_path = os.getcwd()
        self.conf_file = conf_file = os.path.join(self.execution_path, "Conf\\config.cnf")

    def open_image(self):
        """
        打开图片进行物体识别
        :return: 无文件返回空
        """

        abs_path, filetype = QtWidgets.QFileDialog.getOpenFileName(self.ui,"请打开图片文件", self.execution_path,
                                                                "Image Files (*.jpg;*.png;*.jpeg;*.bmp;*.tif;*.ppm)")  # 设置文件扩展名过滤,

        # 无文件返回空
        if len(abs_path) == 0:
            return
        print(abs_path)
        content = self.detect_image(abs_path)
        self.showMsgbox('识别结果', content)
        self.save_log(content)
    def detect_image(self,abs_path):
        start = time.time()
        self.ui.progressBar.setValue(0);
        try:
            self.conf.read(self.conf_file)
            model_type = self.conf.get("model", "model_type")

        except:
            self.showMsgbox("提示", "配置文件读取出错！")
            return
        if (not model_type):
            self.showMsgbox("提示", "请选定模型！")
            return
        try:
            self.model_dict[model_type]()
            self.detector.setModelPath(os.path.join(self.execution_path,'model',model_type))
            self.detector.loadModel()
            self.ui.progressBar.setValue(40);
            new_image = os.path.splitext(abs_path)[0] + "new" + os.path.splitext(abs_path)[1]
            predictions, probabilities = self.detector.predictImage(abs_path, result_count=5 )
            self.ui.progressBar.setValue(80);

            #输出结果
            content_buffer = '使用的模型为' + model_type + '\n\n'
            for eachPrediction, eachProbability in zip(predictions, probabilities):
                content_buffer += str(eachPrediction) + " : " + str(eachProbability) + '\n\n'
            content_buffer += "执行时间为：" + str(time.time() - start) + "秒"

            self.ui.progressBar.setValue(100);
            return content_buffer
        except Exception as e:
            self.showMsgbox("错误提示",str(e))
            return

    def change_model(self,n):
        #只有第n个按钮为才为选中
        #其他不选中
        print(n)
        self.set_checked(n)
        #存储到conf里面
        self.conf.set("model", "model_type", self.model_list[n])
        f = open(self.conf_file, 'w')
        self.conf.write(f)
        f.close()

    def set_checked(self,n):
        #print(n)
        for num, action in enumerate(self.ui.action_list):
            if (num != n):
                self.ui.action_list[num].setChecked(False)
            else:
                self.ui.action_list[n].setChecked(True)

    def hook_dropfiles(self):
        print('hook_dropfiles')

    def get_model(self):
        pass

    def about_author(self):
        self.showMsgbox("关于作者",self.__author_about__)

    def version(self):
        self.showMsgbox("版本信息",self.__version_content__)

    def showMsgbox(self,title,content):
        QtWidgets.QMessageBox\
            .information(self.ui, title, content, QtWidgets.QMessageBox.Ok)

    def init_model(self):
        try:
            self.conf.read(self.conf_file)
            model_type = self.conf.get("model", "model_type")
            self.set_checked(self.model_list.index(model_type))
        except:
            try:
                self.conf.add_section("model")
                self.conf.set("model", "model_type", self.model_list[2])
                f = open(self.conf_file, 'w')
                self.conf.write(f)
                f.close()
                self.set_checked(2)
            except Exception as e:
                print(e)
            return
        if (not model_type):
            self.showMsgbox("提示", "请选定模型！")
            return

    def save_log(self, content):
        t = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        filename = t + '.txt'
        f = open(os.path.join(self.execution_path,'log',filename),'w')
        f.write('-------------*****------------' + "\n")
        f.write(t + "\n")
        f.write(content + "\n")
        f.write('-------------*****------------')
        f.close()
