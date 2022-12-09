#!/usr/bin/env python
# coding: utf-8
#author: Basha Syed


from IPython.display import clear_output


def display_board(board):
    clear_output()
    print(board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('----------')
    print(board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('----------')
    print(board[7] + ' | ' + board[8] + ' | ' + board[9])
    print()



import random

def choose_first():
    frst=random.randint(1,2)
    return frst



def player_input():
    mark = ''
    while mark.upper() != 'X' and mark.upper() != 'O':
        mark = input('Player , choose X or O: ')

    p1 = mark.upper()
    if p1 == 'X':
        bot = 'O'
    else:
        bot= 'X'

    print(f'Player: {p1}')
    print(f'Bot: {bot}')
    return mark.upper()


def place_marker(board, mark, position):
    board[position] = mark


def win_check(board, mark):
    if board[1]==mark and board[2]==mark and board[3]==mark:
        return True
    elif board[4]==mark and board[5]==mark and board[6]==mark:
        return True
    elif board[7]==mark and board[8]==mark and board[9]==mark:
        return True
    elif board[1]==mark and board[4]==mark and board[7]==mark:
        return True
    elif board[2]==mark and board[5]==mark and board[8]==mark:
        return True
    elif board[3]==mark and board[6]==mark and board[9]==mark:
        return True
    elif board[1]==mark and board[5]==mark and board[9]==mark:
        return True
    elif board[3]==mark and board[5]==mark and board[7]==mark:
        return True
    else:
        return False


def space_check(board, position):
    if board[position] != 'X' and board[position] != 'O':
        return True
    else:
        return False


def full_board_check(board):
    for po in board[1:]:

        if po != 'X' and po != 'O':
            return False
    return True



def player_choice(board,mark):
    valid = True

    while valid:
        if not full_board_check(board):
            try:
                
                position = int(input('Next position (as a number 1-9): '))
                if position <=9 and position >=1:
                    pass
                else:
                    print('Please enter a valid integer between 1-9 ')
                    continue
            except:
                print('Please enter a valid integer between 1-9 ')
                continue
            if space_check(board, position):
                return place_marker(board, mark, position)
            else:
                print('Position already occupied please enter again..')



def bot_choice(board,bc,pc):
    board_copy=board[:]
    possible_positions=[i for i,x in enumerate(board) if x==' ']
    # check winning chance
    for chance in possible_positions:
        for mark in [bc,pc]:
            place_marker(board_copy, mark, chance)
            if win_check(board_copy,mark):
                return place_marker(board, bc, chance)
            place_marker(board_copy, ' ', chance)
    #check if middle pos is empty
    if 5 in possible_positions:
        return place_marker(board, bc, 5)
    
    #take corners if empty
    for corner in [1,3,7,9]:
        if corner in possible_positions:
            return place_marker(board, bc, corner)
        
    #take edges if empty
    for edge in [2,4,6,8]:
        if edge in possible_positions:
            return place_marker(board, bc, edge)
    
    
    

print('Welcome to Tic Tac Toe!')
ready = input('Are you ready to play?(Y/N)')
print(ready)
player_turn=True
while ready.lower() == 'y':

    board = ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    #board = ['#', 'X', 'O', 'O', 'O', 'X', 'X', 'X', 'O', 'O']
    display_board(board)
    mark = player_input()
    if mark == 'X':
        pc,bc = 'X','O'
    else:
        pc,bc = 'O','X'
    if choose_first()==1:
        print('Player will go first ')
    else:
        print('Bot will go first')
        player_turn=False
    while True:
        #Player's turn
        if player_turn:
            player_choice(board,pc)
            display_board(board)
            if win_check(board, pc):
                print('Congrats, You won the game!!!')
                break
            elif full_board_check(board):
                print("It's a TIE")
            player_turn=False
        #Bot's turn
        else:
            bot_choice(board,bc,pc)
            display_board(board)
            if win_check(board,bc):
                print('You lost,Better luck next time!')
                break
            elif full_board_check(board):
                print("It's a TIE")
                break
            player_turn=True
   

    if not input('Do you want to play again?(Y/N) ').lower()=='y':
        break

print('Thanks for playing...\n Exit Successfully')





