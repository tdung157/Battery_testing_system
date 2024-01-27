import paho.mqtt.client as mqtt
from PyQt5.QtCore import QDateTime
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtCore


class CommPortHandler:
    def __init__(self, parent):
        super(CommPortHandler, self).__init__()
        self.parent = parent
        self.scan_port()
        self.open_flag = False
        self.msg_timer = QtCore.QTimer()
        self.timeout_counter = 0
        self.serial_port = QSerialPort()
        self.mqtt_port = mqtt.Client()
        self.mqtt_port.on_message = self.on_message

        # connect
        self.parent.comm_scan_button.clicked.connect(lambda: self.scan_port())
        self.parent.comm_connect_button.clicked.connect(lambda: self.handle_connect_button())
        self.parent.command_button.clicked.connect(lambda: self.send_command(self.parent.command_line_edit.text()))
        self.msg_timer.timeout.connect(self.message_timeout)

    def on_message(self, client, userdata, msg):
        self.message_parse(str(msg.payload))
        self.parent.comm_port_label.setStyleSheet("color: black;")
        self.timeout_counter = 0

    def scan_port(self):
        self.parent.comm_port_combobox.clear()
        self.parent.comm_port_combobox.addItems(["MQTT server"])
        self.parent.comm_port_combobox.addItems([port.portName() for port in QSerialPortInfo().availablePorts()])

    def handle_connect_button(self):
        if self.open_flag:
            self.disconnect_port()
        else:
            self.connect_port()

    def connect_port(self):
        if self.parent.comm_port_combobox.currentText() == "MQTT server":
            try:
                self.mqtt_port.connect("192.168.1.94", 1883, 60)
                self.mqtt_port.subscribe("monitor_topic")
                r = True
            except:
                r = False
            self.mqtt_port.loop_start()
        else:
            self.serial_port.setBaudRate(115200)
            self.serial_port.setPortName(self.parent.comm_port_combobox.currentText())
            self.serial_port.setDataBits(QSerialPort.DataBits.Data8)
            self.serial_port.setParity(QSerialPort.Parity.NoParity)
            self.serial_port.setStopBits(QSerialPort.StopBits.OneStop)
            self.serial_port.setFlowControl(QSerialPort.FlowControl.NoFlowControl)
            r = self.serial_port.open(QtCore.QIODevice.OpenModeFlag.ReadWrite)
        if not r:
            self.parent.log_window.insert('Port open error')
        else:
            self.parent.log_window.insert('Port successfully opened')
            self.parent.comm_scan_button.setEnabled(False)
            self.parent.comm_port_combobox.setEnabled(False)
            self.msg_timer.start(1000)
            self.open_flag = True

    def disconnect_port(self):
        if self.parent.comm_port_combobox.currentText() == "MQTT server":
            self.mqtt_port.loop_stop()
            self.mqtt_port.disconnect()
            self.mqtt_port.__del__()
            self.mqtt_port.__init__()
            self.mqtt_port.on_message = self.on_message
        else:
            self.serial_port.close()
        self.parent.comm_port_label.setStyleSheet("color: black;")
        self.timeout_counter = 0
        self.parent.log_window.insert('Port closed')
        self.parent.comm_scan_button.setEnabled(True)
        self.parent.comm_port_combobox.setEnabled(True)
        self.open_flag = False

    def message_parse(self, buffer=""):
        if self.parent.comm_port_combobox.currentText() == "MQTT server":
            buffer = buffer.split('\'', 1)[1].split('\'', 1)[0]
            param = buffer.split(' ')
            self.parent.soc_progress.setValue(int(param[0]))
            self.parent.vol1.update_value(param[1])
            self.parent.vol2.update_value(param[2])
            self.parent.vol3.update_value(param[3])
            self.parent.vol4.update_value(param[4])
            self.parent.pack_vol.update_value(param[5])  
            self.parent.curr_vol.update_value(param[6])
            print("message being parsed", param[4])
            if param[7] == "1":
                self.parent.n_fet_sts.update_value("Close")
            else:
                self.parent.n_fet_sts.update_value("Open")
        else:
            pass

    def send_command(self, payload):
        # self.mqtt_port.publish("monitor_topic", payload)
        print("" + str(self.msg_timer.isActive()) + " " + str(self.msg_timer.remainingTime()))

    def message_timeout(self):
        self.timeout_counter += 1
        if self.timeout_counter == 5:
            self.parent.comm_port_label.setStyleSheet("color: red;")
            self.parent.log_window.insert("Message timeout!!")
