#Implementation of Two Player Tic-Tac-Toe game in Python on Raspberry PI.
# for using a membrane keypad with the Raspberry Pi to play Tic-Tac-Toe

# A module to control Raspberry Pi GPIO channels
# use the following command: sudo pip install RPi.GPIO

''' We will make the board using dictionary 
    in which keys will be the location(i.e : top-left,mid-right,etc.)
    and initialliy it's values will be empty space and then after every move 
    we will change the value according to player's choice of move.
'''

from itertools import count
from shutil import move
from tkinter import Y
import RPi.GPIO as GPIO
import time

# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

KEYPAD = [["1","2","3"," "],
          ["4","5","6"," "],
          ["7","8","9"," "],
          ["n"," ","y"," "]]
ROW_LINES = [L1, L2, L3, L4]
COLUMN_LINES = [C1, C2, C3, C4] 

theBoard = {'1': ' ' , '2': ' ' , '3': ' ' ,
            '4': ' ' , '5': ' ' , '6': ' ' ,
            '7': ' ' , '8': ' ' , '9': ' ' ,
            'n': ' ' , ' ': ' ' , 'y': ' '}

board_keys = []

for key in theBoard:
    board_keys.append(key)

def readKey(key):
    for i, rowLine in enumerate(ROW_LINES):
        GPIO.output(rowLine, GPIO.HIGH)
        for j, columnLine in enumerate(COLUMN_LINES):
            if(GPIO.input(columnLine)):
                key = KEYPAD[i][j]
        GPIO.output(rowLine, GPIO.LOW) 
        time.sleep(0.05)   
    return key

global board
    
def printBoard(board):
    print(board['1'] + '|' + board['2'] + '|' + board['3'])
    print('-+-+-')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+-')
    print(board['7'] + '|' + board['8'] + '|' + board['9'])

# Now we'll write the main function which has all the gameplay functionality.
try:
    def game():

        global turn
        global count
        global theBoard
        global pressedKey
        global move
        
        turn = 'X'
        count = 0

        for i in range(10):
            printBoard(theBoard)
            print("It's your turn," + turn + ".Move to which place ?")    
        
            pressedKey = move
            while(pressedKey == move):
                move = readKey(pressedKey)
    
                if move == "n" or move == "y":
                    move = pressedKey
                    
            if theBoard[move] == ' ': 
                theBoard[move] = turn 
                count += 1

            else:
                print("That place is already filled.\nMove to which place ?")
                continue

            # Now we will check if player X or O has won,for every move after 5 moves. 
            if count >= 5:
                if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ': # across the top
                    printBoard(theBoard)
                    print("\nGame Over.\n")                
                    print(" **** " +turn + " won. ****")                
                    break
                elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ': # across the middle
                    printBoard(theBoard)
                    print("\nGame Over.\n")                
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ': # across the bottom
                    printBoard(theBoard)
                    print("\nGame Over.\n")                
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ': # down the left side
                    printBoard(theBoard)
                    print("\nGame Over.\n")                
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ': # down the middle
                    printBoard(theBoard)
                    print("\nGame Over.\n")                
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ': # down the right side
                    printBoard(theBoard)
                    print("\nGame Over.\n")                
                    print(" **** " +turn + " won. ****")
                    break 
                elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ': # diagonal
                    printBoard(theBoard)
                    print("\nGame Over.\n")                
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ': # diagonal
                    printBoard(theBoard)
                    print("\nGame Over.\n")                
                    print(" **** " +turn + " won. ****")
                    break 

            # If neither X nor O wins and the board is full, we'll declare the result as 'Tie'.
            if count == 9:
                print("\nGame Over.\n")                
                print("It's a Tie!!")

            # Now we have to change the player after every move.
            if turn =='X':
                turn = 'O'
            else:
                turn = 'X'        

        # Now we will ask if player wants to restart the game or not.
        restart = readKey("")
        print("\nDo want to play Again?(y/n)")
        while restart == "":
            restart = readKey("")
        if restart == "y":             
            for key in board_keys:
                theBoard[key] = " "    
        
            game()

    if __name__ == "__main__":
        game()

except KeyboardInterrupt:
    print("\nGame Stopped !!")
    GPIO.cleanup()
