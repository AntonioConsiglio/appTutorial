from multiprocessing import Process, Queue

from PySide2.QtCore import QThread,Signal
from PySide2.QtGui import QImage,QPixmap

from cameraLib import DeviceManager

class VideoHandler(QThread):

    new_image = Signal(QPixmap)

    def __init__(self,imagequeue):
        super(VideoHandler,self).__init__()
        self.state = True
        self.imagequeu = imagequeue

    def run(self):
        while self.state:
            image = self.imagequeu.get()
            image = self._convert_to_qt(image)
            self.new_image.emit(image)

    def _convert_to_qt(self,image):
        image = QImage(image,640,480,QImage.Format.Format_BGR888)
        qtimage = QPixmap.fromImage(image)
        return qtimage

    def stop(self):
        self.state = False



class VideoManager():

    def __init__(self,size,fps):
        self.image_queue = Queue()
        self.stopqueue = Queue()
        self.p = Process(name='camera',target=self.run,args=[size,fps,self.image_queue,self.stopqueue])
        self.p.start()

    def run(self,size,fps,imagequeue,stopqueue):
        self.size = size
        self.fps = fps
        self.image_queue = imagequeue
        self.stopqueue = stopqueue
        self.camera = DeviceManager(self.size,self.fps,False)
        self.camera.enable_device()

        while self.stopqueue.empty():
            state,frames = self.camera.poll_for_frames()
            if state:
                self.image_queue.put(frames['color_image'])
