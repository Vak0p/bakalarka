# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(781, 646)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.side_bar = QFrame(self.central_widget)
        self.side_bar.setObjectName(u"side_bar")
        self.side_bar.setMaximumSize(QSize(250, 16777211))
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.side_bar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.surface_surfer_label = QLabel(self.side_bar)
        self.surface_surfer_label.setObjectName(u"surface_surfer_label")
        self.surface_surfer_label.setTextFormat(Qt.PlainText)

        self.verticalLayout.addWidget(self.surface_surfer_label)

        self.task_button_1 = QPushButton(self.side_bar)
        self.task_button_1.setObjectName(u"task_button_1")
        self.task_button_1.setStyleSheet(u"QPushButton {\n"
"    background-color: #3A3A3A;\n"
"    color: #FFFFFF;\n"
"    text-align: left;\n"
"    padding: 10px 15px;\n"
"    border: none;\n"
"    border-left: 4px solid #C38B6B;\n"
"    border-radius: 5px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"}")

        self.verticalLayout.addWidget(self.task_button_1)

        self.task_button_2 = QPushButton(self.side_bar)
        self.task_button_2.setObjectName(u"task_button_2")
        self.task_button_2.setStyleSheet(u"QPushButton {\n"
"    background-color: #2D2D2D;\n"
"    color: #FFFFFF;\n"
"    text-align: left;\n"
"    padding: 10px 15px;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    font-size: 14px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3A3A3A;\n"
"}")

        self.verticalLayout.addWidget(self.task_button_2)

        self.task_button_3 = QPushButton(self.side_bar)
        self.task_button_3.setObjectName(u"task_button_3")
        self.task_button_3.setStyleSheet(u"QPushButton {\n"
"    background-color: #2D2D2D;\n"
"    color: #FFFFFF;\n"
"    text-align: left;\n"
"    padding: 10px 15px;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    font-size: 14px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3A3A3A;\n"
"}")

        self.verticalLayout.addWidget(self.task_button_3)

        self.v_spacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.v_spacer_4)

        self.recent_files_label = QLabel(self.side_bar)
        self.recent_files_label.setObjectName(u"recent_files_label")

        self.verticalLayout.addWidget(self.recent_files_label)

        self.recent_files_list = QListWidget(self.side_bar)
        self.recent_files_list.setObjectName(u"recent_files_list")
        self.recent_files_list.setMaximumSize(QSize(240, 16777215))
        self.recent_files_list.setStyleSheet(u"QListWidget {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    border-left: 3px solid #C38B6B;\n"
"    padding-left: 10px;\n"
"    color: #FFFFFF;\n"
"    outline: none;\n"
"}")
        self.recent_files_list.setSpacing(0)

        self.verticalLayout.addWidget(self.recent_files_list)

        self.v_spacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.v_spacer_5)

        self.recent_projects_label = QLabel(self.side_bar)
        self.recent_projects_label.setObjectName(u"recent_projects_label")

        self.verticalLayout.addWidget(self.recent_projects_label)

        self.recent_projects_list = QListWidget(self.side_bar)
        self.recent_projects_list.setObjectName(u"recent_projects_list")
        self.recent_projects_list.setStyleSheet(u"QListWidget {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    border-left: 3px solid #C38B6B;\n"
"    padding-left: 10px;\n"
"    color: #FFFFFF;\n"
"    outline: none;\n"
"}")

        self.verticalLayout.addWidget(self.recent_projects_list)


        self.horizontalLayout.addWidget(self.side_bar)

        self.main_area = QFrame(self.central_widget)
        self.main_area.setObjectName(u"main_area")
        self.main_area.setFrameShape(QFrame.StyledPanel)
        self.main_area.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.main_area)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(15, -1, -1, -1)
        self.label_3 = QLabel(self.main_area)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(self.main_area)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.drag_and_drop_zone = QFrame(self.main_area)
        self.drag_and_drop_zone.setObjectName(u"drag_and_drop_zone")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drag_and_drop_zone.sizePolicy().hasHeightForWidth())
        self.drag_and_drop_zone.setSizePolicy(sizePolicy)
        self.drag_and_drop_zone.setMinimumSize(QSize(0, 200))
        self.drag_and_drop_zone.setStyleSheet(u"#drag_and_drop_zone {\n"
"    border: 2px dashed #C38B6B;\n"
"    border-radius: 10px;\n"
"    background-color: transparent;\n"
"}")
        self.drag_and_drop_zone.setFrameShape(QFrame.StyledPanel)
        self.drag_and_drop_zone.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.drag_and_drop_zone)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.v_spacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.v_spacer_2)

        self.video_icon_label = QLabel(self.drag_and_drop_zone)
        self.video_icon_label.setObjectName(u"video_icon_label")

        self.verticalLayout_3.addWidget(self.video_icon_label, 0, Qt.AlignHCenter)

        self.drop_here_label = QLabel(self.drag_and_drop_zone)
        self.drop_here_label.setObjectName(u"drop_here_label")

        self.verticalLayout_3.addWidget(self.drop_here_label, 0, Qt.AlignHCenter)

        self.upload_button = QPushButton(self.drag_and_drop_zone)
        self.upload_button.setObjectName(u"upload_button")
        self.upload_button.setStyleSheet(u"QPushButton {\n"
"    background-color: #C38B6B;\n"
"    color: black;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #D49D7E;\n"
"}")

        self.verticalLayout_3.addWidget(self.upload_button)

        self.formats_label = QLabel(self.drag_and_drop_zone)
        self.formats_label.setObjectName(u"formats_label")

        self.verticalLayout_3.addWidget(self.formats_label, 0, Qt.AlignHCenter)

        self.v_spacer_1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.v_spacer_1)


        self.verticalLayout_2.addWidget(self.drag_and_drop_zone)

        self.requirements_area = QFrame(self.main_area)
        self.requirements_area.setObjectName(u"requirements_area")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.requirements_area.sizePolicy().hasHeightForWidth())
        self.requirements_area.setSizePolicy(sizePolicy1)
        self.requirements_area.setMaximumSize(QSize(16777215, 150))
        self.requirements_area.setFrameShape(QFrame.StyledPanel)
        self.requirements_area.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.requirements_area)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.requirements_label = QLabel(self.requirements_area)
        self.requirements_label.setObjectName(u"requirements_label")

        self.verticalLayout_4.addWidget(self.requirements_label)

        self.requirement_label_1 = QLabel(self.requirements_area)
        self.requirement_label_1.setObjectName(u"requirement_label_1")

        self.verticalLayout_4.addWidget(self.requirement_label_1)

        self.requirement_label2 = QLabel(self.requirements_area)
        self.requirement_label2.setObjectName(u"requirement_label2")

        self.verticalLayout_4.addWidget(self.requirement_label2)

        self.requirement_label_3 = QLabel(self.requirements_area)
        self.requirement_label_3.setObjectName(u"requirement_label_3")

        self.verticalLayout_4.addWidget(self.requirement_label_3)

        self.v_spacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.v_spacer_3)


        self.verticalLayout_2.addWidget(self.requirements_area)


        self.horizontalLayout.addWidget(self.main_area)

        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"MainWindow", None))
        self.surface_surfer_label.setText(QCoreApplication.translate("main_window", u"Surface Surfer", None))
        self.task_button_1.setText(QCoreApplication.translate("main_window", u"1. Source Video Upload", None))
        self.task_button_2.setText(QCoreApplication.translate("main_window", u"2. Trim and Preview", None))
        self.task_button_3.setText(QCoreApplication.translate("main_window", u"3. Stitched Output Map", None))
        self.recent_files_label.setText(QCoreApplication.translate("main_window", u"Recent Files", None))
        self.recent_projects_label.setText(QCoreApplication.translate("main_window", u"Recent projects", None))
        self.label_3.setText(QCoreApplication.translate("main_window", u"Task Sequence #1", None))
        self.label_4.setText(QCoreApplication.translate("main_window", u"Upload Source Video of the Surface", None))
        self.video_icon_label.setText(QCoreApplication.translate("main_window", u"(Video Icon placeholder)", None))
        self.drop_here_label.setText(QCoreApplication.translate("main_window", u"Drag & drop your surface video file here", None))
        self.upload_button.setText(QCoreApplication.translate("main_window", u"+ CHOOSE VIDEO FILE", None))
        self.formats_label.setText(QCoreApplication.translate("main_window", u"Supported video fortmats:", None))
        self.requirements_label.setText(QCoreApplication.translate("main_window", u"Source Video Requirements", None))
        self.requirement_label_1.setText(QCoreApplication.translate("main_window", u"1.", None))
        self.requirement_label2.setText(QCoreApplication.translate("main_window", u"2. ", None))
        self.requirement_label_3.setText(QCoreApplication.translate("main_window", u"3.", None))
    # retranslateUi

