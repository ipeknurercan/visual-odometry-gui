# 📷 Visual Odometry Calibration GUI

This project is a PyQt5-based graphical user interface (GUI) for manually entering, saving, and analyzing camera calibration parameters. It is designed for use in electronic warfare environments where live camera input is not feasible, and the focus is on testing and validating calibration parameters for visual odometry tasks.

---

## 🧩 Features

- Manual input of camera intrinsic and distortion parameters
- Auto-fill fields with default calibration values
- Save and load calibration data using JSON
- Reprojection error histogram visualization
- Built-in log window with save-to-file option

---

## 📦 Requirements

To run the project, install the required Python packages using:

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install PyQt5 matplotlib numpy
```

---

## 🚀 How to Run

In the terminal, navigate to the project directory and run:

```bash
python main.py
```

> Make sure Python is installed and you are using Python 3.7 or later.

---

## 🖼️ Screenshots

### 🛠 Calibration Tab
![calibration_tab](https://github.com/user-attachments/assets/56243fee-7672-4fa8-8942-d86cb800b934)


### 📊 Test Tab
![test_tab](https://github.com/user-attachments/assets/44cd3325-d5b5-426c-8fe7-cfadcef7dc9b)


### 🧾 Logs Tab
![logs_tab](https://github.com/user-attachments/assets/5c98760d-658a-4ad2-bd73-b195cea63630)


> You can find these images in the `screenshots/` folder.

---

## 📁 Project Structure

```
visual-odometry-gui/
├── main.py               # Main Python GUI code
├── README.md             # This documentation file
├── requirements.txt      # Python dependency list
└── screenshots/          # Folder for UI screenshots
```

---

