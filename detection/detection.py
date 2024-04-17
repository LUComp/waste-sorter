import cv2
import imageio
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
from time import sleep

# Compare current frame to background
def compare_frame_with_image(frame, reference_image):
    img_reference = cv2.imread(reference_image)
    frame_resized = cv2.resize(frame, (img_reference.shape[1], img_reference.shape[0]))
    mse = (frame_resized ** 2).mean()
    ssim = compare_ssim(frame_resized, img_reference) 
    return mse, ssim

# Compare current frame from image
def is_frame_different_from_image(frame, reference_image, threshold_ssim=0.95):
    img_reference = cv2.imread(reference_image)
    frame_resized = cv2.resize(frame, (img_reference.shape[1], img_reference.shape[0]))
    gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(img_reference, cv2.COLOR_BGR2GRAY)
    ssim = compare_ssim(gray_frame, gray_reference)
    
    if ssim >= threshold_ssim:
        return False  # Frame is similar to the reference image
    else:
        return True  # Frame is different from the reference image

def recognition_loop(cap, reference_image):
    while True:
        object_captured = False
        ret, frame = cap.read() 
        
        if is_frame_different_from_image(frame, reference_image):
            imageio.imwrite('c2.jpg', imageio.imread('c1.jpg'))
            #sleep(0.5)
            print("Object detected.")

            while True:
                # Take reference picture C2. Take photos every frame, to detect object movement. Replace c2 with new photo
                ret, frame = cap.read()

                if not is_frame_different_from_image(frame,reference_image='c2.jpg'):
                    cv2.imwrite('waste.jpg', frame)
                    object_captured = True
                    
                    break
                else:
                    cv2.imwrite('c2.jpg', frame)
                    sleep(0.25)
            
        else:
            print("Nothing to declare.")

        # video preview
        # cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q') or object_captured:
            break

def main():
    # Get Background Reference
    cap = cv2.VideoCapture(2) 
    ret,frame = cap.read()
    cv2.imwrite('c1.jpg',frame)
    cap.release()
    reference_image = "c1.jpg"


    # Set camera to rolling
    cap = cv2.VideoCapture(2) 
    recognition_loop(cap, reference_image)
    # Release the capture and close all OpenCV windows
    cap.release()
    # cv2.destroyAllWindows()

main()