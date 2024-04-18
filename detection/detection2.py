import cv2
from skimage.metrics import structural_similarity as compare_ssim

def is_frame_different_from_image(frame, reference_image, threshold_ssim=0.85):
    img_reference = cv2.imread(reference_image)
    frame_resized = cv2.resize(frame, (img_reference.shape[1], img_reference.shape[0]))
    gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(img_reference, cv2.COLOR_BGR2GRAY)
    ssim = compare_ssim(gray_frame, gray_reference)
    
    if ssim >= threshold_ssim:
        return False  # Frame is similar to the reference image
    else:
        return True  # Frame is different from the reference image


def detect_movement():
    c2 = cv2.imread("c2.jpg")

    if is_frame_different_from_image(c2, "c1.jpg"):
        print("Movement detected")
        return True
    
    return False
    

def detect_object():
    cap = cv2.VideoCapture(1)  # Try different API here
    ret, frame = cap.read()
    cv2.imwrite("c3.jpg", frame)
    print("RET", ret)

    if not is_frame_different_from_image(frame,"c2.jpg"):
        print("Done")
        cv2.imwrite('waste.jpg', frame)
        return 'waste.jpg'
    
    print("Object moving")
    return ""