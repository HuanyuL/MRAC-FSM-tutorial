import socket

# === CONFIG ===
UDP_IP = "192.168.10.120"
UDP_PORT_GH = 5060
SEND_RATE = 1  # seconds

# === SETUP SOCKET ===
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

i = 0
 # Send FSM state to Grasshopper
while i<1:
    # Send the FSM state to Grasshopper
    fsm_state = "I love Huanyu"
    print(f"[INFO] Sending FSM state: {fsm_state}")
    sock_send.sendto(fsm_state.encode("utf-8"), (UDP_IP, UDP_PORT_GH))
    i += 1 


