from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QTextEdit, QLabel, \
    QProgressBar, QLineEdit, QComboBox, QPushButton
from PyQt5.QtCore import QDateTime, QSize, Qt
import commport


class BatteryStatus:
    def __init__(self, name, size):
        self.value = None
        self.ui = QHBoxLayout()
        self.label = QLabel()
        self.label.setText(name)
        self.label.setFixedSize(QSize(size, 20))
        self.line_edit = QLineEdit()
        self.line_edit.setReadOnly(True)
        self.line_edit.setText("HaveNotReceived")
        self.line_edit.setFixedSize(QSize(100, 20))
        self.ui.addWidget(self.label)
        self.ui.addWidget(self.line_edit)

    def update_value(self, new_value):
        self.value = new_value
        self.line_edit.setText(new_value)


class LogWindow(QTextEdit):
    def __init__(self):
        super().__init__()

    def insert(self, input_text):
        self.append(QDateTime.currentDateTime().toString("hh:mm:ss.zzz") + ": " + input_text)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("BMS GUI by Dungnt232")
        self.setFixedSize(QSize(650, 600))

        # prepare all members for v_layout
        # prepare main_title
        self.main_title = QLabel("APES LAB BATTERY MANAGEMENT SYSTEM")
        self.main_title.setFixedSize(650, 40)
        self.main_title.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # prepare comm_port layout
        self.h_layout_comm = QHBoxLayout()
        self.comm_port_label = QLabel()
        self.comm_port_label.setText("Comm Port:")
        self.comm_port_label.setFixedSize(80, 25)
        self.comm_port_combobox = QComboBox()
        self.comm_port_combobox.setFixedSize(300, 25)
        self.comm_scan_button = QPushButton()
        self.comm_scan_button.setText("Rescan")
        self.comm_scan_button.setFixedSize(100, 25)
        self.comm_connect_button = QPushButton()
        self.comm_connect_button.setText("Connect")
        self.comm_connect_button.setFixedSize(100, 25)
        self.h_layout_comm.addWidget(self.comm_port_label)
        self.h_layout_comm.addWidget(self.comm_port_combobox)
        self.h_layout_comm.addWidget(self.comm_scan_button)
        self.h_layout_comm.addWidget(self.comm_connect_button)

        # prepare command layout
        self.h_layout_command = QHBoxLayout()
        self.command_label = QLabel()
        self.command_label.setText("Command:")
        self.command_label.setFixedSize(80, 25)
        self.command_line_edit = QLineEdit()
        self.command_line_edit.setFixedSize(410, 25)
        self.command_button = QPushButton()
        self.command_button.setText("Send command")
        self.command_button.setFixedSize(100, 25)
        self.h_layout_command.addWidget(self.command_label)
        self.h_layout_command.addWidget(self.command_line_edit)
        self.h_layout_command.addWidget(self.command_button)

        # prepare soc label
        self.soc_label = QLabel()
        self.soc_label.setText("Battery SOC estimated by EKF:")
        self.soc_label.setFixedSize(1000, 40)
        self.soc_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.soc_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # prepare soc progress bar
        self.soc_progress = QProgressBar()

        # prepare label for cell voltages
        self.voltage_label = QLabel()
        self.voltage_label.setText("Battery cell voltages:")
        self.voltage_label.setFixedSize(1000, 40)
        self.voltage_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.voltage_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # prepare g_layout_vol
        self.g_layout_vol = QGridLayout()
        self.vol1 = BatteryStatus("Cell 1:", 40)
        self.vol2 = BatteryStatus("Cell 2:", 40)
        self.vol3 = BatteryStatus("Cell 3:", 40)
        self.vol4 = BatteryStatus("Cell 4:", 40)
        self.g_layout_vol.addLayout(self.vol1.ui, 0, 0, 1, 1)
        self.g_layout_vol.addLayout(self.vol2.ui, 0, 1, 1, 1)
        self.g_layout_vol.addLayout(self.vol3.ui, 0, 2, 1, 1)
        self.g_layout_vol.addLayout(self.vol4.ui, 0, 3, 1, 1)

        # prepare parameter label
        self.parameter_label = QLabel()
        self.parameter_label.setText("Other parameters:")
        self.parameter_label.setFixedSize(1000, 40)
        self.parameter_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.parameter_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # prepare other parameter layout
        self.g_layout_params = QGridLayout()
        self.n_fet_sts = BatteryStatus("N_FET status:", 70)
        self.pack_vol = BatteryStatus("Pack voltage (V):", 90)
        self.curr_vol = BatteryStatus("Pack current (A):", 90)
        self.g_layout_params.addLayout(self.pack_vol.ui, 0, 0, 1, 1)
        self.g_layout_params.addLayout(self.curr_vol.ui, 0, 1, 1, 1)
        self.g_layout_params.addLayout(self.n_fet_sts.ui, 0, 2, 1, 1)

        self.log_window = LogWindow()

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.main_title)
        self.v_layout.addLayout(self.h_layout_comm)
        self.v_layout.addLayout(self.h_layout_command)
        self.v_layout.addWidget(self.soc_label)
        self.v_layout.addWidget(self.soc_progress)
        self.v_layout.addWidget(self.voltage_label)
        self.v_layout.addLayout(self.g_layout_vol)
        self.v_layout.addWidget(self.parameter_label)
        self.v_layout.addLayout(self.g_layout_params)

        self.v_layout.addWidget(self.log_window)
        self.widget = QWidget()
        self.widget.setLayout(self.v_layout)
        self.setCentralWidget(self.widget)

        # prepare communication port and communication port handler
        port = commport.CommPortHandler(self)
