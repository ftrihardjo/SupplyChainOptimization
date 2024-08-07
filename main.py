import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pm4py

# Initialize the dataframe globally
df = pd.DataFrame(columns=['case_id', 'activity', 'timestamp'])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Process Mining Desktop App")
        self.setGeometry(100, 100, 800, 600)

        # Set up the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Form for manual data entry
        self.formLayout = QFormLayout()
        self.caseIdInput = QLineEdit()
        self.activityInput = QLineEdit()
        self.timestampInput = QLineEdit()
        self.submitButton = QPushButton("Submit Entry")
        self.submitButton.clicked.connect(self.submit_entry)

        self.formLayout.addRow("Case ID:", self.caseIdInput)
        self.formLayout.addRow("Activity:", self.activityInput)
        self.formLayout.addRow("Timestamp:", self.timestampInput)
        self.formLayout.addWidget(self.submitButton)

        self.loadButton = QPushButton("Load Data")
        self.loadButton.clicked.connect(self.load_data)
        self.formLayout.addWidget(self.loadButton)

        # Add form layout to the main layout
        self.layout.addLayout(self.formLayout)

        # Table to display data
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Case ID', 'Activity', 'Timestamp'])
        self.layout.addWidget(self.table)

        # Set up matplotlib canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Initial update to table and plot
        self.update_table()
        self.update_plot()

    def submit_entry(self):
        global df
        case_id = self.caseIdInput.text()
        activity = self.activityInput.text()
        timestamp = self.timestampInput.text()

        try:
            timestamp = pd.to_datetime(timestamp)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "The timestamp format is incorrect. Please use YYYY-MM-DD HH:MM:SS.")
            return

        new_row = {'case_id': case_id, 'activity': activity, 'timestamp': timestamp}
        df = df.append(new_row, ignore_index=True)
        self.update_table()
        self.update_plot()
        self.clear_inputs()

    def load_data(self):
        global df
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Load Data File", "", "CSV Files (*.csv);;Excel Files (*.xls *.xlsx)", options=options)
        if fileName:
            try:
                if 'csv' in fileName:
                    df = pd.read_csv(fileName)
                elif 'xls' in fileName or 'xlsx' in fileName:
                    df = pd.read_excel(fileName)
                self.update_table()
                self.update_plot()
                QMessageBox.information(self, "Data Loaded", "The data file has been loaded successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")

    def update_table(self):
        global df
        self.table.setRowCount(len(df))
        for i, (index, row) in enumerate(df.iterrows()):
            self.table.setItem(i, 0, QTableWidgetItem(str(row['case_id'])))
            self.table.setItem(i, 1, QTableWidgetItem(row['activity']))
            self.table.setItem(i, 2, QTableWidgetItem(str(row['timestamp'])))
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_plot(self):
        global df
        self.ax.clear()
        if not df.empty:
            try:
                event_log = pm4py.format_dataframe(df, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
                process_model = pm4py.discover_petri_net_alpha(event_log)
                gviz = pm4py.visualization.petrinet.visualizer.apply(process_model[0], process_model[1], process_model[2])
                pm4py.visualization.petrinet.visualizer.view(gviz, self.ax)
                self.canvas.draw()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update plot: {str(e)}")

    def clear_inputs(self):
        self.caseIdInput.clear()
        self.activityInput.clear()
        self.timestampInput.clear()

if __name__ == '__main__':
    # Create the PyQt application
    app = QApplication(sys.argv)

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    # Execute the application
    sys.exit(app.exec_())
