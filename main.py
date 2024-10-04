from gui.control_panel import ControlPanel
from kuka_comm_lib import KukaRobot
import cv2
import torch
import bluetooth

if __name__ == "__main__":
    server_address = "B8:27:EB:9A:19:C0"  # raspberry pi server (claw)
    port = 1

    robot = KukaRobot("192.168.128.195")
    robot.connect()
    robot.set_speed(1)

    rp_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    rp_socket.connect((server_address, port))
    print(f"Connected to the raspberrypi server at {server_address}")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model_d = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
    model_c = torch.load("checkpoints/trash.pth", map_location=device)

    cap = cv2.VideoCapture(0)

    panel = ControlPanel(robot, rp_socket, "Waste Sorter")

    panel.video_stream(cap, model_d, model_c)

    panel.mainloop()

    # Release the webcam when the window is closed
    cap.release()
    cv2.destroyAllWindows()
