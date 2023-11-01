import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap


class ImageOperations:
    def __init__(self):
        self.currentImage = QImage()
        self.previousImages = []
        self.nextImages = []
        self.brightnessFlag = 0

    def applyAverageFilter(self, value):
        try:
            self.getPreviousImages().append(self.getCurrentImage())

            if self.getCurrentImage() is not None:
                self.currentImage = cv2.blur(self.currentImage, (value, value))

            else:
                print("Failed to load the image.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def applyMedianFilter(self, value):
        try:
            self.getPreviousImages().append(self.getCurrentImage())

            if self.getCurrentImage() is not None:
                self.currentImage = cv2.medianBlur(self.currentImage, value)

            else:
                print("Failed to load the image.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def imageToGrayScale(self):
        try:
            self.getPreviousImages().append(self.getCurrentImage())

            if self.getCurrentImage() is not None:
                grayImage = cv2.cvtColor(self.currentImage, cv2.COLOR_BGR2GRAY)
                self.currentImage = cv2.merge((grayImage, grayImage, grayImage))

            else:
                print("Failed to load the image.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def changeBrightness(self, value):
        try:
            self.getPreviousImages().append(self.getCurrentImage())

            if self.getCurrentImage() is not None:
                if value >= self.brightnessFlag:
                    self.currentImage = cv2.convertScaleAbs(self.currentImage, alpha=1, beta=abs(value))
                elif value < self.brightnessFlag:
                    self.currentImage = cv2.convertScaleAbs(self.currentImage, alpha=1, beta=-abs(value))

                self.brightnessFlag = value
                # self.currentImage=cv2.addWeighted(self.currentImage, value, self.currentImage, 0, 100)

            else:
                print("Failed to load the image.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def cvMatToQImage(self):
        qImage = QImage(self.getCurrentImage().data, self.getCurrentImage().shape[1],
                        self.getCurrentImage().shape[0],
                        self.getCurrentImage().shape[1] * 3, QImage.Format_RGB888)

        return qImage

    def getCurrentImage(self):
        return self.currentImage

    def setCurrentImage(self, currentImage):
        self.currentImage = currentImage

    def getPreviousImages(self):
        return self.previousImages

    def getNextImages(self):
        return self.nextImages
