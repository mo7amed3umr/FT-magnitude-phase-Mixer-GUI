## This is the abstract class that the students should implement  

from modesEnum import Modes
import numpy as np
import cv2


class ImageModel():
    height = 0
    width = 0
    temp = np.array([])
    original_arr = np.array([])
    complex_arr = np.array([])
    spectrum_arr = np.array([])
    phase_arr = np.array([])
    real_arr = np.array([])
    img_arr = np.array([])

    """
    A class that represents the ImageModel"
    """

    def __init__(self):
        pass

    def __init__(self, imgPath: str):
        self.imgPath = imgPath
        ###
        # ALL the following properties should be assigned correctly after reading imgPath 
        ###
        self.imgByte = cv2.imread(imgPath, 0)

        self.original_arr = np.copy(self.imgByte)
        self.height, self.width = self.imgByte.shape[:2]
        print(self.imgByte.shape)

        self.dft = np.fft.fft2(self.imgByte)

        fshift = np.fft.fftshift(self.dft)
        self.magnitude = 20 * np.log(np.abs(fshift))
        self.phase = np.angle(self.dft)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.spectrum_arr = np.copy(self.magnitude)
        self.phase_arr = np.copy(self.phase)
        self.real_arr = np.copy(self.real)
        self.img_arr = np.copy(self.imaginary)

   
    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration 
        """

        print("slider:",magnitudeOrRealRatio)
        print("slider2",phaesOrImaginaryRatio)
        n = magnitudeOrRealRatio/100
        print('n :',n)
        m = phaesOrImaginaryRatio /100
        print('m:',m)
        if mode == Modes.magnitudeAndPhase:
            mag = np.add(self.spectrum_arr*n, imageToBeMixed.spectrum_arr*(1-n))
            mag = mag / 20
            mag = np.exp(mag)
            magorg = np.fft.ifftshift(mag)
            # print("mag size : ",magorg.shape)
            print('magnitude:',magorg)
            phaseadd = np.add(imageToBeMixed.phase_arr*m, self.phase_arr*(1-m))
            phase = np.exp(1j*phaseadd)
            # print("phase size : ",phase.shape)
            print('Phase:',phase)
            form = np.multiply(magorg,phase)
            # print("form size : ",form.shape)
            # print(form)
            mix1 = np.fft.ifft2(form)
            print("mix1 size : ",mix1.shape)
            print(np.real(mix1))
            return np.real(mix1)
        elif mode == Modes.realAndImaginary:
            real1 = np.add(self.real_arr * n ,imageToBeMixed.real_arr*(1-n))
            imaginary1 = np.add(imageToBeMixed.img_arr * m , self.img_arr*(1-m))
            mix2 = np.add(real1,1j*imaginary1)
            imix2 = np.fft.ifft2(mix2)
            return np.real(imix2)

