import sys
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 256, 256
screen = pygame.display.set_mode((width, height))
 
########## Images ##########
bg = pygame.image.load('assets/bluedungeonbg256px.png')

##### Drawing logic lives here, to keep it out of the main function #####
def redrawGameWindow():
    screen.blit(bg, (0,0)) #background image, tuple is the position (0,0)
    # man.draw(win)
    # for bullet in bullets:
    #     bullet.draw(win)
    pygame.display.update()


########## Game loop ########## 
while True:
  screen.fill((0, 0, 0))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  # Update.
  
  # Draw.
  redrawGameWindow()


  pygame.display.flip()
  fpsClock.tick(fps)