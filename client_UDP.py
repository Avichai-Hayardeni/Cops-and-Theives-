
import socket  # import socket module to enable working over sockets
from ex2_utils_UDP import IPADDR, PORT, MAX_MSG_SIZE  # shared consts for connection details
import keyboard
import time

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # init new socket and its protocol
my_socket.connect((IPADDR, PORT))  # connect to the server via address and port
my_socket.sendto("sup".encode(), (IPADDR, PORT))
while True:
    (data, adder) = my_socket.recvfrom(MAX_MSG_SIZE) # initial message from server
    print(data.decode())

    arena_type = input(": ")
    while arena_type not in ['1', '2', '3', 'q']: # accepted responses for arena type
        print("Wrong map buddy. Try again:")
        arena_type = input(": ")
    my_socket.sendto(arena_type.encode(), (IPADDR, PORT))
    if arena_type == "q":
        break

    move = ""
    while True:
        (data, adder) = my_socket.recvfrom(MAX_MSG_SIZE)
        data = data.decode()
        if data in ["You win", "You lose"]: # if game is over:
            break
        print(data)
        while True: # gets a move or a status request using the arrows on keyboard or the 's' key
            try:
                if keyboard.is_pressed("s"):
                    move = "status"
                    break
                elif keyboard.is_pressed("up"):
                    move = "up"
                    break
                elif keyboard.is_pressed("down"):
                    move = "down"
                    break
                elif keyboard.is_pressed("right"):
                    move = "right"
                    break
                elif keyboard.is_pressed("left"):
                    move = "left"
                    break
            except:
                break
        my_socket.sendto(move.encode(), (IPADDR, PORT)) # sends move
        time.sleep(0.5)
        (data, adder) = my_socket.recvfrom(MAX_MSG_SIZE) # gets whether the move was accepted (no wall) or game is over
        data = data.decode()
        if data in ["You win", "You lose"]:
            break
        print(data)
    print(data)


my_socket.close()