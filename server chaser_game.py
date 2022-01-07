import socket
import sys
import random
from _thread import *

from Main_game_functions import *

#classes and functions of questions
class Player:
    def __init__(self, Name, Money_sum):
        self.Name = Name
        self.Money_sum = Money_sum

class Questions:
    def __init__(self, Question, Answer1, Answer2, Answer3, Answer4, Correct_Answer, Use):
        self.Question = Question
        self.Answer1 = Answer1
        self.Answer2 = Answer2
        self.Answer3 = Answer3
        self.Answer4 = Answer4
        self.Correct_Answer = Correct_Answer
        self.Use = Use
        Use = 0

    def Random_Order(self):
        Answers_Arr = [self.Answer1, self.Answer2, self.Answer3, self.Answer4]
        option1 = random.choice(Answers_Arr)
        option2 = random.choice(Answers_Arr)
        while option2 == option1:
            option2 = random.choice(Answers_Arr)
        option3 = random.choice(Answers_Arr)
        while option3 == option1 or option3 == option2:
            option3 = random.choice(Answers_Arr)
        option4 = random.choice(Answers_Arr)
        while option4 == option1 or option4 == option2 or option4 == option3:
            option4 = random.choice(Answers_Arr)
        Option_Arr = [option1, option2, option3, option4]
        return Option_Arr



def question_arrey():
    question_1 = Questions('How many Star Wars movies are there?', "18", "9", "11", "12", '12', 0)
    question_2 = Questions('Whats the name of the USA president?', "Barack Obama", "Bill Clinton", "Donald Trump",
                           "Joe Biden", "Joe Biden",  0)
    question_3 = Questions('Who is the author behind the Harry Potter books?', 'J.K. Rowling', 'Brandon Senderson',
                           'Stephenie Meyer', 'Jules Verne', 'J.K. Rowling', 0)
    question_4 = Questions('Which of Shakespeare’s plays is the longest?', 'Romeo and Juliet', 'Hamlet', 'King Lear',
                           'The Taming of the Shrew', 'Hamlet', 0)
    question_arr = [question_1, question_2, question_3, question_4]
    return question_arr

def Question_Pick(Question_Arr):
    Question = random.choice(Question_Arr)
    while Question.Use == 1:
        Question = random.choice(Question_Arr)
    Question.Use = 1
    return Question

def part_one(player, question_arr):
    question_left = 3  # counter for number of questions left
    while question_left > 0:
        question = Question_Pick(question_arr)  # pick a random question from all the questions
        answers_arr = Questions.Random_Order(question)  # randomize the order of the answers
        question_send=question+'\n1.'+answers_arr[0]+'\n2.'+answers_arr[1]+'\n3.'+answers_arr[2]+'\n4.'+answers_arr[3]
        conn.send(question_send.encode())#sending the string of question send to the client

        conn.send("Your Answer :".encode())
        answer = conn.recv(1024)
        int_answer = int(answer)  # get the answer and change it from string to int
        while 1 > int_answer or int_answer > 4:  # checking its a valid answer
            conn.send("Your new Answer :".encode())
            answer = conn.recv(1024)
            int_answer = int(answer)
        if answers_arr[int_answer - 1] == question.Correct_Answer:  # if he right and if he wrong
            conn.send('Correct!'.encode())
            player.Money_sum += 5000  # he get money for the right answer
        else:
            conn.send('Wrong...'.encode())
            conn.send('The correct answer is ' + question.Correct_Answer.encode())
        question_left = question_left - 1  # the question counter goes down by one


def threadFunc(conn , addr):#function that send message to the player and then receives
    question_arr = question_arrey()
    conn.send("welcome to the chaser game\n".encode())#sending to the player the message of starting to play
    msg = conn.recv(1024).decode()

    #part 1


       a = part_one(player, question_arr)


#part2
conn.send("where do you want to start?\n you have three options\n 1.start at line 3 with our normal sum\n 2.start closer to the chaser in line 2 for double yours amount\n 3.start further from the chaser in line 4 for half of yours amount".encode())

conn.send('\n|------|-------------------|\n|   0  |      Chaser       |\n|------|-------------------|\n|   1  |                   |\n|------|-------------------|\n|   2  |     ' + player.Money_sum * 2 + '     |\n|------|------------------|\n|   3  |       ' + player.Money_sum + '       |\n|------|-------------------|\n|   4  |       ' + player.Money_sum * 0.5 + '       |\n|------|-------------------|\n|   5  |                   |\n|------|-------------------|\n|   6  |                   |\n|------|-------------------|\n|   7  |    ***BANK***     |\n|______|___________________|\n'.encode())

 choice = input('your choice:')  # where he chose to start
 choice_int = int(choice)
    while choice_int < 2 or choice_int > 4:  # checking it is a correct one
        choice = input('your new choice:')
        choice_int = int(choice)
    if choice_int == 2:  # we change the amount base on his decision
        player.Money_sum = player.Money_sum * 2  # if he start closer to the chaser
    elif choice_int == 4:
        player.Money_sum = player.Money_sum * 0.5  # if he start further from the chaser
        player.Money_sum = int(player.Money_sum)
    board[choice_int - 1] = 'player'  # placing him in his location



HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#opening socket between the chaser and the player
s.bind((HOST, PORT))
s.listen()#the chaser listens to 3 players



while True:
    conn, addr = s.accept()  # the actual connection between the the player and the chaser
    start_new_thread(threadFunc, (conn, addr))


s.close()#