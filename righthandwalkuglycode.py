



#SETUP
###################################################################
import sys
import random
import math
from graphics import *


def printmap():
	for y in range(mapsize):
		for x in range(mapsize):
			print map [x][y],
			#print " "
		print "\n"


def prettyprintmap():
	win = GraphWin("Right Hand Walk", mapsize*20,mapsize*20)
	for y in range(mapsize):
		for x in range(mapsize):
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))
			if map[x][y] == ".":
				r.setFill("black")
			if map[x][y] == "x" and (x==0 or x==mapsize-1 or y==0 or y==mapsize-1):
				r.setFill("grey90")
			#elif map[x][y] == "x" and (x==1 or x==mapsize-2 or y==1 or y==mapsize-2):
			#	r.setFill("gray60")
			elif map[x][y] == "x":
				r.setFill("grey40")
			if map[x][y] == "0":
				r.setFill("red")
			r.draw(win)
	click=win.getMouse()

def prettyprintwalk():
	#prettyprintmap code
	######################
	win = GraphWin("Right Hand Walking", mapsize*20,mapsize*20)
	for y in range(mapsize):
		for x in range(mapsize):
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))
			if map[x][y] == ".":
				r.setFill("black")
			if map[x][y] == "x" and (x==0 or x==mapsize-1 or y==0 or y==mapsize-1):
				r.setFill("grey90")
			#elif map[x][y] == "x" and (x==1 or x==mapsize-2 or y==1 or y==mapsize-2):
			#	r.setFill("gray60")
			elif map[x][y] == "x":
				r.setFill("grey40")
			if map[x][y] == "0":
				r.setFill("red")
			r.draw(win)
	click=win.getMouse()
	
	
	#back at the center, looking left
	######################
	x, y, direction = halfway,halfway, 4
	
	#goes up until he hits a wall...
	######################
	try:
		while map[x][y-1] != ".":
			y=y-1;
			map[x][y] = "0"
	except:
		print "Can't go up"
		

	
	#right hand walk code, with additional color added.
	######################
	while (x!=0 and x!=(mapsize-1) and y!=0 and y!=(mapsize-1)):
		
		#if theres something to his right, and nothing in front,go forward
		if map[x + xArray[direction +1]][y + yArray[direction +1]] == "." and map[x+xArray[direction]][y+yArray[direction]]!=".":
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))
			r.setFill("grey90")
			r.draw(win)
			y=y+yArray[direction]
			x=x+xArray[direction]
			map[x][y]="0"
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))
			r.setFill("red")
			r.draw(win)
		#if theres something to his right, and something in front,turn left
		elif map[x + xArray[direction +1]][y + yArray[direction +1]] == "." and map[x+xArray[direction]][y+yArray[direction]]==".":
			direction=direction-1
		#if theres nothing to his right, turn right and go forward
		elif map[x + xArray[direction +1]][y + yArray[direction +1]] != ".":
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))
			r.setFill("grey90")
			r.draw(win)
			direction=direction+1
			y=y+yArray[direction]
			x=x+xArray[direction]
			r=Rectangle(Point(x*20,y*20),Point(x*20+20,y*20+20))
			r.setFill("red")
			r.draw(win)
			map[x][y]="0"
		if direction ==5:
			direction=1
		if direction ==0:
			direction=4	
		time.sleep(0.01)
			
#Gets user input for the map size, defaults to 5			
try:
	mapsize = int(sys.argv[1])
except:
	mapsize = 5
halfway = mapsize/2

#Get user input for the seed, default to random.
try:
	seed = int(sys.argv[2])
except:
	seed = random.randrange(sys.maxsize)
random.seed(seed)
print "Seed was:", seed


#CREATING THE MAP
###################################################################
#Creates the map, and sets all values to 0. for loop in for loop.
map=[["." for j in range(mapsize)] for i in range(mapsize)]


#Starts the random walk at the beginning of the map, and the direction to nothing just to declare it

x, y, = halfway,halfway 

#Fills out the map. As long as the current location is not a border, it walks.
while (x!=0 and x!=(mapsize-1) and y!=0 and y!=(mapsize-1)):
	map [x][y]="x"
	creationdirection=random.randint(1,4)
	if (creationdirection==1):			#up
		y=y+1
	elif (creationdirection==2):			#down
		y=y-1
	elif (creationdirection==3):			#right
		x=x+1
	elif (creationdirection==4):			#left
		x=x-1
	map [x][y]="x"	

#Prints the map.
printmap()
#prettyprintmap()

#RIGHT HAND WALK
###################################################################
#Prints a divider

for i in range(mapsize):
	print "=",
print "\nRight Hand Walk\n"

#Sets the "walker" back at the center, facing left. 
x, y, direction = halfway, halfway, 4
#Create arrays for directional interface; 0,1,2,3,4,5 = W, N, E, S, W, N
#There is overlap so that adding or subtracting values doesn't go out of range. 

xArray=[-1,0,1,0,-1,0]
yArray=[0,-1,0,1,0,-1]

#First, Go up until you hit a wall. Since he may start in the center, he needs a wall for the right hand walk to work.
#Otherwise he will spin in circles. As soon as he hits a wall, he should have a wall to his right.
try:
	while map[x][y-1] != ".":
		y=y-1;
		map[x][y] = "0"
except:
	print "Can't go up"


prettyprintwalk()

while (x!=0 and x!=(mapsize-1) and y!=0 and y!=(mapsize-1)):
	
	#if theres something to his right, and nothing in front,go forward
	if map[x + xArray[direction +1]][y + yArray[direction +1]] == "." and map[x+xArray[direction]][y+yArray[direction]]!=".":
		y=y+yArray[direction]
		x=x+xArray[direction]
		map[x][y]="0"
	#if theres something to his right, and something in front,turn left
	elif map[x + xArray[direction +1]][y + yArray[direction +1]] == "." and map[x+xArray[direction]][y+yArray[direction]]==".":
		direction=direction-1
	#if theres nothing to his right, turn right and go forward
	elif map[x + xArray[direction +1]][y + yArray[direction +1]] != ".":
		direction=direction+1
		y=y+yArray[direction]
		x=x+xArray[direction]
		map[x][y]="0"
	if direction ==5:
		direction=1
	if direction ==0:
		direction=4	
#printmap()
prettyprintmap()

