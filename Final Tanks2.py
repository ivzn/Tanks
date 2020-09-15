import pygame
import math
from pygame.locals import *

#initializes Pygame modules
pygame.init()
pygame.font.init()

#colours
white = (255,255,255)
black = (0,0,0)
red = (234,41,44)
blue = (67,104,255)
green = (34,139,34)
brown = (139,69,19)
skyblue = (135,206,235)

#images
backarrow = pygame.image.load("back.png")
redTank = pygame.image.load("redTank1.png")
blueTank = pygame.image.load("blueTank1.png")
redMissile = pygame.image.load("redMissile.png")
blueMissile = pygame.image.load("blueMissile.png")
grenade = pygame.image.load("grenade.png")
mine = pygame.image.load("mine.png")
how = pygame.image.load("instruction.png")
mainphoto = pygame.image.load("mainpage.png")

#main setup
#size = (800,600) # gameDisplay is 0,0 at topleft. x,y
#gameDisplay = pygame.display.set_mode(size)

all_fonts = pygame.font.get_fonts() # Add all fonts
f = open("Highscore.txt","r") # Opens textfile for highscore

newscore = 0 # Variable

maxx = 800 # Window dimensions
maxy = 600 # Window dimensions
gameDisplay = pygame.display.set_mode((maxx,maxy)) # Pygame window screen
pygame.display.set_caption("Tanks") # Game window Title
clock = pygame.time.Clock() # import delays and time

## IVAN
redPowerPercent = 1 #0.02 - 1 multiplier for how much power each player chooses
bluePowerPercent = 1

redPowerPercentChange = 0 # delta change for powerPercent
bluePowerPercentChange = 0

redHPBarX = 180 # HP bar
blueHPBarX = 180 # HP bar
turn = "red" # Turn based. Red starts

blueScore = 999999 # Score
redScore = 999999 # Score
writename = 0 #An indicator for if highscore is put
text = "" # Variable for writing Highscore name
winnerlist = list() # A list of the winners. For the highscore
damageCords = [] 
newscreen = 0 # Variable

#tank1 start pos
x1 = maxx - redTank.get_width() - 3
y1 = maxy/2
#tank2 start pos
x2 = 3
y2 = maxy/2

dx1 = 0 # change in x for each tank 
dx2 = 0

redTurPos = 5 #mid point between the 9 positions 
blueTurPos = 5


winner = 0 # 1 = red | 2 = blue
newname = "" #Variable 

def start(): # This function is used to reinitalize all the variables so we can restart the game
  global redPowerPercent
  global bluePowerPercent
  global redPowerPercentChange
  global bluePowerPercentChange
  global redHPBarX
  global blueHPBarX
  global x1
  global y1
  global x2 
  global y2
  global dx1
  global dx2
  global redTurPos
  global blueTurPos
  global redWeaponList
  global blueWeaponList
  global blueScore
  global redScore
  global damageCords
  global turn
  global Initals
  global winner
  global writename
  global text

  text = ""
  writename = 0 
  winner = 0 
  Initals= False

  blueScore = 999999
  redScore = 999999

  redPowerPercent = 1
  bluePowerPercent = 1

  redPowerPercentChange = 0
  bluePowerPercentChange = 0

  redHPBarX = 180
  blueHPBarX = 180
  turn = "red"
  #tank1 start pos
  x1 = maxx - redTank.get_width() -3
  y1 = maxy/2
  #tank2 start pos
  x2 = 3
  y2 = maxy/2 
  dx1 = 0
  dx2 = 0
  redTurPos = 5
  blueTurPos = 5
  redPowerPercent = 1
  bluePowerPercent = 1
  damageCords = []
  redWeaponList = { #directory for weapons
  "shell" : [30, 20, 10, 80],# hole size,damage,ammo,maxpower(velocity)
  "missile" : [80, 60 , 2, 75],# 150,40%
  "grenade" : [60, 50, 4, 50],
  "mine" : [60, 75, 3, 60],
  }
  blueWeaponList = { #directory for weapons
  "shell" : [30, 20, 10, 80],# hole size,damage,ammo,maxpower(velocity)
  "missile" : [80, 60 , 2, 75],# 150,40%
  "grenade" : [60, 50, 4, 50],
  "mine" : [60, 75, 3, 60],
  }
  redWeaponSelection = "shell"
  blueWeaponSelection = "shell"
  
redWeaponList = { #directory for red tank's weapons
 "shell" : [30, 20, 10, 80],# hole size,damage,ammo,maxpower(velocity)
 "missile" : [80, 60 , 2, 75],# 150,40%
 "grenade" : [60, 50, 4, 50],
 "mine" : [60, 75, 3, 60],
}
blueWeaponList = { #directory for blue tank's weapons
 "shell" : [30, 20, 10, 80],# hole size,damage,ammo,maxpower(velocity)
 "missile" : [80, 60 , 2, 75],# 150,40%
 "grenade" : [60, 50, 4, 50],
 "mine" : [60, 75, 3, 60],
}
redWeaponSelection = "shell"
blueWeaponSelection = "shell"

def drawTank1(x,y,turPos): # draws tank and returns its current turret postion 
    gameDisplay.blit(redTank,(x,y))
    redPossibleTurrets = [(x-8,y+4),
                           (x-7,y+1),
                           (x-6,y-2),
                           (x-5,y-5),
                           (x-4,y-8),
                           (x-3,y-9),
                           (x-2,y-11),
                           (x+1,y-12),
                           (x+5,y-13)
                           ]
    pygame.draw.line(gameDisplay,red,(x+15,y+5),redPossibleTurrets[turPos],6)
    return redPossibleTurrets[turPos]

def drawTank2(x,y,turPos):
    gameDisplay.blit(blueTank,(x,y))
    bluePossibleTurrets = [(x+48,y+4),
                           (x+46,y+1),
                           (x+42,y-2),
                           (x+40,y-5),
                           (x+38,y-8),
                           (x+36,y-10),
                           (x+34,y-11),
                           (x+33,y-12),
                           (x+32,y-13) 
                           ]
    pygame.draw.line(gameDisplay,blue,(x+25,y+5),bluePossibleTurrets[turPos],6)
    return bluePossibleTurrets[turPos]

def getTurAngle(turEndCords,tank):# caclulates the angle of each turret and returns it 
    turEndX = turEndCords[0]
    turEndY = turEndCords[1]
    if tank == "red":
        turStartX = x1 + 15
        turStartY = y1 + 5
    elif tank == "blue":
        turStartX = x2 + 25
        turStartY = y2 + 5
    xLength = abs(turStartX - turEndX)# caclulates angle with the end and start point of the rectangle that is the turrent
    yLength = abs(turStartY - turEndY)
    angle = math.atan(yLength/xLength)# uses trig to solve and changes it to rad
    return angle

# checks if a bullet shot hits the enemy tank , returns boolean 
def collisonDetect(bulletX,bulletY,enemyTank,bulletType, bulletWidth, bulletHeight):
    if enemyTank == "blue":
        if bulletType == "shell":
            if (bulletX-4 >= x2 and bulletX-4 <= x2 + blueTank.get_width()) or (bulletX + 4 >= x2 and bulletX + 4 <= x2 + blueTank.get_width()):
                if ( bulletY-4 >= y2 and bulletY -4 <= y2 + blueTank.get_height()) or (bulletY + 4 >= y2 and bulletY + 4 <= y2 + blueTank.get_height()):
                    return True
        else:
            if (bulletX >= x2 and bulletX <= x2 + blueTank.get_width()) or (bulletX + bulletWidth >= x2 and bulletX + bulletWidth <= x2 + blueTank.get_width()):
                if ( bulletY >= y2 and bulletY <= y2 + blueTank.get_height()) or (bulletY + bulletHeight >= y2 and bulletY + bulletHeight <= y2 + blueTank.get_height()):
                    return True
    elif enemyTank == "red":
        if bulletType == "shell":
            if (bulletX-4 >= x1 and bulletX-4 <= x1 + redTank.get_width()) or (bulletX + 4 >= x1 and bulletX + 4 <= x1 + redTank.get_width()):
                if ( bulletY-4 >= y1 and bulletY -4 <= y1 + redTank.get_height()) or (bulletY + 4 >= y1 and bulletY + 4 <= y1 + redTank.get_height()):
                    return True
        else:
            if (bulletX >= x1 and bulletX <= x1 + redTank.get_width()) or (bulletX + bulletWidth >= x1 and bulletX + bulletWidth <= x1 + redTank.get_width()):
                if ( bulletY >= y1 and bulletY <= y1 + redTank.get_height()) or (bulletY + bulletHeight >= y1 and bulletY + bulletHeight <= y1 + redTank.get_height()):
                    return True
                
def fireTurret(tank,bulletType,turCords,powerPercent): 
    global redHPBarX
    global blueHPBarX
    global turn
    
    bulletX = float(turCords[0])
    bulletY = float(turCords[1])

    t = 0 #represents time in velocity equation but actually arbituatry just adds 0.1 evey time while loop runs

    grenadeCounter = 100# times the lopp runs when a grenade hits the ground and continues rolling

    #power percent is set by user from 0-100%
    #the 4th row(bulletType[3]) of the redWeaponList selction is the maxpower that weapon has 
    power = powerPercent*redWeaponList[bulletType][3]

    angle = getTurAngle(turCords,tank)# gets the angle the turrets at

    vy = power*math.sin(angle)# velocity in the y direction by multiplying the angle by the the power
    vx = power*math.cos(angle)# velocity in the x direction 
    
    if tank == "red":
        missileAngle = -1*math.degrees(angle)#flips image and orients to proper angle for barrel

         #print ("Fired at",(bulletX,bulletY),angle)

        #runs when ammo is not empty and the bullet is on screen
        while redWeaponList[bulletType][2] > 0 and bulletX >= 6 and bulletY <= maxy:
            
            #draws background and tanks
            drawScreen()
            redTurXY = drawTank1(x1,y1,redTurPos)
            blueTurXY = drawTank2(x2,y2,blueTurPos)

            if bulletType == "shell":# draws circle to represent shell shot 
                pygame.draw.circle(gameDisplay,red,(int(bulletX),int(bulletY)),4)

                adjustedBulletX = bulletX
                adjustedBulletY = bulletY
                
                bulletWidth = 4
                bulletHeight = 4
                
                
            elif bulletType == "missile":# draws missile shot 
                
                angledMissile = pygame.transform.rotate(redMissile,missileAngle)
                gameDisplay.blit(angledMissile,(int(bulletX)- angledMissile.get_width(), int(bulletY)-angledMissile.get_height()))
                missileAngle += 0.75#rotates missile angle
                
                adjustedBulletX = bulletX- angledMissile.get_width()
                adjustedBulletY = bulletY- angledMissile.get_height()
                
                bulletWidth = angledMissile.get_width()
                bulletHeight = angledMissile.get_height()
                
            elif bulletType == "grenade":#draws grenade shot
                #spins grenade
                grenadeRotate = pygame.transform.rotate(grenade,-1*math.degrees(angle)*t)
                gameDisplay.blit(grenadeRotate,(int(bulletX)- grenadeRotate.get_width(), int(bulletY)-grenadeRotate.get_height()))
                
                adjustedBulletX = bulletX- grenadeRotate.get_width()
                adjustedBulletY = bulletY- grenadeRotate.get_height()
                
                bulletWidth = grenade.get_width()
                bulletHeight = grenade.get_height()

            elif bulletType == "mine":# draw mine shot
                gameDisplay.blit(mine,(int(bulletX)- mine.get_width(), int(bulletY)-mine.get_height()))

                adjustedBulletX = bulletX- mine.get_width()
                adjustedBulletY = bulletY- mine.get_height()
                
                bulletWidth = mine.get_width()
                bulletHeight = mine.get_height()

            # collision dectection with the ground
            if bulletX >= 5 and adjustedBulletX >= 5:
                if bulletType == "shell":
                    if gameDisplay.get_at((int(bulletX)-5,int(bulletY)+5))[:-1] == brown:
                        pygame.draw.circle(gameDisplay,skyblue,(int(bulletX),int(bulletY)),redWeaponList["shell"][0])
                        #for all weapons adds cords of the impact to global list so every time it updates the screen the damage is redrawn
                        damageCords.append((int(bulletX),int(bulletY),redWeaponList["shell"][0]))
                        break
                elif bulletType == "missile":
                    if gameDisplay.get_at((int(adjustedBulletX),int(adjustedBulletY)))[:-1] == brown or gameDisplay.get_at((int(adjustedBulletX)+bulletWidth,int(adjustedBulletY)+bulletHeight))[:-1] == brown:
                        pygame.draw.circle(gameDisplay,skyblue,(int(bulletX),int(bulletY)),redWeaponList[bulletType][0])
                        damageCords.append((int(bulletX),int(bulletY),redWeaponList[bulletType][0]))
                        break
                elif bulletType == "grenade":#makes grenade keep spinning on the ground 
                    if gameDisplay.get_at((int(bulletX),int(bulletY)))[:-1] == brown:
                        while (grenadeCounter >= 0):
                            bulletX -= 0.4
                            # "gravity" for grenade so it drops if theres sky underneath
                            if gameDisplay.get_at((int(bulletX),int(bulletY)))[:-1] == skyblue:
                                bulletY += 0.4
                            drawScreen()
                            redTurXY = drawTank1(x1,y1,redTurPos)
                            blueTurXY = drawTank2(x2,y2,blueTurPos)
                            grenadeRotate = pygame.transform.rotate(grenade,-1*math.degrees(angle)*t)
                            gameDisplay.blit(grenadeRotate,(int(bulletX)- grenadeRotate.get_width(), int(bulletY)-grenadeRotate.get_height()))
                            pygame.display.update()
                            clock.tick(100)
                            grenadeCounter -= 1
                            t+=0.3
                            
                        pygame.draw.circle(gameDisplay,skyblue,(int(adjustedBulletX),int(adjustedBulletY)),redWeaponList[bulletType][0])
                        damageCords.append((int(bulletX),int(bulletY),redWeaponList[bulletType][0]))
                        break
                elif bulletType == "mine":
                    if gameDisplay.get_at((int(adjustedBulletX),int(adjustedBulletY)))[:-1] == brown or gameDisplay.get_at((int(adjustedBulletX)+bulletWidth,int(adjustedBulletY)+bulletHeight))[:-1] == brown:
                        pygame.draw.circle(gameDisplay,skyblue,(int(bulletX),int(bulletY)),redWeaponList[bulletType][0])
                        damageCords.append((int(bulletX),int(bulletY),redWeaponList[bulletType][0]))
                        break

            #checks bullet collision with enemy tank 
            if (collisonDetect(adjustedBulletX,adjustedBulletY,"blue",bulletType,bulletWidth,bulletHeight) == True):
                blueHPBarX -= redWeaponList[bulletType][1]# subtracts damage based on type of weapon from enemy 
                break
            

            bulletX = turCords[0] - vx*t # formula for the bullet's x direction 
            bulletY = turCords[1] - (vy*t - (9.81/2) * t**2)# formula for the bullet's y direction 
            t += 0.1#"time" add 0.1

            pygame.display.update()# updates screen
            clock.tick(100)
            
        if redWeaponList[bulletType][2] > 0:# if the ammo for the weapon selection is more than 0 subtact one per shot
            redWeaponList[bulletType][2] -= 1

        textbox("Blue's Turn",0,50,150,40,70,20)#displays blues turn
        pygame.display.update()
        turn = "blue"#changes the turn to blue
        pygame.time.wait(700)#waits 700 miliseconds to let user read whos turns
        
    elif tank == "blue":#same thing but for blue 
        missileAngle = math.degrees(angle)
        
        while blueWeaponList[bulletType][2] > 0 and bulletX <= maxx-5 and bulletY <= maxy:
            drawScreen()            
            redTurXY = drawTank1(x1,y1,redTurPos)
            blueTurXY = drawTank2(x2,y2,blueTurPos)

            #print ("Fired at",(bulletX,bulletY),angle, "Tur Pos: ", turCords)

            if bulletType == "shell":
                pygame.draw.circle(gameDisplay,blue,(int(bulletX),int(bulletY)),4)

                adjustedBulletX = bulletX
                adjustedBulletY = bulletY
                
                bulletWidth = 4
                bulletHeight = 4
                
               
            elif bulletType == "missile":
                
                blueAngledMissile = pygame.transform.rotate(blueMissile,missileAngle)
                gameDisplay.blit(blueAngledMissile,(int(bulletX), int(bulletY)-blueAngledMissile.get_height()))
                missileAngle -= 0.75
                
                adjustedBulletX = bulletX+ blueAngledMissile.get_width()
                adjustedBulletY = bulletY- blueAngledMissile.get_height()
                
                bulletWidth = blueAngledMissile.get_width()
                bulletHeight = blueAngledMissile.get_height()
                
            elif bulletType == "grenade":
                
                grenadeRotate = pygame.transform.rotate(grenade,-1*math.degrees(angle)*t)
                gameDisplay.blit(grenadeRotate,(int(bulletX), int(bulletY)-grenadeRotate.get_height()))
                
                adjustedBulletX = bulletX- grenadeRotate.get_width()
                adjustedBulletY = bulletY- grenadeRotate.get_height()
                
                bulletWidth = grenade.get_width()
                bulletHeight = grenade.get_height()

            elif bulletType == "mine":
                gameDisplay.blit(mine,(int(bulletX), int(bulletY)-mine.get_height()))

                adjustedBulletX = bulletX- mine.get_width()
                adjustedBulletY = bulletY- mine.get_height()
                
                bulletWidth = mine.get_width()
                bulletHeight = mine.get_height()

            if bulletX <= maxx-5 and adjustedBulletX <= maxx-5:    
                if bulletType == "shell":
                    if gameDisplay.get_at((int(bulletX)+5,int(bulletY)+5))[:-1] == brown:
                        pygame.draw.circle(gameDisplay,skyblue,(int(bulletX),int(bulletY)),blueWeaponList["shell"][0])
                        damageCords.append((int(bulletX),int(bulletY),blueWeaponList["shell"][0]))
                        break
                elif bulletType == "missile":
                    if gameDisplay.get_at((int(bulletX),int(bulletY)-blueAngledMissile.get_height()))[:-1] == brown:
                        pygame.draw.circle(gameDisplay,skyblue,(int(bulletX),int(bulletY)-blueAngledMissile.get_height()),blueWeaponList[bulletType][0])
                        damageCords.append((int(bulletX),int(bulletY)-blueAngledMissile.get_height(),blueWeaponList[bulletType][0]))
                        break
                elif bulletType == "grenade":
                    if gameDisplay.get_at((int(bulletX),int(bulletY)))[:-1] == brown:
                        while (grenadeCounter >= 0):
                            bulletX += 0.4
                            
                            if gameDisplay.get_at((int(bulletX),int(bulletY)))[:-1] == skyblue:
                                bulletY += 0.4
                                
                            drawScreen()
                            redTurXY = drawTank1(x1,y1,redTurPos)
                            blueTurXY = drawTank2(x2,y2,blueTurPos)
                            grenadeRotate = pygame.transform.rotate(grenade,-1*math.degrees(angle)*t)
                            gameDisplay.blit(grenadeRotate,(int(bulletX), int(bulletY)-grenadeRotate.get_height()))
                            pygame.display.update()
                            clock.tick(100)
                            grenadeCounter -= 1
                            t+=0.3
                            
                        pygame.draw.circle(gameDisplay,skyblue,(int(adjustedBulletX),int(adjustedBulletY)),blueWeaponList[bulletType][0])
                        damageCords.append((int(bulletX),int(bulletY),blueWeaponList[bulletType][0]))
                        break
                elif bulletType == "mine":
                    if gameDisplay.get_at((int(adjustedBulletX),int(adjustedBulletY)))[:-1] == brown or gameDisplay.get_at((int(adjustedBulletX)+bulletWidth,int(adjustedBulletY)+bulletHeight))[:-1] == brown:
                        pygame.draw.circle(gameDisplay,skyblue,(int(bulletX),int(bulletY)),blueWeaponList[bulletType][0])
                        damageCords.append((int(bulletX),int(bulletY),blueWeaponList[bulletType][0]))
                        break  
            
            if (collisonDetect(adjustedBulletX,adjustedBulletY,"red",bulletType,bulletWidth,bulletHeight) == True):
                redHPBarX -= blueWeaponList[bulletType][1]
                break
            
            
            bulletX = turCords[0] + vx*t
            bulletY = turCords[1] - (vy*t - (9.81/2) * t**2)
            t += 0.1

            pygame.display.update()
            clock.tick(100)
            
        if blueWeaponList[bulletType][2] > 0:
            blueWeaponList[bulletType][2] -= 1

        textbox("Red's Turn",maxx-150,50,150,40,70,20)
        pygame.display.update()
        turn = "red"
        pygame.time.wait(700)
     
def textObjects(text,font):#returns the rendered font and rectangle around it
     textSurface = font.render(text,True,black)
     return textSurface, textSurface.get_rect()
    
def textbox(text,x,y,width,height,textY,textSize):# main function to display text
    
    textFont = pygame.font.Font("freesansbold.ttf",textSize)#creates text font
    
    textSurf1, textRect1 = textObjects(text,textFont)#creates text surface and rectangle
    textRect1.center = ((x + width/2),textY)#sets the center of the text
    
    gameDisplay.blit(textSurf1,textRect1)#displays text
    
def redButton(text,x,y,width,height,colour,textY,textSize):# same as text box but checks clickability for weapon selection on the red side and changes to the weapon clicked
    global redWeaponSelection
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        if click[0] == 1:
            for weapon in redWeaponList:
                if weapon == text[:-1].lower():
                    redWeaponSelection = weapon
                    
    pygame.draw.rect(gameDisplay, colour, (x,y,width,height))
    
    textFont = pygame.font.Font("freesansbold.ttf",textSize)
    
    textSurf1, textRect1 = textObjects(text,textFont)
    textRect1.center = ((x + width/2),textY)
    
    gameDisplay.blit(textSurf1,textRect1)
    
def blueButton(text,x,y,width,height,colour,textY,textSize):
    global blueWeaponSelection
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        if click[0] == 1:
            for weapon in blueWeaponList:
                if weapon == text[:-1].lower():
                    blueWeaponSelection = weapon
                    
    pygame.draw.rect(gameDisplay, colour, (x,y,width,height))
    
    textFont = pygame.font.Font("freesansbold.ttf",textSize)
    
    textSurf1, textRect1 = textObjects(text,textFont)
    textRect1.center = ((x + width/2),textY)
    
    gameDisplay.blit(textSurf1,textRect1)
    
def drawWeaponButtons():#self explanatory
    
    redButton("Shell:",maxx-40,5,35,40,white,15,12)
    textbox(str(redWeaponList["shell"][2]),maxx-40,30,35,15,35,12)
    
    redButton("Missile:",maxx-80,5,35,40,white,15,8)
    textbox(str(redWeaponList["missile"][2]),maxx-80,30,35,15,35,12)
    
    redButton("Grenade:",maxx-120,5,35,40,white,15,7)
    textbox(str(redWeaponList["grenade"][2]),maxx-120,30,35,15,35,12)
    
    redButton("Mine:",maxx-160,5,35,40,white,15,12)
    textbox(str(redWeaponList["mine"][2]),maxx-160,30,35,15,35,12)
    
    blueButton("Shell:",5,5,35,40,white,15,12)
    textbox(str(blueWeaponList["shell"][2]),5,30,35,15,35,12)
    
    blueButton("Missile:",45,5,35,40,white,15,8)
    textbox(str(blueWeaponList["missile"][2]),45,30,35,15,35,12)
    
    blueButton("Grenade:",85,5,35,40,white,15,7)
    textbox(str(blueWeaponList["grenade"][2]),85,30,35,15,35,12)
    
    blueButton("Mine:",125,5,35,40,white,15,12)
    textbox(str(blueWeaponList["mine"][2]),125,30,35,15,35,12)
    
def drawBars():#self explanatory
    #hp bars
    pygame.draw.rect(gameDisplay,red,(maxx/2 + 50,15,redHPBarX,10))
    pygame.draw.rect(gameDisplay,blue,(maxx/2 - 230,15,blueHPBarX,10))
    
    #weapon power bars
    pygame.draw.rect(gameDisplay,green,(maxx-100,maxy - 30,redPowerPercent*80,10))
    pygame.draw.rect(gameDisplay,green,(20,maxy- 30,bluePowerPercent*80,10))
    
def drawBackground():#self explanatory

    gameDisplay.fill(skyblue)
    pygame.draw.rect(gameDisplay, black, (0,0,maxx,50))
    pygame.draw.rect(gameDisplay,brown,(0,maxy/2 + redTank.get_height(),maxx,maxy))

    if len(damageCords) != 0:#after the first time damge is done to the terrian 
        for cord in damageCords:
            pygame.draw.circle(gameDisplay,skyblue,(cord[0],cord[1]),cord[2])
            
def drawScreen():#self explanatory
    drawBackground()
    drawWeaponButtons()
    drawBars()
    
def score(): # This function displays the score texts on the game screen
  #Global Variables
  global redScore
  global blueScore
  #Draw Text
  redScorefont = pygame.font.Font(None,25)
  redScorefont2 = redScorefont.render(str(redScore),True,red,None)
  redScorefont3 = redScorefont2.get_rect()
  redScorefont3.center = (480,37)

  blueScorefont = pygame.font.Font(None,25)
  blueScorefont2 = blueScorefont.render(str(blueScore),True,blue,None)
  blueScorefont3 = blueScorefont2.get_rect()
  blueScorefont3.center = (320,37)

  Scorefont = pygame.font.Font(None,25)
  Scorefont2 = Scorefont.render("Score",True,white,None)
  Scorefont3 = Scorefont2.get_rect()
  Scorefont3.center = (400,38)

  hpfont = pygame.font.Font(None,25)
  hpfont2 = hpfont.render("Health",True,white,None)
  hpfont3 = hpfont2.get_rect()
  hpfont3.center = (400,20)

  gameDisplay.blit(redScorefont2,redScorefont3)
  gameDisplay.blit(blueScorefont2,blueScorefont3)
  gameDisplay.blit(Scorefont2,Scorefont3)
  gameDisplay.blit(hpfont2,hpfont3)

  #Score decreases by 1. This function is constantly running, always updating the score as the game goes on until someone wins.
  blueScore -= 1 
  redScore -= 1

def mainpage():##Main page
  # Adding global variables
  global counter
  global Main 
  #Getting Mouse coordinates and checking if pressed
  pointer = pygame.mouse.get_pos()
  pointerclick = pygame.mouse.get_pressed()
  gameDisplay.blit(mainphoto,(0,0))#Background image

  #Tank Text
  tankfont = pygame.font.Font(None,100)
  tankfont2 = tankfont.render("Tanks",True,white,None)
  tankfont3 = tankfont2.get_rect()
  tankfont3.center = (400,125)
  #Play text
  playfont = pygame.font.Font(None,100)
  playfont2 = playfont.render("Play",True,blue,None)
  playfont3 = playfont2.get_rect()
  playfont3.center = (400,300)
  #instructions text
  instrutionsfont = pygame.font.Font(None,100)
  instrutionsfont2 = instrutionsfont.render("Instructions",True,red,None)
  instrutionsfont3 = instrutionsfont2.get_rect()
  instrutionsfont3.center = (400,425)
  ##text squares 
  pygame.draw.rect(gameDisplay,black,(200,75,400,100))
  pygame.draw.rect(gameDisplay,red,(250,250,300,100))
  pygame.draw.rect(gameDisplay,blue,(180,375,440,100))
  ##Initilizing Text
  gameDisplay.blit(tankfont2,tankfont3)
  gameDisplay.blit(playfont2,playfont3)
  gameDisplay.blit(instrutionsfont2,instrutionsfont3)

  ## Clicking buttons to change into other screens
  if pointer[0] >= 250 and pointer[0] <= 550 and pointer[1]>= 250 and pointer[1] <= 350 and pointerclick[0] == 1:
    start()
    Main = True ## if pressed in these areas (Play button), STARTS the game. 
  if pointer[0] >= 180 and pointer[0] <= 620 and pointer[1]>= 375 and pointer[1] <= 475 and pointerclick[0] == 1:
    counter = 1 # If pressed in these areas (Instrutions), puts you into instructions page

def instructions101():#instructions window for players
  #Importing global variables
  global counter
  # Text boxes
  x = "Hello! Welcome to the game of Tanks."
  textfont = pygame.font.Font(None, 60)
  textfont2 = textfont.render(x, True, blue, None)
  textfont3 = textfont2.get_rect()
  textfont3.center = (400, 80)

  backfont = pygame.font.Font(None,25)
  backfont2 = backfont.render("Main Menu",True,black,None)
  backfont3 = backfont2.get_rect()
  backfont3.center = (100,30)

  gameDisplay.blit(textfont2, textfont3)
  gameDisplay.blit(backfont2,backfont3)
  gameDisplay.blit(backarrow,(10,10))
  gameDisplay.blit(how,(40,110))

  # If pressed in these areas, Go back to the original mainscreen
  if pointer[0] >= 0 and pointer[0] <= 50 and pointer[1]>= 0 and pointer[1] <= 50 and pointerclick[0] == 1:
    counter = 0

def gameOver():
  # globa variables
  global counter 
  global Main
  global text
  global redScore
  global blueScore
  global newname
  global winner 
  global writename 
  global text
  global winnerlist
  global newscore
  # Clock and colour
  clock = pygame.time.Clock()
  color = pygame.Color('dodgerblue2')
  # Get mouse coordinates and check if pressured
  pointer = pygame.mouse.get_pos()
  pointerclick = pygame.mouse.get_pressed()
  #text
  gameOverfont = pygame.font.Font(None,100)
  gameOverfont2 = gameOverfont.render("Game Over!",True,red,None)
  gameOverfont3 = gameOverfont2.get_rect()
  gameOverfont3.center = (350,100)

  quitfont = pygame.font.Font(None,60)
  quitfont2 = quitfont.render("Quit",True,red,None)
  quitfont3 = quitfont2.get_rect()
  quitfont3.center = (600,425)
  
  playagainfont = pygame.font.Font(None,60)
  playagainfont2 = playagainfont.render("Play again!",True,blue,None)
  playagainfont3 = playagainfont2.get_rect()
  playagainfont3.center = (600,280)

  backfont = pygame.font.Font(None,25)
  backfont2 = backfont.render("Main Menu",True,blue,None)
  backfont3 = backfont2.get_rect()
  backfont3.center = (100,30)

  highscorefont = pygame.font.Font(None,60)
  highscorefont2 = highscorefont.render("Top 5 Highscores",True,blue,None)
  highscorefont3 = highscorefont2.get_rect()
  highscorefont3.center = (200,250)

  winnerfont = pygame.font.Font(None,60)
  winnerfont2 = winnerfont.render("Winner",True,blue,None)
  winnerfont3 = winnerfont2.get_rect()
  winnerfont3.center = (680,80)

  #If write name is 0, You are able to input text onto the game screen. When pressed Enter. Your name goes up on scoreboard IF your score is highenough and You can no longer input data.
  if writename == 0:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          writename = 1 
          gameDisplay.fill(white)
        elif event.key == pygame.K_BACKSPACE:
          text = text[:-1]
          gameDisplay.fill(white)
        else:
          text += event.unicode

  # Text box
  font = pygame.font.Font(None, 32)
  txt_surface = font.render(text, True, color)
  gameDisplay.blit(txt_surface, (220, 488))

  # Update the Highscore list
  if winner == 1 :
    newscore = redScore
    gameDisplay.blit(blueTank, (650, 100))
  elif winner == 2 :
    newscore = blueScore
    gameDisplay.blit(redTank, (650, 100))
  if writename == 1:
    newname = text
    updateHighscore(newscore,newname)
    pygame.time.wait(10)
    writename = 2

  # Text for the highscore
  HIGHSCORE1 = pygame.font.Font(None,30)
  HIGHSCORE12 = HIGHSCORE1.render((str(winnerlist[0][0]) + "  " + winnerlist[0][1]),True,red,None)
  HIGHSCORE13 = HIGHSCORE12.get_rect()
  HIGHSCORE13.center = (200,300)
  gameDisplay.blit(HIGHSCORE12,HIGHSCORE13)

  HIGHSCORE2 = pygame.font.Font(None,30)
  HIGHSCORE22 = HIGHSCORE2.render((str(winnerlist[1][0]) + "  " + winnerlist[1][1]),True,red,None)
  HIGHSCORE23 = HIGHSCORE22.get_rect()
  HIGHSCORE23.center = (200,325)
  gameDisplay.blit(HIGHSCORE22,HIGHSCORE23)

  HIGHSCORE3 = pygame.font.Font(None,30)
  HIGHSCORE32 = HIGHSCORE3.render((str(winnerlist[2][0]) + "  " + winnerlist[2][1]),True,red,None)
  HIGHSCORE33 = HIGHSCORE32.get_rect()
  HIGHSCORE33.center = (200,350)
  gameDisplay.blit(HIGHSCORE32,HIGHSCORE33)

  HIGHSCORE4 = pygame.font.Font(None,30)
  HIGHSCORE42 = HIGHSCORE4.render((str(winnerlist[3][0]) + "  " + winnerlist[3][1]),True,red,None)
  HIGHSCORE43 = HIGHSCORE42.get_rect()
  HIGHSCORE43.center = (200,375)
  gameDisplay.blit(HIGHSCORE42,HIGHSCORE43)

  HIGHSCORE5 = pygame.font.Font(None,30)
  HIGHSCORE52 = HIGHSCORE5.render((str(winnerlist[4][0]) + "  " + winnerlist[4][1]),True,red,None)
  HIGHSCORE53 = HIGHSCORE52.get_rect()
  HIGHSCORE53.center = (200,400)
  gameDisplay.blit(HIGHSCORE52,HIGHSCORE53)

  pokemonfont = pygame.font.Font(None,30)
  pokemonfont2 = pokemonfont.render("Enter your initals:",True,red,None)
  pokemonfont3 = pokemonfont2.get_rect()
  pokemonfont3.center = (120,500)
  gameDisplay.blit(pokemonfont2,pokemonfont3)

    # int text
  gameDisplay.blit(winnerfont2,winnerfont3)
  gameDisplay.blit(gameOverfont2,gameOverfont3) 
  gameDisplay.blit(quitfont2,quitfont3)
  gameDisplay.blit(playagainfont2,playagainfont3)
  gameDisplay.blit(backfont2,backfont3)
  gameDisplay.blit(backarrow,(10,10))
  gameDisplay.blit(highscorefont2,highscorefont3)
  #clicky clicky
  if pointer[0] >= 0 and pointer[0] <= 50 and pointer[1]>= 0 and pointer[1] <= 50 and pointerclick[0] == 1:
    counter = 0 ## if clicked, go to mainscreen
  if pointer[0] >= 325 and pointer[0] <= 480 and pointer[1]>= 390 and pointer[1] <= 450 and pointerclick[0] == 1:
    pygame.quit() # if clicked, quit window/program
  # play again  
  if pointer[0] >= 200 and pointer[0] <= 590 and pointer[1]>= 250 and pointer[1] <= 300 and pointerclick[0] == 1:
    start();
    Main = True # if clicked, replay the game 

def updateHighscore(updatescore,newname2): ## Returns the list of highscore.txt
  global winnerlist# global variable
  z = list() # New list
  biglist = list() # new list
  topscore = 0 # new score 
  name = "" # name
  # opens text file in append mode
  f = open("Highscore.txt","a+")
  # Add a line of text. new score and new name
  f.write(str(updatescore)+", "+ newname2 +"\n")
  f.close()

  # Opens text file in read mode
  f = open("Highscore.txt","r")
  for i in (f):
    x = "".join(i) # joins the letters of each line to form a single string
    x = x[:len(x)-1] # Remove the ending. Which is a tab aka "\n"
    z.append(x) # Add this single string to the Z list
  f.close()
  # Add all the names on the textfile in the Z list

  for a in range(6):   # Seperate the top 6 scores & names and sort them into another list, biglist. 
    for b in range(len(z[a])):
      if z[a][b] == ",": # All the letters behind the comma becomes a seperate int, which is the highscore for "a"
        topscore = (int(z[a][:b]))
      if z[a][b] == " ": # All the letters after the space is recorded as a string, the name of the player with the high score
        name = ((z[a][b+1:]))
    # Make the score and string a tuple and imports the tuple into a list called biglist
    faker = (topscore,name)
    biglist.append(faker)
  
  # Sort the biglist list from highest to lowest score
  biglist = sorted(biglist,reverse=True)

  # Open the text file in write mode.
  f = open("Highscore.txt","w+")

  for i in range(5):
    f.write(str(biglist[i][0])+", "+ biglist[i][1] +"\n")
  f.close()
  #rewrite all the names with the 5 high scores. If your new score was one of the highest, it goes on the scoreboard otherwise it is not counted and gone.
  winnerlist = biglist
  # Makes the global winnerlist the same as biglist. 

#variables & main code
counter = 0
run = True
Main = False 
updateHighscore(0,"") # Required for the updatehighscore code.

#variables & main code
counter = 0
run = True
Main = False 

while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
  pygame.event.get()

  pointer = pygame.mouse.get_pos() # tuple[] --> 0=x,1=y
  pointerclick = pygame.mouse.get_pressed()# tuple and, left middle and right click.

  # When the screen changes, the screen clears and puts new items
  if newscreen == 1 :
    gameDisplay.fill(white)
    newscreen = 0 

  if counter == 0: # if counter= 0 you see the mainpage
    newscreen = 1
    mainpage()
  if counter == 1: # if counter = 1 you see the instructions
    newscreen = 1 
    instructions101()
  if counter == 2: # if the counter = 2 you see the game over screen
    newscreen = 1
    gameOver()

  while Main: # Game Running Window
      
      #midline
      #pygame.draw.line(gameDisplay,black,(maxx/2,maxy),(maxx/2,0))
      
    drawScreen()
    
    redTurXY = drawTank1(x1,y1,redTurPos)
    blueTurXY = drawTank2(x2,y2,blueTurPos)

    if redHPBarX <= 0: # When the red tank dies
        Main = False # Stops the game while loop
        winner = 1 # 1 means The blue tank is the winner
        counter = 2 # This tells opens the gameover screen. Look at line 892
        break # Breaks the while loop
    if blueHPBarX <= 0:# When the blue tank dies
        Main = False # Stops the game while loop
        winner = 2 # 2 means The red tank is the winner
        counter = 2# This tells opens the gameover screen. Look at linke 892
        break # Breaks the while loop

    #checks if tanks is offscreen and reloads ammo but takes hp 
    if x2 < 0 :
      blueWeaponList["shell"][2] += 1
      blueWeaponList["missile"][2] += 1
      blueWeaponList["grenade"][2] += 1
      blueWeaponList["mine"][2] += 1
      blueHPBarX -= 2
    if x1 + redTank.get_width() > 800 :
      redWeaponList["shell"][2] += 1
      redWeaponList["missile"][2] += 1
      redWeaponList["grenade"][2] += 1
      redWeaponList["mine"][2] += 1
      redHPBarX -= 2
      
    # print (blueTurXY)
    for event in pygame.event.get():

      #checks if any of the keys pressed are buttons that do something 
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
              #checks if you are in a hole and are trying to move when on screen 
                if x1 + redTank.get_width() < maxx-10:
                  
                  if gameDisplay.get_at((int(x1) -10 ,int(y1 + redTank.get_height())-2)) == brown:
                      y1 -= 10
                      dx1 = -2
                  elif gameDisplay.get_at((int(x1) -1 ,int(y1 + redTank.get_height())-2)) == skyblue:
                      dx1 = -3
                else:
                  dx1 = -3
                    
            if event.key == pygame.K_RIGHT:
                if x1 + redTank.get_width() < maxx-10:
                    if gameDisplay.get_at((int(x1+ redTank.get_width()) + 10 ,int(y1 + redTank.get_height())-2)) == brown:
                        y1 -= 10
                        dx1 = 2
                    elif gameDisplay.get_at((int(x1 + redTank.get_width())+1,int(y1 + redTank.get_height())-2)) == skyblue:
                        dx1 = 3
                else:
                    dx1 = 3

            if event.key == pygame.K_UP:
                if redTurPos < 8:
                    redTurPos +=1
            if event.key == pygame.K_DOWN:
                if redTurPos > 0:
                    redTurPos -=1
            if event.key == pygame.K_RIGHTBRACKET:#changes power 
                if redPowerPercent < 1:
                    redPowerPercentChange = 0.02

            if event.key == pygame.K_LEFTBRACKET:
                if redPowerPercent > 0.02:
                    redPowerPercentChange = -0.02
            
            if event.key == pygame.K_SPACE and turn == "red":#fires turrent 
                fireTurret("red",redWeaponSelection,redTurXY,redPowerPercent)
                
                
                    
            if event.key == pygame.K_a:#same as above for blue tank
                if x2 > 10:
                    if gameDisplay.get_at((int(x2) -10 ,int(y2 + blueTank.get_height())-2)) == brown:
                        y2 -= 10
                        dx2 = -2
                    elif gameDisplay.get_at((int(x2) -1 ,int(y2 + blueTank.get_height())-2)) == skyblue:
                        dx2 = -3
                else:
                    dx2 = -3
            if event.key == pygame.K_d:
                if x2 > 10:
                    if gameDisplay.get_at((int(x2+ blueTank.get_width()) + 10 ,int(y2 + blueTank.get_height())-2)) == brown:
                      y2 -= 10
                      dx2 = 2
                    elif gameDisplay.get_at((int(x2 + blueTank.get_width())+1,int(y2 + blueTank.get_height())-2)) == skyblue:
                      dx2 = 3
                else:
                      dx2 = 3

            if event.key == pygame.K_w:
                if blueTurPos < 8:
                    blueTurPos += 1
            if event.key == pygame.K_s:
                if blueTurPos > 0:
                    blueTurPos -= 1

            if event.key == pygame.K_j:
                if bluePowerPercent < 1:
                    bluePowerPercentChange = 0.02

            if event.key == pygame.K_h:
                if bluePowerPercent > 0.02:
                    bluePowerPercentChange = -0.02
            
            if event.key == pygame.K_f and turn == "blue":
                fireTurret("blue",blueWeaponSelection,blueTurXY,bluePowerPercent)

            
            if event.key == pygame.K_ESCAPE:#escapes when press esc button
                pygame.quit()
                quit()
                
        if event.type == pygame.KEYUP:# if these keps go up stop moving stuff
            keysList = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d, pygame.K_UP, pygame.K_DOWN,pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_j, pygame.K_h]
            for key in keysList:
                if event.key == key:
                    dx1 = 0
                    dx2 = 0
                    redPowerPercentChange = 0
                    bluePowerPercentChange = 0 
 
    #restricts tank movement to half the screen         
    if x1 < maxx/2:
        dx1 = 0
        x1 = maxx/2
    if x2 > maxx/2-blueTank.get_width():
        dx2 = 0
        x2 = maxx/2-blueTank.get_width()
        
    #doesnt let the power for each to go into negatives or above 1
    if redPowerPercent < 0.02:
        redPowerPercent = 0.02
    elif redPowerPercent > 1:
        redPowerPercent = 1

    if bluePowerPercent < 0.02:
        bluePowerPercent = 0.02
    elif bluePowerPercent > 1:
        bluePowerPercent = 1

    if x1 + redTank.get_width() < maxx-10: #checks if tank is onscreen and stops it from going into the ground if its in a hole

        if gameDisplay.get_at((int(x1) -1 ,int(y1 + redTank.get_height())-2)) == brown:
            dx1 = 0
            x1 +=1

        if gameDisplay.get_at((int(x1 + redTank.get_width())+1,int(y1 + redTank.get_height())-2)) == brown:
            dx1 = 0
            x1 -= 1

        if gameDisplay.get_at((int(x1)-2,int(y1 + redTank.get_height()))) == skyblue and gameDisplay.get_at((int(x1 + redTank.get_width())+2,int(y1 + redTank.get_height()))) == skyblue:
            y1+= 2
    if x2 > 10:
        if gameDisplay.get_at((int(x2) -1 ,int(y2 + blueTank.get_height())-2)) == brown:
            dx2 = 0
            x2 +=1
        if gameDisplay.get_at((int(x2 + blueTank.get_width())+1,int(y2 + blueTank.get_height())-2)) == brown:
            dx2 = 0
            x2 -= 1

        if gameDisplay.get_at((int(x2)-2,int(y2 + blueTank.get_height()))) == skyblue and gameDisplay.get_at((int(x2 + blueTank.get_width())+2,int(y2 + blueTank.get_height()))) == skyblue:
            y2+= 2
            


    #adds the change in values to the actual value
    x1 += dx1
    x2 += dx2
    redPowerPercent += redPowerPercentChange
    bluePowerPercent += bluePowerPercentChange


    score()                      
    pygame.display.update()
    clock.tick(60)
      
  pygame.display.update()  
