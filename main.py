from detection.detection import detect_movement, detect_object
import time
import cv2
import imageio.v2 as iio

def camera_preview():
      starttime = time.time()
      frame = None

      while time.time() - starttime < 0.1:
            cap = cv2.VideoCapture(0)  # Try different API here
            ret, frame = cap.read()
            if not ret:
                  print("Error: Failed to capture frame")
                  break
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                  break

      cap.release()
      cv2.imwrite('c2.jpg',frame)


def main():

      while True:

            cap = cv2.VideoCapture(0) 
            ret, frame = cap.read()
            # print("RET", ret)
            cv2.imwrite('c1.jpg',frame)
            cap.release()
            img = ""

            while True:
                  camera_preview()
                  if detect_movement():
                        img = detect_object()
                        if img != "":
                              break
                        
main()
