import cv2
from PyQt5.QtCore import Qt

import ImageOperations
from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QMessageBox, \
    QFileDialog, QSlider, QComboBox, QApplication, QUndoStack, QTreeWidget, QTreeWidgetItem, QColorDialog, \
    QListWidgetItem, QListWidget
from PyQt5.QtGui import QPixmap, QColor, QIcon


class UX(QMainWindow):
    def __init__(self):
        super().__init__()

        self.imageOperations = ImageOperations.ImageOperations()

        self.menubar = self.menuBar()
        self.horizontalLayout = QVBoxLayout()

        self.central_widget = QWidget()

        self.undoButton = QPushButton("Undo", self.central_widget)
        self.redoButton = QPushButton("Redo", self.central_widget)

        self.averageFilterButton = QPushButton("Average Filter", self.central_widget)
        self.medianFilterButton = QPushButton("Median Filter", self.central_widget)
        self.gaussianFilterButton = QPushButton("Gaussian Filter", self.central_widget)
        self.grayScaleButton = QPushButton("Gray Scale", self.central_widget)

        self.brushButton = QPushButton("Brush", self.central_widget)
        self.sprayButton = QPushButton("Spray", self.central_widget)
        self.penButton = QPushButton("Pen", self.central_widget)
        self.fillButton = QPushButton("Fill", self.central_widget)
        self.rectangleButton = QPushButton("Rectangle", self.central_widget)
        self.circleButton = QPushButton("Circle", self.central_widget)

        self.redColorButton = QPushButton("", self.central_widget)
        self.greenColorButton = QPushButton("", self.central_widget)
        self.blueColorButton = QPushButton("", self.central_widget)
        self.yellowColorButton = QPushButton("", self.central_widget)
        self.magentaColorButton = QPushButton("", self.central_widget)
        self.cyanColorButton = QPushButton("", self.central_widget)
        self.maroonColorButton = QPushButton("", self.central_widget)
        self.darkGreenColorButton = QPushButton("", self.central_widget)
        self.navyColorButton = QPushButton("", self.central_widget)
        self.grayColorButton = QPushButton("", self.central_widget)

        self.colorListLayout = QVBoxLayout()

        self.brightnessLabel = None
        self.filterComboBoxLabel = None

        self.brightnessSlider = None
        self.filterComboBox = None

        self.image_label = QLabel(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.undoRedo_button_layout = QHBoxLayout()
        self.filter_button_layout = QHBoxLayout()
        self.filter_size_layout = QVBoxLayout()
        self.brightness_widgets_layout = QVBoxLayout()
        self.paintButtonsLayout = QVBoxLayout()
        self.centerLayout=QHBoxLayout()

        self.initUI()
        self.fileMenu()
        self.viewMenu()
        self.helpMenu()

        self.hidden = 0

    def initUI(self):
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 900, 900)

        self.initUndoRedoButtonsAndLayout()
        self.initFilterButtonsAndLayout()

        self.button_layout.addWidget(self.grayScaleButton)

        self.initBrightnessSlider()

        self.initPaintWidgets()

        self.main_layout.addLayout(self.button_layout)

        self.paintButtonsLayout.addWidget(self.brushButton)
        self.paintButtonsLayout.addWidget(self.sprayButton)
        self.paintButtonsLayout.addWidget(self.penButton)
        self.paintButtonsLayout.addWidget(self.fillButton)
        self.paintButtonsLayout.addWidget(self.rectangleButton)
        self.paintButtonsLayout.addWidget(self.circleButton)

        self.paintButtonsLayout.addLayout(self.colorListLayout)

        self.centerLayout.addLayout(self.paintButtonsLayout)
        self.centerLayout.addWidget(self.image_label)

        self.main_layout.addLayout(self.centerLayout)

        self.central_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.central_widget)

        self.setStyleOfWidgets()

        self.connectWidgets()

    def initUndoRedoButtonsAndLayout(self):
        self.undoButton.setDisabled(True)
        self.redoButton.setDisabled(True)

        self.undoRedo_button_layout.addWidget(self.undoButton)
        self.undoRedo_button_layout.addWidget(self.redoButton)
        self.button_layout.addLayout(self.undoRedo_button_layout)

    def initFilterButtonsAndLayout(self):
        self.filter_button_layout.addWidget(self.averageFilterButton)
        self.filter_button_layout.addWidget(self.medianFilterButton)
        self.filter_button_layout.addWidget(self.gaussianFilterButton)

        self.filterComboBoxLabel = QLabel('Fileter Size')
        self.filterComboBox = QComboBox(self)
        self.filterComboBox.addItem("3")
        self.filterComboBox.addItem("5")
        self.filterComboBox.addItem("7")
        self.filterComboBox.addItem("9")
        self.filterComboBox.addItem("11")
        self.filterComboBox.addItem("13")
        self.filterComboBox.addItem("15")

        self.filter_size_layout.addWidget(self.filterComboBoxLabel)
        self.filter_size_layout.addWidget(self.filterComboBox)
        self.filter_button_layout.addLayout(self.filter_size_layout)

        self.button_layout.addLayout(self.filter_button_layout)

    def initBrightnessSlider(self):
        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setSingleStep(1)
        self.brightnessSlider.setValue(0)
        self.brightnessLabel = QLabel('Brightness Value: 0')

        self.brightnessSlider.setMaximumSize(140, 20)
        self.brightnessLabel.setMaximumSize(140, 20)

        self.brightness_widgets_layout.addWidget(self.brightnessLabel)
        self.brightness_widgets_layout.addWidget(self.brightnessSlider)

        self.button_layout.addLayout(self.brightness_widgets_layout)


    def initPaintWidgets(self):
        self.brushButton.setFixedWidth(150)
        self.sprayButton.setFixedWidth(150)
        self.penButton.setFixedWidth(150)
        self.fillButton.setFixedWidth(150)
        self.rectangleButton.setFixedWidth(150)
        self.circleButton.setFixedWidth(150)

        original_pixmap = QPixmap("D:/anul 4/eu/Proiect PIU - Image Editor/icons/spray.png")
        desired_size = (32, 32)
        pixmap = original_pixmap.scaled(*desired_size)
        icon = QIcon(pixmap)
        self.sprayButton.setIcon(icon)
        self.sprayButton.setIconSize(pixmap.size())

        original_pixmap = QPixmap("D:/anul 4/eu/Proiect PIU - Image Editor/icons/fill.png")
        desired_size = (32, 32)
        pixmap = original_pixmap.scaled(*desired_size)
        icon = QIcon(pixmap)
        self.fillButton.setIcon(icon)
        self.fillButton.setIconSize(pixmap.size())

        original_pixmap = QPixmap("D:/anul 4/eu/Proiect PIU - Image Editor/icons/square.png")
        desired_size = (32, 32)
        pixmap = original_pixmap.scaled(*desired_size)
        icon = QIcon(pixmap)
        self.rectangleButton.setIcon(icon)
        self.rectangleButton.setIconSize(pixmap.size())

        original_pixmap = QPixmap("D:/anul 4/eu/Proiect PIU - Image Editor/icons/circle.png")
        desired_size = (32, 32)
        pixmap = original_pixmap.scaled(*desired_size)
        icon = QIcon(pixmap)
        self.circleButton.setIcon(icon)
        self.circleButton.setIconSize(pixmap.size())


        original_pixmap = QPixmap("D:/anul 4/eu/Proiect PIU - Image Editor/icons/brush.png")
        desired_size = (32, 32)
        pixmap = original_pixmap.scaled(*desired_size)
        icon = QIcon(pixmap)
        self.brushButton.setIcon(icon)
        self.brushButton.setIconSize(pixmap.size())

        # Red Color Button
        self.redColorButton.setStyleSheet("QPushButton { background-color: rgb(255, 0, 0); }"
                                          "QPushButton:hover { background-color: rgb(200, 0, 0); }")
        self.redColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.redColorButton)

        # Green Color Button
        self.greenColorButton.setStyleSheet("QPushButton { background-color: rgb(0, 255, 0); }"
                                            "QPushButton:hover { background-color: rgb(0, 200, 0); }")
        self.greenColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.greenColorButton)

        # Blue Color Button
        self.blueColorButton.setStyleSheet("QPushButton { background-color: rgb(0, 0, 255); }"
                                           "QPushButton:hover { background-color: rgb(0, 0, 200); }")
        self.blueColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.blueColorButton)

        # Yellow Color Button
        self.yellowColorButton.setStyleSheet("QPushButton { background-color: rgb(255, 255, 0); }"
                                             "QPushButton:hover { background-color: rgb(200, 200, 0); }")
        self.yellowColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.yellowColorButton)

        # Magenta Color Button
        self.magentaColorButton.setStyleSheet("QPushButton { background-color: rgb(255, 0, 255); }"
                                              "QPushButton:hover { background-color: rgb(200, 0, 200); }")
        self.magentaColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.magentaColorButton)

        # Cyan Color Button
        self.cyanColorButton.setStyleSheet("QPushButton { background-color: rgb(0, 255, 255); }"
                                           "QPushButton:hover { background-color: rgb(0, 200, 200); }")
        self.cyanColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.cyanColorButton)

        # Maroon Color Button
        self.maroonColorButton.setStyleSheet("QPushButton { background-color: rgb(128, 0, 0); }"
                                             "QPushButton:hover { background-color: rgb(100, 0, 0); }")
        self.maroonColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.maroonColorButton)

        # Dark Green Color Button
        self.darkGreenColorButton.setStyleSheet("QPushButton { background-color: rgb(0, 128, 0); }"
                                                "QPushButton:hover { background-color: rgb(0, 100, 0); }")
        self.darkGreenColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.darkGreenColorButton)

        # Navy Color Button
        self.navyColorButton.setStyleSheet("QPushButton { background-color: rgb(0, 0, 128); }"
                                           "QPushButton:hover { background-color: rgb(0, 0, 100); }")
        self.navyColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.navyColorButton)

        # Gray Color Button
        self.grayColorButton.setStyleSheet("QPushButton { background-color: rgb(128, 128, 128); }"
                                           "QPushButton:hover { background-color: rgb(100, 100, 100); }")
        self.grayColorButton.setFixedWidth(50)
        self.colorListLayout.addWidget(self.grayColorButton)



    def setStyleOfWidgets(self):
        self.setStyleSheet("")

        border_style = "border: 2px solid black;"
        self.image_label.setStyleSheet(border_style)

        self.setStyleSheet("""
            QMenuBar {
                background-color: #333333;
                color: #ffaa00;
                border: 1px solid #000000;
            }

            QMenuBar::item {
                background-color: #333333;
                color: #ffaa00;
                padding: 8px 16px;
                border-radius: 4px;
            }

            QMenuBar::item:selected {
                background-color: #ffaa00;
                color: #333333;
            }

            QMenu {
                background-color: #333333;
                color: #ffaa00;
                border: 1px solid #000000;
            }

            QMenu::item {
                background-color: #333333;
                color: #ffaa00;
                padding: 8px 16px;
                border-radius: 4px;
            }

            QMenu::item:selected {
                background-color: #ffaa00;
                color: #333333;
            }

            QPushButton {
                background-color: #ffaa00;
                color: #333333;
                border: 1px solid #000000;
                padding: 10px 20px;
                border-radius: 5px;
            }

            QPushButton:hover 
                background-color: #ffcc33;
            }

            QPushButton:pressed {
                background-color: #cc8800;
            }

            QSlider::groove:horizontal {
                background: #555555;
                height: 5px;
            }

            QSlider::handle:horizontal {
                background: #ffaa00;
                border: 1px solid #000000;
                width: 16px;
                margin: -8px 0;
                border-radius: 8px;
            }

            QLabel {
                color: #000000;
                padding: 4px;
            }
        """)

        self.filter_button_layout.setContentsMargins(15, 10, 15, 10)
        self.brightness_widgets_layout.setContentsMargins(15, 0, 15, 0)

    def connectWidgets(self):
        self.undoButton.clicked.connect(self.undo)
        self.redoButton.clicked.connect(self.redo)

        self.averageFilterButton.clicked.connect(self.onAverageFilterButtonPressed)
        self.medianFilterButton.clicked.connect(self.onMedianFilterButtonPressed)
        self.gaussianFilterButton.clicked.connect(self.onGaussianFilterButtonPressed)
        self.filterComboBox.currentIndexChanged.connect(self.onComboIndexChanged)
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
            self.filterComboBox.hide()
            self.medianFilterButton.hide()
            self.grayScaleButton.hide()
            self.brightnessLabel.hide()
            self.brightnessSlider.hide()

            self.hidden = 1

        elif self.hidden == 1:
            self.redoButton.setHidden(False)
            self.undoButton.setHidden(False)
            self.averageFilterButton.setHidden(False)
            self.filterComboBox.setHidden(False)
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
        if len(self.imageOperations.getPreviousImages()) != 0:
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

    def closeEvent(self, event):
        self.exitFile()
        event.accept()

    def onComboIndexChanged(self):
        self.filterComboBox.currentText()

    def onAverageFilterButtonPressed(self):
        try:
            self.imageOperations.applyAverageFilter(int(self.filterComboBox.currentText()))
            self.updatePixmap()

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Empty Image", "Cannot apply Average Filter to an empty image.")

    def onMedianFilterButtonPressed(self):
        try:
            self.imageOperations.applyMedianFilter(int(self.filterComboBox.currentText()))
            self.updatePixmap()

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Empty Image", "Cannot apply Median Filter to an empty image.")

    def onGaussianFilterButtonPressed(self):
        try:
            self.imageOperations.applyGaussianFilter(int(self.filterComboBox.currentText()))
            self.updatePixmap()

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Empty Image", "Cannot apply Gaussian Filter to an empty image.")

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
        self.qUndoStack.push()
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
