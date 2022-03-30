import time
from os import path
from pydm import Display
from pydm.widgets.pushbutton import PyDMPushButton
from pydm.widgets import PyDMLabel
from typhos.alarm import TyphosAlarmCircle
from typhos.related_display import TyphosRelatedSuiteButton

from qtpy.QtWidgets import QHBoxLayout, QLabel
from qtpy import QtCore, QtGui
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont

from ophyd import EpicsSignal


class MirrorScreen(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(MirrorScreen, self).__init__(parent=parent, args=args, macros=macros)
        if macros != None:
            self.x_stop = EpicsSignal(macros['XAXIS'] + ".STOP")
            self.y_stop = EpicsSignal(macros['YAXIS'] + ".STOP")
            self.p_stop = EpicsSignal(macros['PITCH'] + ".STOP")

        self.alarm_box_x = QHBoxLayout()
        self.alarm_box_y = QHBoxLayout()
        self.alarm_box_p = QHBoxLayout()
        self.alarm_box_gantry_x = QHBoxLayout()
        self.alarm_box_gantry_y = QHBoxLayout()
        self.ghost = QHBoxLayout()

        self.alarm_x = TyphosAlarmCircle()
        self.alarm_x.channel = "ca://" + macros['XAXIS']
        self.alarm_x.setMaximumHeight(35)
        self.alarm_x.setMaximumWidth(35)

        self.alarm_y = TyphosAlarmCircle()
        self.alarm_y.channel = "ca://" + macros['YAXIS']
        self.alarm_y.setMaximumHeight(35)
        self.alarm_y.setMaximumWidth(35)

        self.alarm_p = TyphosAlarmCircle()
        self.alarm_p.channel = "ca://" + macros['PITCH']
        self.alarm_p.setMaximumHeight(35)
        self.alarm_p.setMaximumWidth(35)

        label_font = QFont()
        label_font.setBold(True) 


        self.x_label = QLabel("x")
        #self.x_label.setFont(label_font)
        self.y_label = QLabel("y")
        #self.y_label.setFont(label_font)
        self.p_label = QLabel("pitch")
        #self.p_label.setFont(label_font)
        self.gantry_x_label = QLabel("gantry x")
        #self.gantry_x_label.setFont(label_font)
        self.gantry_y_label = QLabel("gantry y")
        #self.gantry_y_label.setFont(label_font)

        self.alarm_gantry_x = TyphosAlarmCircle()
        self.alarm_gantry_x.channel = "ca://" + macros['MIRROR'] + ":HOMS:ALREADY_COUPLED_X_RBV"
        self.alarm_gantry_x.setMaximumHeight(35)
        self.alarm_gantry_x.setMaximumWidth(35)

        self.alarm_gantry_y = TyphosAlarmCircle()
        self.alarm_gantry_y.channel = "ca://" + macros['MIRROR'] + ":HOMS:ALREADY_COUPLED_Y_RBV"
        self.alarm_gantry_y.setMaximumHeight(35)
        self.alarm_gantry_y.setMaximumWidth(35)




        
        self.alarm_box_x.addWidget(self.x_label)
        self.alarm_box_x.setAlignment(self.x_label, Qt.AlignCenter)
        self.alarm_box_x.addWidget(self.alarm_x)

        self.alarm_box_y.addWidget(self.y_label)
        self.alarm_box_y.setAlignment(self.y_label, Qt.AlignCenter)
        self.alarm_box_y.addWidget(self.alarm_y)

        self.alarm_box_p.addWidget(self.p_label)
        self.alarm_box_p.setAlignment(self.p_label, Qt.AlignCenter)
        self.alarm_box_p.addWidget(self.alarm_p)

        self.alarm_box_gantry_x.addWidget(self.gantry_x_label)
        self.alarm_box_gantry_x.setAlignment(self.gantry_x_label, Qt.AlignCenter)
        self.alarm_box_gantry_x.addWidget(self.alarm_gantry_x)

        self.alarm_box_gantry_y.addWidget(self.gantry_y_label)
        self.alarm_box_gantry_y.setAlignment(self.gantry_y_label, Qt.AlignCenter)
        self.alarm_box_gantry_y.addWidget(self.alarm_gantry_y)


        self.stop_button = PyDMPushButton(label="Stop")
        self.stop_button.setMaximumHeight(120)
        self.stop_button.setMaximumWidth(120)
        self.stop_button.clicked.connect(self.stop_motors)
        self.stop_button.setStyleSheet("background: rgb(255,0,0)")

        self.advanced_button = TyphosRelatedSuiteButton()
        
        self.advanced_button.happi_names = [macros['MIRROR'].lower() + "_homs"]
        self.advanced_button.setText("Advanced")

        
        self.ui.horizontalLayout_8.addLayout(self.alarm_box_x)
        self.ui.horizontalLayout_8.addLayout(self.alarm_box_y)
        self.ui.horizontalLayout_8.addLayout(self.alarm_box_p)
        self.ui.horizontalLayout_8.addLayout(self.alarm_box_gantry_x)
        self.ui.horizontalLayout_8.addLayout(self.alarm_box_gantry_y)
        #self.ui.horizontalLayout_8.addWidget(self.alarm_x)
        #self.ui.horizontalLayout_8.addWidget(self.alarm_y)
        #self.ui.horizontalLayout_8.addWidget(self.alarm_p)
        #self.ui.horizontalLayout_8.addWidget(self.stop_button)

        #self.ui.verticalLayout_6.setAlignment(Qt.AlignCenter)
        self.ui.horizontalLayout_14.addWidget(self.advanced_button)
        self.ui.horizontalLayout_14.addSpacing(50)
        self.ui.horizontalLayout_14.addWidget(self.stop_button)
        self.ui.horizontalLayout_14.addSpacing(160)

        self.ui.setGeometry(QtCore.QRect(0,0, 360, 385))

    def stop_motors(self):
        self.x_stop.put(1)
        self.y_stop.put(1)
        self.p_stop.put(1)

    def ui_filename(self):
        # Point to our UI file
        return 'mirrorScreen.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
