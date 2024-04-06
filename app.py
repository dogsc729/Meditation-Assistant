import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import argparse
import subprocess
from parse_data.parse import parse
from threading import Thread
from sig_process import processing

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-time Frequency Response Plot")
        self.setGeometry(100, 100, 1920, 1080)

        # Create main layout
        layout = QVBoxLayout()

        # Create a Matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Initialize the plots
        self.init_plots()

        # Timer for updating the plots
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000)  # Update plots every 300 milliseconds

    def init_plots(self):
        # Initialize the subplots for each channel
        self.axes = []
        for i in range(8):
            ax = self.figure.add_subplot(4, 2, i+1)
            ax.set_title(f'Channel {i+1}')
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Magnitude')
            self.axes.append(ax)

    def update_plots(self):
        # Get new frequency response data from the processing function
        frequency_responses = processing()

        # Clear the existing plots and plot the new frequency responses for each channel
        for ax, response, i in zip(self.axes, frequency_responses, range(8)):
            ax.clear()
            ax.plot(response[0], response[1])
            ax.set_title(f'Channel {i+1}')
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Magnitude')
        # Update the canvas
        self.canvas.draw()

    def processing(self):
        # Placeholder for processing function, replace this with your actual processing logic
        num_channels = 8
        frequencies = np.linspace(0, 10, 100)
        frequency_responses = []
        for _ in range(num_channels):
            magnitude = np.random.rand(100)
            frequency_responses.append((frequencies, magnitude))
        return frequency_responses

if __name__ == "__main__":
    sys.path.append('./parse_data')
    from parse_data.parse import parse
    parser = argparse.ArgumentParser(description='Script to process a file at a custom location')
    parser.add_argument('file', metavar='FILE', type=str, help='Path to the file to process')
    args = parser.parse_args()
    target = args.file
    target_folder = f"../../../../OpenBCI_GUI/Recordings/OpenBCISession_{target}/"
    output = subprocess.check_output(f"ls -t {target_folder} | head -n 1", shell=True)
    file_name = output.decode("utf-8")
    target_file = target_folder + file_name[:-1] # remove the new line

    t1 = Thread(target = parse, args = (target_file,))
    t1.start()

    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
