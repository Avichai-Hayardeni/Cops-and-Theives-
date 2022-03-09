import socket
from ex2_utils import IPADDR, PORT, MAX_MSG_SIZE, square, Arena, get_arena
import time


my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init new socket and its protocol
my_socket.bind((IPADDR, PORT))                                 # bind the socket with the address
my_socket.listen()                                             # listen to messages from clients

(client_socket, client_address) = my_socket.accept()       # accept connection from a client
print("client connected")
while True:
    client_socket.send("Please choose game arena. \n Reply with '1' to play on icehockey \n '2' to play on pacman \n '3' to play on randomwalls. \n 'q' to quit".encode())

    arena_type = client_socket.recv(MAX_MSG_SIZE).decode() # getting arena number from client
    if arena_type == "q":
        break
    square_list = get_arena(arena_type) # getting a list of the object 'square' using the function in ex2_utils
    game_arena = Arena(square_list) # implementation of the class Arena using the list of squares
    print(game_arena) # using the __str__ method
    while True:
        client_socket.send("Please make your move using the arrows in your keyboard.\nPress the 's' key to get current status.\n".encode()) # asking client to make a move
        move = client_socket.recv(MAX_MSG_SIZE).decode()
        time.sleep(0.5)
        if move == "status":
            near_treasure, near_cop = game_arena.closeness() # 'True' if the cop or the treasure are close
            response = ""
            if near_cop:
                response = "NEAR COP\n"
                if near_treasure:
                    response += "AND NEAR TREASURE\n"
            elif near_treasure:
                response = "NEAR TREASURE\n"
            else:
                response = "GAME ON\n"
            print(game_arena) # prints the game arena in the server
            client_socket.send(response.encode())
        else:
            moved = True
            if not game_arena.can_be_moved(move): # checks whether the square is a wall or not
                client_socket.send("Can't go there buddy. It's a wall!\n".encode())
                moved = False
            else:
                game_arena.move_thief(move) # moves thief accordingly
            game_arena.move_cop() # moves cop randomly
            if game_arena.game_over():
                break
            if moved:
                client_socket.send(f"Moved {move}!\n".encode()) # sends confirmation for moving the thief

    if game_arena.check_lose(): # in case game is over, sends response accordingly
        client_socket.send("You lose\n".encode())
    else:
        client_socket.send("You win\n".encode())
    break

my_socket.close()