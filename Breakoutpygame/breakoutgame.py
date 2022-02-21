# Evan Dartt
# C200 Final Project

import math
import pygame
import random
import time

pygame.init
pygame.font.init()

screen = pygame.display.set_mode([800,600])            # Setting the size of the game-box
pygame.display.set_caption('Team 23 - Breakout')       # Setting the name of the game
pygame.mouse.set_visible(0)                            # Making the mouse invisible so the player does not see it
font = pygame.font.Font(None, 48)                      # Setting the font that is used for the score and the Game Over text
gameBackground = pygame.Surface(screen.get_size())     # Setting the game background to allow text on it

# ==================================================================================================

# Colors for the ball/player, background, and bricks (Using RGB color codes)

blue = (0, 0, 255)           # ball
black = (0, 0, 0)            # background
red = (255, 0, 0)            # bricks
white = (255, 255, 255)      # bar

# ==================================================================================================

# Setting the size of the bricks (height and width)

brickWidth = 60
brickHeight = 30

# ==================================================================================================
score = 0
score = score + 1

# Making the Ball class

class Ball(pygame.sprite.Sprite):

    # Set position for ball 
    x = 500.0
    y = 500.0

    # Set direction for ball
    direction = 350

    width = 10
    height = 10

    # Set speed for ball
    speed = 10 #this var needs to change 

    # Need to pass in the color of the ball and its position
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([self.width, self.height])                      # Creates the pixel image that represents the ball
        self.image.fill((blue))                                                     # Sets the color for the ball
        self.rect = self.image.get_rect()                                           # Gets the rectangular area of the surface
        self.gameScreenWidth = pygame.display.get_surface().get_width()             # Gets the width of the game screen
        self.gameScreenHeight = pygame.display.get_surface().get_height()           # Gets the height of the game screen

    def bounceHorizontal(self, difference):                                         # Function that makes the ball bounce off of horizontal surfaces
        self.direction = (180 - self.direction) % 360
        self.direction += difference

    def refreshBallLocation(self):                                                  # Function that updates the location of the ball
        directionRadians = math.radians(self.direction)
        self.x += self.speed * math.sin(directionRadians)
        self.y -= self.speed * math.cos(directionRadians)

        # Setting the rect to match our X and Y locations
        self.rect.x = self.x
        self.rect.y = self.y

        # Detection for when the ball hits the top of the screen
        if self.y <= 0:
            return 3
            
     
        # Detection for when the ball hits either side wall, resulting in change of direction
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        if self.x > self.gameScreenWidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.gameScreenWidth - self.width - 1

            # Detection for if the ball is missed by the player and hits the bottom of the screen
        if self.y > 600:
            return True
        else:
            return False

    # Allows each function to be easily called when new level begins
    @classmethod
    def updateBallSpeed(self, speed):
        self.speed = speed

    def resetBallPos(self):
        self.x = 500.0
        self.y = 500.0

    def resetBallDir(self):
        self.direction = 350

    

# ==================================================================================================

# Making the Bar class

class Bar(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

        #Setting the parameters for the bar that the player controls, including the size and color
        self.width = 80
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))
        self.rect = self.image.get_rect()
        self.gameScreenWidth = pygame.display.get_surface().get_width()
        self.gameScreenHeight = pygame.display.get_surface().get_height()
        self.rect.x = 0
        self.rect.y = self.gameScreenHeight - self.height

    def refreshBarLocation(self):                                                   # Function that updates the location of the bar                                                          
        # Use the mouse as the location  for the bar
        barPosition = pygame.mouse.get_pos()
        self.rect.x = barPosition[0]

        # Lock the barPosition into the screen window
        if self.gameScreenWidth - self.width < self.rect.x:
            self.rect.x = self.gameScreenWidth - self.width

    def resetBarPos(self):
        self.x = 250.0

        
# ==================================================================================================

# Making the Brick class

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        # The bricks need size, color, and position

        super().__init__()

        self.image = pygame.Surface([brickWidth, brickHeight])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# ==================================================================================================

# Creating groups for all the sprites 

gameBricks = pygame.sprite.Group()
gameBall = pygame.sprite.Group()
allGameSprites = pygame.sprite.Group()

# ===================================================================================================

# Setting parameters for the bricks
top = 20
numberOfBricks = 32
#this code generates blocks 
def brickGen(top, numberOfBricks):
    global gameBricks
    global allGameSprites

    for row in range(5):
        for column in range(0, numberOfBricks):
            brick = Brick(red, column * (brickWidth + 2) + 1, top)
            gameBricks.add(brick)
            allGameSprites.add(brick)
        top += brickHeight + 2
    return brick

brick = brickGen(top, numberOfBricks)

# Creating the player/bar, and ball

player = Bar()
allGameSprites.add(player)

ball = Ball()
allGameSprites.add(ball)
gameBall.add(ball)

# Check the state of the game
gameOver = False
exitGame = False

#====================================================================================================================
# Limit clock  speed
clock = pygame.time.Clock()

counter, text = 0, "0".rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont(None, 30)

# ==================================================================================================
#Creating levels

def lvl():
    return False

def newLevel():
    #generate new bricks
    brick = brickGen(top, numberOfBricks)
    ball.resetBallPos() #reset ball pos
    player.resetBarPos() #reset bar pos
    ball.updateBallSpeed(ball.speed + 3) #update ball speed + x to make each level harder


# ==================================================================================================

# While Loop that runs the Breakout game

score = 0 # was setting the score back to 0 each loop
nxtLvl = False
currentLevel = 1
pause = False
lives = 5

startTime = time.time()

while not exitGame:
    clock.tick(30)
    screen.fill(black)

    currentTime = int(time.time() - startTime)
    timeDisplay = font.render(str(currentTime) + " seconds ", 1, white)
    timeLoc = (10, 525)
    screen.blit(timeDisplay, timeLoc)

    ringOfLife = lives - 1
    lifeDisplay = font.render(str(ringOfLife) + " lives ", 1, white)
    lifeLoc = (697, 525)
    screen.blit(lifeDisplay, lifeLoc)

    myfont = pygame.font.SysFont(None, 15)
    label = myfont.render("click mouse to pause/unpause", 1, white)
    labelLoc = (350, 10)
    screen.blit(label, labelLoc)

  
    

    if pause == True:
        pauseDisplay = font.render(str("Click to unpause"), 0, white)
        textPause = (400, 250)
        screen.blit(pauseDisplay, textPause)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame = True
        if event.type == pygame.MOUSEBUTTONDOWN:
           if pause == False:
               pause = True
           else:
               pause = False

    if pause:
        continue

    if not gameOver:
        player.refreshBarLocation()
        gameOver = ball.refreshBallLocation()
        if gameOver == 3:
            nxtLvl = True
            gameOver = False
            pause = True

    if nxtLvl:
        newLevel()
        currentLevel = currentLevel + 1
        nxtLvl = False     

    if gameOver:
        if lives > 1:
            gameOver = False
            lives = lives - 1
            ball.resetBallPos() #reset ball pos
            ball.resetBallDir() #reset ball dir
            player.resetBarPos() #reset bar pos

            pause = True
            continue
        text = font.render("The Game is Over", True, white)
        textPosition = text.get_rect(centerx=gameBackground.get_width()/2)
        textPosition.top = 300
        screen.blit(text, textPosition)                                             # Allow the text to be drawn onto the screen

     # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player, gameBall, False):

        difference = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
 
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounceHorizontal(difference)

    deleteTheBrick = pygame.sprite.spritecollide(ball, gameBricks, True)

    if len(deleteTheBrick) > 0:
        score = score + currentLevel
        ball.bounceHorizontal(0)

     # The objective is not to delete all bricks, but to hit the ceiling and advance to next level

    # Making a score system
     
    for brick in gameBricks:
        if brick.rect.colliderect(ball.rect):
            deleteTheBrick(brick)
            speed = -speed
            scoreDisplay = font.render(str(score), 1, white)
            textScore = (5,10)
            screen.blit(scoreDisplay, textScore)
    width, height = pygame.display.get_surface().get_size()
    scoreText = font.render(str(score) + " brix ", False, (255, 255, 255))
    screen.blit(scoreText, (width - 100, height - 50))

    #Display level
    currentLevelText = "Level: " + str(currentLevel)
    levelDisplay = font.render(str(currentLevelText), 1, white)
    textLevel = (25, 550)
    screen.blit(levelDisplay, textLevel)

    allGameSprites.draw(screen)
    pygame.display.flip()


# ========================================================================================================

# highscores

def get_highscore():
    scoreFile = open("highscores.txt", "r")
    highscore = scoreFile.read()
    scoreFile.close()
    print (highscore)
    return highscore

def save_highscores(new_highscores):
    text_file = open("highscores.txt", "w")
    text_file.write(str(new_highscores))
    text_file.close()

def main():
    highscore = get_highscore()
    current_score = score
    if current_score > highscore:
        save_highscores(current_score)
        print ("You beat the old highscore: " + str(highscore) + " by scoring " + str(score))
    else:
        print("Your score " + str(score) + " didn't beat the high score " + str(highscore))


# =======================================================================================================================
