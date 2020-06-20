from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog
from task3 import Ui_MainWindow
import sys
import cv2
import numpy as np
from modesEnum import Modes
from imageModel import ImageModel
import logging
logging.basicConfig(filename='console.log',level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s :: %(lineno)s',filemode='w')
logger = logging.getLogger()

class ApplicationWindow(Ui_MainWindow):
    Var = np.array([])
    loaded = [False,False]
    # loaded2 = False
    input_widgets = np.array([])
    widgets = np.array([])
    sliderarr = np.array([])
    add_btns_arr = np.array([])
    combo_edit = np.array([])
    array_component = np.array([])
    array_data = np.array([])
    class_arr = np.array([])
    graphs_ip_arr = np.array([])
    box_arr = np.array([])
    image1 = None
    image2 = None
    svalue = [0,0]
    combo_op = np.array([])
    component = ['','']
    image_combo = ['','']
    removebtn = np.array([])

    def __init__(self,MainWindow):
        super(ApplicationWindow, self).setupUi(MainWindow)
        self.class_arr = [self.image1,self.image2]
        self.array_component = ["Magnitude","Phase","Real","Imaginary"]
        #self.array_data = [self.class_arr[i].spectrum_arr,image1,real_arr,img_arr]
        self.widgets = [self.image1_org,self.image1_edit,self.image2_org,self.image2_edit,self.output1_img,self.output2_img]
        self.sliderarr = [self.Slider1,self.Slider2]
        #self.svalue = [self.svalue1,self.svalue2]
        self.combo_op = [self.combo_mix1,self.combo_mix2]
        self.image_combo = [self.compo_comp1,self.compo_comp2]
        self.input_widgets = [self.image1_org,self.image2_org]
        self.combo_edit_arr = [self.combo_edit1,self.combo_edit2]
        self.graphs_ip_arr = [self.image1_edit,self.image2_edit]
        self.add_btns_arr = [self.image1Btn,self.image2Btn]
        self.box_arr = [self.slider_box1,self.slider_box2]
        self.removebtn = [self.remove1Btn, self.remove2Btn]
        self.compo_output.currentIndexChanged.connect(self.test)
        self.action_insert = [self.actionImage_one,self.actionImage_two]
        for i in range (6):
            self.hide(i)

        for i in range(2):
            self.combo_Btn(i)
            self.add_Btn(i)
        self.combo_mix1.currentTextChanged.connect(lambda: self.obj_no(0))
        self.combo_mix2.currentTextChanged.connect(lambda: self.obj_no(1))
        for i in range(2):
            self.connect_sliders(i)
            self.remove_img(i)

    def connect_sliders(self,i):
        self.sliderarr[i].valueChanged.connect(lambda: self.slidervalue(i))

    def add_Btn(self,i):
        self.add_btns_arr[i].clicked.connect(lambda: self.read_file(i))
        self.action_insert[i].triggered.connect(lambda: self.read_file(i))

    def combo_Btn(self,i):
        self.combo_edit_arr[i].currentTextChanged.connect(lambda: self.combo_fn(i))

    def hide(self,i):
        self.widgets[i].ui.histogram.hide()
        self.widgets[i].ui.roiBtn.hide()
        self.widgets[i].ui.menuBtn.hide()
        self.widgets[i].ui.roiPlot.hide()

    def read_file(self,i):
        filename = QFileDialog.getOpenFileName()
        if filename[0] == "":
            pass
        else:
            logger.info("Reading Image " + str(i))
            self.class_arr[i] = ImageModel(filename[0])
            if i == 0:
                if self.loaded[1] == True:
                    if self.class_arr[0].original_arr.shape == self.class_arr[1].original_arr.shape:
                        self.input_widgets[i].setImage(self.class_arr[i].original_arr.T)
                        self.input_widgets[i].view.setRange(xRange=[0,self.class_arr[0].width],yRange=[0,self.class_arr[0].height],padding=0)
                        self.loaded[0]= True
                    else:
                        logger.error("Error : check the Image size")
                else:
                    self.input_widgets[i].setImage(self.class_arr[i].original_arr.T)
                    self.input_widgets[i].view.setRange(xRange=[0, self.class_arr[0].width],
                                                        yRange=[0, self.class_arr[0].height],padding=0)
                    self.loaded[0] = True
            elif i == 1:
                if self.loaded[0] == True:
                    if self.class_arr[1].original_arr.shape == self.class_arr[0].original_arr.shape:
                        self.input_widgets[i].setImage(self.class_arr[i].original_arr.T)
                        self.input_widgets[i].view.setRange(xRange=[0, self.class_arr[1].width],
                                                            yRange=[0, self.class_arr[1].height],padding=0)
                        self.loaded[1] = True
                    else:
                        logger.error("Error : check the Image size")
                else:
                    self.input_widgets[i].setImage(self.class_arr[i].original_arr.T)
                    self.input_widgets[i].view.setRange(xRange=[0, self.class_arr[1].width],
                                                        yRange=[0, self.class_arr[1].height],padding=0)
                    self.loaded[1] = True

    def remove_img(self,x):
        self.removebtn[x].clicked.connect(lambda: self.remove(x))


    def combo_fn(self,no):
        option = self.combo_edit_arr[no].currentText()
        if self.loaded[no]:
            if option == 'Component':
                logger.info('No component is Selected')
            elif option == 'Magnitude':
                self.graphs_ip_arr[no].setImage(self.class_arr[no].spectrum_arr.T)
                logger.info('Magnitude Component of Image ' + str(no+1) + ' is Selected')
            elif option == 'Phase':
                self.graphs_ip_arr[no].setImage(self.class_arr[no].phase_arr.T)
                logger.info('Phase Component of Image ' + str(no+1) + ' is Selected')
            elif option == 'Real':
                self.graphs_ip_arr[no].setImage(self.class_arr[no].real_arr.T)
                logger.info('Real Component of Image ' + str(no+1) + ' is Selected')
            elif option == 'Imaginary':
                self.graphs_ip_arr[no].setImage(self.class_arr[no].img_arr.T)
                logger.info('Imaginary Component of Image ' + str(no+1) + ' is Selected')


        else:
            logger.info("No Image Found, Please Insert Image First")

    def slidervalue(self, x):
        self.svalue[x] = self.sliderarr[x].value()
        logger.info('The Value of Slider ' + str(x+1) + ' is equal to ' + str(self.svalue[x]) )
        print(self.svalue[1])
        self.box_arr[x].setText(str(self.svalue[x]))

    def remove(self,x):
        if self.loaded[x] == False:
            logger.info('No Image to be removed')

        else:
            self.input_widgets[x].clear()
            self.loaded[x] = False
    def obj_no(self,i):
        x = self.image_combo[i].currentText()
        if i == 0:
            if x == 'Image no':
                logger.info("No Image Selected for Component 1")
            if x == 'Image1':
                logger.info("Image 1 Selected for Component 1")
                self.opchoice(0,1)
            if x == 'Image2':
                logger.info("Image 2 Selected for Component 1")
                self.opchoice(1,0)
        if i == 1:
            if x == 'Image no':
                logger.info("No Image Selected for Component 2")
            if x == 'Image1':
                logger.info("Image 1 Selected for Component 2")
                self.uniforms(0,1)
            if x == 'Image2':
                logger.info("Image 2 Selected for Component 2")
                self.uniforms(1,0)


    def opchoice(self,current,next):
        option = self.combo_mix1.currentText()
        logger.info('You Select ' + str(option) + ' Component for mixing')

        if option == 'Component':
            pass
        elif option == 'Magnitude':
            self.class_arr[current].spectrum_arr = np.copy(self.class_arr[current].magnitude)
            self.combo_op[1].clear()
            self.combo_op[1].addItem('Component')
            self.combo_op[1].addItem('Phase')
            self.combo_op[1].addItem('Uniform_phase')

        elif option == 'Phase':
            self.class_arr[current].phase_arr = np.copy(self.class_arr[current].phase)
            self.combo_op[1].clear()
            self.combo_op[1].addItem('Component')
            self.combo_op[1].addItem('Magnitude')
            self.combo_op[1].addItem('Uniform_mag')

        elif option == 'Real':
            self.combo_op[1].clear()
            self.combo_op[1].addItem('Component')
            self.combo_op[1].addItem('Imaginary')


        elif option == 'Imaginary':
            self.combo_op[1].clear()
            self.combo_op[1].addItem('Component')
            self.combo_op[1].addItem('Real')


        elif option == 'Uniform_mag':
            self.class_arr[current].spectrum_arr = np.ones([self.class_arr[current].height, self.class_arr[current].width])
            self.class_arr[next].spectrum_arr = np.ones([self.class_arr[next].height, self.class_arr[next].width])
            self.sliderarr[0].setValue(50)
            self.combo_op[1].clear()
            self.combo_op[1].addItem('Component')
            self.combo_op[1].addItem('Phase')
            self.combo_op[1].addItem('Uniform_phase')


        elif option == 'Uniform_phase':
            self.class_arr[current].phase_arr = np.zeros([self.class_arr[current].height,self.class_arr[current].width])
            self.class_arr[next].phase_arr = np.zeros([self.class_arr[next].height,self.class_arr[next].width])
            self.combo_op[1].clear()
            self.combo_op[1].addItem('Component')
            self.combo_op[1].addItem('Magnitude')
            self.combo_op[1].addItem('Uniform_mag')


    def uniforms(self,current,next):
        option = self.combo_mix2.currentText()
        image = self.compo_comp2.currentText()
        logger.info('You Select ' + str(option) + ' Component for mixing')

        if option == 'Component':
            pass
        elif option == 'Magnitude':
            self.class_arr[current].spectrum_arr = np.copy(self.class_arr[current].magnitude)

        elif option == 'Phase':
            self.class_arr[current].phase_arr = np.copy(self.class_arr[current].phase)

        elif option == 'Uniform_mag':
            self.class_arr[current].spectrum_arr = np.ones(
                [self.class_arr[current].height, self.class_arr[current].width])
            self.class_arr[next].spectrum_arr = np.ones([self.class_arr[next].height, self.class_arr[next].width])
            self.sliderarr[1].setValue(50)


        elif option == 'Uniform_phase':
            self.class_arr[current].phase_arr = np.zeros(
                [self.class_arr[current].height, self.class_arr[current].width])
            self.class_arr[next].phase_arr = np.zeros([self.class_arr[next].height, self.class_arr[next].width])


    def test(self):
        op_component = self.compo_output.currentIndex()
        obj_value = self.compo_comp1.currentText()
        component1 = self.combo_mix1.currentText()
        logger.info('You Select ' + str(op_component) + ' To show output')

        if self.loaded[0] and self.loaded[1]:
            if op_component ==0:
                pass
            elif op_component ==1:
                if obj_value == 'Image no':
                    pass
                elif obj_value == 'Image1':
                    if component1 == 'Component':
                        pass
                    elif component1 == 'Magnitude' or 'Phase' or 'Uniform_mag' or 'Uniform_phase':
                        self.Var = self.class_arr[0].mix(self.class_arr[1],self.svalue[0],self.svalue[1],Modes.magnitudeAndPhase)
                        self.output1_img.setImage(self.Var.T)
                    elif component1 == 'Real' or 'Imaginary':
                        self.Var = self.class_arr[0].mix(self.class_arr[1], self.svalue[0], self.svalue[1], Modes.realAndImaginary)
                        self.output1_img.setImage(self.Var.T)

                elif obj_value == 'Image2':
                    if component1 == 'Component':
                        pass
                    elif component1 == 'Magnitude' or 'Phase' or 'Uniform_mag' or 'Uniform_phase':
                        self.Var = self.class_arr[1].mix(self.class_arr[0],self.svalue[0],self.svalue[1],Modes.magnitudeAndPhase)
                        self.output1_img.setImage(self.Var.T)

                    elif component1 == 'Real' or 'Imaginary':
                        self.Var = self.class_arr[1].mix(self.class_arr[0], self.svalue[0], self.svalue[1], Modes.realAndImaginary)
                        self.output1_img.setImage(self.Var.T)

            else:
                if obj_value == 'Image no':
                    pass
                elif obj_value == 'Image1':
                    if component1 == 'Component':
                        pass
                    elif component1 == 'Magnitude' or 'Phase' or 'Uniform_mag' or 'Uniform_phase':
                        self.Var = self.class_arr[0].mix(self.class_arr[1],self.svalue[0],self.svalue[1],Modes.magnitudeAndPhase)
                        self.output2_img.setImage(self.Var.T)
                    elif component1 == 'Real' or 'Imaginary':
                        self.Var = self.class_arr[0].mix(self.class_arr[1], self.svalue[0], self.svalue[1], Modes.realAndImaginary)
                        self.output2_img.setImage(self.Var.T)

                elif obj_value == 'Image2':
                    if component1 == 'Component':
                        pass
                    elif component1 == 'Magnitude' or 'Phase' or 'Uniform_mag' or 'Uniform_phase':
                        self.Var = self.class_arr[1].mix(self.class_arr[0],self.svalue[0],self.svalue[1],Modes.magnitudeAndPhase)
                        self.output2_img.setImage(self.Var.T)

                    elif component1 == 'Real' or 'Imaginary':
                        self.Var = self.class_arr[1].mix(self.class_arr[0], self.svalue[0], self.svalue[1], Modes.realAndImaginary)
                        self.output2_img.setImage(self.Var.T)

        else:
            logger.info('One of the Two Images Is Not Found, Please make Sure u Insert both ')


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ApplicationWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()