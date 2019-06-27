#David Rhett
#Python 1
#Escape the Cave
#This program creates a cave using a random walk function, and then tests two different methods of trying to escape.
#The first method is the right hand walk. Essentially, always keep the wall on the right.
#The other method is the right hand run. It keeps going forward 'till it hits something, then turns right.
#The right hand walk is the most efficient method by far, but the right hand run sometimes beats it in number of steps (when it successfully runs)
#The right hand run has a tendency to hit loops, more times than not. This is because it never turns left. If there is a left turn on the way to the exit, it will turn around and loop.
#The right hand walk is not without errors either. The method requires a wall to the right, but it starts in the middle. Therefore, he needs to run up until he hits a wall, then the actual walk starts.
#However, there is the rare chance that he may run into an island before hitting the actual cave of the wall. Always keeping this on the right, he will run in circles and loop. (mapsize 30, seed 2)
#I guarded against endless loops by stopping the while loop after the runner has gone the 10x the length of the map. This is more reliable than a set number, like 100, in case a person tries a large map size
#I could have even chosen a smaller number (3x the length of the map would suffice) but I like watching the guy run around.


#The program uses two direction arrays to allow the walker/runner to escape without requiring "if facing north, if facing east, if facing.." 
#The two arrays, xArray and yArray,  are corresponding to the x and y directions. They contain the values for movement North, East, South, and West.
#That is, the value in the xArray for East is 1, while in the y array, it is 0. 
#To go forward, in any direction, the xArray is added to the x value,and the yArray is added to the y value. However, one of those arrays will have a value of 0.
#Because the program is constantly moving up and down in those arrays as the walker turns left and right, I added some overlap so that he would never go over the list area.
#The arrays actually correspond to W, N, E, S, W, N. At the end of the loop, if the direction is at the 0 position (w), it jumps to 4 (w). This way, the runner can turn right without worrying about going outside the array.

#After writing the program with ugly ascii pictures (which used X's and .'s instead of 0's and 1's, because those are ugly), I rewrote it using graphics.
#First I rewrote it to show the path after the run, then I rewrote it again to make it an active path by updating it after every iteration of the loop. 
#The ugly ascii pictures still exist in the printmap() function, after running the dowalk() or dorun() functions.

#A lot of this code is repetitive. I probably could have made the code more efficient by passing variables into the modules, but this was easier.

#Final Regex code imported from https://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python

#DEFINING FUNCTIONS
###################################################################

def printmap():
	#for every member in the array, print it's value. At the end of a row, print a newline.
	for y in range(mapsize):
		for x in range(mapsize):
			print map [x][y],
		print "\n"


def prettyprintmap():
	#Creates a Window of the size mapsize times 20 by mapsize times 20. This is because the printed boxes are 20x20. 
	win = GraphWin("The Map", mapsize*20,mapsize*20)	
	#For the every value in the array (y by x)...
	for y in range(mapsize):
		for x in range(mapsize):
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))	#create a rectangle of size 20x20. 
			if map[x][y] == ".":									#if it's a wall,
				r.setFill("black")									#print in black.
			elif map[x][y] == "x" and (x==0 or x==mapsize-1 or y==0 or y==mapsize-1):	
				r.setFill("grey90")									#if this box is actually the cave exit, print in white
			#I wanted the exit white, with boxes near the exit a lighter grey. However, there was no way to differentiate boxes near the exit and those just on the edge, so it didn't look right sometimes.
			#elif map[x][y] == "x" and (x==1 or x==mapsize-2 or y==1 or y==mapsize-2):
			elif map[x][y] == "0":
				r.setFill("yellow")	
			else:													#if it is an open area,
				r.setFill("grey40")									#print in grey
			r.draw(win)												#This actually draws the box that we just colored for. 
	click=win.getMouse()											#and it waits for a click before closing.

def dowalk():
	#PRINTS A DIVIDER
	######################
	for i in range(mapsize):
		print "=",
	print "\nRight Hand Walk\n"
	
	#DECLARING VARIABLES
	######################
	#Sets the "walker" back at the center, facing left. Also declares steps, which counts steps.
	x, y, direction, steps = halfway, halfway, 4, 0
	#Create arrays for directional interface; 0,1,2,3,4,5 = W, N, E, S, W, N. Note that north is actually (0,-1) because the array runs from top down, with 0 at the top.
	#There is overlap so that adding or subtracting values doesn't go out of range. 
	xArray=[-1,0,1,0,-1,0]
	yArray=[0,-1,0,1,0,-1]

	#SETTING UP AGAINST WALL
	#First, Go up until you hit a wall. Since he may start in the center, he needs a wall for the right hand walk to work.
	#Otherwise he will spin in circles. As soon as he hits a wall, he should be facing left, so he can begin the right hand walk.
	try:
		while map[x][y-1] != ".":
			y=y-1;
			map[x][y] = "0"
			steps+=1
	except:
		print "Can't go up"

	#WALKING
	######################
	while (x!=0 and x!=(mapsize-1) and y!=0 and y!=(mapsize-1) and steps<(mapsize*20)):  #While not on the edge, and steps is less than maplength*4 (to prevent endless looping)
		
		#if theres something to his right, and nothing in front,go forward
		if map[x + xArray[direction +1]][y + yArray[direction +1]] == "." and map[x+xArray[direction]][y+yArray[direction]]!=".":
			y=y+yArray[direction]			#This moves forward, if he is facing up or down
			x=x+xArray[direction]			#This moves forward, if he is facing left or right
			steps+=1						#increments the step counter
			map[x][y]="0"					#This marks his location in the array. It doesn't print to the screen until the printmap() function is called, though				
		#if theres something to his right, and something in front,turn left
		elif map[x + xArray[direction +1]][y + yArray[direction +1]] == "." and map[x+xArray[direction]][y+yArray[direction]]==".":
			direction=direction-1			#This sets his direction left (or counter clockwise)	
		#if theres nothing to his right, turn right and go forward
		elif map[x + xArray[direction +1]][y + yArray[direction +1]] != ".":
			direction=direction+1			#This sets his direction right(or clockwise)
			y=y+yArray[direction]			#This moves forward, if he is facing up or down
			x=x+xArray[direction]			#This moves forward, if he is left or right
			steps+=1						#increments the step counter
			map[x][y]="0"					#This marks his location in the array. It doesn't print to the screen until the printmap() function is called, though
		
		#Because the direction variable is constantly being added to and subtracted from, it mustn't go out of range. If it gets to the edge, it loops around.
		if direction ==5:					
			direction=1
		if direction ==0:
			direction=4	
	print "\nThe number of steps for the Right Hand Walk code is :", steps

def prettyprintwalk():
	#PRETTYPRINTMAP() CODE, simply copied over. I could not simply run the prettyprintmap() module because the 'win' window variable doesn't carry over.
	######################
	win = GraphWin("Right Hand Walking", mapsize*20,mapsize*20)
	for y in range(mapsize):
		for x in range(mapsize):
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))
			if map[x][y] == ".":
				r.setFill("black")
			elif map[x][y] == "x" and (x==0 or x==mapsize-1 or y==0 or y==mapsize-1):
				r.setFill("grey90")
			else:
				r.setFill("grey40")
			r.draw(win)
	click=win.getMouse()
	
	
	#SET BACK AT CENTER, LOOKING LEFT
	######################
	x, y, direction, steps = halfway,halfway, 4, 0
	
	#DECLARING DIRECTION ARRAYS
	######################
	#Create arrays for directional interface; 0,1,2,3,4,5 = W, N, E, S, W, N
	#There is overlap so that adding or subtracting values doesn't go out of range.
	xArray=[-1,0,1,0,-1,0]
	yArray=[0,-1,0,1,0,-1]
	
	#GO UP UNTIL UP AGAINST A WALL
	######################
	try:
		while map[x][y-1] != ".":
			y=y-1;
			map[x][y] = "0"
			steps+=1						#increments the step counter
	except:
		map[x][y] = "0"
	
	#DO RIGHT HAND WALK (SAME CODE AS BEFORE, WITH ADDITIONAL GRAPHICS ADDED (MARKED WITH COMMENTS)
	######################
	while (x!=0 and x!=(mapsize-1) and y!=0 and y!=(mapsize-1) and steps<(mapsize*20)):
		#if theres something to his right, and nothing in front,go forward
		if map[x + xArray[direction +1]][y + yArray[direction +1]] == "." and map[x+xArray[direction]][y+yArray[direction]]!=".":
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))	#First, create rectangle at old location
			r.setFill("grey90")										#Set that rectangle to grey
			r.draw(win)												#And draw it on the screen
			y=y+yArray[direction]
			x=x+xArray[direction]
			steps+=1												#increments the step counter
			map[x][y]="0"
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))	#Create a rectangle at the new location	
			r.setFill("red")										#Set that rectangle to red
			r.draw(win)												#And draw it on the screen
		#if theres something to his right, and something in front,turn left
		elif map[x + xArray[direction +1]][y + yArray[direction +1]] == "." and map[x+xArray[direction]][y+yArray[direction]]==".":
			direction=direction-1
		#if theres nothing to his right, turn right and go forward
		elif map[x + xArray[direction +1]][y + yArray[direction +1]] != ".":
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))	#First, create rectangle at old location
			r.setFill("grey90")										#Set that rectangle to grey
			r.draw(win)												#And draw it on the screen
			direction=direction+1
			y=y+yArray[direction]
			x=x+xArray[direction]
			steps+=1												#increments the step counter
			
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))	#Create a rectangle at the new location	
			r.setFill("red")										#Set that rectangle to red
			r.draw(win)												#And draw it on the screen
			map[x][y]="0"
		if direction ==5:
			direction=1
		if direction ==0:
			direction=4	
		time.sleep(0.01)
	print "\nThe number of steps for the Right Hand Walk code is :", steps
	click=win.getMouse()

def dorun():

	
	#PRINTS A DIVIDER
	######################
	for i in range(mapsize):
		print "=",
	print "\nRight Hand Run\n"
	
	#SET BACK AT CENTER, LOOKING RIGHT
	######################
	x, y, direction, steps = halfway,halfway, 2, 0
	
	#DECLARING DIRECTION ARRAYS
	######################
	#Create arrays for directional interface; 0,1,2,3,4,5 = W, N, E, S, W, N
	#There is overlap so that adding or subtracting values doesn't go out of range. 
	xArray=[-1,0,1,0,-1,0]
	yArray=[0,-1,0,1,0,-1]

	
	
	#DO RUN
	######################
	while (x!=0 and x!=(mapsize-1) and y!=0 and y!=(mapsize-1) and steps<(mapsize*20)):
		#if theres something in front, turn right
		if map[x+xArray[direction]][y+yArray[direction]]==".":
			direction = direction +1;

		#if theres nothing in front, run
		if map[x+xArray[direction]][y+yArray[direction]]!=".":
			y=y+yArray[direction]
			x=x+xArray[direction]
			steps+=1						#increments the step counter
			map[x][y]="0"
			
			#This marks his location in the array. It doesn't print to the screen until the printmap() function is called, though		
		if direction ==5:
			direction=1
		if direction ==0:
			direction=4	
	print "\nThe number of steps for the Right and Run code is :", steps
	
	
def prettyprintrun():

	#PRETTYPRINTMAP() CODE, simply copied over. I could not simply run the prettyprintmap() module because the 'win' window variable doesn't carry over.
	######################
	win = GraphWin("Right Turn Running", mapsize*20,mapsize*20)
	for y in range(mapsize):
		for x in range(mapsize):
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))
			if map[x][y] == ".":
				r.setFill("black")
			elif map[x][y] == "x" and (x==0 or x==mapsize-1 or y==0 or y==mapsize-1):
				r.setFill("grey90")
			else:
				r.setFill("grey40")
			r.draw(win)
	click=win.getMouse()
	

	#SET BACK AT CENTER, LOOKING RIGHT
	######################
	x, y, direction, steps = halfway,halfway, 2, 0
	
	#DECLARING DIRECTION ARRAYS
	######################
	#Create arrays for directional interface; 0,1,2,3,4,5 = W, N, E, S, W, N
	#There is overlap so that adding or subtracting values doesn't go out of range. 
	xArray=[-1,0,1,0,-1,0]
	yArray=[0,-1,0,1,0,-1]


	
	#DO RUN CODE, WITH ADDITIONAL GRAPHICS (MARKED WITH COMMENTS
	######################
	while (x!=0 and x!=(mapsize-1) and y!=0 and y!=(mapsize-1) and steps<(mapsize*20)):
		#if theres something in front, turn right
		if map[x+xArray[direction]][y+yArray[direction]]==".":
			direction = direction +1;
		#if theres nothing in front, run
		if map[x+xArray[direction]][y+yArray[direction]]!=".":
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))	#First, create rectangle at old location
			r.setFill("grey90")										#Set that rectangle to grey
			r.draw(win)												#And draw it on the screen
			y=y+yArray[direction]
			x=x+xArray[direction]
			steps+=1												#increments the step counter
			map[x][y]="0"
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))	#Create a rectangle at the new location	
			r.setFill("blue")										#Set that rectangle to red
			r.draw(win)												#And draw it on the screen
		if direction ==5:
			direction=1
		if direction ==0:
			direction=4	
		time.sleep(0.01)
	print "\nThe number of steps for the Right and Run code is :", steps
	click=win.getMouse()
	
#SETUP
###################################################################
#importing necessary modules
import sys
import random
import math
from graphics import *
import re
		
#GETS USER INPUT AS SYSTEM ARGUMENT
######################		
#Gets user input for mapsize, defaults to 20. Uses regex to filter out the numbers.
#originally, the program took the system argument as an integer, with int(sys.argv[1]). For the new project,
#I needed the form 'seed = #', so I had to add Regex. I played around with re.findall and re.split, but was 
#unable to find a way to convert a list to anything else. I believe group() does that though. Reference site
#posted at the top of the program, in the notes.



#Gets user input for seed, defaults to random.        
try:
	seedstring = sys.argv[1]
	seed= int(re.search(r'\d+', seedstring).group())	
except:
	seed = random.randrange(sys.maxsize)
random.seed(seed)
print "Seed was:", seed

try:														# ..And this will be part 3! Yay!
	mapsizestring = sys.argv[2] 	  							
	mapsize=int(re.search(r'\d+', mapsizestring).group())	
	
except:
	mapsize = 20
halfway = mapsize/2



#CREATING THE MAP (Random Walk)
###################################################################

#Creates the map as a double array. This line is a for loop within a for loop
map=[["." for j in range(mapsize)] for i in range(mapsize)]

#Starts the random walk at the beginning of the map, and the direction to nothing just to declare it
x, y = halfway, halfway 

#Fills out the map. As long as the current location is not a border, it walks.
while (x!=0 and x!=(mapsize-1) and y!=0 and y!=(mapsize-1)):
	map [x][y]="x"
	creationdirection=random.randint(1,4)
	if (creationdirection==1):				#down
		y=y+1
	elif (creationdirection==2):			#up
		y=y-1
	elif (creationdirection==3):			#right
		x=x+1
	elif (creationdirection==4):			#left
		x=x-1
	map [x][y]="x"	


#ESCAPING AND PRINTING FUNCTION CALLS
###################################################################
	




printmap()
#prettyprintmap()
#dorun()
dowalk()
printmap()
#prettyprintmap()
prettyprintwalk()
prettyprintrun()

