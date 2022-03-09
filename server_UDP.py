import socket
from ex2_utils_UDP import IPADDR, PORT, MAX_MSG_SIZE, square, Arena, get_arena
import time


my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # init new socket and its protocol
my_socket.bind((IPADDR, PORT))                                 # bind the socket with the address

(msg, client_address) = my_socket.recvfrom(MAX_MSG_SIZE)
print(msg.decode())
print("client connected")
while True:
    my_socket.sendto("Please choose game arena. \n Reply with '1' to play on icehockey \n '2' to play on pacman \n '3' to play on randomwalls. \n 'q' to quit".encode(), client_address)

    (arena_type, adder) = my_socket.recvfrom(MAX_MSG_SIZE) # getting arena number from client
    arena_type = arena_type.decode()
    if arena_type == "q":
        break
    square_list = get_arena(arena_type) # getting a list of the object 'square' using the function in ex2_utils
    game_arena = Arena(square_list) # implementation of the class Arena using the list of squares
    print(game_arena) # using the __str__ method
    while True:
        my_socket.sendto("Please make your move using the arrows in your keyboard.\nPress the 's' key to get current status.\n".encode(), client_address) # asking client to make a move
        (move, adder) = my_socket.recvfrom(MAX_MSG_SIZE)
        move = move.decode()
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
            my_socket.sendto(response.encode(), client_address)
        else:
            moved = True
            if not game_arena.can_be_moved(move): # checks whether the square is a wall or not
                my_socket.sendto("Can't go there buddy. It's a wall!\n".encode(), client_address)
                moved = False
            else:
                game_arena.move_thief(move) # moves thief accordingly
            game_arena.move_cop() # moves cop randomly
            if game_arena.game_over():
                break
            if moved:
                my_socket.sendto(f"Moved {move}!\n".encode(), client_address) # sends confirmation for moving the thief

    if game_arena.check_lose(): # in case game is over, sends response accordingly
        my_socket.sendto("You lose\n".encode(), client_address)
    else:
        my_socket.sendto("You win\n".encode(), client_address)
    break

my_socket.close()