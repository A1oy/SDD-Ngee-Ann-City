#Starting of the game
print("Welcome, Mayor of Simp City!")

import csv
import random
import sys
import json


columnName =  ["A", "B", "C", "D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
turn = 1
currency = 16
totalBuildingList = []
buildingType = []
savedFileMap = []


#Main Menu Choices
def mainMenu():
    while True:
        try:
            #ask for chioce
            menuChoice = int(input("----------------------------\
                \n1. Start new game\n2. Load saved game\n3. See high score leaderboard\n\n0. Exit\nYour choice? "))
            #Gives assertion error if statement = False
            assert 0<=menuChoice<=3
            return menuChoice
        except:
            print("Invalid Option")

#Map Layout
def layout(columnName):
    #Prints map layout
    print("   ",end="")
    #Print top Alphabets
    for i in range(len(columnName)):
        print(" {} ".format(columnName[i]),end=" ")
    print("        Currency")
    for row in range(20):
        #leaving 2 spaces before printing map to look organized
        print("  ",end="")
        #prints +-----+-----+-----+-----+
        for i in range(20):
            print("+---",end="")
        print("+",end="")
        if row == 0:
            print("        --------")
        else:
            print()
        #Prints row number
        print("{:<2}".format(row+1),end="")
        for column in range(20):
            #prints map list into the map
            print("| {} ".format(mapList[row,column]),end="")
        if row == 0:
            print("|",end="")
            print("           "+str(currency))
        else:
            print("|")
    print("  ",end="")
    #prints last +-----+-----+-----+-----+
    for row in range(20):
        print("+---",end="")
    print("+",end="")
    print()

def createEmptyMap(map_dimensions):
    mapList = {}
    for x in range(map_dimensions):
        for y in range(map_dimensions):
            mapList[x,y] = ' '
    return mapList

#Adds all buildings into pool
def totalBuildings(buildingType):
    totalBuildingList = []
    #Adds all building types 8 times
    for i in range(8):
        totalBuildingList.extend(buildingType)
    return totalBuildingList

#During Game choices
def inGameChoice():
    #repeats the input if invalid option
    while True:
        #prints turn and map layout
        print("Turn "+str(turn))
        layout(columnName)
        try:
            #ask for choice input
            choice = int(input("1. Build a {}\n2. Build a {}\
                \n3. See current score\n\n4. Save game\
                \n0. Exit to main menu\nYour choice? ".format(building1, building2)))
            #gives assertion error if statement is false
            assert 0<=choice<=4
            return choice
        except:         
            print("Invalid Option")

#Save building and map Data
def saveData():

    w = csv.writer(open("output.csv", "w"))

    # loop over dictionary keys and values
    for key, val in mapList.items():
        # write every key and value to file
        w.writerow([key, val])

    with open('data.txt', 'w') as f:
        #writes turn and goes to next line
        f.write('Turn {}\n'.format(turn))
        f.write('Currency {}\n'.format(currency))
        #Saving total build list
        a = ""
        for i in range(len(totalBuildingList)):
            a = a + totalBuildingList[i] + ","
        f.write(a[:-1] + '\n')
        
#Save the current building 1 and 2
def saveCurrentRandomBuilding():
    with open('CurrentRandomBuilding.txt', 'w') as f:
        s = building1 + "," + building2
        f.write(s)

#Load data
def load():
    #Try to find file else loads new game
    try:

        with open("output.csv","r") as obj:
            reader=csv.reader(obj)
            mapList = {}
            for row in reader:
                if len(row) != 0:
                    first_int, last_int = row[0][1:-1].split(',')
                    mapList[int(first_int), int(last_int)]= row[1]

        with open("data.txt", "r") as f:
            #Adding all text into a list
            for i in f:
                savedFile = i.strip("\n").split(",")
                savedFileMap.append(savedFile)

        #Getting turn Number
        turn = savedFileMap[0][0]
        turn = int(turn.replace("Turn",""))
        currency = savedFileMap[1][0]
        currency = int(currency.replace("Currency",""))

        #getting total building list
        totalBuildingList = savedFileMap[2]

    except:
        #returns new game
        print("No save file found, starting new game.")
        buildingChoice()
        turn = 1
        mapList = createEmptyMap(20)
        totalBuildingList = totalBuildings(buildingType)
        for i in range(len(buildingType)):
            list = []
            list.append(buildingType[i])
            list.append(totalBuildingList.count(buildingType[i]))

    return turn, currency,mapList, totalBuildingList

#Loads the current building 1 and 2
def loadCurrentRandomBuilding():
    buildings = []
    #Try to load in file else make random building
    try:
        with open('CurrentRandomBuilding.txt', 'r') as f:
            for i in f:
                savedFile = i.split(",")
                buildings.append(savedFile)
                #Get buildings out from file
                building1 = buildings[0][0]
                building2 = buildings[0][1]

    except:
        #Makes random building
        num1 = random.randint(0,len(totalBuildingList)-1)
        num2 = random.randint(0,len(totalBuildingList)-1)
        #Make sure the same building index cannot be chosen
        while num1 == num2:
            #Reroll for another building index
            num2 = random.randint(0,len(totalBuildingList)-1)
        building1 = totalBuildingList[num1]
        building2 = totalBuildingList[num2] 

    return building1, building2

#Function for coordinates
def cord():
    cols = "abcdefghijklmnopqrst"
    cordList = []
    for y in range(20):
        for x in range(20):
            cord = cols[y]+str(x+1)
            cordList.append(cord)

    while True:
        try:
            cords = input("Build where? (e.g. a1) ")
            #Checks with cord list for valid building coordinates
            assert cords in cordList
            for i in range(len(cordList)):
                #takes alphabet
                alphabet = cords[0]
                alphabet = alphabet.upper()
                #takes Number
                row = int(cords[1:len(cords)])-1
                column = columnName.index(alphabet)
                return row, column
        except:
            #Tell player that input cords are incorrect
            print("Error, Incorrect coordinates.")

#Checking for Valid building position
def adjacent(turn, row, column):
    if turn == 1:
        validPos = True
        return validPos
    else:
        try:
            #checking for adjacent buildings
            #Checks top, bottom, left, right respectively
            if row+1 != 20 and mapList[row+1,column] != " "\
            or row-1 != -1 and mapList[row-1,column] != " "\
            or column-1 != -1 and mapList[row,column-1] != " "\
            or column+1 != 20 and mapList[row,column+1] != " ":
                #Check if current space is 
                if mapList[row,column] == " ":
                    #Position is a valid position
                    validPos = True
            assert validPos
            return validPos
        except:
            #Tells player that cords is invalid
            print("Building must be adjacent to first building or on a clear space")

#Function for total score and printing score
def score():
    score = 0

    RESscore = 0
    statement = "RES: "
    #Score for RES
    #Search through the map list
    for row in range(20):
        for column in range(20):
            #Finding RES  cords
            if mapList[row,column] == "R":
                #If
                if mapList[row-1,column] == "I" or mapList[row+1,column] == "I" or mapList[row,column-1] == "I" or mapList[row,column+1] == "I":
                    RESscore = 1
                    statement = statement + "1" + " + "
                elif mapList[row-1,column] == "R" or mapList[row+1,column] == "R" or mapList[row,column-1] == "R" or mapList[row,column+1] == "R":
                    #Adds to the RES's score
                    RESscore = RESscore+1
                    #Adds string to show player 
                    statement = statement + "1" + " + "
                elif mapList[row-1,column] == "C" or mapList[row+1,column] == "C" or mapList[row,column-1] == "C" or mapList[row,column+1] == "C":
                    #Adds to the RES's score
                    RESscore = RESscore+1
                    #Adds string to show player 
                    statement = statement + "1" + " + "
                elif mapList[row-1,column] == "O" or mapList[row+1,column] == "O" or mapList[row,column-1] == "O" or mapList[row,column+1] == "O":
                    #Adds to the RES's score
                    RESscore = RESscore+2
                    #Adds string to show player 
                    statement = statement + "2" + " + "
                else:
                    RESscore = 0
                    
    #Finds if RES score = 0
    if RESscore != 0:
        #Formats RES score statement to print
        statement = statement[:-2] + '= ' + str(RESscore)
    else:
        #If score == 0 
        statement = "RES: 0"
    print()
    print(statement)
    score = score + RESscore

    #Score for IND
    IndScore = 0
    #loops to go through map 
    for row in range(20):
        for column in range(20):
            #If find Ind, addscore
            if "I" == mapList[row,column]:
                IndScore = IndScore + 1
                #If
                if mapList[row-1,column] == "R":
                    currency += 1
                elif mapList[row+1,column] == "R":
                    currency += 1
                elif mapList[row,column-1] == "R":
                    currency += 1
                elif mapList[row,column+1] == "R":
                    currency += 1
    #Finding if Ind score = 0
    if IndScore != 0:
        statement = statement[:-2] + '= ' + str(IndScore)
    else:
        statement = "IND: 0"
    print(statement)
    score = score + IndScore
    
    #Score for Comm
    CommScore = 0
    statement = "COMM: "
    #Loops through map for to find cords of Comm
    for row in range(20):
        for column in range(20):
            #Finding Comm cords
            if mapList[row,column] == "C":
                if mapList[row-1,column] == "R" or mapList[row+1,column] == "R" or mapList[row,column-1] == "R" or mapList[row,column+1] == "R":
                    #Add currency
                    currency += 1
                elif mapList[row-1,column] == "C" or mapList[row+1,column] == "C" or mapList[row,column-1] == "C" or mapList[row,column+1] == "C":
                    #Adds to the Comm's score
                    CommScore = CommScore+1
                    #Adds string to show player 
                    statement = statement + "1" + " + "
                else:
                    CommScore = 0        
    #Finding if Ind score = 0
    if CommScore != 0:
        statement = statement[:-2] + '= ' + str(IndScore)
    else:
        statement = "Comm: 0"
    print(statement)
    score = score + CommScore

    #Score for Park
    ParkScore = 0
    statement = "PAR: "
    #Loops through map for to find cords of PAR
    for row in range(20):
        for column in range(20):
            #Finding Comm cords
            if mapList[row,column] == "O":
                if mapList[row-1,column] == "O" or mapList[row+1,column] == "O" or mapList[row,column-1] == "O" or mapList[row,column+1] == "O":
                    #Add Score
                    ParkScore += 1
    #Finding if Park score = 0
    if ParkScore != 0:
        statement = statement[:-2] + '= ' + str(ParkScore)
    else:
        statement = "SHP: 0"
    print(statement)
    score = score + ParkScore               

    #Score for Road
    statement = "ROAD: "
    RoadScore = 0
    RoadStreakNum = 0
    #Loops through map for Road cords
    for row in range(20):
        for column in range(20):
            #Finding for Road
            if mapList[row,column] == "*":
                #Each Road found increases streak
                RoadStreakNum = RoadStreakNum + 1
                #restarts streak since Road only works for rows
                if column == 3:
                    statement = statement + (str(RoadStreakNum) + " + ")*RoadStreakNum
                    Roadscore = Roadscore + (RoadStreakNum*RoadStreakNum)
                    RoadStreakNum = 0
            #restarts streak since no other Road found beside
            else:
                statement = statement + (str(RoadStreakNum) + " + ")*RoadStreakNum
                RoadScore = RoadScore + (RoadStreakNum*RoadStreakNum)
                RoadStreakNum = 0
    #Finding if Road score = 0
    if RoadScore != 0:
        statement = statement[:-2] + '= ' + str(RoadScore)
    else:
        statement = "Road: 0"
    print(statement)
    score = score + RoadScore

    print("Total score: "+str(score))
    return(score)

#Function to load in high score leaderboard
def loadHighScore():
    try:
        with open("highscore.txt", "r") as f:
            f = f.readlines()
            #makes the leaderboard from highest to lowest
            f = sorted(f, reverse=True)  
            #prints the actual leaderboard
            #Formats the leaderboard
            print("--------- HIGH SCORES ---------")
            print("{:4}{:22}{}".format("Pos", "Player", "Score"))
            print("--- ------                -----")
            #more than 10 players, print only top 10
            if range(len(f)>10):
                for lines in range(10):
                    p = str(f[lines]).strip("\n").split(",")
                    #Prints position number, player name and score respectively
                    print("{:4}{:25}{}".format(str(lines + 1) + ".", str(p[1]), str(p[0])))
            else:
                #print all players
                for lines in range(len(f)):
                    p = str(f[lines]).strip("\n").split(",")
                    #Prints position number, player name and score respectively
                    print("{:4}{:25}{}".format(str(lines + 1) + ".", str(p[1]), str(p[0])))
            print("-------------------------------")
    except:
        print("No high score found.")
        
#Function to save score into leaderboard
def enterScore():
    try:
        with open("highscore.txt", "r") as f:
            f = f.readlines()
            #makes the leaderboard from highest to lowest
            f = sorted(f, reverse=True)
            #more than 10 highscores, finds if score is higher than top 10
            if range(len(f)>10):
                p = str(f[9]).strip("\n").split(",")
                if score() > int(p[0]):
                    with open("highscore.txt", "a") as a:
                        player = input("Input your name: ")
                        s = str(score()) + "," + player + "\n"
                        a.write(s)
            #Not more than 10 highscores, adds in score
            else:
                with open("highscore.txt", "a") as a:
                    player = input("Input your name: ")
                    s = str(score()) + "," + player + "\n"
                    a.write(s)
    except:
        #If no highscore file/ deleted highscore file
        with open("highscore.txt", "a") as a:
            player = input("Input your name: ")
            s = str(score()) + "," + player + "\n"
            a.write(s)

#Function for building choices before the start of a new game
def buildingChoice():
    buildings = ["R", "I", "C", "O", "*"]
    if len(buildings) > 5:
        while True:
            try:
                print(buildings)
                choice = input("Choose your 5 building types for this game session. e.g. C | ")
                assert choice in buildings
                buildings.remove(choice)
                buildingType.append(choice)
            except AssertionError:
                print("Please input correct buildings in caps.")
            if len(buildingType) == 5:
                break
    else:
        for i in range(len(buildings)):
            choice = buildings[i]
            buildingType.append(choice)

#Game Main Code
while True:
    menuChoice = mainMenu()
    if menuChoice == 1:
        buildingChoice()
        #Resetting the map since it is new game
        mapList = createEmptyMap(20)
        totalBuildingList = totalBuildings(buildingType)
        #Finds first pair of random buildings
        num1 = random.randint(0,len(totalBuildingList)-1)
        num2 = random.randint(0,len(totalBuildingList)-1)
        #Make sure the same building index cannot be chosen
        while num1 == num2:
            #Reroll for another building index
            num2 = random.randint(0,len(totalBuildingList)-1)
        building1 = totalBuildingList[num1]
        building2 = totalBuildingList[num2] 

        while True:
            choice = inGameChoice()

            if choice == 1:
                #Removes chosen building
                totalBuildingList.remove(building1)
                totalBuildingList.remove(building2)
                while True:
                    row, column = cord()
                    #Checks Adjacent buildings
                    validPos = adjacent(turn, row, column)
                    if validPos == True:
                        mapList[row,column] = building1
                        turn = turn+1
                        currency -= 1
                        #setting coming pair of buildings
                        num1 = random.randint(0,len(totalBuildingList)-1)
                        num2 = random.randint(0,len(totalBuildingList)-1)
                        #Make sure the same building index cannot be chosen
                        while num1 == num2:
                            #Reroll for another building index
                            num2 = random.randint(0,len(totalBuildingList)-1)
                        building1 = totalBuildingList[num1]
                        building2 = totalBuildingList[num2] 
                        break

            if choice == 2:
                #Removes chosen building
                totalBuildingList.remove(building1)
                totalBuildingList.remove(building2)
                while True:
                    row, column = cord()
                    #Checks Adjacent buildings
                    validPos = adjacent(turn, row, column)
                    if validPos == True:
                        mapList[row,column] = building2
                        turn = turn+1
                        currency -= 1
                        #setting coming pair of buildings
                        num1 = random.randint(0,len(totalBuildingList)-1)
                        num2 = random.randint(0,len(totalBuildingList)-1)
                        #Make sure the same building index cannot be chosen
                        while num1 == num2:
                            #Reroll for another building index
                            num2 = random.randint(0,len(totalBuildingList)-1)
                        building1 = totalBuildingList[num1]
                        building2 = totalBuildingList[num2] 
                        break

            if choice == 3:
                score()

            if choice == 4:
                #Functions for saving
                saveData()
                saveCurrentRandomBuilding()
                print("Game Saved!")

            if choice == 0:
                turn = 1
                break

            if turn > 16:
                print("Final layout of Simp City: ")
                layout(columnName)
                score()
                enterScore()
                break

    #Loading save file
    if menuChoice == 2:
        turn, currency,mapList, totalBuildingList = load()
        building1, building2 = loadCurrentRandomBuilding()
        #Setting first pair of buildings
        while True:
            choice = inGameChoice()

            if choice == 1:
                #Removes chosen building
                totalBuildingList.remove(building1)
                totalBuildingList.remove(building2)
                while True:
                    row, column = cord()
                    #Checks Adjacent buildings
                    validPos = adjacent(turn, row, column)
                    if validPos == True:
                        mapList[row,column] = building1
                        turn = turn+1
                        currency -= 1
                        #setting coming pair of buildings
                        num1 = random.randint(0,len(totalBuildingList)-1)
                        num2 = random.randint(0,len(totalBuildingList)-1)
                        #Make sure the same building index cannot be chosen
                        while num1 == num2:
                            #Reroll for another building index
                            num2 = random.randint(0,len(totalBuildingList)-1)
                        building1 = totalBuildingList[num1]
                        building2 = totalBuildingList[num2] 
                        break

            if choice == 2:
                #Removes chosen building
                totalBuildingList.remove(building1)
                totalBuildingList.remove(building2)
                while True:
                    row, column = cord()
                    #Checks Adjacent buildings
                    validPos = adjacent(turn, row, column)
                    if validPos == True:
                        mapList[row,column] = building2
                        turn = turn+1
                        currency -= 1
                        #setting coming pair of buildings
                        num1 = random.randint(0,len(totalBuildingList)-1)
                        num2 = random.randint(0,len(totalBuildingList)-1)
                        #Make sure the same building index cannot be chosen
                        while num1 == num2:
                            #Reroll for another building index
                            num2 = random.randint(0,len(totalBuildingList)-1)
                        building1 = totalBuildingList[num1]
                        building2 = totalBuildingList[num2] 
                        break

            if choice == 3:
                score()

            if choice == 4:
                #Functions for saving
                saveData()
                saveCurrentRandomBuilding()
                print("Game Saved!")

            if choice == 0:
                turn = 1
                break
        
            if turn > 16:
                print("Final layout of Simp City: ")
                layout(columnName)
                score()
                enterScore()
                break

    if menuChoice == 3:
        loadHighScore()

    if menuChoice == 0:
        #function to exit
        sys.exit(0)
