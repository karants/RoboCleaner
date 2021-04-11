"""
Project: The Bot Project
Module: Main
Course: 3PR3
Author: Karan Shah
Created: 29/3/2021
"""

#Importing Modules
import robocleaner
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

#Global robots dictionary with serialnumber,name and cleaning speed(tiles/sec)
#Usually imported from a database connection
robotscatalog = {'1':['Pioneer','1'],'2':['Horizon','2']}

#Maximum number of inidividual robots the service can offer
MAX_ROBOTS = 5

#Colour definition for each individual robot
robotcolours = {1:'Red', 2:'Blue',3:'Green',4:'Yellow',5:'Cyan'}

#Maximum dimensions in ft. Scalable based on matplotlib's plotting capablities
MAX_LENGTH = 26
MAX_WIDTH = 30

#Function to display a border of asterisks
def DisplayBorder(length):
    print("\n")
    for header in range(length):
        print("*", end="")


#Function to accept room dimensions from the user
def InputRoomDimensions():

    #Accepting Length & Width and Catching Exceptions
    while True:
        try:
            RoomLength = int(input("\nEnter the length of the room (in ft): "))
            break

        except ValueError:
            print("\nError: Expecting an integer between 1 and", MAX_LENGTH)

    while (RoomLength < 1 or RoomLength > MAX_LENGTH):
            print("\nNumber of tiles must be between 1 and", MAX_LENGTH)

            while True:
                try:
                    RoomLength = int(input("Enter the length again: "))
                    break

                except ValueError:
                    print("\nError: Expecting an integer between 1", MAX_LENGTH)

    while True:
        try:
            RoomWidth = int(input("Enter the width of the room (in ft): "))
            break

        except ValueError:
            print("\nError: Expecting an integer between 1 and", MAX_WIDTH)

    while (RoomWidth < 1 or RoomWidth > MAX_WIDTH):
            print("\nNumber of tiles must be between 1 and", MAX_WIDTH)

            while True:
                try:
                    RoomWidth = int(input("Enter the width again: "))
                    break

                except ValueError:
                    print("\nError: Expecting an integer between 1 and", MAX_WIDTH)


    return RoomLength, RoomWidth

#Function to present the catalog and allow user to select the robots of their choice
def InputRobotChoice(RoomLength, RoomWidth):

    DisplayBorder(14)
    print("\nChoose a Robot", end = "")
    DisplayBorder(14)
    print("\n\nNumber\t Robot\t\t Speed (tiles/second)")
    for roboname in robotscatalog:
        print(roboname, "\t\t", robotscatalog[roboname][0], "\t", robotscatalog[roboname][1])


    #Accepting Robot Choice and Catching Exceptions
    while True:
        try:
            RoboChoice = int(input("\nEnter the choice number of the robot: "))
            break

        except ValueError:
            print("\nError: Expecting an integer between", min(robotscatalog), "and", max(robotscatalog))

    while (RoboChoice < int(min(robotscatalog)) or RoboChoice > int(max(robotscatalog))):
            print("\nChoice number must be between", min(robotscatalog), "and", max(robotscatalog))

            while True:
                try:
                    RoboChoice = int(input("Enter the choice number again: "))
                    break

                except ValueError:
                    print("\nError: Expecting an integer between", min(robotscatalog), "and", max(robotscatalog))



    #Function call to calculate the max number of robots that can fit for the specific room size
    SpecificMaxRobots = CalculateSpecificMaxRobots(RoomWidth)

    #Accepting Number of Robots
    while True:
        try:
            RoboArmy = int(input(f"Enter the number of {robotscatalog[str(RoboChoice)][0]} robots (max {SpecificMaxRobots}): "))

            break

        except ValueError:
            print("\nError: Expecting an integer between 1 and", SpecificMaxRobots)

    while (RoboArmy < 1 or RoboArmy > SpecificMaxRobots):

            if(SpecificMaxRobots < MAX_ROBOTS):
                print("\nNumber of robots requested are more than required for the job.")
            else:
                print("\nNumber of robots must be between 1 and", SpecificMaxRobots)

            while True:
                try:
                    RoboArmy = int(input(f"Enter the number of {robotscatalog[str(RoboChoice)][0]} robots again: "))
                    break

                except ValueError:
                    print("\nError: Expecting an integer between 1 and", SpecificMaxRobots)


    return RoboChoice, RoboArmy


#Function to calculate the specific amount of maximum robots the user can select based on the room size
def CalculateSpecificMaxRobots(RoomWidth):

    if(RoomWidth > MAX_ROBOTS):

            SpecificMaxRobots = MAX_ROBOTS
    else:
            SpecificMaxRobots = int(RoomWidth)


    return SpecificMaxRobots

#Function to initialize the RoboCleaner class and robot instances
def InitializeRobots(RoomLength, RoomWidth, RoboChoice, RoboArmy):

    robots = list()
    for robo in range(RoboArmy):

        #calculating the initial and the final coordinates for each robot
        initialX = 1
        finalX = RoomLength
        initialY = ((int(RoomWidth/RoboArmy) * (robo+1)) - (int(RoomWidth/RoboArmy) -1))
        finalY = (int(RoomWidth/RoboArmy) * (robo+1))

        #for odd room sizes where robots cannot equally divide the work, the last robot continues
        #to finish the remaining tiles
        if((RoomWidth % RoboArmy != 0) & ((robo+1) == RoboArmy)):
            finalY = RoomWidth

        #Creating a list of instances
        robots.append(robocleaner.RoboCleaner(RoboChoice, \
               robotscatalog[str(RoboChoice)][0],\
               robotscatalog[str(RoboChoice)][1],(robo+1),\
               robotcolours[robo+1], initialX,initialY,finalX,finalY))


    return robots

#Function to calculate the maximum number of tiles covered by a single robot
def MaxTiles(robots):

    MaximumTiles = 0
    for robot in range(len(robots)):
        if(robots[robot].GetTotalTiles() > MaximumTiles):
            MaximumTiles = robots[robot].GetTotalTiles()

    return MaximumTiles

#Function to visualize the room cleaning process
def PlotProgress(robots, RoomLength, RoomWidth):

    plt.ion()

    #Unfortunately, the legend is hardcoded is not dynamically programmed.
    blue_line = mlines.Line2D([], [], color='blue', label='Robot 2')
    red_line = mlines.Line2D([], [], color='red', label='Robot 1')
    green_line = mlines.Line2D([], [], color='green', label='Robot 3')
    yellow_line = mlines.Line2D([], [], color='yellow', label='Robot 4')
    cyan_line = mlines.Line2D([], [], color='cyan', label='Robot 5')
    plt.legend(handles=[red_line, blue_line, green_line,\
                        yellow_line, cyan_line ],loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.grid()
    x=list()
    y=list()
    plt.title("RoboCleaning Service", fontsize = 20)

    # Initializing the axes
    for num in range(RoomLength+1):
            x.append(num)
    for numy in range(RoomWidth+1):
            y.append(numy)

    plt.xlabel('Room Length (feet)', fontsize = 12)
    plt.ylabel('Room Width (feet)', fontsize = 12)
    plt.xlim(xmin=0, xmax=1)
    plt.ylim(ymin=0, ymax=1)
    plt.xticks(x)
    plt.yticks(y)

    #variable to keep track of time based on the speed of the robot
    time = (1/int(robots[0].GetSpeed()))

    #the for loop stops at the max number of tiles to be cleaned by a robot
    for counter in range(MaxTiles(robots)):

        #simultaneous cleaning to achieve efficiency
        for robot in range(len(robots)):

            #move the robot to the cleaning tile only if the tile is supposed to be cleaning by the robot
            #robot cleans the tile only if it's tile counter is lower than the max number of tiles it is assigned to clean
            if((counter < robots[robot].GetTotalTiles())):
                if(counter == 0):

                     a, b = robots[robot].GetInitialCoordinates()
                     fa, fb = robots[robot].GetFinalCoordinates()

                else:
                     a, b = robots[robot].GetCoordinates()

                RoboColour = robots[robot].GetColour()

                #line graph coordinates
                particularBox_xCoord = [(a), (a-1), (a-1), (a), (a)]
                particularBox_yCoord = [(b), (b), (b-1), (b-1), (b)]

                #plot the graph
                plt.plot(particularBox_xCoord, particularBox_yCoord,RoboColour, label='robot')

                #update the elapsed time subtitle
                plt.suptitle(f"Time elapsed - {format(time,'.2f')} seconds", fontsize = 15)

                #update the value of the coordinates for the next tile to be cleaned
                if(((a) % int(fa)) != 0):
                     a += 1
                else:
                     a = 1
                     b += 1

                #set the values of the coordinates for the next tile in the instance of the robot
                robots[robot].SetCoordinates(a, b)

        #calculate time based on the speed and update the graph based on the speed of the robot
        time += 1/int(robots[0].GetSpeed())
        plt.pause(1/int(robots[0].GetSpeed()))

    #pause the graph for 2 seconds after the cleaning is done for the user to have a good look before closing
    plt.pause(2)
    plt.close()


#Function to present the menu options to the user
def CoverageChoice(RoomLength,RoomWidth, robots):

    #Initializing menu option
    option = -1

    #While loop to drive the program menu
    while (option != 4):

        DisplayBorder(17)
        print("\nEstimate Coverage",end="")
        DisplayBorder(17)
        print("\n\n1. Find the percentage of coverage by entering time (in seconds): ")
        print("2. Find the time needed by entering the coverage percentage: ")
        print("3. Start the robots and monitor real time. ")
        print("4. Exit")

        #Catching Exceptions
        while True:
            try:
                option = int(input("Enter your choice:  "))
                break

            except ValueError:
                print("\nError: Expecting a number between 1 and 4")

        while (option < 1 or option > 4):
            print("\nYour choice must be between 1 and 4")

            while True:
                try:
                    option = int(input("Enter your choice again:  "))
                    break

                except ValueError:
                    print("\nError: Expecting a number between 1 and 4")

        #Menu Option 1
        if ( option == 1 ):

            DisplayBorder(22)
            print("\nPercentage of Coverage",end="")
            DisplayBorder(22)
            #Accepting Time
            while True:
                try:
                    time = int(input("Enter the time in seconds: "))
                    break

                except ValueError:
                    print("\nError: Expecting an integer")

            while (time < 1 or time > (RoomLength*RoomWidth)):
                print("\nTime in seconds must be between 1 and", (RoomLength*RoomWidth))

                while True:
                    try:
                        time = int(input("Enter the time again:  "))
                        break

                    except ValueError:
                        print("\nError: Expecting a number between 1 and", (RoomLength*RoomWidth))

            #Function call to calculate the percentage based on the time entered by the user
            PercentageCovered = CalculatePercentage(time, RoomLength, RoomWidth, robots)

            print("\nPercentage of room covered =", format(PercentageCovered,".2f"), "%")

        #Menu option 2
        elif(option == 2):

            DisplayBorder(13)
            print("\nTime Required",end="")
            DisplayBorder(13)

            #Accepting Time
            while True:
                try:
                    percentage = int(input("Enter the percentage: "))
                    break

                except ValueError:
                    print("\nError: Expecting an integer")

            while (percentage < 1 or percentage > 100):
                print("\nPercentage must be between 1 and 100")

                while True:
                    try:
                        percentage = int(input("Enter the percentage again:  "))
                        break

                    except ValueError:
                        print("\nError: Expecting a number between 1 and 100")

            #Function call to calculate the time needed based on the percentage entered by the user
            TimeNeeded = CalculateTime(percentage, RoomLength, RoomWidth, robots)
            print("\nTime needed to cover",percentage,"% of the room =", format(TimeNeeded,".2f"), "seconds")

        #Menu option 3
        elif(option == 3):
                DisplayBorder(25)
                print("\nCleaning the room...", end = "")
                DisplayBorder(25)
                PlotProgress(robots, RoomLength, RoomWidth)
                print("\n\nYour room has been cleaned in", format(CalculateTime(100, RoomLength, RoomWidth, robots),'.2f'), \
                      "seconds.\n\nThank you for choosing RoboCleaner!")
                break

#Function to calculate the percentage based on time entered by the user
def CalculatePercentage(time, RoomLength, RoomWidth, robots):

    #math behind calculating the total number of tiles covered based on the time entered by the user
    #total number of tiles covered by each robot is then added and divided by the total number of tiles
    #a percentage is then calculated and returned

    TotalTiles = RoomLength * RoomWidth
    TotalCoveredTiles = 0
    for robot in range(len(robots)):
        TotalCoveredTiles += robots[robot].GetTilesOnTime(time)

    PercentageCovered = (TotalCoveredTiles/TotalTiles) * 100

    if(PercentageCovered > 100):
        PercentageCovered = 100

    return PercentageCovered

#Function to calculate the time needed based on the percentage entered by the user
def CalculateTime(percentage,RoomLength, RoomWidth, robots):


    #Calculating the total number of tiles covered by the robots using the percentage
    #for odd size rooms, the last robot cleans more tiles than the other robots
    #accomodating for that by calculating how many tiles were cleaned equally by all robots
    #and how many were cleaned just by the last one
    #and then calculating the time needed based on the speed of the robot

    TotalTiles = RoomLength * RoomWidth
    TotalCoveredTiles = (percentage * TotalTiles) / 100
    RowsPerRobot = int(RoomWidth/len(robots))
    RowsCoveredEqually = RowsPerRobot * len(robots)

    if(RowsCoveredEqually != RoomWidth):

        if(TotalCoveredTiles > (RowsCoveredEqually*RoomLength)):
            TimeNeeded = (RowsCoveredEqually*RoomLength)/ (len(robots)*int(robots[0].GetSpeed()))
            TimeNeeded += (TotalCoveredTiles - (RowsCoveredEqually*RoomLength)) / int(robots[0].GetSpeed())

        else:
            TimeNeeded = TotalCoveredTiles / (len(robots)*int(robots[0].GetSpeed()))


    else:
        TimeNeeded = TotalCoveredTiles / (len(robots)*int(robots[0].GetSpeed()))

    return TimeNeeded


#Main function
def main():

    DisplayBorder(32)
    print("\n\t\tRoboCleaner\nAutomated Room Cleaning Service",end = "")
    DisplayBorder(32)
    RoomLength, RoomWidth = InputRoomDimensions()
    RoboChoice, RoboArmy = InputRobotChoice(RoomLength, RoomWidth)
    robots = InitializeRobots(RoomLength, RoomWidth, RoboChoice, RoboArmy)
    CoverageChoice(RoomLength, RoomWidth, robots)


#main function call
main()
