import sys
import pygame
from pygame.locals import *
import random as randy
pygame.init()

########## Pygame Settings ##########
screenwidth, screenheight = 512, 512
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Danger Dungeon")
clock = pygame.time.Clock()

########## misc variables, constants and list initialisations ##########
# global counter
# counter = 0
global intervalcounter
intervalcounter = 0
myfont = pygame.font.SysFont("monospace", 16)
skeletons = [] #List to store the skeleton objects
skeletonsgroup = pygame.sprite.Group() #Group to act on or test all skeleton objects at once
allspritesgroup = pygame.sprite.Group()
########## Images ##########
bg = pygame.image.load('assets/bluedungeonbg256px.png')
bg = pygame.transform.scale(bg, (512, 512))
# the number of pixels which is a "Border" at the bottom of the background image
bottomborder = 36
sideborder = 3
char = pygame.image.load('assets/standl.png')
walkRightUnscaled = [pygame.image.load('assets/walkr1.png'), pygame.image.load(
    'assets/walkr2.png'), pygame.image.load('assets/walkr3.png'), pygame.image.load('assets/walkr4.png')]
walkLeftUnscaled = [pygame.image.load('assets/walkl1.png'), pygame.image.load(
    'assets/walkl2.png'), pygame.image.load('assets/walkl3.png'), pygame.image.load('assets/walkl4.png')]
walkRight = []
walkLeft = []
skeletonUnscaledwalk = [pygame.image.load('assets/skeleton1.png'), pygame.image.load(
    'assets/skeleton2.png'), pygame.image.load('assets/skeleton3.png'), pygame.image.load('assets/skeleton4.png')]
skeletonwalk = []

### Scale the images at runtime ###
for img in walkRightUnscaled:
    walkRight.append(pygame.transform.scale(img, (64, 64)))
for img in walkLeftUnscaled:
    walkLeft.append(pygame.transform.scale(img, (64, 64)))
for img in skeletonUnscaledwalk:
    skeletonwalk.append(pygame.transform.scale(img, (48, 48)))


########## Classes ##########
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, endx, endy):
                # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.endx = endx
        self.pathx = [self.x, self.endx]
        self.endy = endy
        self.pathy = [self.y, self.endy]
        self.walkCount = 0
        self.velx = 1
        self.vely = 1
        self.hitbox = (self.x+11, self.y+6, 24, 42)
        self.rect = self.image.get_rect() #defines a rect to use in collision tests

    def draw(self, screen):
        self.movex()
        self.movey()
        # self.walkCount = 0
        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if self.velx > 0:  # if moving right
            screen.blit(skeletonwalk[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        else:  # if walking left (same actions for now, until I have some reversed images)
            screen.blit(skeletonwalk[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x+11, self.y+6, 24, 42)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def movex(self):
        if self.velx > 0:
            if self.x + self.velx < self.pathx[1]:  # x movement to the right
                self.x += self.velx
            else:
                self.velx = self.velx * -1
                self.walkCount = 0
        else:
            if self.x - self.velx > self.pathx[0]:  # x movement to the left
                self.x += self.velx
            else:
                self.velx = self.velx * -1
                self.walkCount = 0

    def movey(self):
        if self.vely > 0:
            if self.y + self.vely < self.pathy[1]:  # y movement down?
                self.y += self.vely
            else:
                self.vely = self.vely * -1
                self.walkcount = 0
        else:
            if self.y - self.vely > self.pathy[0]:  # y movement to up
                self.y += self.vely
            else:
                self.vely = self.vely * -1
                self.walkCount = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
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
        self.hitbox = (self.x+11, self.y+6, 24, 42)
        self.rect = self.image.get_rect() #defines a rect to use in collision tests

    def draw(self, screen):
        if self.walkCount + 1 >= 12:  # there are only 4 images, we want to display each for 3 frames, so we'll get an index error if we go over 12
            self.walkCount = 0
        if not(self.standing):  # if we're not standing still
            if self.left:
                # // means integer division, excludes all the decimals. eg 4//3 = 1.
                screen.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:  # standing still
            if self.right:  # if last facing position was right, return the 1st image from the right images
                screen.blit(walkRight[0], (self.x, self.y))
            else:  # return first image from the left images
                screen.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x+15, self.y+27, 31, 40)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

class Projectile(object):
    def __init__(self, x, y, radius, colour, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)


def drawskeletons():
    for s in skeletons:
        Enemy.draw(s, screen)

def checkcollision():
    collided = pygame.sprite.spritecollide(player,skeletonsgroup,True)
    # Check the list of collisions.
    for c in collided:
        # score +=1
        # print(score)
        print('collision')



############################################ Enemy spawn functions ##################################################

def enemyspawn():
    # skeletons.append(Enemy(randy.randint(40, (screenwidth-40)), randy.randint(40, (screenheight-40)),32, 32, randy.randint(40, (screenwidth-40)), randy.randint(40, (screenheight-40))))
    # skeletonsgroup.add(skeletons[-1]) #add the latest element from the skeletons list

    for i in range(5):
    # This represents a block
        skeleton = Enemy(randy.randint(40, (screenwidth-40)), randy.randint(40, (screenheight-40)),32, 32, randy.randint(40, (screenwidth-40)), randy.randint(40, (screenheight-40)))
        skelly = Enemy(100,100, 32, 32, randy.randint(40, (screenwidth-40)), randy.randint(40, (screenheight-40)))
    # Set a random location for the block
    # skeleton.rect.x = random.randrange(screen_width)
    # skeleton.rect.y = random.randrange(screen_height)
 
    # Add the block to the list of objects
        skeletonsgroup.add(skeleton)
        allspritesgroup.add(skeleton)

        skeletonsgroup.add(skelly)
        allspritesgroup.add(skelly)
# x,y,width,height, endx, endy


##############################################################################################
########## Drawing logic lives here, to keep it out of the main function ##########
def redrawGameWindow():
    # screen.blit(bg, (0, 0))  # background image, tuple is the position (0,0)
    elapsedtimetext = myfont.render(
        "Elapsed time in seconds= " + str(int(intervalcounter/60)), 1, (255, 0, 0))
    screen.blit(elapsedtimetext, (2, 3))

    # Draw all the spites
    allspritesgroup.draw(screen)
    pygame.display.update()


#Create a player
player = Player(300, 415, 64, 64) #Create a player
allspritesgroup.add(player)

bullets = []

score = 0

run = True
########## Game loop ##########
while run:
    # counter += 1
    intervalcounter += 1
  
    clock.tick(27)

    # Clear the screen
    screen.fill((0,0,0))

    # See if the player block has collided with anything.
    hitlist = pygame.sprite.spritecollide(player, skeletonsgroup, False)
 
    # # Check the list of collisions.
    # for b in hitlist:
    #     score += 1
    #     print(score)


    ##### check if the close button is pressed #####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ##### bullets #####
    for bullet in bullets:
        if bullet.x < screenwidth and bullet.x > 0:  # for bullets on screen
            bullet.x += bullet.vel
        else:  # delete the bullet if it goes off screen
            bullets.pop(bullets.index(bullet))

        ##### key presses & movement #####
    keys = pygame.key.get_pressed()

    if keys[pygame.K_x]:
        if player.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(player.x + player.width // 2),
                                      round(player.y + player.height // 2), 6, (0, 0, 0), facing))

### LEFT ###
    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False  # just to make sure both right and left are not true
        player.standing = False
### RIGHT ###
    elif keys[pygame.K_RIGHT] and player.x < (screenwidth) - player.width - player.vel - sideborder:
        player.x += player.vel
        player.right = True
        player.left = False  # just to make sure both right and left are not true
        player.standing = False
### UP ###
    elif keys[pygame.K_UP] and player.y > player.vel:
        player.y -= player.vel
        if player.right == True:
            player.left = False
            player.standing = False
        elif player.left == True:
            player.right = False
            player.standing = False
        else:
            player.right = True
            player.left = False
            player.standing = False
### DOWN ###
    # screenheight: #and player.y < player.vel:
    elif keys[pygame.K_DOWN] and player.y <= (screenheight - player.height - bottomborder):
        player.y += player.vel
        if player.right == True:
            player.left = False
            player.standing = False
        elif player.left == True:
            player.right = False
            player.standing = False
        else:
            player.right = True
            player.left = False
            player.standing = False
    else:
        player.standing = True
        player.walkCount = 0  # counts the number of steps


    if intervalcounter == 60:
        enemyspawn()
        intervalcounter = 0
    
   # checkcollision()
    redrawGameWindow()

pygame.quit()
# pygame.display.flip()
# fpsClock.tick(fps)