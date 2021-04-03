size = 750
limit = 12
bg = (173,216,230)
import pygame
pygame.init()
import math
import random
import time

xval = size
yval = size
wn = pygame.display.set_mode((size,size))
verticies = [(-0.5,0.5,-0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),(0.5,0.5,-0.5),(0.5,0.5,0.5),(-0.5,0.5,0.5),(-0.5,-0.5,0.5),(0.5,-0.5,0.5)]
edges = [(0,1),(0,3),(1,2),(2,3),(0,5),(5,4),(3,4),(1,6),(2,7),(7,4),(6,7),(5,6)]
faces = [(2,1,6,7),(0,1,2,3),(4,5,6,7),(0,3,4,5),(0,1,6,5),(3,4,7,2)]

dirt_color = [(128,199,31),(145,100,20),(145,100,30),(140,100,0),(140,100,20),(130,90,20)]

stone_color = [(90,90,90),(80,80,80),(100,100,100),(95,95,95),(110,110,110),(100,100,100)]

sand_color = [(190, 174, 124),(204, 188, 138),(184, 168, 118),(194, 178, 128),(185, 165, 118),(194, 178, 128)]

wood_color = [(200,145,90),(85,60,40),(85,55,55),(190,135,80),(80,60,48),(80,60,45)]

leaf_color = [(100,175,25),(118,189,21),(128,199,31),(115,180,25),(110,189,21),(128,179,11)]

colors = [dirt_color,stone_color,sand_color,wood_color,leaf_color]
class PLAYER():
    def __init__(self):
        self.x_og = 0
        self.y_og = -10
        self.z_og = 0
        
        self.x = self.x_og
        self.y = self.y_og
        self.z = self.z_og
        
        self.anglex = 45
        self.angley = 45
        self.FOV_OG = 60
        self.FOV = self.FOV_OG
        self.speed = 0.3
        self.anglespeed = 5
        self.gravity = 0.05
        self.velocity = 0
        self.jump = 0.35
        self.mode = "survival"
        self.timer = 0
        self.timerlimit = 5
        self.chosenblock = 0
        self.inventory = [0,1,2,3,4,5,6,7,8]
    def DISTANCE(self,pointa,pointb):
        return math.sqrt((pointa[0]-pointb[0])**2+(pointa[1]-pointb[1])**2)
    def PLACE(self,cubes):
        cubes2 = []
        for cube in cubes:
            cubes2.append((math.sqrt((cube[0]-PLAYER.x)**2+(cube[1]-PLAYER.y)**2+(cube[2]-PLAYER.z)**2),cube[0],cube[1],cube[2],cube[3]))
            
        cubes2.sort()
        for cube in cubes2:
            draw_sides = []
            for face in faces:
                sides = []
                for vertex in (verticies[face[0]],verticies[face[1]],verticies[face[2]],verticies[face[3]]):
                    old_x = vertex[0]-PLAYER.x+cube[1]
                    old_y = vertex[1]-PLAYER.y+cube[2]
                    old_z = vertex[2]-PLAYER.z+cube[3]
                    
                    sides.append([old_x,old_y,old_z])
                        
                
                x = int(sides[0][0]+sides[1][0]+sides[2][0]+sides[3][0]/4)
                y = int(sides[0][1]+sides[1][1]+sides[2][1]+sides[3][1]/4)
                z = int(sides[0][2]+sides[1][2]+sides[2][2]+sides[3][2]/4)
                dis = math.sqrt(x**2+y**2+z**2)
                draw_sides.append(dis)
                
            draw_sides2 = draw_sides.copy() 
            draw_sides2.sort()
            faces1 = draw_sides.index(draw_sides2[0])
            faces2 = draw_sides.index(draw_sides2[1])
            faces3 = draw_sides.index(draw_sides2[2])
            faces4 = draw_sides.index(draw_sides2[3])
            faces5 = draw_sides.index(draw_sides2[4])
            faces6 = draw_sides.index(draw_sides2[5])
            for face in (faces[faces1],faces[faces2],faces[faces3],faces[faces4],faces[faces5],faces[faces6]):
                sides = []
                for vertex in (verticies[face[0]],verticies[face[1]],verticies[face[2]],verticies[face[3]]):
                    old_x = vertex[0]-PLAYER.x+cube[1]
                    old_y = vertex[1]-PLAYER.y+cube[2]
                    old_z = vertex[2]-PLAYER.z+cube[3]
                    
                    old_x,old_z = old_x*math.cos(PLAYER.anglex*math.pi/180)-old_z*math.sin(PLAYER.anglex*math.pi/180),old_z*math.cos(PLAYER.anglex*math.pi/180)+old_x*math.sin(PLAYER.anglex*math.pi/180)
                    old_y,old_z = old_y*math.cos(PLAYER.angley*math.pi/180)-old_z*math.sin(PLAYER.angley*math.pi/180),old_z*math.cos(PLAYER.angley*math.pi/180)+old_y*math.sin(PLAYER.angley*math.pi/180)
                    
                    if old_z>0:
                        new_x = math.degrees(math.atan(old_x/(old_z+0.001)))/PLAYER.FOV*xval
                        new_y = math.degrees(math.atan(old_y/(old_z+0.001)))/PLAYER.FOV*yval
                        
                        new_x+=xval//2
                        new_y+=yval//2
                        
                        
                        sides.append([new_x,new_y,vertex[0],vertex[1],vertex[2]])
                                            
                if len(sides)>=4:
                    points = [sides[0][0:2],sides[1][0:2],sides[2][0:2],sides[3][0:2]]
                    
                    times = 0
                    for i in range(4):
                        i2 = (i+1)%4
                        if points[i][0]-points[i2][0] != 0:
                            slope = (points[i][1]-points[i2][1])/(points[i][0]-points[i2][0])
                            
                            if slope!=0:
                                c = points[i][1]-slope*points[i][0]
                                x = (yval//2-c)/slope
                                y = yval//2
                                if x>xval//2 and y>min(points[i][1],points[i2][1]) and y<max(points[i][1],points[i2][1]):
                                    times+=1
                                    
                        #a = self.DISTANCE(points[i],(xval//2,yval//2))
                        #b = self.DISTANCE(points[(i+1)%4],(xval//2,yval//2))
                        #c = self.DISTANCE(points[0],points[1])
                        #angles += math.degrees(math.acos(max(min( (a**2+b**2-c**2) / (2*a*b),1),0)))
                        
                    if times/2 != times//2:
                        
                        Cube = cubes[cubes.index((cube[1],cube[2],cube[3],cube[4]))]                        
                        if faces.index(face)==0:
                            cubes.append((Cube[0],Cube[1]-1,Cube[2],self.inventory[self.chosenblock]))
                            Place((Cube[0],Cube[1]-1,Cube[2],self.inventory[self.chosenblock]))
                            return
                        if faces.index(face)==1:
                            cubes.append((Cube[0],Cube[1],Cube[2]-1,self.inventory[self.chosenblock]))
                            Place((Cube[0],Cube[1],Cube[2]-1,self.inventory[self.chosenblock]))

                            return
                        if faces.index(face)==2:
                            cubes.append((Cube[0],Cube[1],Cube[2]+1,self.inventory[self.chosenblock]))
                            Place((Cube[0],Cube[1],Cube[2]+1,self.inventory[self.chosenblock]))
                            return
                        
                        if faces.index(face)==3:
                            cubes.append((Cube[0],Cube[1]+1,Cube[2],self.inventory[self.chosenblock]))
                            Place((Cube[0],Cube[1]+1,Cube[2],self.inventory[self.chosenblock]))
                            return
                        
                        if faces.index(face)==4:
                            cubes.append((Cube[0]-1,Cube[1],Cube[2],self.inventory[self.chosenblock]))
                            Place((Cube[0]-1,Cube[1],Cube[2],self.inventory[self.chosenblock]))
                            return
                        
                        if faces.index(face)==5:
                            cubes.append((Cube[0]+1,Cube[1],Cube[2],self.inventory[self.chosenblock]))
                            Place((Cube[0]+1,Cube[1],Cube[2],self.inventory[self.chosenblock]))
                            return
    def REMOVE(self,cubes):
        cubes2 = []
        for cube in cubes:
            cubes2.append((math.sqrt((cube[0]-PLAYER.x)**2+(cube[1]-PLAYER.y)**2+(cube[2]-PLAYER.z)**2),cube[0],cube[1],cube[2],cube[3]))
            
        cubes2.sort()
        for cube in cubes2:
            draw_sides = []
            for face in faces:
                sides = []
                for vertex in (verticies[face[0]],verticies[face[1]],verticies[face[2]],verticies[face[3]]):
                    old_x = vertex[0]-PLAYER.x+cube[1]
                    old_y = vertex[1]-PLAYER.y+cube[2]
                    old_z = vertex[2]-PLAYER.z+cube[3]
                    
                    sides.append([old_x,old_y,old_z])
                        
                
                x = int(sides[0][0]+sides[1][0]+sides[2][0]+sides[3][0]/4)
                y = int(sides[0][1]+sides[1][1]+sides[2][1]+sides[3][1]/4)
                z = int(sides[0][2]+sides[1][2]+sides[2][2]+sides[3][2]/4)
                dis = math.sqrt(x**2+y**2+z**2)
                draw_sides.append(dis)
                
            draw_sides2 = draw_sides.copy() 
            draw_sides2.sort()
            faces1 = draw_sides.index(draw_sides2[0])
            faces2 = draw_sides.index(draw_sides2[1])
            faces3 = draw_sides.index(draw_sides2[2])
            faces4 = draw_sides.index(draw_sides2[3])
            faces5 = draw_sides.index(draw_sides2[4])
            faces6 = draw_sides.index(draw_sides2[5])
            for face in (faces[faces1],faces[faces2],faces[faces3],faces[faces4],faces[faces5],faces[faces6]):
                sides = []
                for vertex in (verticies[face[0]],verticies[face[1]],verticies[face[2]],verticies[face[3]]):
                    old_x = vertex[0]-PLAYER.x+cube[1]
                    old_y = vertex[1]-PLAYER.y+cube[2]
                    old_z = vertex[2]-PLAYER.z+cube[3]
                    
                    old_x,old_z = old_x*math.cos(PLAYER.anglex*math.pi/180)-old_z*math.sin(PLAYER.anglex*math.pi/180),old_z*math.cos(PLAYER.anglex*math.pi/180)+old_x*math.sin(PLAYER.anglex*math.pi/180)
                    old_y,old_z = old_y*math.cos(PLAYER.angley*math.pi/180)-old_z*math.sin(PLAYER.angley*math.pi/180),old_z*math.cos(PLAYER.angley*math.pi/180)+old_y*math.sin(PLAYER.angley*math.pi/180)
                    
                    if old_z>0:
                        new_x = math.degrees(math.atan(old_x/(old_z+0.001)))/PLAYER.FOV*xval
                        new_y = math.degrees(math.atan(old_y/(old_z+0.001)))/PLAYER.FOV*yval
                        
                        new_x+=xval//2
                        new_y+=yval//2
                        
                        
                        sides.append([new_x,new_y,vertex[0],vertex[1],vertex[2]])
                                            
                if len(sides)>=4:
                    points = [sides[0][0:2],sides[1][0:2],sides[2][0:2],sides[3][0:2]]
                    
                    times = 0
                    for i in range(4):
                        i2 = (i+1)%4
                        if points[i][0]-points[i2][0] != 0:
                            slope = (points[i][1]-points[i2][1])/(points[i][0]-points[i2][0])
                            
                            if slope!=0:
                                c = points[i][1]-slope*points[i][0]
                                x = (yval//2-c)/slope
                                y = yval//2
                                if x>xval//2 and y>min(points[i][1],points[i2][1]) and y<max(points[i][1],points[i2][1]):
                                    times+=1
                                    
                        #a = self.DISTANCE(points[i],(xval//2,yval//2))
                        #b = self.DISTANCE(points[(i+1)%4],(xval//2,yval//2))
                        #c = self.DISTANCE(points[0],points[1])
                        #angles += math.degrees(math.acos(max(min( (a**2+b**2-c**2) / (2*a*b),1),0)))
                        
                    if times/2 != times//2:
                        
                        Cube = cubes[cubes.index((cube[1],cube[2],cube[3],cube[4]))]
                        
                        cubes.remove(Cube)
                        Remove(Cube)
                        return
                        
            
    def JUMP(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.velocity=-self.jump
    def MOVE(self,cubes):
        self.timer+=1
        if self.y>100:
            self.x = self.x_og
            self.y = self.y_og
            self.z = self.z_og
            self.velocity = 0
        if self.mode=="survival":
            self.velocity+=self.gravity
            self.y+=self.velocity
        if self.anglex>360:
            self.anglex-=360
        if self.anglex<0:
            self.anglex+=360
        if self.angley>=90:
            self.angley=90
        if self.angley<=-90:
            self.angley=-90
            
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.z+=self.speed*math.cos(PLAYER.anglex*math.pi/180)
            self.x+=self.speed*math.sin(PLAYER.anglex*math.pi/180)
        if key[pygame.K_s]:
            self.z-=self.speed*math.cos(PLAYER.anglex*math.pi/180)
            self.x-=self.speed*math.sin(PLAYER.anglex*math.pi/180)
        if key[pygame.K_d]:
            self.z+=self.speed*math.cos((PLAYER.anglex+90)*math.pi/180)
            self.x+=self.speed*math.sin((PLAYER.anglex+90)*math.pi/180)
        if key[pygame.K_a]:
            self.z+=self.speed*math.cos((PLAYER.anglex-90)*math.pi/180)
            self.x+=self.speed*math.sin((PLAYER.anglex-90)*math.pi/180)
        if key[pygame.K_RIGHT]:
            self.anglex+=self.anglespeed
        if key[pygame.K_LEFT]:
            self.anglex-=self.anglespeed
        if key[pygame.K_UP]:
            self.angley-=self.anglespeed
        if key[pygame.K_DOWN]:
            self.angley+=self.anglespeed
        if key[pygame.K_e] and self.timer>self.timerlimit:
            self.PLACE(cubes)
            self.timer = 0
        if key[pygame.K_r] and self.timer>self.timerlimit:
            self.REMOVE(cubes)
            self.timer = 0
        if key[pygame.K_SPACE] and self.mode == "creative":
            self.y-=self.speed
        if key[pygame.K_LSHIFT]:
            self.y+=self.speed
        self.FOV = self.FOV_OG
        if key[pygame.K_c]:
            self.FOV = self.FOV_OG//5
        
        if key[pygame.K_q]:
            if self.mode == "creative":
                self.mode = "survival"
            else:
                self.mode = "creative"
            pygame.time.delay(500)
            
        if key[pygame.K_1]:
            self.chosenblock=0
        if key[pygame.K_2]:
            self.chosenblock=1
        if key[pygame.K_3]:
            self.chosenblock=2
        if key[pygame.K_4]:
            self.chosenblock=3
        if key[pygame.K_5]:
            self.chosenblock=4
        if key[pygame.K_6]:
            self.chosenblock=5
        if key[pygame.K_7]:
            self.chosenblock=6
        if key[pygame.K_8]:
            self.chosenblock=7
        if key[pygame.K_9]:
            self.chosenblock=8

cubes = [(0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 2, 0), (0, 0, 3, 0), (0, 0, 4, 0), (0, 0, 5, 0), (0, 0, 6, 0), (0, 0, 7, 0), (0, 0, 8, 0), (0, 0, 9, 0), (0, 0, 10, 0), (0, 0, 11, 0), (0, 0, 12, 0), (0, 0, 13, 0), (0, 0, 14, 0), (0, 0, 15, 0), (0, 0, 16, 0), (0, 0, 17, 0), (0, 0, 18, 0), (0, 0, 19, 0), (1, 0, 0, 0), (1, 0, 2, 0), (1, 0, 3, 0), (1, 0, 4, 0), (1, 0, 5, 0), (1, 0, 6, 0), (1, 0, 7, 0), (1, 0, 8, 0), (1, 0, 9, 0), (1, 0, 10, 0), (1, 0, 11, 0), (1, 0, 12, 0), (1, 0, 13, 0), (1, 0, 14, 0), (1, 0, 15, 0), (1, 0, 16, 0), (1, 0, 17, 0), (1, 0, 18, 0), (1, 0, 19, 0), (2, 0, 0, 0), (2, 0, 3, 0), (2, 0, 4, 0), (2, 0, 5, 0), (2, 0, 6, 0), (2, 0, 7, 0), (2, 0, 8, 0), (2, 0, 9, 0), (2, 0, 10, 0), (2, 0, 11, 0), (2, 0, 12, 0), (2, 0, 13, 0), (2, 0, 14, 0), (2, 0, 15, 0), (2, 0, 16, 0), (2, 0, 17, 0), (2, 0, 18, 0), (2, 0, 19, 0), (3, 0, 0, 0), (3, 0, 1, 0), (3, 0, 4, 0), (3, 0, 5, 0), (3, 0, 6, 0), (3, 0, 7, 0), (3, 0, 8, 0), (3, 0, 9, 0), (3, 0, 10, 0), (3, 0, 11, 0), (3, 0, 12, 0), (3, 0, 13, 0), (3, 0, 14, 0), (3, 0, 15, 0), (3, 0, 16, 0), (3, 0, 17, 0), (3, 0, 18, 0), (3, 0, 19, 0), (4, 0, 0, 0), (4, 0, 1, 0), (4, 0, 2, 0), (4, 0, 5, 0), (4, 0, 6, 0), (4, 0, 7, 0), (4, 0, 8, 0), (4, 0, 9, 0), (4, 0, 10, 0), (4, 0, 11, 0), (4, 0, 12, 0), (4, 0, 13, 0), (4, 0, 14, 0), (4, 0, 15, 0), (4, 0, 16, 0), (4, 0, 17, 0), (4, 0, 18, 0), (4, 0, 19, 0), (5, 0, 0, 0), (5, 0, 1, 0), (5, 0, 2, 0), (5, 0, 6, 0), (5, 0, 7, 0), (5, 0, 8, 0), (5, 0, 9, 0), (5, 0, 10, 0), (5, 0, 11, 0), (5, 0, 12, 0), (5, 0, 13, 0), (5, 0, 14, 0), (5, 0, 15, 0), (5, 0, 16, 0), (5, 0, 17, 0), (5, 0, 18, 0), (5, 0, 19, 0), (6, 0, 0, 0), (6, 0, 1, 0), (6, 0, 2, 0), (6, 0, 4, 0), (6, 0, 7, 0), (6, 0, 8, 0), (6, 0, 9, 0), (6, 0, 10, 0), (6, 0, 11, 0), (6, 0, 12, 0), (6, 0, 13, 0), (6, 0, 14, 0), (6, 0, 15, 0), (6, 0, 16, 0), (6, 0, 17, 0), (6, 0, 18, 0), (6, 0, 19, 0), (7, 0, 0, 0), (7, 0, 2, 0), (7, 0, 3, 0), (7, 0, 4, 0), (7, 0, 8, 0), (7, 0, 9, 0), (7, 0, 10, 0), (7, 0, 11, 0), (7, 0, 12, 0), (7, 0, 13, 0), (7, 0, 14, 0), (7, 0, 15, 0), (7, 0, 16, 0), (7, 0, 17, 0), (7, 0, 18, 0), (7, 0, 19, 0), (8, 0, 0, 0), (8, 0, 13, 0), (8, 0, 14, 0), (8, 0, 16, 0), (8, 0, 17, 0), (8, 0, 18, 0), (8, 0, 19, 0), (9, 0, 12, 0), (9, 0, 13, 0), (9, 0, 14, 0), (9, 0, 15, 0), (9, 0, 16, 0), (9, 0, 17, 0), (9, 0, 18, 0), (9, 0, 19, 0), (10, 0, 0, 0), (10, 0, 12, 0), (10, 0, 13, 0), (10, 0, 14, 0), (10, 0, 15, 0), (10, 0, 16, 0), (10, 0, 17, 0), (10, 0, 18, 0), (10, 0, 19, 0), (11, 0, 0, 0), (11, 0, 13, 0), (11, 0, 14, 0), (11, 0, 15, 0), (11, 0, 16, 0), (11, 0, 17, 0), (11, 0, 18, 0), (11, 0, 19, 0), (12, 0, 0, 0), (12, 0, 12, 0), (12, 0, 13, 0), (12, 0, 14, 0), (12, 0, 15, 0), (12, 0, 16, 0), (12, 0, 17, 0), (12, 0, 18, 0), (12, 0, 19, 0), (13, 0, 0, 0), (13, 0, 12, 0), (13, 0, 13, 0), (13, 0, 14, 0), (13, 0, 15, 0), (13, 0, 16, 0), (13, 0, 17, 0), (13, 0, 18, 0), (13, 0, 19, 0), (14, 0, 0, 0), (14, 0, 12, 0), (14, 0, 13, 0), (14, 0, 14, 0), (14, 0, 15, 0), (14, 0, 16, 0), (14, 0, 17, 0), (14, 0, 18, 0), (14, 0, 19, 0), (15, 0, 0, 0), (15, 0, 12, 0), (15, 0, 13, 0), (15, 0, 14, 0), (15, 0, 15, 0), (15, 0, 16, 0), (15, 0, 17, 0), (15, 0, 18, 0), (15, 0, 19, 0), (16, 0, 0, 0), (16, 0, 12, 0), (16, 0, 13, 0), (16, 0, 14, 0), (16, 0, 15, 0), (16, 0, 16, 0), (16, 0, 17, 0), (16, 0, 18, 0), (16, 0, 19, 0), (17, 0, 0, 0), (17, 0, 12, 0), (17, 0, 13, 0), (17, 0, 14, 0), (17, 0, 15, 0), (17, 0, 16, 0), (17, 0, 17, 0), (17, 0, 18, 0), (17, 0, 19, 0), (18, 0, 0, 0), (18, 0, 12, 0), (18, 0, 13, 0), (18, 0, 14, 0), (18, 0, 15, 0), (18, 0, 16, 0), (18, 0, 17, 0), (18, 0, 18, 0), (18, 0, 19, 0), (19, 0, 0, 0), (19, 0, 12, 0), (19, 0, 13, 0), (19, 0, 14, 0), (19, 0, 15, 0), (19, 0, 16, 0), (19, 0, 17, 0), (19, 0, 18, 0), (19, 0, 19, 0), (1, 0, 1, 1), (2, 0, 1, 1), (2, 0, 2, 1), (3, 0, 2, 1), (3, 0, 3, 1), (4, 0, 3, 1), (4, 0, 4, 1), (5, 0, 4, 1), (5, 0, 5, 1), (6, 0, 5, 1), (7, 0, 6, 0), (7, 0, 7, 0), (6, 0, 6, 0), (7, -1, 4, 3), (7, -1, 6, 3), (7, -2, 6, 3), (7, -3, 6, 3), (7, -2, 4, 3), (7, -3, 4, 3), (7, -4, 4, 3), (7, -4, 6, 3), (7, -4, 5, 3), (7, -2, 3, 3), (7, -3, 3, 3), (7, -4, 3, 3), (7, -1, 2, 2), (7, -2, 2, 2), (7, -4, 2, 2), (7, -3, 2, 2), (7, -1, 1, 2), (7, -2, 1, 2), (7, -3, 1, 2), (7, -4, 1, 2), (7, -1, 0, 2), (7, -2, 0, 2), (7, -3, 0, 2), (7, -4, 0, 2), (8, -1, 0, 2), (8, -2, 0, 2), (8, -3, 0, 2), (8, -4, 0, 2), (9, 0, 0, 0), (9, -1, 0, 2), (9, -2, 0, 2), (10, -1, 0, 1), (10, -2, 0, 1), (5, 0, 3, 0), (6, 0, 3, 0), (7, -1, 3, 3), (9, -3, 0, 1), (9, -4, 0, 1), (12, -1, 0, 1), (12, -2, 0, 1), (11, -1, 0, 2), (11, -2, 0, 2), (13, -1, 0, 2), (13, -2, 0, 2), (15, -1, 0, 2), (15, -2, 0, 2), (17, -1, 0, 2), (17, -2, 0, 2), (19, -1, 0, 2), (19, -2, 0, 2), (18, -1, 0, 1), (18, -2, 0, 1), (16, -1, 0, 1), (16, -2, 0, 1), (14, -1, 0, 1), (14, -2, 0, 1), (11, -3, 0, 1), (11, -4, 0, 1), (13, -3, 0, 1), (13, -4, 0, 1), (15, -3, 0, 1), (15, -4, 0, 1), (17, -3, 0, 1), (17, -4, 0, 1), (19, -3, 0, 1), (19, -4, 0, 1), (18, -3, 0, 2), (18, -4, 0, 2), (16, -3, 0, 2), (16, -4, 0, 2), (14, -3, 0, 2), (14, -4, 0, 2), (12, -3, 0, 2), (12, -4, 0, 2), (10, -3, 0, 2), (10, -4, 0, 2), (7, -1, 7, 3), (7, -2, 7, 3), (7, -3, 7, 3), (7, -4, 7, 3), (7, -1, 8, 2), (7, -2, 8, 2), (7, -3, 8, 2), (7, -4, 8, 2), (7, -2, 9, 2), (7, -3, 9, 2), (7, -4, 9, 2), (7, -1, 10, 2), (7, -2, 10, 2), (7, -3, 10, 2), (7, -4, 10, 2), (7, -1, 11, 2), (7, -2, 11, 2), (7, -3, 11, 2), (7, -4, 11, 2), (7, -1, 12, 2), (7, -2, 12, 2), (7, -3, 12, 2), (7, -4, 12, 2), (8, 0, 15, 0), (8, -1, 12, 2), (8, -2, 12, 2), (8, -3, 12, 2), (8, -4, 12, 2), (10, -1, 12, 2), (10, -2, 12, 2), (10, -3, 12, 1), (10, -4, 12, 1), (9, -1, 12, 1), (9, -2, 12, 1), (9, -3, 12, 2), (9, -4, 12, 2), (11, 0, 12, 0), (11, -1, 12, 1), (11, -2, 12, 1), (11, -3, 12, 2), (11, -4, 12, 2), (12, -2, 12, 2), (12, -1, 12, 2), (12, -3, 12, 1), (12, -4, 12, 1), (13, -1, 12, 1), (13, -2, 12, 1), (13, -3, 12, 2), (13, -4, 12, 2), (14, -1, 12, 2), (14, -2, 12, 2), (14, -3, 12, 1), (14, -4, 12, 1), (15, -1, 12, 1), (15, -2, 12, 1), (15, -3, 12, 2), (15, -4, 12, 2), (16, -1, 12, 2), (16, -2, 12, 2), (16, -3, 12, 1), (16, -4, 12, 1), (17, -1, 12, 1), (17, -2, 12, 1), (17, -3, 12, 2), (17, -4, 12, 2), (18, -1, 12, 2), (18, -2, 12, 2), (18, -3, 12, 1), (18, -4, 12, 1), (19, -1, 12, 1), (19, -2, 12, 1), (19, -3, 12, 2), (19, -4, 12, 2), (7, -1, 9, 2), (7, 0, 1, 0), (8, 0, 12, 0), (7, 0, 5, 1), (8, 0, 5, 1), (9, 0, 5, 1), (10, 0, 5, 1), (11, 0, 5, 1), (12, 0, 5, 1), (14, 0, 5, 1), (15, 0, 5, 1), (16, 0, 5, 1), (17, 0, 5, 1), (18, 0, 5, 1), (19, 0, 5, 1), (19, 0, 1, 1), (18, 0, 1, 1), (16, 0, 1, 1), (17, 0, 1, 1), (15, 0, 1, 1), (14, 0, 1, 1), (13, 0, 1, 1), (12, 0, 1, 1), (10, 0, 1, 1), (9, 0, 1, 1), (8, 0, 1, 1), (11, 0, 1, 1), (11, 0, 2, 1), (12, 0, 2, 1), (13, 0, 2, 1), (14, 0, 2, 1), (15, 0, 2, 1), (16, 0, 2, 1), (17, 0, 2, 1), (19, 0, 2, 1), (18, 0, 2, 1), (18, 0, 3, 1), (19, 0, 3, 1), (17, 0, 3, 1), (16, 0, 3, 1), (14, 0, 3, 1), (11, 0, 3, 1), (10, 0, 2, 1), (8, 0, 2, 1), (9, 0, 2, 1), (9, 0, 3, 1), (8, 0, 3, 1), (10, 0, 3, 1), (12, 0, 3, 1), (13, 0, 3, 1), (15, 0, 3, 1), (15, 0, 4, 1), (14, 0, 4, 1), (12, 0, 4, 1), (10, 0, 4, 1), (8, 0, 4, 1), (9, 0, 4, 1), (11, 0, 4, 1), (13, 0, 4, 1), (16, 0, 4, 1), (18, 0, 4, 1), (19, 0, 4, 1), (17, 0, 4, 1), (10, 0, 6, 1), (8, 0, 6, 1), (9, 0, 6, 1), (11, 0, 6, 1), (14, 0, 6, 1), (16, 0, 6, 1), (18, 0, 6, 1), (19, 0, 6, 1), (17, 0, 6, 1), (15, 0, 6, 1), (15, 0, 7, 1), (14, 0, 7, 1), (12, 0, 7, 1), (10, 0, 7, 1), (8, 0, 7, 1), (9, 0, 7, 1), (11, 0, 7, 1), (16, 0, 7, 1), (18, 0, 7, 1), (19, 0, 7, 1), (17, 0, 7, 1), (13, 0, 7, 1), (13, 0, 8, 1), (11, 0, 8, 1), (10, 0, 8, 1), (8, 0, 8, 1), (9, 0, 8, 1), (12, 0, 8, 1), (14, 0, 8, 1), (16, 0, 8, 1), (18, 0, 8, 1), (19, 0, 8, 1), (17, 0, 8, 1), (15, 0, 8, 1), (15, 0, 9, 1), (14, 0, 9, 1), (12, 0, 9, 1), (10, 0, 9, 1), (11, 0, 9, 1), (13, 0, 9, 1), (16, 0, 9, 1), (18, 0, 9, 1), (19, 0, 9, 1), (17, 0, 9, 1), (9, 0, 9, 1), (8, 0, 9, 1), (9, 0, 10, 1), (10, 0, 10, 1), (11, 0, 10, 1), (13, 0, 10, 1), (15, 0, 10, 1), (17, 0, 10, 1), (18, 0, 10, 1), (19, 0, 10, 1), (16, 0, 10, 1), (14, 0, 10, 1), (12, 0, 10, 1), (8, 0, 10, 1), (8, 0, 11, 1), (9, 0, 11, 1), (10, 0, 11, 1), (11, 0, 11, 1), (12, 0, 11, 1), (13, 0, 11, 1), (14, 0, 11, 1), (15, 0, 11, 1), (16, 0, 11, 1), (17, 0, 11, 1), (18, 0, 11, 1), (19, 0, 11, 1), (19, -1, 11, 3), (19, -1, 10, 3), (19, -1, 9, 3), (19, -1, 8, 3), (19, -1, 7, 3), (19, -1, 6, 3), (19, -1, 5, 3), (19, -1, 4, 3), (19, -1, 3, 3), (19, -1, 2, 3), (19, -1, 1, 3), (19, -2, 2, 3), (19, -2, 1, 3), (19, -2, 4, 3), (19, -2, 6, 3), (19, -2, 7, 3), (19, -2, 11, 3), (19, -2, 10, 3), (19, -3, 7, 3), (19, -3, 4, 3), (19, -2, 5, 3), (19, -3, 6, 3), (19, -3, 5, 3), (19, -2, 8, 3), (19, -2, 9, 3), (19, -3, 9, 3), (19, -3, 8, 3), (19, -3, 10, 3), (19, -3, 11, 3), (19, -4, 8, 3), (19, -4, 5, 3), (19, -4, 4, 3), (19, -2, 3, 3), (19, -3, 2, 3), (19, -3, 3, 3), (19, -3, 1, 3), (19, -4, 2, 3), (19, -4, 1, 3), (19, -4, 3, 3), (19, -4, 6, 3), (19, -4, 7, 3), (19, -4, 9, 3), (19, -4, 10, 3), (19, -4, 11, 3), (19, -5, 12, 3), (18, -5, 12, 3), (17, -5, 12, 3), (16, -5, 12, 3), (15, -5, 12, 3), (14, -5, 12, 3), (13, -5, 12, 3), (12, -5, 12, 3), (11, -5, 12, 3), (10, -5, 12, 3), (9, -5, 12, 3), (8, -5, 12, 3), (7, -5, 12, 3), (7, -5, 11, 3), (7, -5, 9, 3), (7, -5, 7, 3), (7, -5, 8, 3), (7, -5, 10, 3), (7, -5, 6, 3), (7, -5, 4, 3), (7, -5, 2, 3), (7, -5, 3, 3), (7, -5, 5, 3), (7, -5, 0, 3), (7, -5, 1, 3), (9, -5, 0, 3), (8, -5, 0, 3), (10, -5, 0, 3), (11, -5, 0, 3), (12, -5, 0, 3), (14, -5, 0, 3), (15, -5, 0, 3), (16, -5, 0, 3), (17, -5, 0, 3), (18, -5, 0, 3), (19, -5, 0, 3), (19, -5, 1, 3), (19, -5, 2, 3), (19, -5, 3, 3), (19, -5, 4, 3), (19, -5, 5, 3), (19, -5, 7, 3), (19, -5, 8, 3), (19, -5, 9, 3), (19, -5, 10, 3), (19, -5, 11, 3), (19, -5, 6, 3), (18, -5, 1, 3), (17, -5, 1, 3), (18, -5, 2, 3), (17, -5, 2, 3), (16, -5, 1, 3), (15, -5, 1, 3), (14, -5, 1, 3), (13, -5, 0, 3), (13, -5, 1, 3), (12, -5, 1, 3), (9, -5, 1, 3), (11, -5, 1, 3), (8, -5, 2, 3), (8, -5, 1, 3), (8, -5, 3, 3), (8, -5, 5, 3), (8, -5, 4, 3), (8, -5, 7, 3), (8, -5, 6, 3), (8, -5, 11, 3), (8, -5, 10, 3), (8, -5, 9, 3), (8, -5, 8, 3), (9, -5, 11, 3), (9, -5, 10, 3), (9, -5, 9, 3), (9, -5, 8, 3), (9, -5, 7, 3), (9, -5, 6, 3), (9, -5, 2, 3), (9, -5, 3, 3), (9, -5, 5, 3), (9, -5, 4, 3), (11, -5, 2, 3), (12, -5, 2, 3), (10, -2, 0, 3), (14, -5, 2, 3), (15, -5, 2, 3), (16, -5, 2, 3), (13, -5, 2, 3), (10, -5, 3, 3), (10, -5, 5, 3), (10, -5, 6, 3), (10, -5, 4, 3), (11, -5, 4, 3), (11, -5, 3, 3), (11, -5, 5, 3), (13, 0, 5, 1), (11, -5, 6, 3), (10, -5, 7, 3), (11, -5, 7, 3), (10, -4, 0, 3), (10, -5, 1, 3), (10, -5, 2, 3), (10, -5, 8, 3), (10, -5, 9, 3), (10, -5, 10, 3), (10, -5, 11, 3), (11, -5, 11, 3), (12, -5, 11, 3), (13, -5, 11, 3), (14, -5, 11, 3), (15, -5, 11, 3), (16, -5, 11, 3), (16, -5, 10, 3), (16, -5, 9, 3), (16, -5, 8, 3), (16, -5, 7, 3), (16, -5, 6, 3), (16, -5, 5, 3), (16, -5, 4, 3), (16, -5, 3, 3), (15, -5, 10, 3), (15, -5, 9, 3), (15, -5, 8, 3), (15, -5, 7, 3), (15, -5, 6, 3), (15, -5, 5, 3), (15, -5, 4, 3), (15, -5, 3, 3), (11, -5, 10, 3), (11, -5, 9, 3), (11, -5, 8, 3), (12, -5, 10, 3), (12, -5, 9, 3), (12, -5, 8, 3), (12, -5, 7, 3), (12, -5, 6, 3), (12, -5, 5, 3), (12, -5, 4, 3), (12, -5, 3, 3), (13, -5, 10, 3), (14, -5, 10, 3), (14, -5, 9, 3), (13, -5, 9, 3), (13, -5, 8, 3), (14, -5, 8, 3), (14, -5, 7, 3), (14, -5, 6, 3), (13, -5, 7, 3), (13, -5, 6, 3), (13, -5, 5, 3), (14, -5, 5, 3), (14, -5, 4, 3), (13, -5, 4, 3), (13, -5, 3, 3), (14, -5, 3, 3), (18, -1, 3, 2), (17, -1, 3, 2), (18, -2, 4, 2), (17, -2, 4, 2), (18, -3, 5, 2), (17, -3, 5, 2), (18, -4, 6, 2), (17, -4, 6, 2), (18, -5, 7, 2), (17, -5, 7, 2), (18, -5, 11, 3), (18, -5, 10, 3), (17, -5, 11, 3), (17, -5, 10, 3), (18, -5, 9, 3), (18, -5, 8, 3), (17, -5, 9, 3), (17, -5, 8, 3), (12, -6, 10, 1), (11, -6, 10, 1), (10, -6, 10, 1), (9, -6, 9, 1), (9, -6, 10, 1), (12, -6, 9, 1), (10, -6, 9, 1), (11, -6, 9, 1), (9, -7, 9, 1), (9, -7, 10, 1), (10, -7, 10, 1), (11, -7, 10, 1), (12, -7, 10, 1), (12, -7, 9, 1), (11, -8, 10, 1), (10, -8, 10, 1), (9, -6, 4, 1), (10, -6, 4, 1), (11, -6, 4, 1), (11, -6, 3, 1), (12, -6, 4, 1), (12, -6, 3, 1), (10, -6, 3, 1), (9, -6, 3, 1), (9, -7, 3, 1), (10, -7, 3, 1), (11, -7, 3, 1), (12, -7, 3, 1), (11, -8, 3, 1), (10, -8, 3, 1), (9, -7, 4, 1), (12, -7, 4, 1), (11, -6, 6, 4), (11, -6, 7, 4), (10, -6, 7, 4), (10, -6, 6, 4), (12, -1, 9, 2), (13, -1, 8, 2), (11, -1, 8, 2), (11, -2, 8, 2), (13, -2, 8, 2), (12, -1, 8, 2), (12, -2, 9, 2), (12, -3, 9, 2), (13, -1, 9, 2), (11, -1, 9, 2), (11, -2, 9, 2), (13, -2, 9, 2), (12, 0, 6, 1), (12, -1, 6, 3), (13, 0, 6, 1), (13, -1, 6, 3), (13, -1, 5, 3), (12, -1, 5, 3), (11, -1, 5, 3), (11, -1, 6, 3), (12, -1, 3, 2), (13, -1, 3, 2), (11, -1, 3, 2), (12, -1, 2, 2), (13, -1, 2, 2), (11, -1, 2, 2), (13, -2, 3, 2), (11, -2, 3, 2), (11, -2, 2, 2), (13, -2, 2, 2), (12, -2, 2, 2), (12, -3, 2, 2), (3, -1, 15, 3), (3, -2, 15, 3), (3, -3, 15, 3), (3, -4, 15, 3), (2, -4, 15, 4), (3, -4, 14, 4), (3, -4, 16, 4), (3, -5, 15, 4), (4, -5, 15, 4), (3, -5, 16, 4), (4, -4, 16, 4), (2, -5, 16, 4), (2, -4, 14, 4), (2, -4, 16, 4), (2, -5, 15, 4), (3, -5, 14, 4), (4, -4, 15, 4), (4, -4, 14, 4), (14, -1, 16, 3), (14, -2, 16, 3), (14, -3, 16, 3), (14, -4, 16, 3), (14, -5, 16, 4), (14, -5, 17, 4), (15, -5, 16, 4), (15, -5, 17, 4), (13, -5, 16, 4), (13, -5, 17, 4), (14, -5, 15, 4), (13, -5, 15, 4), (15, -5, 15, 4), (15, -6, 16, 4), (14, -6, 16, 4), (14, -6, 15, 4), (13, -6, 16, 4), (14, -6, 17, 4), (1, -1, 9, 3), (1, -2, 9, 3), (1, -3, 9, 3), (1, -4, 9, 3), (1, -5, 9, 4), (2, -5, 9, 4), (1, -5, 8, 4), (2, -5, 8, 4), (0, -5, 9, 4), (1, -5, 10, 4), (0, -5, 10, 4), (1, -6, 9, 4), (0, -6, 9, 4), (0, -6, 10, 4), (1, -6, 8, 4), (0, -5, 8, 4), (2, -5, 10, 4)]

        

hashmap = []
def Hash(tupp):
    
    tup = (tupp[0],tupp[1],tupp[2])
    return (tup[0]*1019+tup[1]*1009+tup[2]*1013)%len(hashmap)

def Setup_Map(number):
    for num in range(number):
        hashmap.append([])
    



def inside(tupp):
    tup = (tupp[0],tupp[1],tupp[2])
    if hashmap[Hash(tup)]!=[]:
        for num in hashmap[Hash(tup)]:
            if num[0:3] == tup:
                return True
            
def inside2(tupp):
    tup = (tupp[0],tupp[1],tupp[2])
    Num = []
    if hashmap[Hash(tup)]!=[]:
        for num in hashmap[Hash(tup)]:
            if num[0:3] == tup:
                Num.append(num)
    return Num

            
def Place(tupp):
    tup = (tupp[0],tupp[1],tupp[2])
    if not inside(tupp):
        hashmap[Hash(tup)].append(tupp)
        
def Remove(tupp):
    tup = (tupp[0],tupp[1],tupp[2])
    if inside(tupp):
        hashmap[Hash(tupp)].remove(tupp)
        
def draw_tree(loc):
    cubes.append((loc[0],loc[1],loc[2],3))
    cubes.append((loc[0],loc[1]-1,loc[2],3))
    cubes.append((loc[0],loc[1]-2,loc[2],3))
    cubes.append((loc[0],loc[1]-3,loc[2],3))
    cubes.append((loc[0],loc[1]-4,loc[2],4))
    cubes.append((loc[0]-1,loc[1]-4,loc[2],4))
    cubes.append((loc[0]+1,loc[1]-4,loc[2],4))
    cubes.append((loc[0],loc[1]-4,loc[2]+1,4))
    cubes.append((loc[0],loc[1]-4,loc[2]-1,4))
    cubes.append((loc[0]-1,loc[1]-4,loc[2]-1,4))
    cubes.append((loc[0]-1,loc[1]-4,loc[2]+1,4))
    cubes.append((loc[0]+1,loc[1]-4,loc[2]-1,4))
    cubes.append((loc[0]+1,loc[1]-4,loc[2]+1,4))
    cubes.append((loc[0],loc[1]-5,loc[2],4))
    cubes.append((loc[0],loc[1]-5,loc[2]+1,4))
    cubes.append((loc[0],loc[1]-5,loc[2]-1,4))
    cubes.append((loc[0]+1,loc[1]-5,loc[2],4))
    cubes.append((loc[0]-1,loc[1]-5,loc[2],4))
    
    Place((loc[0],loc[1],loc[2],3))
    Place((loc[0],loc[1]-1,loc[2],3))
    Place((loc[0],loc[1]-2,loc[2],3))
    Place((loc[0],loc[1]-3,loc[2],3))
    Place((loc[0],loc[1]-4,loc[2],4))
    Place((loc[0]-1,loc[1]-4,loc[2],4))
    Place((loc[0]+1,loc[1]-4,loc[2],4))
    Place((loc[0],loc[1]-4,loc[2]+1,4))
    Place((loc[0],loc[1]-4,loc[2]-1,4))
    Place((loc[0]-1,loc[1]-4,loc[2]-1,4))
    Place((loc[0]-1,loc[1]-4,loc[2]+1,4))
    Place((loc[0]+1,loc[1]-4,loc[2]-1,4))
    Place((loc[0]+1,loc[1]-4,loc[2]+1,4))
    Place((loc[0],loc[1]-5,loc[2],4))
    Place((loc[0],loc[1]-5,loc[2]+1,4))
    Place((loc[0],loc[1]-5,loc[2]-1,4))
    Place((loc[0]+1,loc[1]-5,loc[2],4))
    Place((loc[0]-1,loc[1]-5,loc[2],4))
    
Setup_Map(1000)




    
def update():
    pass
    
    
    
def check_cube(cube,PLAYER):
    if math.sqrt((cube[0]-PLAYER.x)**2+(cube[1]-PLAYER.y)**2+(cube[2]-PLAYER.z)**2)<15:
        
        if PLAYER.x>=cube[0]-0.5 and PLAYER.x<=cube[0]+0.5 and PLAYER.y>=cube[1]-2.4 and PLAYER.y<=cube[1]+0.5 and PLAYER.z<=cube[2]-0.5 and PLAYER.z>=cube[2]-1:
            PLAYER.z = cube[2]-1
        elif PLAYER.x>=cube[0]-0.5 and PLAYER.x<=cube[0]+0.5 and PLAYER.y>=cube[1]-2.4 and PLAYER.y<=cube[1]+0.5 and PLAYER.z>=cube[2]+0.5 and PLAYER.z<=cube[2]+1:
            PLAYER.z = cube[2]+1
        elif PLAYER.z>=cube[2]-0.5 and PLAYER.z<=cube[2]+0.5 and PLAYER.y>=cube[1]-2.4 and PLAYER.y<=cube[1]+0.5 and PLAYER.x>=cube[0]+0.5 and PLAYER.x<=cube[0]+1:
            PLAYER.x = cube[0]+1
        elif PLAYER.z>=cube[2]-0.5 and PLAYER.z<=cube[2]+0.5 and PLAYER.y>=cube[1]-2.4 and PLAYER.y<=cube[1]+0.5 and PLAYER.x<=cube[0]-0.5 and PLAYER.x>=cube[0]-1:
            PLAYER.x = cube[0]-1
        elif PLAYER.x>=cube[0]-0.5 and PLAYER.x<=cube[0]+0.5 and PLAYER.z>=cube[2]-0.5 and PLAYER.z<=cube[2]+0.5 and PLAYER.y>=cube[1]+0.5 and PLAYER.y<=cube[1]+1:
            PLAYER.y = cube[1]+1
        elif PLAYER.x>=cube[0]-0.5 and PLAYER.x<=cube[0]+0.5 and PLAYER.z>=cube[2]-0.5 and PLAYER.z<=cube[2]+0.5 and PLAYER.y<=cube[1]-0.5 and PLAYER.y>=cube[1]-2.5:
            PLAYER.y = cube[1]-2.5
            PLAYER.velocity = 0
            PLAYER.JUMP()
        
            
            
        





     
def draw_cube(cube,PLAYER):
    if math.sqrt((cube[0]-PLAYER.x)**2+(cube[1]-PLAYER.y)**2+(cube[2]-PLAYER.z)**2)<limit:
        buried = 0
            
        if inside((cube[0],cube[1],cube[2]-1,0)):
            buried += 1
        if inside((cube[0],cube[1],cube[2]+1,0)):
            buried += 1
        if inside((cube[0],cube[1]-1,cube[2],0)):
            buried += 1
        if inside((cube[0],cube[1]+1,cube[2],0)):
            buried += 1
        if inside((cube[0]+1,cube[1],cube[2],0)):
            buried += 1
        if inside((cube[0]-1,cube[1],cube[2],0)):
            buried += 1
                
        if buried!=6:
            '''for edge in edges:
                line = []
                for vertex in (verticies[edge[0]],verticies[edge[1]]):
                    old_x = vertex[0]-PLAYER.x+cube[0]
                    old_y = vertex[1]-PLAYER.y+cube[1]
                    old_z = vertex[2]-PLAYER.z+cube[2]
                    old_x,old_z = old_x*math.cos(PLAYER.anglex*math.pi/180)-old_z*math.sin(PLAYER.anglex*math.pi/180),old_z*math.cos(PLAYER.anglex*math.pi/180)+old_x*math.sin(PLAYER.anglex*math.pi/180)
                    old_y,old_z = old_y*math.cos(PLAYER.angley*math.pi/180)-old_z*math.sin(PLAYER.angley*math.pi/180),old_z*math.cos(PLAYER.angley*math.pi/180)+old_y*math.sin(PLAYER.angley*math.pi/180)

                    if old_z>1:
                        new_x = math.degrees(math.atan(old_x/(old_z+0.001)))/PLAYER.FOV*xval
                        new_y = math.degrees(math.atan(old_y/(old_z+0.001)))/PLAYER.FOV*yval
                        
                        new_x+=xval//2
                        new_y+=yval//2
                        
                        line.append([new_x,new_y])
                if len(line)>=2:
                    pygame.draw.line(wn,(0,0,0),line[0],line[1],20)'''
            draw_sides = []
            for face in faces:
                sides = []
                for vertex in (verticies[face[0]],verticies[face[1]],verticies[face[2]],verticies[face[3]]):
                    old_x = vertex[0]-PLAYER.x+cube[0]
                    old_y = vertex[1]-PLAYER.y+cube[1]
                    old_z = vertex[2]-PLAYER.z+cube[2]
                    
                    sides.append([old_x,old_y,old_z])
                        
                
                x = (sides[0][0]+sides[1][0]+sides[2][0]+sides[3][0]/4)
                y = (sides[0][1]+sides[1][1]+sides[2][1]+sides[3][1]/4)
                z = (sides[0][2]+sides[1][2]+sides[2][2]+sides[3][2]/4)
                dis = math.sqrt(x**2+y**2+z**2)
                draw_sides.append(dis)
                
            draw_sides2 = draw_sides.copy() 
            draw_sides2.sort()
            faces1 = draw_sides.index(draw_sides2[0])
            faces2 = draw_sides.index(draw_sides2[1])
            faces3 = draw_sides.index(draw_sides2[2])
            faces4 = draw_sides.index(draw_sides2[3])
            faces5 = draw_sides.index(draw_sides2[4])
            faces6 = draw_sides.index(draw_sides2[5])
            for face in [faces[faces6],faces[faces5],faces[faces4],faces[faces3],faces[faces2],faces[faces1]]:
                if inside((cube[0],cube[1]+1,cube[2],cube[3])) and faces.index(face) == 3 or inside((cube[0],cube[1]-1,cube[2],cube[3])) and faces.index(face) == 0 or inside((cube[0]-1,cube[1],cube[2],cube[3])) and faces.index(face) == 4 or inside((cube[0]+1,cube[1],cube[2],cube[3])) and faces.index(face) == 5 or inside((cube[0],cube[1],cube[2]-1,cube[3])) and faces.index(face) == 1 or inside((cube[0],cube[1],cube[2]+1,cube[3])) and faces.index(face) == 2:
                    pass
                else:
                    sides = []
                    for vertex in (verticies[face[0]],verticies[face[1]],verticies[face[2]],verticies[face[3]]):
                        old_x = vertex[0]-PLAYER.x+cube[0]
                        old_y = vertex[1]-PLAYER.y+cube[1]
                        old_z = vertex[2]-PLAYER.z+cube[2]
                        
                        old_x,old_z = old_x*math.cos(PLAYER.anglex*math.pi/180)-old_z*math.sin(PLAYER.anglex*math.pi/180),old_z*math.cos(PLAYER.anglex*math.pi/180)+old_x*math.sin(PLAYER.anglex*math.pi/180)
                        old_y,old_z = old_y*math.cos(PLAYER.angley*math.pi/180)-old_z*math.sin(PLAYER.angley*math.pi/180),old_z*math.cos(PLAYER.angley*math.pi/180)+old_y*math.sin(PLAYER.angley*math.pi/180)
                        
                        if old_z>0:
                            new_x = math.degrees(math.atan(old_x/(old_z+0.001)))/PLAYER.FOV*xval
                            new_y = math.degrees(math.atan(old_y/(old_z+0.001)))/PLAYER.FOV*yval
                            
                            new_x+=xval//2
                            new_y+=yval//2
                            
                            
                            sides.append([new_x,new_y,vertex[0],vertex[1],vertex[2]])
                            
                                                
                    if len(sides)>=4:
                        color = colors[cube[3]][faces.index(face)]
                        colorx=color[0]
                        colory=color[1]
                        colorz=color[2]
                        dis = (math.sqrt((cube[0]-PLAYER.x)**2+(cube[1]-PLAYER.y)**2+(cube[2]-PLAYER.z)**2)/limit)**5
                        if color[0]<bg[0]:
                            colorx = colorx+(bg[0]-colorx)*dis
                        if color[0]<bg[1]:
                            colory = colory+(bg[1]-colory)*dis
                        if color[0]<bg[2]:
                            colorz = colorz+(bg[2]-colorz)*dis
                        if color[0]>bg[0]:
                            colorx = colorx-(colorx-bg[0])*dis
                        if color[0]>bg[1]:
                            colory = colory-(colory-bg[1])*dis
                        if color[0]>bg[2]:
                            colorz = colorz-(colorz-bg[2])*dis
                        
                        color = (colorx,colory,colorz)
                        pygame.draw.polygon(wn,color,(sides[0][0:2],sides[1][0:2],sides[2][0:2],sides[3][0:2]))
                        
                    


PLAYER = PLAYER()

def draw():
    wn.fill(bg)
    PLAYER.MOVE(cubes)
    
    cubes2 = []
    
    for cube in cubes:
        cubes2.append((math.sqrt((cube[0]-PLAYER.x)**2+(cube[1]-PLAYER.y)**2+(cube[2]-PLAYER.z)**2),cube[0],cube[1],cube[2],cube[3]))
    cubes2.sort()
    cubes2.reverse()
    if cubes2!=[]:
        if PLAYER.mode == "survival":
            for cube in cubes2:
                    check_cube((cube[1],cube[2],cube[3],cube[4]),PLAYER)
        for cube in cubes2:
            
            draw_cube((cube[1],cube[2],cube[3],cube[4]),PLAYER)
    
    pygame.draw.circle(wn,(0,0,0),(xval//2,yval//2),5)
    
update()     
run = True
delay = 0
for cube in cubes:
    Place(cube)
while run:
    timer = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    draw()
    pygame.display.update()
    
    timer-=time.time()
    timer*=-1000
    if timer>=25:
        delay-=0.3
    else:
        delay+=10
    
    delay = max(0,min(delay,30))
    pygame.time.delay(int(delay))
    
pygame.quit()
print(cubes)
