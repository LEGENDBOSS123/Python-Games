import pygame
import math
import random
pygame.init()

wn = pygame.display.set_mode((1500,750))
wn.fill((225,225,225))
class YOU(object):
    def __init__(self):
        self.money = 1000
    def draw(self,wave):
        font = pygame.font.Font("freesansbold.ttf",32)
        text = font.render("MONEY:"+"$"+str(self.money)+"$", True, (128,128,0),(225,225,225))
        recttext =(1000, 0)   
        wn.blit(text, recttext)

        font = pygame.font.Font("freesansbold.ttf",32)
        text = font.render("WAVE:"+str(wave), True, (0,0,0),(225,225,225))
        recttext =(1000, 32)   
        wn.blit(text, recttext)
class SPRITES(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.mx = pygame.mouse.get_pos()[0]
        self.mx = pygame.mouse.get_pos()[1]
        
    def goto(itself,pointx,pointy,speed):
        speed = speed+1
        slope_x = pointx - itself.x
        slope_y = pointy - itself.y
        try:
            distance = math.sqrt((pointx-itself.x)**2+(pointy-itself.y)**2)
            if distance <= speed:
                #itself.goto_x,itself.goto_y = random.randint(0,1500),random.randint(0,750)
                itself.arrived = True
                return 0,0
            the_final_speed = distance/speed
            return int(slope_x//the_final_speed),int(slope_y//the_final_speed)
        except:
            #itself.goto_x,itself.goto_y = random.randint(0,1500),random.randint(0,750)
            itself.arrived = True
            return 0,0
class BULLET(SPRITES):
    def __init__(self,thing,aim,image):
        self.x = thing.x
        self.y = thing.y
        self.ox = thing.x
        self.oy = thing.y
        self.host = thing
        self.aim = aim
        self.aimx = self.aim.x-50
        self.aimy = self.aim.y-50
        
        
        self.arrived = False
        self.image = pygame.image.load(image)
    def draw(self,speed,damage):
        self.aimx = self.aim.x-50
        self.aimy = self.aim.y-50
        xx,yy = self.goto(self.aimx+35,self.aimy+55,speed)
        
        degrees = self.host.degrees
        if self.aimx<=self.x:
            turn = 90
            neg = -1
        else:
            turn = 270
            neg = 1
        image = pygame.transform.rotate(self.image,neg*degrees+turn)
        self.x+=xx
        
        self.y+=yy
        if self.arrived == True:
            self.x = self.ox
            self.y = self.oy
            self.aim.HP-=damage
            self.arrived = False
            self.host.bullets.remove(self)
        #pygame.draw.circle(wn,(0,0,0),(self.x,self.y),radius)
        rect = self.image.get_rect()
        rect.center = ((self.x,self.y))
        wn.blit(image,rect)
class SHOOTER(SPRITES):
    def __init__(self,x,y,char):
        self.char = char
        self.x = x
        self.y = y
        
        self.mx = pygame.mouse.get_pos()[0]
        self.my = pygame.mouse.get_pos()[1]
        self.click = pygame.mouse.get_pressed()
        self.level = 1
        self.money = 0
        if self.char == "ROCK THROWER":
            self.maxlvl = 5
            self.cost = 250
            self.speed = 30
            self.B_IMAGE = "WFI.png"
            self.image = pygame.image.load("SHOOTER.png")
        if self.char == "MINIGUNNER":
            self.maxlvl = 5
            self.cost = 2000
            self.B_IMAGE = "WFI.png"
            self.speed = 10
            self.image = pygame.image.load("MINIGUNNER1.png")
        if self.char == "ENFORCER":
            self.maxlvl = 5
            self.cost = 800
            self.B_IMAGE = "WFI.png"
            self.speed = 30
            self.image = pygame.image.load("SHOOTER.png")


        self.firerate = 0
        self.damage = 0
        self.range = 0
        
        self.arrived = False
        self.shoot_count = self.firerate
        
        
        self.degrees = 0
        self.bullets = []

        self.lvl_up_scrn = False
    def restore(self):
        self.mx = pygame.mouse.get_pos()[0]
        self.my = pygame.mouse.get_pos()[1]
        self.click = pygame.mouse.get_pressed()
    def check_lvl1(self):
        
        if self.level == 1:
            self.money = 300
            self.firerate = 100
            self.damage = 1
            self.range = 300
            
        if self.level == 2:
            self.money = 500
            self.firerate = 80
            self.damage = 2
            self.range = 400
            
        if self.level == 3:
            self.money = 800
            self.firerate = 60
            self.damage = 3
            self.range = 500
            self.radius = 300
            
        if self.level == 4:
            self.money = 1000
            self.firerate = 50
            self.damage = 7
            self.range = 600
            
        if self.level == 5:
            self.money = 1500
            self.firerate = 30
            self.damage = 15
            self.range = 1000
    def check_lvl2(self):
        
        if self.level == 1:
            self.money = 250
            self.firerate = 15
            self.damage = 1
            self.range = 200
            
        if self.level == 2:
            self.money = 525
            self.firerate = 9
            self.damage = 2
            self.range = 250
            
        if self.level == 3:
            self.money = 2000
            self.firerate = 12
            self.damage = 2
            self.range = 300
            
        if self.level == 4:
            self.image = pygame.image.load("MINIGUNNER2.png")
            self.money = 5500
            self.firerate = 6.5
            self.damage = 2
            self.range = 300
            
        if self.level == 5:
            self.money = 8500
            self.firerate = 6.5
            self.damage = 4
            self.range = 400
    def check_lvl3(self):
        
        if self.level == 1:
            self.money = 450
            self.firerate = 300
            self.damage = 12
            self.range = 100
            
        if self.level == 2:
            self.money = 500
            self.firerate = 275
            self.damage = 16
            self.range = 100
            
        if self.level == 3:
            self.money = 1500
            self.firerate = 250
            self.damage = 20
            self.range = 100
            
        if self.level == 4:
            self.money = 3000
            self.firerate = 250
            self.damage = 45
            self.range = 200
            
        if self.level == 5:
            self.money = 4400
            self.firerate = 200
            self.damage = 70
            self.range = 300
    def check_all_levels(self):
        if self.char == "ROCK THROWER":
            self.check_lvl1()
        if self.char == "MINIGUNNER":
            self.check_lvl2()
        if self.char == "ENFORCER":
            self.check_lvl3()
    def level_up(self):
        self.restore()
        rect = self.image.get_rect()
        rect.center = (self.x,self.y)
        self.check_all_levels()
        if self.click[0] == 1 and self.mx>=rect[0] and self.mx<=rect[0] + rect[2] and self.my>=rect[1] and self.my<=rect[1] + rect[3]:
            self.lvl_up_scrn = True
        if self.lvl_up_scrn == True:
            
                
            pygame.draw.circle(wn,(100,100,255),(self.x,self.y),self.range)
            
            box = pygame.Surface((200,200))
            rect = box.get_rect()
            rect.center = ((self.x,self.y))
            box.fill((0,0,0))
            wn.blit(box,rect)
            size = 32
            font = pygame.font.Font("freesansbold.ttf",size)
            text = font.render("LEVEL:"+str(self.level), True, (255,255,255),(0,0,0))
            recttext = text.get_rect()
            recttext.center = rect.center
            recttext[1]-=75
            wn.blit(text, recttext)
            size = 14
            font = pygame.font.Font("freesansbold.ttf",size)
            text = font.render("DAMAGE:"+str(self.damage), True, (255,255,255),(0,0,0))
            recttext = text.get_rect()
            recttext.center = rect.center
            recttext[1]-=50
            wn.blit(text, recttext)

            size = 14
            font = pygame.font.Font("freesansbold.ttf",size)
            text = font.render("FIRERATE:"+str(self.firerate), True, (255,255,255),(0,0,0))
            recttext = text.get_rect()
            recttext.center = rect.center
            recttext[1]-=25
            wn.blit(text, recttext)

            

            
            box = pygame.Surface((100,50))
            rect = box.get_rect()
            rect.center = ((self.x+50,self.y+75))
            box.fill((255,0,0))
            wn.blit(box,rect)
            size = 32
            font = pygame.font.Font("freesansbold.ttf",size)
            text = font.render("QUIT", True, (0,0,0),(255,0,0))
            recttext = text.get_rect()
            recttext.center = rect.center
            wn.blit(text, recttext)
            
            if self.click[0] == 1 and self.mx>=rect[0] and self.mx<=rect[0] + rect[2] and self.my>=rect[1] and self.my<=rect[1] + rect[3]:
                self.lvl_up_scrn = False
            box = pygame.Surface((100,50))
            rect = box.get_rect()
            rect.center = ((self.x-50,self.y+75))
            box.fill((0,255,0))
            wn.blit(box,rect)
            size = 10
            font = pygame.font.Font("freesansbold.ttf",size)
            if self.level!=self.maxlvl:
                text = font.render("$"+str(self.money)+"$", True, (0,0,0),(0,255,0))
            else:
                text = font.render("MAX LEVEL", True, (0,0,0),(0,255,0))

            recttext = text.get_rect()
            recttext.center = rect.center
            
            wn.blit(text, recttext)

            if self.click[0] == 1 and self.mx>=rect[0] and self.mx<=rect[0] + rect[2] and self.my>=rect[1] and self.my<=rect[1] + rect[3]:
                if self.level!=self.maxlvl and you.money>=self.money:
                    self.level += 1
                    you.money-=self.money
                self.lvl_up_scrn = False

            
                
    def draw(self):
        record = 100000000
        neg = 0
        turn = 0
        aim = None
        
        for i in zombies:
            
            
            dis = math.sqrt((self.x-i.x)**2+(self.y-i.y)**2)
            if record>dis and dis<=self.range:
                record = dis
                aim = i
            
                    
        self.shoot_count+=1
        if aim!=None:
            
            if aim.x<=self.x:
                turn = 0
                neg = -1
            else:
                turn = 180
                neg = 1
            
                
            slope_x = self.x-aim.x
            slope_y = self.y-aim.y
            
            self.degrees = math.degrees(math.asin(slope_y/record))            
            
            if self.shoot_count >= self.firerate:
                
                self.bullets.append(BULLET(self,aim,self.B_IMAGE))
                self.shoot_count = 0
        try:
            for b in self.bullets:
                b.draw(self.speed,self.damage)
        except Exception as e:
            pass
        image = pygame.transform.rotate(self.image,neg*self.degrees+turn)
        rect = image.get_rect()
        rect.center = (self.x,self.y)
        wn.blit(image,rect)

        

        
class ZOMBIE(SPRITES):
    def __init__(self,x,y,speed,hp):
        self.x = x
        self.y = y
        self.arrived = False
        self.speed = speed
        self.speed+=1
        self.speed_x = 0
        self.speed_y = 0
        self.count = 1
        self.HP = hp
        self.HPoriginal = self.HP
        self.HPp = 100
        self.HPratio = self.HPp/self.HP
        self.ZOMBIE_LEFT = pygame.image.load("ZOMBIE.png")
        self.ZOMBIE_RIGHT = pygame.transform.flip(pygame.image.load("ZOMBIE.png"),True,False)
        self.image = self.ZOMBIE_RIGHT
    def death(self):
        you.money+=self.HPoriginal
        del zombies[zombies.index(self)]
    def hitbase(self):
        HQ.HP-=self.HP
        self.HP = 0
        del zombies[zombies.index(self)]

    def move(self):
        if self.HP>0:
            self.speed_x,self.speed_y=self.goto(tracks[self.count-1].x,tracks[self.count-1].y,self.speed)
            if self.arrived == True:
                self.arrived = False
                if self.count!=len(tracks):
                    self.count+=1
                else:
                    self.hitbase()
                
            self.x+=self.speed_x
            self.y+=self.speed_y
        else:
            self.death()
    def draw(self):
        if self.HP>0:
            font = pygame.font.Font("freesansbold.ttf",16)
            
            
            self.move()
            if self.speed_x>=0:
                self.image = self.ZOMBIE_RIGHT
            if self.speed_x<0:
                self.image = self.ZOMBIE_LEFT
            rect = self.image.get_rect()
            rect.center = (self.x,self.y)
            wn.blit(self.image,rect)

            
            pygame.draw.rect(wn,(150,150,150),(self.x-50,self.y-80,self.HPp,20))
            
            pygame.draw.rect(wn,(255,0,0),(self.x-50,self.y-80,self.HP*self.HPratio,20))
            text = font.render("HP:"+str(self.HP)+"/"+str(self.HPoriginal), True, (0,0,0),(225,225,225))
            recttext = text.get_rect()
            recttext.center = ((self.x,self.y-90))
            wn.blit(text, recttext)
        else:
            self.death()
class BAR(object):
    def __init__(self,image,thing):
        self.mx = pygame.mouse.get_pos()[0]
        self.my = pygame.mouse.get_pos()[1]
        self.click = pygame.mouse.get_pressed()
        self.drag = False
        
        self.image = pygame.image.load(image)
        self.thing = thing
        self.x = 1450
        self.rex = self.x
        if thing == "ROCK THROWER":
            self.y = 100
        if thing == "MINIGUNNER":
            self.y = 300
            
        if thing == "ENFORCER":
            self.y = 500
        self.rey = self.y            
        
        self.host = SHOOTER(self.x,self.y,thing).cost
    def restore(self):
        self.mx = pygame.mouse.get_pos()[0]
        self.my = pygame.mouse.get_pos()[1]
        self.click = pygame.mouse.get_pressed()
    def work(self):
        self.restore()
        
        rect = self.image.get_rect()
        rect.center = (self.x,self.y)
        wn.blit(self.image,rect)
        if you.money>=self.host and self.click[0] == 1 and self.mx>=rect[0] and self.mx<=rect[0] + rect[2] and self.my>=rect[1] and self.my<=rect[1] + rect[3]:
            self.drag = True

        if self.drag == True:
            record = False
            ran = 100
            for i in shooters:
                pygame.draw.circle(wn,(100,100,255),(i.x,i.y),ran)
                dx = i.x-self.mx
                dy = i.y-self.my
                distance = math.sqrt(dx**2 + dy**2)
                if distance<=ran:
                    record = True
            rects = self.image.get_rect()
            rects.center = (self.mx,self.my)
            wn.blit(self.image,rects)
            if self.click[2] == 1 and self.mx<1380 and record == False:
                check = False
                
                for i in tracks:
                    if self.mx>i.x-i.width/2-5 and self.mx<i.x+i.width/2+5 and self.my>i.y-i.height/2-5 and self.my<i.y+i.height/2+5:
                        check = True
                if check == False:
                    shooters.append(SHOOTER(self.mx,self.my,self.thing))
                    you.money-=self.host
                    self.drag = False
                    self.x = self.rex
                    self.y = self.rey
                    rects = self.image.get_rect()
                    rects.center = (self.mx,self.my)
                    wn.blit(self.image,rects)
                
        pygame.draw.line(wn,(0,0,0),(1400,0),(1400,750),5)
        size = 10
        font = pygame.font.Font("freesansbold.ttf",size)
        
        text = font.render("$"+str(self.host)+"$", True, (128,128,0),(225,225,225))
        recttext = text.get_rect()
        recttext.center = rect.center
        recttext[1]+=25
        wn.blit(text, recttext)
        size = 7
        font = pygame.font.Font("freesansbold.ttf",size)
        text = font.render(str(self.thing), True, (128,128,0),(225,225,225))
        recttext = text.get_rect()
        recttext.center = rect.center
        recttext[1]-=30
        recttext[0]-=15
        wn.blit(text, recttext)

class HOME(object):
    def __init__(self,tracks):
        self.host = tracks[-1]
        self.x = self.host.x
        self.y = self.host.y
        self.HP = 300
        self.HPoriginal = self.HP
        self.HPp = 200
        self.image = pygame.image.load("THEBASE.png")
        self.ratio = self.HPp/self.HP
    def draw(self):
        global run
        rect = self.image.get_rect()
        rect.center = ((self.x,self.y))
        wn.blit(self.image,rect)
        font = pygame.font.Font("freesansbold.ttf",32)
        if self.HP<0:
            self.HP = 0
        text = font.render("HP:"+str(self.HP)+"/"+str(self.HPoriginal), True, (0,0,0),(225,225,225))
        recttext =(1000,64)   
        wn.blit(text, recttext)
        pygame.draw.rect(wn,(150,150,150),(self.x-100,self.y+150,self.HPp,30))

        if self.HP>0:
            pygame.draw.rect(wn,(0,255,0),(self.x-100,self.y+150,self.HP*self.ratio,30))
        else:
            run = False
            print("GAME OVER")
            print("YOU SURVIVED FOR"+" "+str(wave)+" "+"WAVES")
        
class TRACK(object):
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        
        
        self.width = w
        self.height = h
        self.color = (x%255,y%255,h%255)
    def draw(self):
        image = pygame.Surface((self.width,self.height))
        image.fill(self.color)
        rect = image.get_rect()
        rect.center = (self.x,self.y)
        wn.blit(image,rect)
        
        
    

bars = [BAR("SHOOTER.png","ROCK THROWER"),BAR("MINIGUNNER1.png","MINIGUNNER"),BAR("SHOOTER.png","ENFORCER")]
shooters = []

you = YOU()
wave = 0
zombies = []
tracks = [TRACK(300,100,600,100),TRACK(650,100,100,100),TRACK(650,350,100,400),TRACK(650,550,100,100),TRACK(950,550,500,100),TRACK(1150,550,100,100),TRACK(1150,350,100,300),TRACK(1150,250,100,100),TRACK(600,250,1000,100),TRACK(150,250,100,100),TRACK(150,450,100,300),TRACK(150,550,100,100)]

HQ = HOME(tracks)
def draw():
    global wave
    
    wn.fill((225,225,225))
    
    for bar in bars:
        bar.work()
    for t in tracks:
        t.draw()
    
        
    for s in shooters:
        s.draw()
        s.level_up()
        
        
    
    
    
    if zombies!=[]:
        for z in zombies:
            z.draw()
        
    
    else:
        wave+=1
        you.money+=(wave-1)*30
        for z in range(wave):
            zombies.append(ZOMBIE(0-z*200,100,3,wave))
    you.draw(wave)
    HQ.draw()
run = True
while run:
    pygame.time.delay(20)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    draw() 
    pygame.display.update()
pygame.quit()
