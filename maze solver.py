import turtle
import os
import copy
import time

# this program will only solve mazes where the start is the top left corner
# and the end is the bottom right corner



MAXIMUM_ALLOWED_THREADS = 50000 # number of threads to allow running simultaneously before giving up.


SHOW_SEARCH = True # if set to True, steps visited by any thread will be shown in green wile solving.
                    # this slows down the search significantly, set to False for better performance.

SUPER_FAST_MODE = True # finds solution faster and uses less RAM, but can ONLY FIND ONE solution, rather than all the same length ones


ROOT_PATH = os.path.dirname(__file__) + "/mazes/"
try:
    os.mkdir(ROOT_PATH)
except:
    pass

turtle.title("Maze Solver")
turtle.hideturtle()
turtle.speed(0)
turtle.penup()

cell_turtles = []
cell_data = []
threads = []# this array will hold all the possible paths that could be taken,
            # while the computer is solving.

solutions = []
visitedCells = []

HEIGHT = 0
WIDTH = 0


def initMaze(height, width, pixelsize, data):
    global HEIGHT
    global WIDTH
    global cell_data
    global cell_turtles
    global threads
    global solutions
    global visitedCells
    visitedCells = []
    solutions = []
    threads = [ [ [0, 0] ] ]
    HEIGHT = height
    WIDTH = width
    cell_data = copy.deepcopy(data)
    for a in range(0, height):
        rowTurtles = []
        for b in range(0, width):
            t = turtle.Turtle()
            t.penup()
            t.speed(0)
            t.shape("square")
            
            t.turtlesize(pixelsize / 20, pixelsize / 20, 1)
            t.goto((b - int(width/2) ) *(pixelsize+1), (-a + int(height/2) ) *(pixelsize+1))
            
            if a == 0 and b == 0:
                t.left(90)
                t.forward(pixelsize/2 + 10)
                t.color("red")
                t.write("Start", align="right", font=("Arial", 10, "bold"))
                t.backward(pixelsize/2 + 10)
                t.right(90)
                
            if a == height-1 and b == width-1:
                t.right(90)
                t.forward(pixelsize/2 + 15)
                t.color("red")
                t.write("End", align="left", font=("Arial", 10, "bold"))
                t.backward(pixelsize/2 + 15)
                t.left(90)
            
            if data[a][b] == True:
                t.color("black")
            else:
                t.color("light gray")
            rowTurtles.append(t)
        cell_turtles.append(rowTurtles)

def readCell(x, y): # must say that cells off the map are walls, as well as reading from the data
    global cell_data
    global HEIGHT
    global WIDTH

    if x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT:
        return True
    else:
        return cell_data[y][x]



def get_next_possible_moves(x, y, path_taken):
    global cell_data
    global HEIGHT
    global WIDTH
    
    possibilities = []
    
    if readCell(x+1, y) != True:
        possibilities.append([x+1, y])
    
    if readCell(x-1, y) != True:
        possibilities.append([x-1, y])
        
    if readCell(x, y+1) != True:
        possibilities.append([x, y+1])
    
    if readCell(x, y-1) != True:
        possibilities.append([x, y-1])

    index = 0
    while index < len(possibilities):
        poss = possibilities[index]
        found = False
        if poss in visitedCells:
            possibilities.pop(index)
            found = True
        if found == False:
            index += 1
    
    return possibilities


def next_square():
    global HEIGHT
    global WIDTH
    global cell_data
    global cell_turtles
    global threads
    global solutions

    next_threads = []

    for thread in threads:
        currentPos = thread[len(thread)-1]
        x = currentPos[0]
        y = currentPos[1]
        if x == WIDTH-1 and y == HEIGHT-1:
            solutions.append(copy.deepcopy(thread))
        nextMoves = get_next_possible_moves(x, y, thread)
        for move in nextMoves:
            if SHOW_SEARCH:
                if cell_turtles[move[1]][move[0]].color() != "light green":
                    cell_turtles[move[1]][move[0]].color("light green")

            if SUPER_FAST_MODE == True:
                visitedCells.append(move)
            
            nThread = copy.deepcopy(thread)
            nThread.append(move)
            next_threads.append(copy.deepcopy(nThread))

    threads = copy.deepcopy(next_threads)

    if SUPER_FAST_MODE == False:
        for thread in threads:
            visitedCells.append(thread[len(thread)-1])




for i in range(10):
    print()

print("Maze Solver")
print()
files = sorted(os.listdir(ROOT_PATH))
try:
    files.remove(".DS_Store") # hidden file added to each folder by MacOS
except:
    pass

loaded = False

while loaded == False:
    
    if len(files) > 0:
        print("Your files:")
        for i in range(0, len(files)):
            print(str(i+1) + ". " + files[i])

        print()
        print("Enter the number corresponding to the file you want to load.")
        #if True:
        try:
            fNum = int(input("Enter here: "))
            if fNum > 0 and fNum <= len(files):
                print()
                #if True:
                try:
                    print(ROOT_PATH + files[fNum-1])
                    file = open(ROOT_PATH + files[fNum-1], "r")
                    img = file.read()
                    file.close()
                    try:
                        img = img.remove("\n")
                    except:
                        pass
                    try:
                        img = img.remove("\r")
                    except:
                        pass

                    #if True:
                    try:
                        print("Drawing maze, please wait...")
                        img = img.split(",")
                        width = int(img[0])
                        height = int(img[1])
                        img.pop(0)
                        img.pop(0)
                        data = []
                        
                        for y in range(0, height):
                            row = []
                            for x in range(0, width):
                                row.append(int(img[width*y + x]))
                                
                            data.append(row)
                        if height > width:
                            pxSize = 450/height
                        else:
                            pxSize = 450/width
                        initMaze(height, width, pxSize, data)
                        loaded = True

                    except:
                        print()
                        print("Failed to process file")
                        print("This might not be a .bim file")
                        print("only .bim (MaxCloud Binary Image) files are supported by this program")
                        print("if this is a .bim file, it may be corrupted")
                except:
                    print()
                    print("Failed to open file")
            else:
                print()
                print("Your input must be between 1 and " + str(len(files)))
        except:
            print()
            print("Your input must be an integer")


    else:
        print("You have no files currently loaded. Please put a .bim file on the 'mazes' folder, so that it can be loaded")
        
        data = [ [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0] ]

        initMaze(5, 5, 20, data)
        loaded = True
    for i in range(5):
        print()




print("done drawing maze")
print()
print()
print("loading, please wait")
startTime = time.perf_counter_ns()
stepsTaken = 0
highestThreads = 0
while solutions == [] and len(threads) > 0:
    next_square()

    stepsTaken += 1
    if len(threads) > highestThreads:
        highestThreads = len(threads)

    #print("Current threads: " + str(len(threads)))

    if len(threads) > MAXIMUM_ALLOWED_THREADS:
        print("ERROR: thread limit passed. This maze is too complicated for this algorithm, and would take too long to solve.")
        threads = []
    
    #for thread in threads:
    #    print(thread)
    #for i in range(6):
    #    print()
    #input("press enter to continue")



endTime = time.perf_counter_ns()
print("done loading")





if len(solutions) > 0:
    
    for point in solutions[0]:
        cell_turtles[point[1]][point[0]].color("blue")

    print()
    print("Steps needed to solve: "+ str(stepsTaken))
    print()
    #print("Time taken (nanoseconds): " + str(endTime-startTime))
    print("Time taken (microseconds): " + str(int((endTime-startTime)/1000)))
    print("Time taken (milliseconds): " + str(round((endTime-startTime)/1000000, 2)))
    print("Time taken (seconds): " + str(round((endTime-startTime)/1000000000, 2)))
    print()
    print("Highest number of threads at any point while solving: " + str(highestThreads))

    for i in range(3):
        print()

    if len(solutions) > 1:
        print(str(len(solutions)) + " equally short solutions were found:")
    else:
        print("This is the path to follow for the shortest solution:")
   # print()
   # print()
   # print("step_number : [x-coordinate, y-coordinate]")
    print()
    print()

   # for solution in solutions:
   #     step = 0
   #     for point in solution:
   #         step += 1
   #         print(step, ":", point)
   #     for i in range(5):
   #         print()



    print()
    print()
    print()
    
    if len(solutions) > 1:

        while True:
            for solution in solutions:
                for point in solution:
                    cell_turtles[point[1]][point[0]].color("blue")
                    
                time.sleep(5)
                
                for point in solution:
                    cell_turtles[point[1]][point[0]].color("light green")



else:
    print("No solution could be found for this maze")
    print()
    print()
    print("Steps calcilated: "+ str(stepsTaken))
    print()
    #print("Time taken (nanoseconds): " + str(endTime-startTime))
    print("Time taken (microseconds): " + str(int((endTime-startTime)/1000)))
    print("Time taken (milliseconds): " + str(round((endTime-startTime)/1000000, 2)))
    print("Time taken (seconds): " + str(round((endTime-startTime)/1000000000, 2)))
    print()
    print("Highest number of threads at any point while solving: " + str(highestThreads))
