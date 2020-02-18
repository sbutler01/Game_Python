# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:45:03 2020

@author: Sunil Butler
"""

#import the proper packages
import pygame
import sys
import random
import math

#inialize the packages
pygame.init()

#set parameter values
width = 800
height= 600

color_aqua = (0,128,128)
color_red = (255,0,0)
color_green = (0,255,0)
color_white = (255,255,255)
color_background = (0,0,0)

size_player = [40,60]
size_enemy = 25
size_bonus = 10
size_bullet = 5
size_loadbar = 1
size_bonusbar = 1

speed_enemy = 10
speed_framerate = 30
speed_player = 5
speed_spawn_bonus = 0.005
speed_bullet = 20

position_player = [(width - size_player[0])/2, height - (2 * size_player[1])]
position_enemy = [random.randint(0,width-(2*size_enemy)), 0]
position_loadbar = [25, height-50]
position_bonusbar = [200, height-50]

#for the multibullet thingy
x_bullet = 0
count = 0

list_enemy = [position_enemy]
list_bonus = []
list_bullet = []

#create a screen
screen = pygame.display.set_mode((width,height))

#create condition to run the game
gameover = False
score = 0
font_score = pygame.font.SysFont("monospace", 25)
loadbar_load = False
loadbar_finish = True
bonusbar_finish = False

##example of a loop that runs the game
#while not gameover:
   ##print anything you do on the game screen
   #for event in pygame.event.get():
       #print(event)
       #if event.type == pygame.QUIT:
        #sys.exit()

#adds new enemies incrementally
def drop_enemies(list_enemy, freq):
  delay = random.random()
  if len(list_enemy) < 10 and delay < freq:
    x_enemy = random.randint(0, width - size_enemy)
    y_enemy = 0
    list_enemy.append([x_enemy, y_enemy])

#defines enemy movement
def move_enemies(list_enemy, points):
  for idx, position_enemy in enumerate(list_enemy):
    #move the enemy
    if position_enemy[1] >= 0 and position_enemy[1] < height:
      position_enemy[1] += speed_enemy
    #remove the enemy
    else:
      list_enemy.pop(idx)
      points += 1
  return points

#designs enemy appearance
def draw_enemies(list_enemy):
  for position_enemy in list_enemy:
    pygame.draw.circle(screen, color_red, (position_enemy[0],
      position_enemy[1]), size_enemy)

#adds new bonus orb
def drop_bonus(list_bonus, freq):
  delay = random.random()
  if len(list_bonus) < 3 and delay < freq:
    x_bonus = random.randint(size_bonus, width - (size_bonus * 2))
    y_bonus = random.randint(size_bonus + (height/4), height + (size_bonus * 2))
    list_bonus.append([x_bonus, y_bonus])

#designs bonus appearance
def draw_bonus(list_bonus):
  for position_bonus in list_bonus:
    pygame.draw.circle(screen, color_green, (position_bonus[0],
      position_bonus[1]), size_bonus)


def drop_bullet(list_bullet):
  x_bullet = position_player[0]+20
  y_bullet = position_player[1]
  list_bullet.append([x_bullet, y_bullet])

def drop_bullet_2(list_bullet):
  x_bullet = position_player[0]+20
  y_bullet = position_player[1]
  for i in list(range(1,4)):
    list_bullet.append([x_bullet, y_bullet])

#moves bullet
def move_bullet(list_bullet):
  for idx, position_bullet in enumerate(list_bullet):
    #move the enemy
    if position_bullet[1] >= 0 and position_bullet[1] < height:
      position_bullet[1] -= speed_bullet
    #remove the enemy
    else:
      list_bullet.pop(idx)

def move_bullet_2(list_bullet, x_bullet, count):
  for idx, position_bullet in enumerate(list_bullet):
    #move the enemy 

    if position_bullet[1] < 0 or position_bullet[0] >= width or position_bullet[0] <= 0:
      list_bullet.pop(idx)

    elif idx == 0 and count <= 2:
      position_bullet[1] -= speed_bullet

    elif idx == 1 and count <= 2:
      position_bullet[0] -= speed_bullet*math.sqrt(2)/2
      position_bullet[1] -= speed_bullet*math.sqrt(2)/2

    elif idx == 2 and count <= 2:
      position_bullet[0] += speed_bullet*math.sqrt(2)/2
      position_bullet[1] -= speed_bullet*math.sqrt(2)/2

    elif position_bullet[0] == x_bullet:
      position_bullet[1] -= speed_bullet

    elif position_bullet[0] < x_bullet:
      position_bullet[0] -= speed_bullet*math.sqrt(2)/2
      position_bullet[1] -= speed_bullet*math.sqrt(2)/2

    elif position_bullet[0] > x_bullet:
      position_bullet[0] += speed_bullet*math.sqrt(2)/2
      position_bullet[1] -= speed_bullet*math.sqrt(2)/2

    count += 1
  return(count)

#designs bonus appearance
def draw_bullet(list_bullet):
  for position_bullet in list_bullet:
    pygame.draw.circle(screen, color_white, (int(position_bullet[0]),
      int(position_bullet[1])), size_bullet)


def draw_loadbar(length_loadbar, outline):
  pygame.draw.rect(screen, color_white, (position_loadbar[0], position_loadbar[1], length_loadbar, 30), outline)

def draw_bonusbar(length_bonusbar, outline):
  pygame.draw.rect(screen, color_green, (position_bonusbar[0], position_bonusbar[1], length_bonusbar, 30), outline)

#detects whether two objects are touching
def detect_collision(pos_player, pos_enemy, size_player, size_enemy):
  x_player = float(pos_player[0] + (size_player[0]/2))
  y_player = float(pos_player[1] + (size_player[1]/2))

  x_enemy = float(pos_enemy[0])
  y_enemy = float(pos_enemy[1])

  dist_tan = (y_enemy - y_player)/(x_enemy - x_player + 0.01)
  dist_theta = math.atan(dist_tan)

  length_player = (((size_player[0])*size_player[1])/4)/math.sqrt((size_player[1]*math.cos(dist_theta)/2)**2
   + ((size_player[0])*math.sin(dist_theta)/2)**2)
  length_enemy = float(size_enemy)

  dist_objects = math.sqrt((x_player - x_enemy)**2 + (y_player - y_enemy)**2)

  if dist_objects < (length_player + length_enemy):
    return(True)
  else:
    return(False)

def detect_collision_circles(pos_bullet, pos_enemy, size_bullet, size_enemy):
  x_bullet = float(pos_bullet[0])
  y_bullet = float(pos_bullet[1])

  x_enemy = float(pos_enemy[0])
  y_enemy = float(pos_enemy[1])

  dist_objects = math.sqrt((x_bullet - x_enemy)**2 + (y_bullet - y_enemy)**2)

  if dist_objects < (size_bullet + size_enemy):
    return(True)
  else:
    return(False)


#determines whetehr any objects are touching the player
def detect_collision_all(position_player, list_enemy, size_player, size_enemy):
  for position_enemy in list_enemy:
    if detect_collision(position_player, position_enemy, size_player, size_enemy):
      return True

def detect_collision_bonus(position_player, list_bonus, points, size_player, size_bonus):
  for idx, position_bonus in enumerate(list_bonus):
    if detect_collision(position_player, position_bonus, size_player, size_bonus):
      list_bonus.pop(idx)
      points += 10
  return points

def detect_collision_bullet(list_bullet, list_enemy, points):
  for idx_bullet, position_bullet in enumerate(list_bullet):
    for idx_enemy, position_enemy in enumerate(list_enemy):
      if detect_collision_circles(position_bullet, position_enemy, size_bullet, size_enemy):
        list_bullet.pop(idx_bullet)
        list_enemy.pop(idx_enemy)
        points += 2
  return points


#now here's the loop for our game
clock = pygame.time.Clock()
while not gameover:
    clock.tick(speed_framerate)

    speed_enemy = int(math.log(float(pygame.time.get_ticks()), 2000) * 10)

    #print anything you do on the game screen
    for event in pygame.event.get():

      if event.type == pygame.QUIT: #exit the game if you press the 'x'
        print(score)
        sys.exit()

      if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_SPACE and loadbar_finish and bonusbar_finish is False: #exit the game if you press the 'x'
          drop_bullet(list_bullet)
          loadbar_load = True
          loadbar_finish = False

        if event.key == pygame.K_SPACE and loadbar_finish and bonusbar_finish: #exit the game if you press the 'x'
          count = 0
          x_bullet = position_player[0]+20
          drop_bullet_2(list_bullet)
          loadbar_load = True
          loadbar_finish = False

    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_LEFT] and position_player[0 ] > 0:
      position_player[0] -= speed_player
    
    if key_pressed[pygame.K_RIGHT] and position_player[0] < (width - size_player[0]):
      position_player[0] += speed_player
    
    if key_pressed[pygame.K_UP] and position_player[1] > 0:
      position_player[1] -= speed_player
    
    if key_pressed[pygame.K_DOWN] and position_player[1] < (height - size_player[1]):
      position_player[1] += speed_player
    

    screen.fill(color_background)

    #design the player
    pygame.draw.ellipse(screen, color_aqua, (position_player[0],
      position_player[1],size_player[0],size_player[1]))

    #set the enemy speed
    rate_enemy = math.log(float(pygame.time.get_ticks()),5000)/10

    #apply enemy functions
    drop_enemies(list_enemy, rate_enemy)
    draw_enemies(list_enemy)
    score = move_enemies(list_enemy, score)

    #apply bonus functions
    score_prebonus = score
    drop_bonus(list_bonus, speed_spawn_bonus/(3 * len(list_bonus) + 1))
    draw_bonus(list_bonus)
    score = detect_collision_bonus(position_player, list_bonus, score, size_player, size_bonus)

    if size_bonusbar >= 150:
      bonusbar_finish = True

    if score_prebonus != score and bonusbar_finish is False:
      size_bonusbar += 30

    draw_bullet(list_bullet)

    if bonusbar_finish is False:
      move_bullet(list_bullet)

    elif bonusbar_finish:
      count = move_bullet_2(list_bullet, x_bullet, count)

    score = detect_collision_bullet(list_bullet, list_enemy, score)

    draw_loadbar(150,1)
    if loadbar_load:
      size_loadbar += 5
    
    draw_loadbar(size_loadbar,0)

    draw_bonusbar(150,1)

    draw_bonusbar(size_bonusbar,0)

    if size_loadbar >= 150:
      loadbar_load = False
      loadbar_finish = True
      size_loadbar = 1

    #calculate and display score
    score_text = "Score: " + str(score)
    score_display = font_score.render(score_text, 1, color_white)
    screen.blit(score_display, (width - 175, height - 50))


    #draw the player
    pygame.display.update()

    #end the game if you're hit
    if detect_collision_all(position_player, list_enemy, size_player, size_enemy):
      gameover = True
      print(score)



#to do
#make it so list empties when bar is full, not when it goes off screen
#turn shot into three-prong after number of bonuses

