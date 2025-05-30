import socket
import json

socket_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
target_ip = "127.0.0.1"
target_port = 5055

def send_gesture(gesture, x, y, z = 0.5):
    message = json.dumps({
        'gesture' : gesture,
        'position' : {'x' : x, 'y' : y, 'z' : z}
    }).encode('utf-8')
    socket_sender.sendto(message, (target_ip, target_port))
    
