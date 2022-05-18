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

from ophyd import EpicsSignal, EpicsSignalRO


class MirrorScreen(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(MirrorScreen, self).__init__(parent=parent, args=args, macros=macros)
        if macros != None:
            self.x_stop = EpicsSignal(macros['BASE_PV'] + ":MMS:XUP.STOP")
            self.y_stop = EpicsSignal(macros['BASE_PV'] + ":MMS:YUP.STOP")
            self.p_stop = EpicsSignal(macros['BASE_PV'] + ":MMS:PITCH.STOP")

        coating1 = EpicsSignalRO(macros['BASE_PV'] + ":COATING:STATE:GET_RBV.ONST")
        coating2 = EpicsSignalRO(macros['BASE_PV'] + ":COATING:STATE:GET_RBV.TWST")

        alarm_box_x = QHBoxLayout()
        alarm_box_y = QHBoxLayout()
        alarm_box_p = QHBoxLayout()
        alarm_box_gantry_x = QHBoxLayout()
        alarm_box_gantry_y = QHBoxLayout()
        self.ghost = QHBoxLayout()

        alarm_x = TyphosAlarmCircle()
        alarm_x.channel = "ca://" + macros['BASE_PV'] + ":MMS:XUP"
        alarm_x.setMaximumHeight(35)
        alarm_x.setMaximumWidth(35)

        alarm_y = TyphosAlarmCircle()
        alarm_y.channel = "ca://" + macros['BASE_PV'] + ":MMS:YUP"
        alarm_y.setMaximumHeight(35)
        alarm_y.setMaximumWidth(35)

        alarm_p = TyphosAlarmCircle()
        alarm_p.channel = "ca://" + macros['BASE_PV'] + ":MMS:PITCH"
        alarm_p.setMaximumHeight(35)
        alarm_p.setMaximumWidth(35)

        label_font = QFont()
        label_font.setBold(True) 


        x_label = QLabel("x")
        #self.x_label.setFont(label_font)
        y_label = QLabel("y")
        #self.y_label.setFont(label_font)
        p_label = QLabel("pitch")
        #self.p_label.setFont(label_font)
        gantry_x_label = QLabel("gantry x")
        #self.gantry_x_label.setFont(label_font)
        gantry_y_label = QLabel("gantry y")
        #self.gantry_y_label.setFont(label_font)

        alarm_gantry_x = TyphosAlarmCircle()
        alarm_gantry_x.channel = "ca://" + macros['BASE_PV'] + ":ALREADY_COUPLED_X_RBV"
        alarm_gantry_x.setMaximumHeight(35)
        alarm_gantry_x.setMaximumWidth(35)

        alarm_gantry_y = TyphosAlarmCircle()
        alarm_gantry_y.channel = "ca://" + macros['BASE_PV'] + ":ALREADY_COUPLED_Y_RBV"
        alarm_gantry_y.setMaximumHeight(35)
        alarm_gantry_y.setMaximumWidth(35)




        
        alarm_box_x.addWidget(x_label)
        alarm_box_x.setAlignment(x_label, Qt.AlignCenter)
        alarm_box_x.addWidget(alarm_x)

        alarm_box_y.addWidget(y_label)
        alarm_box_y.setAlignment(y_label, Qt.AlignCenter)
        alarm_box_y.addWidget(alarm_y)

        alarm_box_p.addWidget(p_label)
        alarm_box_p.setAlignment(p_label, Qt.AlignCenter)
        alarm_box_p.addWidget(alarm_p)

        alarm_box_gantry_x.addWidget(gantry_x_label)
        alarm_box_gantry_x.setAlignment(gantry_x_label, Qt.AlignCenter)
        alarm_box_gantry_x.addWidget(alarm_gantry_x)

        alarm_box_gantry_y.addWidget(gantry_y_label)
        alarm_box_gantry_y.setAlignment(gantry_y_label, Qt.AlignCenter)
        alarm_box_gantry_y.addWidget(alarm_gantry_y)


        stop_button = PyDMPushButton(label="Stop")
        stop_button.setMaximumHeight(120)
        stop_button.setMaximumWidth(120)
        stop_button.clicked.connect(self.stop_motors)
        stop_button.setStyleSheet("background: rgb(255,0,0)")

        advanced_button = TyphosRelatedSuiteButton()
        
        advanced_button.happi_names = [macros['DISP_NAME'].lower() + "_soms"]
        advanced_button.setText("Advanced")
        
        self.ui.PyDMPushButton.setText(coating1.get())
        self.ui.PyDMPushButton_2.setText(coating2.get())
        
        self.ui.horizontalLayout_8.addLayout(alarm_box_x)
        self.ui.horizontalLayout_8.addLayout(alarm_box_y)
        self.ui.horizontalLayout_8.addLayout(alarm_box_p)
        self.ui.horizontalLayout_8.addLayout(alarm_box_gantry_x)
        self.ui.horizontalLayout_8.addLayout(alarm_box_gantry_y)

        self.ui.horizontalLayout_14.addWidget(advanced_button)
        self.ui.horizontalLayout_14.addSpacing(50)
        self.ui.horizontalLayout_14.addWidget(stop_button)
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
