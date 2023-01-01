import cv2
import numpy as np
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
class MyApp(App):
    def build(self):
        self.img = Image()
        return self.img

    def on_start(self):
        # Open the webcam and start capturing frames
        self.cap = cv2.VideoCapture(0)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        self.out = cv2.VideoWriter("output.avi", self.fourcc, 5.0, (1280, 720))

        # Schedule the update method to be called at regular intervals
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        # Capture a frame from the webcam and process it using OpenCV
        ret, frame1 = self.cap.read()
        ret, frame2 = self.cap.read()

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) < 900:
                continue

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "hareket: {}".format('var'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)

        # Set the Kivy Image widget's texture to the processed frame
        buf1 = cv2.flip(frame1, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame1.shape[1], frame1.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture1

kivyApp = MyApp()
kivyApp.run()
