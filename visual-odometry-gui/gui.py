import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QLabel, QPushButton, QHBoxLayout, QTextEdit, QTabWidget,
    QFileDialog, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class CalibrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Electronic Warfare Calibration Interface")
        self.setGeometry(100, 100, 950, 720)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tabs
        self.calibration_tab = QWidget()
        self.test_tab = QWidget()
        self.log_tab = QWidget()

        self.tabs.addTab(self.calibration_tab, "Calibration")
        self.tabs.addTab(self.test_tab, "Test")
        self.tabs.addTab(self.log_tab, "Logs")

        # Setup tabs
        self.init_calibration_tab()
        self.init_test_tab()
        self.init_log_tab()

        # Internal state
        self.calibration_data = {}

    def init_calibration_tab(self):
        layout = QVBoxLayout()

        # --- Camera Intrinsics Group ---
        intrinsics_group = QGroupBox("Camera Intrinsics")
        intrinsics_layout = QFormLayout()
        self.fx_input = QLineEdit()
        self.fy_input = QLineEdit()
        self.skew_input = QLineEdit()
        self.cx_input = QLineEdit()
        self.cy_input = QLineEdit()
        intrinsics_layout.addRow("Focal Length fx:", self.fx_input)
        intrinsics_layout.addRow("Focal Length fy:", self.fy_input)
        intrinsics_layout.addRow("Skew:", self.skew_input)
        intrinsics_layout.addRow("Principal Point cx:", self.cx_input)
        intrinsics_layout.addRow("Principal Point cy:", self.cy_input)
        intrinsics_group.setLayout(intrinsics_layout)

        # --- Radial Distortion ---
        radial_group = QGroupBox("Radial Distortion Coefficients")
        radial_layout = QFormLayout()
        self.k1_input = QLineEdit()
        self.k2_input = QLineEdit()
        radial_layout.addRow("k1:", self.k1_input)
        radial_layout.addRow("k2:", self.k2_input)
        radial_group.setLayout(radial_layout)

        # --- Tangential Distortion ---
        tangential_group = QGroupBox("Tangential Distortion Coefficients")
        tangential_layout = QFormLayout()
        self.p1_input = QLineEdit()
        self.p2_input = QLineEdit()
        tangential_layout.addRow("p1:", self.p1_input)
        tangential_layout.addRow("p2:", self.p2_input)
        tangential_group.setLayout(tangential_layout)

        # --- Image Size ---
        image_size_group = QGroupBox("Image Size")
        image_size_layout = QFormLayout()
        self.img_height_input = QLineEdit()
        self.img_width_input = QLineEdit()
        image_size_layout.addRow("Height (pixels):", self.img_height_input)
        image_size_layout.addRow("Width (pixels):", self.img_width_input)
        image_size_group.setLayout(image_size_layout)

        # --- Calibration Settings ---
        calib_settings_group = QGroupBox("Calibration Settings")
        calib_settings_layout = QFormLayout()
        self.num_patterns_input = QLineEdit()
        self.world_units_input = QLineEdit()
        self.estimate_skew_input = QLineEdit()
        self.num_radial_coeff_input = QLineEdit()
        self.estimate_tangential_input = QLineEdit()
        calib_settings_layout.addRow("Number of Patterns:", self.num_patterns_input)
        calib_settings_layout.addRow("World Units:", self.world_units_input)
        calib_settings_layout.addRow("Estimate Skew (0 or 1):", self.estimate_skew_input)
        calib_settings_layout.addRow("Num Radial Distortion Coefficients:", self.num_radial_coeff_input)
        calib_settings_layout.addRow("Estimate Tangential Distortion (0 or 1):", self.estimate_tangential_input)
        calib_settings_group.setLayout(calib_settings_layout)

        # --- Accuracy of Estimation ---
        accuracy_group = QGroupBox("Accuracy of Estimation")
        accuracy_layout = QFormLayout()
        self.mean_reproj_error_input = QLineEdit()
        accuracy_layout.addRow("Mean Reprojection Error:", self.mean_reproj_error_input)
        accuracy_group.setLayout(accuracy_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_auto_fill = QPushButton("Auto Fill Calibration Data")
        self.btn_auto_fill.clicked.connect(self.auto_fill_calibration)
        self.btn_save_json = QPushButton("Save Calibration Data (JSON)")
        self.btn_save_json.clicked.connect(self.save_calibration)
        self.btn_load_json = QPushButton("Load Calibration Data (JSON)")
        self.btn_load_json.clicked.connect(self.load_calibration)
        btn_layout.addWidget(self.btn_auto_fill)
        btn_layout.addWidget(self.btn_save_json)
        btn_layout.addWidget(self.btn_load_json)

        # Assemble layout
        layout.addWidget(intrinsics_group)
        layout.addWidget(radial_group)
        layout.addWidget(tangential_group)
        layout.addWidget(image_size_group)
        layout.addWidget(calib_settings_group)
        layout.addWidget(accuracy_group)
        layout.addLayout(btn_layout)

        self.calibration_tab.setLayout(layout)

    def init_test_tab(self):
        layout = QVBoxLayout()

        # Figure for plots
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_run_test = QPushButton("Run Test & Plot")
        self.btn_run_test.clicked.connect(self.run_test_and_plot)
        btn_layout.addWidget(self.btn_run_test)

        layout.addWidget(self.canvas)
        layout.addLayout(btn_layout)

        self.test_tab.setLayout(layout)

    def init_log_tab(self):
        layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # Save log button
        self.btn_save_log = QPushButton("Save Log to File")
        self.btn_save_log.clicked.connect(self.save_log_to_file)
        layout.addWidget(self.btn_save_log)

        self.log_tab.setLayout(layout)

    def auto_fill_calibration(self):
        # Fill default calibration values
        self.fx_input.setText("1413.3")
        self.fy_input.setText("1418.8")
        self.skew_input.setText("0")
        self.cx_input.setText("950.0639")
        self.cy_input.setText("543.3796")
        self.k1_input.setText("-0.0091")
        self.k2_input.setText("0.0666")
        self.p1_input.setText("0")
        self.p2_input.setText("0")
        self.img_height_input.setText("1080")
        self.img_width_input.setText("1920")
        self.num_patterns_input.setText("33")
        self.world_units_input.setText("millimeters")
        self.estimate_skew_input.setText("0")
        self.num_radial_coeff_input.setText("2")
        self.estimate_tangential_input.setText("0")
        self.mean_reproj_error_input.setText("0.6450")

        self.log("Auto-filled calibration data with default values.")

    def save_calibration(self):
        try:
            data = self.collect_calibration_data()
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Calibration Data", "", "JSON Files (*.json)", options=options)
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                self.log(f"Calibration data saved to {file_path}")
            else:
                self.log("Save operation canceled.")
        except Exception as e:
            self.log(f"Error saving calibration: {str(e)}")

    def load_calibration(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Load Calibration Data", "", "JSON Files (*.json)", options=options)
            if file_path:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                self.apply_calibration_data(data)
                self.log(f"Calibration data loaded from {file_path}")
            else:
                self.log("Load operation canceled.")
        except Exception as e:
            self.log(f"Error loading calibration: {str(e)}")

    def collect_calibration_data(self):
        # Converts widget text to proper types, raises ValueError if conversion fails
        return {
            "CameraIntrinsics": {
                "FocalLength": [float(self.fx_input.text()), float(self.fy_input.text())],
                "Skew": float(self.skew_input.text()),
                "PrincipalPoint": [float(self.cx_input.text()), float(self.cy_input.text())]
            },
            "RadialDistortion": [float(self.k1_input.text()), float(self.k2_input.text())],
            "TangentialDistortion": [float(self.p1_input.text()), float(self.p2_input.text())],
            "ImageSize": [int(self.img_height_input.text()), int(self.img_width_input.text())],
            "CalibrationSettings": {
                "NumPatterns": int(self.num_patterns_input.text()),
                "WorldUnits": self.world_units_input.text(),
                "EstimateSkew": int(self.estimate_skew_input.text()),
                "NumRadialDistortionCoefficients": int(self.num_radial_coeff_input.text()),
                "EstimateTangentialDistortion": int(self.estimate_tangential_input.text())
            },
            "AccuracyOfEstimation": {
                "MeanReprojectionError": float(self.mean_reproj_error_input.text())
            }
        }

    def apply_calibration_data(self, data):
        try:
            intr = data["CameraIntrinsics"]
            self.fx_input.setText(str(intr["FocalLength"][0]))
            self.fy_input.setText(str(intr["FocalLength"][1]))
            self.skew_input.setText(str(intr["Skew"]))
            self.cx_input.setText(str(intr["PrincipalPoint"][0]))
            self.cy_input.setText(str(intr["PrincipalPoint"][1]))

            rad = data["RadialDistortion"]
            self.k1_input.setText(str(rad[0]))
            self.k2_input.setText(str(rad[1]))

            tan = data["TangentialDistortion"]
            self.p1_input.setText(str(tan[0]))
            self.p2_input.setText(str(tan[1]))

            img = data["ImageSize"]
            self.img_height_input.setText(str(img[0]))
            self.img_width_input.setText(str(img[1]))

            cs = data["CalibrationSettings"]
            self.num_patterns_input.setText(str(cs["NumPatterns"]))
            self.world_units_input.setText(cs["WorldUnits"])
            self.estimate_skew_input.setText(str(cs["EstimateSkew"]))
            self.num_radial_coeff_input.setText(str(cs["NumRadialDistortionCoefficients"]))
            self.estimate_tangential_input.setText(str(cs["EstimateTangentialDistortion"]))

            ae = data["AccuracyOfEstimation"]
            self.mean_reproj_error_input.setText(str(ae["MeanReprojectionError"]))

        except Exception as e:
            self.log(f"Error applying calibration data: {str(e)}")

    def run_test_and_plot(self):
        try:
            # Öncelikle parametreleri al
            calib = self.collect_calibration_data()

            # Mean reprojection error gösterecek şekilde basit histogram örneği yapalım
            mean_err = calib["AccuracyOfEstimation"]["MeanReprojectionError"]

            # Örnek olarak rastgele 100 hata değeri oluşturup histogram yapalım (gerçekte dosyadan veya hesaplama ile olur)
            np.random.seed(0)
            errors = np.abs(np.random.normal(loc=mean_err, scale=mean_err*0.3, size=100))

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.hist(errors, bins=20, color='dodgerblue', edgecolor='black')
            ax.set_title("Reprojection Error Histogram")
            ax.set_xlabel("Error")
            ax.set_ylabel("Frequency")
            ax.grid(True)
            self.canvas.draw()

            self.log("Test completed and plot generated successfully.")

        except Exception as e:
            self.log(f"Test failed: {str(e)}")

    def log(self, message):
        self.log_text.append(message)
        # Scroll to bottom
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def save_log_to_file(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Log File", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(self.log_text.toPlainText())
                self.log(f"Log saved to {file_path}")
            else:
                self.log("Log save operation canceled.")
        except Exception as e:
            self.log(f"Error saving log: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalibrationWindow()
    window.show()
    sys.exit(app.exec_())
