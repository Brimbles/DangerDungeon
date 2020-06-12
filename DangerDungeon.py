import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

################################### animation variables #################################
walk_index_skeleton = 0 #keeps track of the current image in use
current_frame_skeleton = 0 #tracks current frame
animation_frame_skeleton = 0 #number of frames before switching image

################################### Images ###################################
####################### Skeleton ############################

skeletonwalkimages = [pygame.image.load('assets/skeleton1.png'), pygame.image.load(
    'assets/skeleton2.png'), pygame.image.load('assets/skeleton3.png'), pygame.image.load('assets/skeleton4.png')]
####################### boar ############################
boarUnscaledwalk = [pygame.image.load('assets/boarwalk1.png'), pygame.image.load(
    'assets/boarwalk2.png'), pygame.image.load('assets/boarwalk3.png'), pygame.image.load('assets/boarwalk4.png')]
boarwalkimages = []
### Scale the images at runtime ###
for img in boarUnscaledwalk:
    boarwalkimages.append(pygame.transform.scale(img, (32, 32)))

####################### Background ##########################
bg = pygame.image.load('assets/bluedungeonbg256px.png')
bg = pygame.transform.scale(bg, (512, 512))
bglimitleft = 33
bglimitright = 33
bglimittop = 33#65
bglimitbottom =33

###### Skeleton properties ######
skeleton_width = 10#29
skeleton_height = 24

################################### Classes ###################################
class Enemy(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, x, y, width, height, endx, endy):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        super().__init__()
        self.x = x
        self.y = y
        self.width = skeleton_width
        self.height = skeleton_height
        self.endx = endx
        self.pathx = [self.x, self.endx]
        self.endy = endy
        self.pathy = [self.y, self.endy]

        self.velx = 1
        self.vely = 1
        # self.hitbox = (self.x+11, self.y+6, 24, 42)
    #   self.rect = self.image.get_rect() #defines a rect to use in collision tests
         # self.image = pygame.Surface([width,height])

        self.animation_frames = 6
        self.current_frame = 0
        self.index = 0
        self.image = skeletonwalkimages[self.index]  # 'image' is the current image of the animation.
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)#Note the the 'rect' in the the sprite class will always have the same origin point as the 'image'. Create something separate for testing collisions
        
    def update(self):
        """ Called each frame. """
        self.movex()
        self.movey()

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(skeletonwalkimages)
            self.image = skeletonwalkimages[self.index]
        
    def movex(self):
        # self.rect.x +=10
        if self.velx > 0:
            if self.rect.x + self.velx + self.width < self.pathx[1]:  # x movement to the right
                self.x += self.velx
                self.rect.x += self.velx 
                #self.hitbox.x = self.rect.x 
            else:
                self.velx = self.velx * -1 #reverse
                #self.walkCount = 0
        else:
            if self.rect.x - self.velx > self.pathx[0]:  # x movement to the left
                self.x += self.velx
                self.rect.x += self.velx
                # self.hitbox.x = self.rect.x
            else:
                self.velx = self.velx * -1 #reverse

    def movey(self):
        
        if self.vely > 0:
            if self.rect.y + self.vely < self.pathy[1]:  # y movement down?
                self.rect.y += self.vely
            else:
                self.vely = self.vely * -1
        else:
            if self.rect.y - self.vely > self.pathy[0]:  # y movement to up
                self.rect.y += self.vely
            else:
                self.vely = self.vely * -1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__() 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = 0
        self.image = boarwalkimages[0]  # 'image' is the current image of the animation.
        self.rect = self.image.get_rect() #defines a rect to use in collision tests
        self.nextplayeranimation = 1000 #initialise

    def update(self):
        # Get the current mouse position. This returns the position as a list of two numbers.
        pos = pygame.mouse.get_pos()
        ############## Move the player ############## 
       
    # Check if we've gone off the right edge of the screen        
        if pos[0] +1 >= screenwidth - self.width - bglimitright:
            #pygame.mouse.set
            self.rect.x = screenwidth-self.width- bglimitright -2
            self.rect.y = pos[1] #still need to update the y movement, even if x is at it's limit
            #Check if we've gone off the top of the screen
            if pos[1] <= bglimittop:
                self.rect.y = bglimittop
                # self.rect.x = pos[0] #still need to update the x movement, even if y is at it's limit
            #Check if we've gone off the bottom of the screen
            if pos[1] +1 >= screenheight - bglimitbottom - self.height:
                self.rect.y = screenheight - bglimitbottom - self.height -4
                # self.rect.x = pos[0] #still need to update the x movement, even if y is at it's limit

    # Check if we've gone off the left edge of the screen        
        elif pos[0]  -1 <= bglimitleft:
            self.rect.x = bglimitleft -5
            self.rect.y = pos[1] #still need to update the y movement, even if x is at it's limit
            #Check if we've gone off the top of the screen
            if pos[1] <= bglimittop:
                self.rect.y = bglimittop
                # self.rect.x = pos[0] #still need to update the x movement, even if y is at it's limit
            #Check if we've gone off the bottom of the screen
            if pos[1] +1 >= screenheight - bglimitbottom - self.height:
                self.rect.y = screenheight - bglimitbottom - self.height -4
                # self.rect.x = pos[0] #still need to update the x movement, even if y is at it's limit
        
    #Check if we've gone off the top of the screen
        elif pos[1] <= bglimittop:
            self.rect.y = bglimittop
            self.rect.x = pos[0] #still need to update the x movement, even if y is at it's limit
            # Check if we've gone off the right edge of the screen        
            if pos[0] +1 >= screenwidth - self.width - bglimitright:
                #pygame.mouse.set
                self.rect.x = screenwidth-self.width- bglimitright -2
            if pos[0]  -1 <= bglimitleft:
                self.rect.x = bglimitleft -5

        #Check if we've gone off the bottom of the screen
        elif pos[1] +1 >= screenheight - bglimitbottom - self.height:
            self.rect.y = screenheight - bglimitbottom - self.height -4
            self.rect.x = pos[0] #still need to update the x movement, even if y is at it's limit
            # Check if we've gone off the right edge of the screen        
            if pos[0] +1 >= screenwidth - self.width - bglimitright:
                #pygame.mouse.set
                self.rect.x = screenwidth-self.width- bglimitright -2
            if pos[0]  -1 <= bglimitleft:
                self.rect.x = bglimitleft -5
        
        else:
        # Set the player object to the mouse location
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        
        self.image = boarwalkimages[self.index]  # 'image' is the current image of the animation.
        
        if self.nextplayeranimation <= current_time:
            if self.index < len(boarwalkimages)-1:#if the current value is the penultimate one...
                self.index += 1 #This will allow the image to increment (hopefully)
            else: self.index = 0 #start from the first image again
            self.nextplayeranimation = current_time + 333 #roughly 1/3 second
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([random.randint(2,6),random.randint(5,15)]) #pygame.Surface([4, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3
    
########## initialise pygame ##########
pygame.init()

 ########## Pygame Settings ##########
screenwidth, screenheight = 512, 512
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Danger Dungeon")
clock = pygame.time.Clock()

generalfont = pygame.font.SysFont("calibri", 16)
gameoverfont = pygame.font.SysFont("calibri", 60)

################################### Music & sounds ###############################################
pygame.mixer.music.load('assets/music.wav')
pygame.mixer.music.play(-1)

skeletoncrunch = pygame.mixer.Sound('assets/skeletoncrunch.wav')
playerhurt = pygame.mixer.Sound('assets/playerhurt.wav')
projectile = pygame.mixer.Sound('assets/projectile.wav')


# These are lists of sprites
allspritesgroup = pygame.sprite.Group()
bulletgroup = pygame.sprite.Group()
skeletonspritegroup = pygame.sprite.Group()


skeletonslist = []

def enemyspawn(noofskelliies):
    for i in range(noofskelliies):
        skeleton = Enemy(random.randint(bglimitleft, (screenwidth-skeleton_width-bglimitright)), random.randint(bglimittop, (screenheight-skeleton_height-bglimitbottom)),skeleton_width, skeleton_height, random.randint(bglimitleft, (screenwidth-skeleton_width-bglimitright)), random.randint(bglimittop, (screenheight-skeleton_height-bglimitbottom)))
        # Add the skeleton to the sprite groups
        skeletonspritegroup.add(skeleton)
        allspritesgroup.add(skeleton)
        #add the skeleton to the list of skeleton objects
        skeletonslist.append(skeleton)

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0
wounds = 5
 
# Create a red player block
player = Player(200, 100, 24, 26)
allspritesgroup.add(player)

intervalcounter = 1

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(bulletgroup) < 6: #not too many bullets at once please
                #create a new bullet
                bullet = Bullet()
                projectile.play()
                #set the bullet so it's where the player is
                bullet.rect.x = player.rect.x + (player.rect.width / 2)
                bullet.rect.y = player.rect.y
                # Add the bullet to the lists
                allspritesgroup.add(bullet)
                bulletgroup.add(bullet)
    
    #How much time has elapsed?
    current_time = pygame.time.get_ticks() 
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Add in a background
    screen.blit(bg, (0, 0))  # background image, tuple is the position (0,0)

    #draw a rect to test the game area
    # pygame.draw.rect(screen,RED,(33,65,446,414)) 

    #possibly add some more skellies
    intervalcounter += 1
    if intervalcounter == 60:
        enemyspawn(random.randint(1,5))#spawn random no of skellies
        intervalcounter = 0

    # Calls update() method on every sprite in the list
    allspritesgroup.update()

    # Calculate mechanics for each bullet
    for bullet in bulletgroup:
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bulletgroup.remove(bullet)
            allspritesgroup.remove(bullet)

    #Check for bullets hitting skeletons
    bulletskeletonhits = pygame.sprite.groupcollide(bulletgroup,skeletonspritegroup,True,True)
    for hit in bulletskeletonhits:
        score += 1
        skeletoncrunch.play()
        enemyspawn(1) # respawn 1 skeleton
        print(score)

    # See if the player block has collided with anything.
    hitlist = pygame.sprite.spritecollide(player, skeletonspritegroup, True)
 
    # Check the list of collisions.
    for skeleton in hitlist:
        wounds -= 1
        playerhurt.play()
        # print(score)
 
        # Reset block to the top of the screen to fall again.
        enemyspawn(1)

    #Draw the wound count and score
    scoretext = generalfont.render("Score = " + str(score) , 1, (255, 0, 0))
    scoretextwidth = scoretext.get_width()
    screen.blit(scoretext, (bglimitleft, 0))

    woundtext = generalfont.render("Wounds Remaining = " + str(wounds) , 1, (255, 0, 0))
    woundtextwidth = woundtext.get_width()
    screen.blit(woundtext, (screenwidth - woundtextwidth - bglimitright, 0))

    # Limit to 20 frames per second
    clock.tick(20)
    
    # Draw all the spites
    allspritesgroup.draw(screen)    
    
    #Is the game over?
    if wounds <0:
        gameovertext = gameoverfont.render("Game Over" , 1, (255, 0, 0))
        gameovertextwidth = gameovertext.get_width()
        screen.blit(gameovertext, (screenwidth/2 - gameovertextwidth/2, screenheight/2))   

        playagaintext = generalfont.render("press y to play again, press q to quit" , 1, (255, 0, 0))
        screen.blit(playagaintext, (bglimitleft, screenheight - playagaintext.get_height()))  
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            #reset_game()
            wounds = 5
            score = 0
            allspritesgroup.empty()
            skeletonspritegroup.empty()
            skeletonslist.clear()
        # Add the skeleton to the sprite groups
            allspritesgroup.add(skeleton)
            # Create a red player block
            player = Player(200, 100, 24, 26)
            allspritesgroup.add(player)
            # print('game reset')
        elif keys[pygame.K_q]:
            # print('game quit') 
            pygame.quit()
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.update()

pygame.quit()