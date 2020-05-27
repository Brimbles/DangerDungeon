import sys
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
screenwidth, screenheight = 512 , 512
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Danger Dungeon")

clock = pygame.time.Clock()

########## Images ##########
bg = pygame.image.load('assets/bluedungeonbg256px.png')
bg = pygame.transform.scale(bg, (512, 512))
bottomborder = 36 #the number of pixels which is a "Border" at the bottom of the background image
sideborder = 3
char = pygame.image.load('assets/standl.png')
walkRightUnscaled = [pygame.image.load('assets/walkr1.png'), pygame.image.load('assets/walkr2.png'), pygame.image.load('assets/walkr3.png'), pygame.image.load('assets/walkr4.png')]
walkLeftUnscaled = [pygame.image.load('assets/walkl1.png'), pygame.image.load('assets/walkl2.png'), pygame.image.load('assets/walkl3.png'), pygame.image.load('assets/walkl4.png')]
walkRight = []
walkLeft = []

### Scale the images at runtime ###
for img in walkRightUnscaled:
  walkRight.append(pygame.transform.scale(img, (64, 64)))
for img in walkLeftUnscaled:
  walkLeft.append(pygame.transform.scale(img, (64, 64)))

########## Drawing logic lives here, to keep it out of the main function ##########
def redrawGameWindow():
    screen.blit(bg, (0,0)) #background image, tuple is the position (0,0)
    man.draw(screen)
    # for bullet in bullets:
    #     bullet.draw(win)
    pygame.display.update()


########## Variables for game ##########
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        
    
    def draw(self, screen):
        if self.walkCount + 1 >= 12: #there are only 4 images, we want to display each for 3 frames, so we'll get an index error if we go over 12
            self.walkCount = 0
        if not(self.standing): #if we're not standing still
            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x,self.y)) #// means integer division, excludes all the decimals. eg 4//3 = 1. 
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:#standing still
            if self.right: #if last facing position was right, return the 1st image from the right images
                screen.blit(walkRight[0], (self.x,self.y)) 
            else: #return first image from the left images
                screen.blit(walkLeft[0], (self.x,self.y)) 
# def draw(self, screen):
#         if self.walkCount + 1 >= 12: #there are only 4 images, we want to display each for 3 frames, so we'll get an index error if we go over 12
#             self.walkCount = 0
#         if not(self.standing): #if we're not standing still
#             if self.left:
#                 screen.blit(walkLeft[self.walkCount//3], (self.x,self.y)) #// means integer division, excludes all the decimals. eg 4//3 = 1. 
#                 self.walkCount += 1
#             elif self.right:
#                 screen.blit(walkRight[self.walkCount//3], (self.x,self.y))
#                 self.walkCount +=1
#         else:#standing still
#             if self.right: #if last facing position was right, return the 1st image from the right images
#                 screen.blit(walkRight[0], (self.x,self.y)) 
#             else: #return first image from the left images
#                 screen.blit(walkLeft[0], (self.x,self.y)) 
class projectile(object):
    def __init__(self,x,y,radius,colour,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 8 * facing
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

########## Game loop ########## 
man = Player(300,415,64,64)
bullets = [] 
run = True
while run:



    # screen.fill((0, 0, 0))

    #pygame.time.delay(50)
    clock.tick(27)

    ##### check if the close button is pressed #####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    ##### bullets #####
    for bullet in bullets:
        if bullet.x < screenwidth and bullet.x > 0: #for bullets on screen
            bullet.x += bullet.vel
        else: # delete the bullet if it goes off screen
            bullets.pop(bullets.index(bullet))

        ##### key presses & movement #####
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x]:
        if man.left:
            facing= -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2),  round(man.y + man.height //2),6,(0,0,0),facing))

### LEFT ###
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True 
        man.right = False #just to make sure both right and left are not true
        man.standing = False
### RIGHT ###
    elif keys[pygame.K_RIGHT] and man.x < (screenwidth)  - man.width - man.vel - sideborder :
        man.x += man.vel
        man.right = True
        man.left = False #just to make sure both right and left are not true
        man.standing = False
### UP ###
    elif keys[pygame.K_UP] and man.y > man.vel:
        man.y -= man.vel
        if man.right == True:
            man.left = False
            man.standing = False
        elif man.left == True:
            man.right = False
            man.standing = False
        else:
            man.right = True
            man.left = False
            man.standing = False   
### DOWN ###
    elif keys[pygame.K_DOWN] and man.y <= (screenheight - man.height -bottomborder): # screenheight: #and man.y < man.vel:
        man.y += man.vel
        if man.right == True:
            man.left = False
            man.standing = False
        elif man.left == True:
            man.right = False
            man.standing = False
        else:
            man.right = True
            man.left = False
            man.standing = False    
    else:
        man.standing = True
        man.walkCount = 0 #counts the number of steps

#   if not(man.isJump): #if not already jumping
#       if keys[pygame.K_SPACE]:
#           man.isJump = True
#           # man.right = False #to ensure we're not moving right whilst jumping
#           # man.left = False #to ensure we're not moving right whilst jumping
#           man.walkCount = 0
#   else:
#       if man.jumpCount >= -10: #we start at +10, decrement 1 on every iteration (when neg = 1), so after 10 iterations we go negative, at which point the logic to reverse the y position begins (ie rectangle falls)
#           neg = 1
#           if man.jumpCount < 0:
#               neg = -1
#           man.y -= (man.jumpCount ** 2) //2  * neg 
#           man.jumpCount -= 1 #decrement jump count. So after a jump is started, y speed will decrease for 10 iterations (it will be 10 squared, 9 squared, 8 squared etc)
#       else:
#           man.isJump = False
#           man.jumpCount = 10

    redrawGameWindow()

pygame.quit()
  # pygame.display.flip()
  # fpsClock.tick(fps)