import sys

from random import randint
import pygame
import settings as s

'''
TODO: 
start-knap
gøre skibet lokaliserbart
liste af targets
spil-maskine som "spytter" targets ud
tegne text som opdateres dynamisk
collision-detection
'''
def init_targets():
    aliens = []
    for tal in range(s.num_of_aliens):
        xpos = randint(s.delta, s.width - s.delta)
        ypos = 0
        speed = randint(1, 4)
        alien_rect = alien_img.get_rect(center=(xpos, ypos))
        alien = {"image": alien_img, "rect": alien_rect, "name": f"alien_{tal}", "counter": 0, "speed": speed}
        aliens.append(alien)
    return aliens


# init game
pygame.init()

# set screen
screen=pygame.display.set_mode((s.width,s.height))

# set clock
clock=pygame.time.Clock()

# prepare for text
myfont=pygame.font.SysFont('arial',s.font_size)


# load images
bg=pygame.image.load("ressources/bluebg.png")
ship=pygame.image.load("ressources/ship.bmp")
alien_img=pygame.image.load("ressources/alien.bmp")
ship_rect=ship.get_rect()

bg=pygame.transform.scale(bg,(s.width,s.height))
startknap=pygame.image.load("ressources/start.jpg")

# loading targets into list
aliens=init_targets()

# variabler
alien_counter=1
frame_counter=0
frequency=20
score=0


while True:
    frame_counter+=1
    # main loop

    # hente musens position
    mouse_pos=pygame.mouse.get_pos()
    # check events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                s.start_game=not s.start_game

    # alien-counter should count "slower", dvs hver 20.  gang f.eks
    if frame_counter % frequency == 0:
        alien_counter+=1
        if alien_counter==len(aliens):
            #out of bounds. Re-set targets somehow
            alien_counter=1
            aliens=init_targets()

    if s.start_game==True:
        screen.blit(bg,(0,0))
        # adjust stuff that moves
        for alien in aliens[:alien_counter]:
            if ship_rect.colliderect(alien['rect']):
                score+=1
                alien['rect'].centerx=s.width+200
            else:
                alien['rect'].centery+=alien['speed']
                screen.blit(alien['image'],alien['rect'])

        ship_rect.center=mouse_pos
        # paint stuff
        screen.blit(ship,ship_rect)

    else:
        # tegne en startknap
        screen.fill(s.white)
        screen.blit(startknap,(s.width/2,s.height/2))

    text=myfont.render(f"Score: {score}",True,s.white,s.black)
    screen.blit(text,text.get_rect())
    pygame.display.update()
    clock.tick(s.fr)



