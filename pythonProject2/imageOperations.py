import cv2
from PyQt5.QtGui import QImage


class ImageOperations:
    def __init__(self):
        self.currentImage = QImage()
        self.previousImages = []
        self.nextImages = []
        self.brightnessFlag = 0
        self.noBrightnessModificationImage = None

    def applyAverageFilter(self, value):
        try:
            if self.currentImage is None:
                print("Failed to load the image.")
                return

            self.previousImages.append(self.currentImage)
            self.currentImage = cv2.blur(self.currentImage, (value, value))
            self.noBrightnessModificationImage = self.currentImage

            self.removeFirstElementIfNeeded()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def applyMedianFilter(self, value):
        try:
            if self.currentImage is None:
                print("Failed to load the image.")
                return

            self.previousImages.append(self.currentImage)
            self.currentImage = cv2.medianBlur(self.currentImage, value)
            self.noBrightnessModificationImage = self.currentImage

            self.removeFirstElementIfNeeded()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def applyGaussianFilter(self, value):
        try:
            if self.currentImage is None:
                print("Failed to load the image.")
                return

            self.previousImages.append(self.currentImage)
            self.currentImage = cv2.GaussianBlur(self.currentImage, (value, value), 0)
            self.noBrightnessModificationImage = self.currentImage

            self.removeFirstElementIfNeeded()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def imageToGrayScale(self):
        try:
            if self.currentImage is None:
                print("Failed to load the image.")
                return

            self.previousImages.append(self.currentImage)

            grayImage = cv2.cvtColor(self.currentImage, cv2.COLOR_BGR2GRAY)
            self.currentImage = cv2.merge((grayImage, grayImage, grayImage))
            self.noBrightnessModificationImage = self.currentImage

            self.removeFirstElementIfNeeded()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def changeBrightness(self, value):
        try:
            if self.currentImage is None:
                print("Failed to load the image.")
                return

            if self.noBrightnessModificationImage is None:
                self.noBrightnessModificationImage = self.currentImage

            self.previousImages.append(self.currentImage)
            self.currentImage = cv2.convertScaleAbs(self.noBrightnessModificationImage, alpha=1, beta=value)

            self.removeFirstElementIfNeeded()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def cvMatToQImage(self):
        qImage = QImage(self.currentImage.data, self.currentImage.shape[1],
                        self.currentImage.shape[0],
                        self.currentImage.shape[1] * 3, QImage.Format_RGB888)

        return qImage

    def getCurrentImage(self):
        return self.currentImage

    def setCurrentImage(self, currentImage):
        self.currentImage = currentImage

    def getPreviousImages(self):
        return self.previousImages

    def getNextImages(self):
        return self.nextImages

    def removeFirstElementIfNeeded(self):
        max_length = 100
        if len(self.previousImages) > max_length:
            del self.previousImages[0]
            print("image deleted, " + str(len(self.previousImages)))

        if len(self.nextImages) > max_length:
            del self.nextImages[0]
            print("image deleted, " + str(len(self.nextImages)))
