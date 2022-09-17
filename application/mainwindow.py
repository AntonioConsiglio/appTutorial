from tkinter import Button
from PySide2.QtWidgets import QMainWindow

from .utils import loadUi
from .videomanager import VideoHandler,VideoManager
from styles import ButtonStyles

buttonsyle = ButtonStyles()


class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen,self).__init__()
        loadUi("./ui_files\mainwindow.ui",self)
        self.videomanager = None
        self.videohandler = None
        self._create_connection()
    
    def _start_video(self):
        if self.videomanager is None:
            self.videomanager = VideoManager((640,480),30)
            self.videohandler = VideoHandler(self.videomanager.image_queue)
            self.videohandler.new_image.connect(self._update_screen)
            self.videohandler.start()
            self.start_button.setStyleSheet(buttonsyle.stop)
            self.start_button.setText('STOP STREAM')
        else:
            self.videomanager.stopqueue.put('stop')
            self.start_button.setStyleSheet(buttonsyle.start)
            self.start_button.setText('START STREAM')
            self.videohandler.new_image.disconnect()
            self.videohandler.stop()
            self.videomanager = None
            while self.videohandler.isRunning():
                pass
            self.videohandler = None
            

    def _update_screen(self,image):
        self.image_screen.setPixmap(image)

    def _create_connection(self):
        self.start_button.clicked.connect(self._start_video)