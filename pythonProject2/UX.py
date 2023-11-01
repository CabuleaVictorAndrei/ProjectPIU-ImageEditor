import cv2
from PyQt5.QtCore import Qt

import ImageOperations
from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QMessageBox, \
    QFileDialog, QSlider, QComboBox, QApplication
from PyQt5.QtGui import QPixmap


class UX(QMainWindow):
    def __init__(self):
        super().__init__()

        self.imageOperations = ImageOperations.ImageOperations()

        self.menubar = self.menuBar()
        self.horizontalLayout = QVBoxLayout()

        self.central_widget = QWidget()

        self.undoButton = QPushButton("<-", self.central_widget)
        self.redoButton = QPushButton("->", self.central_widget)

        self.averageFilterButton = QPushButton("Average Filter", self.central_widget)
        self.medianFilterButton = QPushButton("Median Filter", self.central_widget)
        self.grayScaleButton = QPushButton("Gray Scale", self.central_widget)

        self.brightnessLabel = None
        self.brightnessSlider = None
        self.averageFilterComboBox = None

        self.image_label = QLabel(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.initUI()
        self.fileMenu()
        self.viewMenu()
        self.helpMenu()

        self.hidden = 0

    def initUI(self):
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 900, 900)

        self.undoButton.setDisabled(True)
        self.redoButton.setDisabled(True)

        self.button_layout.addWidget(self.undoButton)
        self.button_layout.addWidget(self.redoButton)

        self.button_layout.addWidget(self.averageFilterButton)
        self.button_layout.addWidget(self.medianFilterButton)

        self.averageFilterComboBox = QComboBox(self)
        self.averageFilterComboBox.addItem("3")
        self.averageFilterComboBox.addItem("5")
        self.averageFilterComboBox.addItem("7")
        self.averageFilterComboBox.addItem("9")
        self.averageFilterComboBox.addItem("11")
        self.averageFilterComboBox.addItem("13")
        self.averageFilterComboBox.addItem("15")
        self.button_layout.addWidget(self.averageFilterComboBox)

        self.button_layout.addWidget(self.grayScaleButton)

        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setMinimum(-10)
        self.brightnessSlider.setMaximum(10)
        self.brightnessSlider.setSingleStep(1)
        self.brightnessSlider.setValue(0)
        self.brightnessLabel = QLabel('Brightness Value: 0')

        self.button_layout.addWidget(self.brightnessLabel)
        self.button_layout.addWidget(self.brightnessSlider)

        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.image_label)

        self.central_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.central_widget)

        self.setStyleOfWidgets()

        self.connectWidgets()

    def setStyleOfWidgets(self):
        self.setStyleSheet("")

        border_style = "border: 2px solid black;"
        self.image_label.setStyleSheet(border_style)

        self.setStyleSheet("""
            QMenuBar
            {
                background-color: #000000;
                color: #fff;
            }
            QMenuBar::item
            {
                background-color: #000000;
                color: #fff;
            }
            QMenuBar::item::selected
            {
                background-color: #ffb67a;
                color: #fff;
            }
            QMenu
            {
                background-color: #000000;
                color: #fff;
            }
            QMenu::item::selected
            {
                background-color: #ffb67a;
                color: #fff;
            }
            
            QPushButton
            {
                background-color: #333333; /* Default button color */
                color: #fff;
            }
            QPushButton:hover
            {
                background-color: #ff9933; /* Change the color when hovered */
            }
            QPushButton:pressed
            {
                background-color: #ffb67a; /* Change the color when clicked */
            }
            """)

    def connectWidgets(self):
        self.undoButton.clicked.connect(self.undo)
        self.redoButton.clicked.connect(self.redo)
        self.averageFilterButton.clicked.connect(self.onAverageFilterButtonPressed)
        self.medianFilterButton.clicked.connect(self.onMedianFilterButtonPressed)
        self.averageFilterComboBox.currentIndexChanged.connect(self.onComboIndexChanged)
        self.grayScaleButton.clicked.connect(self.imageToGrayScale)
        self.brightnessSlider.valueChanged.connect(self.brightnessSliderValueChanged)

    def fileMenu(self):
        file_menu = self.menubar.addMenu('File')

        open_action = QAction('Open\tCtrl+O', self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        save_action = QAction('Save\tCtrl+S', self)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.exitFile)
        file_menu.addAction(exit_action)

    def viewMenu(self):
        view_menu = self.menubar.addMenu('View')

        showHideMenu_action = QAction('Show/Hide Menu', self)
        showHideMenu_action.triggered.connect(self.showHideMenu)
        view_menu.addAction(showHideMenu_action)

    def helpMenu(self):
        help_menu = self.menubar.addMenu('Help')

        help_action = QAction('About', self)
        help_action.triggered.connect(self.showAboutDialog)
        help_menu.addAction(help_action)

    def showAboutDialog(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Help")
        messageBox.setText(
            "This app is an Image Editor and has been created by Căbulea Victor-Andrei and Cojocaru Rareș.")
        messageBox.exec_()

    def showHideMenu(self):
        if self.hidden == 0:
            self.redoButton.hide()
            self.undoButton.hide()
            self.averageFilterButton.hide()
            self.averageFilterComboBox.hide()
            self.medianFilterButton.hide()
            self.grayScaleButton.hide()
            self.brightnessLabel.hide()
            self.brightnessSlider.hide()

            self.hidden = 1

        elif self.hidden == 1:
            self.redoButton.setHidden(False)
            self.undoButton.setHidden(False)
            self.averageFilterButton.setHidden(False)
            self.averageFilterComboBox.setHidden(False)
            self.medianFilterButton.setHidden(False)
            self.grayScaleButton.setHidden(False)
            self.brightnessLabel.setHidden(False)
            self.brightnessSlider.setHidden(False)

            self.hidden = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
            self.openFile()
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.saveFile()

    # Functions for connections
    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Image Files (*.jpg *.png *.bmp);;All Files (*)", options=options)

        if file_name:
            image = cv2.cvtColor(cv2.imread(file_name), cv2.COLOR_RGB2BGR)

            label_width = self.image_label.width()
            label_height = self.image_label.height()

            aspect_ratio = image.shape[1] / image.shape[0]
            new_width = label_width
            new_height = int(label_width / aspect_ratio)

            if new_height > label_height:
                new_height = label_height
                new_width = int(label_height * aspect_ratio)

            image = cv2.resize(image, (new_width, new_height))

            self.imageOperations.setCurrentImage(image)

            self.updatePixmap()

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png);;All Files (*)",
                                                  options=options)

        file_path, selected_filter = file_dialog

        if file_path:
            qImage = self.imageOperations.cvMatToQImage()

            qImage.save(file_path, "PNG", -1)

    def exitFile(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Question)
        message_box.setWindowTitle("Save and Exit")
        message_box.setText("Do you want to save the file before exiting?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.Yes)

        response = message_box.exec_()

        if response == QMessageBox.Yes:
            self.saveFile()
        else:
            QApplication.quit()

    def onComboIndexChanged(self):
        self.averageFilterComboBox.currentText()

    def onAverageFilterButtonPressed(self):
        try:
            self.imageOperations.applyAverageFilter(int(self.averageFilterComboBox.currentText()))
            self.updatePixmap()

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Empty Image", "Cannot apply average filter to an empty image.")

    def onMedianFilterButtonPressed(self):
        try:
            self.imageOperations.applyMedianFilter(int(self.averageFilterComboBox.currentText()))
            self.updatePixmap()

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Empty Image", "Cannot apply median filter to an empty image.")

    def imageToGrayScale(self):
        try:
            self.imageOperations.imageToGrayScale()
            self.updatePixmap()

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Empty Image", "Cannot convert to grayscale an empty image.")

    def brightnessSliderValueChanged(self):
        try:
            self.brightnessLabel.setText(f'Brightness Value: {self.brightnessSlider.value()}')

            self.imageOperations.changeBrightness(self.brightnessSlider.value())

            self.updatePixmap()

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Empty Image", "Cannot adjust the brightness of an empty image.")

    def updatePixmap(self):
        pixmap = QPixmap.fromImage(self.imageOperations.cvMatToQImage())
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignTop)

    def undo(self):
        if not self.redoButton.isEnabled():
            self.redoButton.setEnabled(True)

        if len(self.imageOperations.getPreviousImages()) == 1:
            if self.undoButton.isEnabled():
                self.undoButton.setEnabled(False)
        elif len(self.imageOperations.getPreviousImages()) > 1:
            self.undoButton.setEnabled(True)

        self.imageOperations.getNextImages().append(self.imageOperations.getCurrentImage())
        self.imageOperations.setCurrentImage(
            self.imageOperations.getPreviousImages()[len(self.imageOperations.getPreviousImages()) - 1])
        self.imageOperations.getPreviousImages().pop()

        self.updatePixmap()

    def redo(self):
        if not self.undoButton.isEnabled():
            self.undoButton.setEnabled(True)

        if len(self.imageOperations.getNextImages()) == 1:
            if self.redoButton.isEnabled():
                self.redoButton.setEnabled(False)
        elif len(self.imageOperations.getNextImages()) > 1:
            self.redoButton.setEnabled(True)

        self.imageOperations.getPreviousImages().append(self.imageOperations.getCurrentImage())
        self.imageOperations.setCurrentImage(
            self.imageOperations.getNextImages()[len(self.imageOperations.getNextImages()) - 1])
        self.imageOperations.getNextImages().pop()

        self.updatePixmap()
