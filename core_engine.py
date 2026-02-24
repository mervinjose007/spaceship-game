import pygame
import os
pygame.mixer.init()
pygame.init()

BULLET_HIT_SOUND = pygame.mixer.Sound('asset/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('asset/Gun+Silencer.mp3')
width,height=900,500
w,h=55,40
win=pygame.display.set_mode((width,height))
health_font=pygame.font.SysFont("comicsans",40)
win_font=pygame.font.SysFont("comicsans",80)
FPS=60
VEL=5
max_bullets=3
bullet_vel=7
red_hit=pygame.USEREVENT+1
yellow_hit=pygame.USEREVENT+2
border=pygame.Rect(width//2 -5,0,10,height)
white=(255,255,255)
black=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

y_image=pygame.image.load(os.path.join("asset","spaceship_yellow.png"))
y_sh=pygame.transform.rotate(pygame.transform.scale(y_image,(w,h)),90)
r_image=pygame.image.load(os.path.join("asset","spaceship_red.png"))
r_sh=pygame.transform.rotate(pygame.transform.scale(r_image,(w,h)),270)
bg=pygame.transform.scale(pygame.image.load(os.path.join("asset","space.png")),(width,height))

def handle_bullets(yellow_bullets, red_bullets, red, yellow):
    for i in yellow_bullets[:]:
        i.x += bullet_vel
        if red.colliderect(i):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(i)
        elif i.x > width:
            yellow_bullets.remove(i)

    for j in red_bullets[:]:
        j.x -= bullet_vel
        if yellow.colliderect(j):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(j)
        elif j.x < 0:
            red_bullets.remove(j)

def draw(red,yellow,red_bullets,yellow_bullets,r_health,y_helath):
    win.blit(bg,(0,0))
    pygame.draw.rect(win,black,border)
    win.blit(y_sh,(yellow.x,yellow.y))
    red_score=health_font.render("health:"+str(r_health),True,white)
    yellow_score=health_font.render("health:"+str(y_helath),True,white)
    win.blit(red_score,(width-red_score.get_width()-10,10))
    win.blit(yellow_score,(10,10))
    win.blit(r_sh,(red.x,red.y))
    for i in red_bullets:
        pygame.draw.rect(win,RED,i)
    for j in yellow_bullets:
        pygame.draw.rect(win,YELLOW,j)
    pygame.display.update()

def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0:
        yellow.x -=VEL
    if keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width < border.x:
        yellow.x +=VEL
    if keys_pressed[pygame.K_w] and yellow.y-VEL>0:
        yellow.y -=VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height < height:
        yellow.y +=VEL  

def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x-VEL> border.x+border.width:
        red.x -=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+VEL+ red.width < width:
        red.x +=VEL
    if keys_pressed[pygame.K_DOWN] and red.y+VEL+red.height < height:
        red.y +=VEL
    if keys_pressed[pygame.K_UP] and red.y-VEL>0:
        red.y -=VEL  

def winner(winner_t):
    draw=win_font.render(winner_t, True ,white)
    win.blit(draw,(width//2-draw.get_width()//2,height//2-draw.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    r_health=10
    y_helath=10
    winner_t=""
    yellow_bullets=[]
    red_bullets=[]
    red=pygame.Rect(700,300,w,h)
    yellow=pygame.Rect(100,300,w,h)
    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(yellow_bullets)<max_bullets:
                    bullet=pygame.Rect(yellow.x+yellow.width-2, yellow.y+yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet) 
                    BULLET_FIRE_SOUND.play() 
                if event.key==pygame.K_RCTRL and  len(red_bullets)<max_bullets:
                    bullet=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet) 
                    BULLET_FIRE_SOUND.play()  
            if event.type==red_hit:
                r_health-=1
                BULLET_HIT_SOUND.play()
            if event.type==yellow_hit:
                y_helath-=1
                BULLET_HIT_SOUND.play()

        if r_health<=0:
            winner_t="YELLOW WON!"
        if y_helath<=0:
            winner_t="RED WON!"

        if winner_t!="":
            winner(winner_t)
            break

        keys_pressed=pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,red,yellow)
        draw(red,yellow,red_bullets,yellow_bullets,r_health,y_helath)


if __name__== "__main__":
    main()







        



            

