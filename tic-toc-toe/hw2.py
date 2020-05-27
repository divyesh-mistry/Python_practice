# make tic-toc-toe

# this is game now and lets try to understand git

#Tic-tac-toe (or noughts and crosses) is a simple strategy game in which two players take turns placing a mark on a 3x3 board, attempting to make a row, column, or diagonal of three with their mark. In this homework, we will use the tools we've covered in the past two weeks to create a tic-tac-toe simulator and evaluate basic winning strategies.
import numpy as np
import random
from matplotlib import pyplot as plt
# Exercise 1
#For our tic-tac-toe board, we will use a numpy array with dimension 3 by 3.
#Write a function create_board() that creates such a board with the value of each cell set to the integer 0. Call create_board() and store it.

def create_board():
	return (np.zeros((3,3),dtype=int))

# Exercise 2
#Players 1 and 2 will take turns changing values of this array from a 0 to a 1 or 2, indicating the number of the player who places a marker there.
# Create a function place(board, player, position), where: - player is the current player (an integer 1 or 2).
#position is a tuple of length 2 specifying a desired location to place their marker.
#Function should only allow the current player to place a marker on the board (change the board position to their number) if that position is empty (zero).
# Use create_board() to store a board as board, and use place to have Player 1 place a marker on location (0, 0).

def place(board,player,position):
	if board[position] == 0:
		board[position] = player
	return board
#print(place(board,1,(0,0)))
#divyesh learning

#Exercise3
#In this exercise, we will determine which positions are available to either player for placing their marker.
# Create a function possibilities(board) that returns a list of all positions (tuples) on the board that are not occupied (0).
# (Hint: numpy.where is a handy function that returns a list of indices that meet a condition.)
# Note that board is defined as at the end of Exercise 2. Call possibilities(board) to see what it returns!
#What does possibilities(board) return?
											#def possibilities(board):
											#	not_occupied=[]
											#	for i in range(3):
											#		for j in range(3):
											#			np.where(board==0)
											#			not_occupied.append((i,j))
											#	return not_occupied
											#print(possibilities(board))

# # NOTE: A= np.array([[1,2],[2,4]])
#         zip(A)
#         list(zip(*np.where(A == 2))) # this gives us array position for desired value
#output: [(0, 1), (1, 0)]

def possiblities(board):
	return list(zip(*np.where (board == 0)))# ''*'' is very important to get output as tupple of current positions
											# aLSO LIST is important to see result of zip(*) is unzip each array position where our condition match
#zip wants a bunch of arguments to zip together, but what you have is a single argument (a list, whose elements are also lists).
#The * in a function call "unpacks" a list (or other iterable), making each of its elements a separate argument.
#print(possiblities(board))

#Exercise 4
#The next step is for the current player to place a marker among the available positions.
#In this exercise, we will select an available board position at random and place a marker there.
#Write a function random_place(board, player) that places a marker for the current player at random among
#all the available positions (those currently set to 0).
#Find possible placements with possibilities(board).
#Select one possible placement at random using random.choice(selection).
#Note that board is already defined as at the end of Exercise 2.
#Call random_place(board, player) to place a random marker for Player 2, and store this as board to update its value.
def random_place(board,player):
	possible_choice=possiblities(board)
	if len(possible_choice) > 0:
		position=random.choice(possible_choice)
		place(board,player,position)
	return board
#random.seed(1)
#print(random_place(board,1))

#Exercise 5
#We will now have both players place three markers each. A new board is given by the sample code.
#Call random_place(board, player) to place three pieces each on board for players 1 and 2. Print board to see your result.
#random.seed(1)
board = create_board()
for i in range(3):
	for player in [1,2]:
		random_place(board,player)
#print(board)
#print(list(zip(*np.where(board==1))))

#In exercises 6 through 9, we will make functions that check whether either player has won the game.
#Make a function row_win(board, player) that takes the player (integer) and determines if any row consists of only their marker.
#Have it return True if this condition is met and False otherwise.
#Note that board is already defined as in Exercise 5. Call row_win to check if Player 1 has a complete row.
def row_win(board,player):
	if np.any(np.all(board==player,axis=1)):#np.any() will Test whether any array element along a given axis evaluates to True.
		return True
	else:
		return False
#print(row_win(board,1))

# Exercise 7
#check column
#In exercises 6 through 9, we will make functions that check whether either player has won the game.
#Make a function col_win(board, player) that takes the player (integer) and determines if any column consists of only their marker.
#Have it return True if this condition is met and False otherwise.

def col_win(board,player):
	if np.any(np.all(board==player,axis=0)):
		return True
	else:
		return False

#print(col_win(board,1))
#Exercise 8
#In exercises 6 through 9, we will make functions that check whether either player has won the game.
#Finally, create a function diag_win(board, player) that takes the player (integer) and determines if any diagonal consists of only their marker.
#Have it return True if this condition is met and False otherwise.

# check diagonal
def diag_win(board,player):
	if np.all(np.diag(board)==player) or np.all(np.diag(np.fliplr(board))==player):# here np.fliplr for other diagonal
		# np.diag returns the diagonal of the array
        # np.fliplr rearranges columns in reverse order
		return True
	else:
		return False

#print(diag_win(board,1))
# In exercises 6 through 9, we will make functions that check whether either player has won the game.
# Create a function evaluate(board) that uses row_win, col_win, and diag_win functions for both players.
# If one of them has won, return that player's number. If the board is full but no one has won, return -1. Otherwise, return 0.
# Note that board is defined as in Exercise 8. Call evaluate to see if either player has won the game yet.
def evaluate(board):
	winner=0
	for player in [1,2]:
		if row_win(board,player) or col_win(board,player) or diag_win(board,player):
			return player
	if np.all(board!=0):# to ensure all player played all boxes
			winner=-1
	return winner
#board[(1,1)]=2
#print(board)
#print(evaluate(board))

#Exercise10
#In this exercise, we will use all the functions we have written to simulate an entire game.
# The functions create_board(), random_place(board, player), and evaluate(board) are all defined as in previous exercises.
# Create a function play_game() that:- Creates a board.
#Alternates taking turns between two players (beginning with Player 1), placing a marker during each turn.
#Evaluates the board for a winner after each placement.
#Continues the game until one player wins (returning 1 or 2 to reflect the winning player), or the game is a draw (returning -1).
#call play_game 1000 times, and store the results of the game in a list called results. Use random.seed(1) so we can check your answer!
#How many times does Player 1 win out of 1000 games?
def play_game():
	board=create_board()
	while True:
		for player in [1,2]:
			random_place(board,player)
			result = evaluate(board)
			if result!=0:
				#print(result)
				return result
result=[]
iteration=1000
random.seed(1)
for i in range(iteration):
	result.append(play_game())
print(result.count(1),"-without strategy")

#Exercise 11
#In the previous exercise, we saw that when guessing at random, it's better to go first, as one would expect. Let's see if Player 1 can improve their strategy.
#Create a function play_strategic_game(), where Player 1 always starts with the middle square, and otherwise both players place their markers randomly.
# Call play_strategic_game 1000 times. Set the seed to 1 using random.seed(1) again.
#How many times does Player 1 win out of 1000 games with this new strategy?
def play_strategic_game():
	winner=0
	board=create_board()
	board[(1,1)]=1 # always player 1 has first try and set it at centre of board
	while winner==0:
		for player in [2,1]:#player 1 already marked his position at first so now player 2 will start the loop
			random_place(board,player)
			winner= evaluate(board)
			if winner!=0:
				break
				#print(result)
	return winner
result2=[]
random.seed(1)
#This result is expected --- when guessing at random, it's better to go first.
#Let's see if Player 1 can improve their strategy. create_board(), random_place(board, player),
#and evaluate(board) have been created from previous exercises. Create a function play_strategic_game(),
#where Player 1 always starts with the middle square, and otherwise both players place their markers randomly.

for i in range(iteration):
	result2.append(play_strategic_game())
print(result2.count(1),"-with strategy")

#Exercise 13
#-----------

#The results from Exercise 12 have been stored. Use the play_strategic_game() function to play 1,000 random games.
#Use the time libary to evaluate how long all these games takes.
plt.hist(result)
plt.hist(result2)
plt.savefig("tic_tac_toe_Hist_2.pdf")
plt.show()
