import socket
import sys


# classes and functions of player
class Player:
    def __init__(self, Name, Money_sum):
        self.Name = Name
        self.Money_sum = Money_sum


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # opening object of type socket
conn.connect((HOST, PORT))


def PlayGame(conn):
    i = 1
    while i > 0:
        msg = conn.recv(1024).decode()
        print(msg)
        if msg == "Do you want to play a game\n":  # a condition for giving the player to set hiw name
            msg = input("\npress 1 for play or 0 for not playing").encode()
            if msg == "0" or msg == "1":
                if msg == "0":
                    print("Goodbye\n")
                    exit.sys
                else:
                    msg = conn.recv(1024).decode()
            else:
                print("put the numbers 1 or 0\n")
        print(msg)
        if msg == "enter your name:":  # a condition for giving the player to set hiw name
            msg = input().encode()
            name = msg
            player = Player(name, 0)
            break
        # player answering
        if msg == '\nyour answer:' or msg == '\nyour new answer:' or msg == '\nyour choice:' or msg == '\nYour new choice:' :
            msg = input().encode()
            name = msg
            player = Player(name, 0)
            conn.send(msg)

        i += 1
        if (conn.recv(1024).decode() == "your answer was..."):
            i = -1
        msg = conn.recv(1024).decode  # saving situation
        if msg == "-----------SAVE WHEEL-----------\n":
            while True:
                # getting the questions from the server
                msg = conn.recv(1024).decode()
                print(msg)
            if msg == '\nyour answer:' or msg == '\nyour new answer:' :
                # player answering
                msg = input().encode()
                conn.send(msg)

                if msg == "Correct!" or msg == "wrong...\nThe correct answer was: " + question.Correct_Answer:
                    break



            # main part
        if msg == "-----------MAIN GAME!-----------\n":
            j = 1
            while j > 0:
                msg = conn.recv(1024).decode()
                print(msg)

            # player answering
            msg = input().encode()
            conn.send(msg)
            j += 1
            if conn.recv(1024).decode() == ['\nThe Winner is ' + player.Name + '!\n' + 'You win : ' + player.Money_sum + '! Congratulations!','\nThe Winner is The Chaser!\nBetter luck next time!']:
                j=(-1)



while True:
    # receive the hello message
    msg = conn.recv(1024).decode()
    print(msg)
    if msg == "The server is full!!":
        msg = "ok.."
        break

    PlayGame(conn)


conn.send(msg.encode())
print("disconnecting from server")
conn.close()
