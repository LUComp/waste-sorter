
import cv2

if __name__ == "__main__":
    cap = cv2.VideoCapture(1)
    # Loop through every frame until we close our webcam
    while cap.isOpened(): 
        ret, frame = cap.read()
        
        # Show image 
        cv2.imshow('Webcam', frame)
        
        # Checks whether q has been hit and stops the loop
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    # Releases the webcam
    cap.release()
    # Closes the frame
    cv2.destroyAllWindows()