import sys, pygame
from math import atan, tan, sin, cos
import ctypes
from random import randint

class asteroid(object):
    def __init__(self,size):
        self.size = size
        self.image= None
        self.pos = (0,0)

        self.vel = (0,0)
        self.out = [False, False]

    def render(self):
        """
        renders the players image
        return: surface containing player image, or green if no iamge is defined
        """

        if self.image:
            img = pygame.transform.scale(self.image, self.size)

            return img
        else:
            s = pygame.Surface(self.size)
            s.fill((0,255,0))
            k = pygame.Surface((self.size[0], self.size[1]/4))
            k.fill((255,255,255))
            s.blit(k, (0,0))

            return s

    def center(self):
        """
        gets the position of the center of the player\n
        return (x,y)
        """

        img = self.render()
        rect = img.get_rect()
        center = rect.center

        x,y = center
        x1,y1 = self.pos
        center = (x+x1,y+y1)

        return center

    def move(self, dt):

        dt = dt/1000

        x,y = self.pos

        x1,y1 = self.vel

        x += x1*dt
        y += y1*dt
        self.pos = (x,y)

    def collision(self, player):
        rect = self.render().get_rect()
        rect.center = self.center()
        for i in player.bullets:
            r = i.render().get_rect()
            r.center = i.center()
            if rect.colliderect(r):
                self.hit(i)
                k = player.bullets.index(i)
                del i
                player.bullets.pop(k)

        r = self.render().get_rect(center=self.center())
        x,y = self.pos
        w,h = self.size
        if r.bottom < 0 and not self.out[1]:
            self.out[1] = True
            y= size[1]
        elif r.top > size[1] and not self.out[1]:
            self.out[1] = True
            y = -h
        
        if r.right < 0 and not self.out[0]:
            self.out[0] = True
            x= size[0]
        elif r.left > size[0] and not self.out[0]:
            self.out[0] = True
            x = -w

        self.pos = (x,y)
        cx,cy = self.center()
        if cx > 0 and cx < size[0]:
            self.out[0] = False
        if cy > 0 and cy < size[1]:
            self.out[1] = False

    def hit(self, bullet):
        x = explodeParticle(self.center(),5,1000,3)
        particles.append(x)


        global asteroids

        #spawn two new asteroids
        
        

        vels = []
        for i in 'ab':

            v1,v2 = self.vel
            vx,vy = self.vel
            vx += randint(-2,2)
            vy += randint(-2,3)

            while True:
                a = (vx < v1)
                b = (vy < v2)
                
                if a and b:
                    vx = vx*1.05
                    vy = vy*1.05
                else: break
            
            vels.append([vx,vy])

        w,h = self.size
        size = (int(w/1.5),int(h/1.5))
        
        if w>h:
            c = w
        else:
            c = h

        if c>60:
            for vel in vels:
                x = asteroid(size)
                
                v = randint(0,1)
                if v == 0: v -=1
                v1 = randint(0,1)
                if v1 == 0: v-=1

                d = randint(0,100)
                d1 = randint(0,100)

                v = str(v) + '.' + str(d)
                v1 = str(v1) + '.' + str(d1)

                v = float(v)
                v1 = float(v1)

                x.vel = (65*v,65*v1)

                
                x.pos = self.center()
                x.image = pygame.image.load('imgs/asteroid.png')
                

                asteroids.append(x)

            
            update(display, screen)
        

        #delete self
        k = asteroids.index(self)
        asteroids.pop(k)

class bulltet(object):
    def __init__(self,pos,velocity,angle,size=(50,20),speed=[10,10]):
        self.vel = velocity
        self.angle = angle
        self.speed = speed
        self.size = size
        self.image = None
        self.pos = pos
        self.rotateBox = (50,50)#increased margins for rotate area
        self.out = [False,False]
        self.distance = 0

    def centerBullet(self):
        img = self.render()
        rect = img.get_rect()
        rect.center = self.pos
        x,y = rect.topleft
        self.pos = (x,y)
       
    def render(self):
        """
        renders the players image
        return: surface containing player image, or green if no iamge is defined
        """
        if self.image:
            img = pygame.transform.scale(self.image, self.size)
            img = pygame.transform.rotate(img, self.angle)

            

            img.set_colorkey((0,255,0))

            return img
        else:
            s = pygame.Surface(self.size)
            s.fill((128,0,0))
            x,y = self.size
            e1,e2 = self.rotateBox
            k = pygame.Surface((x+e1,y+e2))
            k.fill((0,255,0))
            k.blit(s,(25,25))
            k = pygame.transform.rotate(k, self.angle)

            k.set_colorkey((0,255,0))

            return k

    def center(self):
        """
        gets the position of the center of the player\n
        return (x,y)
        """

        img = self.render()
        rect = img.get_rect()
        center = rect.center

        x,y = center
        x1,y1 = self.pos
        center = (x+x1,y+y1)

        return center

    def move(self, dt):
        """
        distance: amount of pixels to move in each direction\n
        return: pixels moved on x, pixels moved on y
        """
        dt = dt/1.2


        x,y = self.vel
        x = x*dt
        y= y*dt

        x1,y1 = self.pos

        self.pos = (x1+x, y1+y)

        self.distance += ((x**2)+(y**2))**0.5

        return x1,y1

    def collision(self):
        r = self.render().get_rect(center=self.center())

        x,y = self.pos
        w,h = self.size
        if r.bottom < 0 and not self.out[1]:
            self.out[1] = True
            y= size[1]
        elif r.top > size[1] and not self.out[1]:
            self.out[1] = True
            y = -h
        
        if r.right < 0 and not self.out[0]:
            self.out[0] = True
            x= size[0]
        elif r.left > size[0] and not self.out[0]:
            self.out[0] = True
            x = -w

        self.pos = (x,y)
        cx,cy = self.center()
        if cx > 0 and cx < size[0]:
            self.out[0] = False
        if cy > 0 and cy < size[1]:
            self.out[1] = False

class player(object):
    """
    player object for asteroids like game\n
    render: renders image\n
    center: gets player center\n
    move: moves player x pixels in each direction\n
    input: handles player input, should be called once per loop\n
    thrust: advanced movement, handles accelration and deceleration\n
    """
    def __init__(self, size=(100,100)):
        self.size = size
        self.image = None
        self.pos = (0,0)

        self.vel = (0,0)
        self.speed = [10,10]
        self.rot = 0
        self.bullets = []
        self.shootTime = 0
        self.angle = 270
        self.out = [False,False]
        self.immune = [True,pygame.time.get_ticks(), [pygame.time.get_ticks(), True]] #[player is immune, time start of immunity, [time since last visibilty, visible]]

        self.deathTime = 0

        self.lives = 3
    
    def render(self):
        """
        renders the players image
        return: surface containing player image, or green if no iamge is defined
        """

        if self.immune[0]:
            if pygame.time.get_ticks() - self.immune[2][0] >= 250:
                self.immune[2][0] = pygame.time.get_ticks()
                if self.immune[2][1]:
                    self.immune[2][1] = False
                else:
                    self.immune[2][1] = True


            if not self.immune[2][1]:
                k = pygame.Surface(self.size)
                k.set_colorkey((0,0,0))
                return k

        if self.image:
            img = pygame.transform.scale(self.image, self.size)

            img = self.rotate(img, self.angle)

            k = pygame.Surface(self.size)
            k.fill((0,255,0))

            
            x,y = img.get_rect().center

            x -= 50
            y -= 50

            k.blit(img, (-x,-y))
            k.set_colorkey((0,255,0))

            return k
        else:
            s = pygame.Surface(self.size)
            s.fill((0,0,255))
            k = pygame.Surface((self.size[0], self.size[1]/4))
            k.fill((255,255,255))
            s.blit(k, (0,0))

            

            return s

    def center(self):
        """
        gets the position of the center of the player\n
        return (x,y)
        """

        img = self.render()
        rect = img.get_rect()
        center = rect.center

        x,y = center
        x1,y1 = self.pos
        center = (x+x1,y+y1)

        return center

    def move(self, distance):
        """
        distance: amount of pixels to move in each direction\n
        return: pixels moved on x, pixels moved on y
        """

        x1,y1 = distance
        x2, y2 = self.pos

        

        self.pos = (x1+x2, y1+y2)

        return x1,y1

    def rotate(self,Surface, angle):
        s = pygame.transform.rotate(Surface, angle)
        return s

    def input(self, dt, mouse):
        """
        gets and handled input for player\n
        dt: delta time from clock.tick
        """
        x,y = self.vel
        lastVel = self.vel
        keys = getKeys()

        #new movement system
        #if 'd' in keys:
        #    x += self.speed[0]*dt/1000
        #if 'a' in keys:
        #    x -= self.speed[0]*dt/1000
        #if 's' in keys:
        #    y += self.speed[1]*dt/1000
        #if 'w' in keys:
        #    y -= self.speed[1]*dt/1000
        #if 'space' in keys:
        #    self.shoot(mouse)
        
        #traditional movement system
        if 'd' in keys:
            self.angle -= 3
        if 'a' in keys:
            self.angle += 3

        if self.angle < 0:
                self.angle = 360-self.angle
        elif self.angle > 360:
            self.angle = self.angle-360

        
        if 'w' in keys:
            x,y = self.vel

            angle = self.angle
            if angle > 90 and angle < 180:
                angle = 180-angle
            elif angle >= 180 and angle <= 270:
                angle = angle - 180
            elif angle > 270 and angle <= 360:
                angle = 360 - angle

            p = tan(angle*(3.14/180))
            x1 = self.speed[0]*(dt/10000)*(cos(angle*(3.1415/180)))*10
            y1 = self.speed[1]*(dt/10000)*(sin(angle*(3.1415/180)))*10

            if self.angle > 90 and self.angle < 270:
                if x1 > 0:
                    x1 = -x1
            if self.angle > 0 and self.angle  < 180:
                if y1 > 0:
                    y1 = -y1
            
            x += x1
            y += y1
        
        if 'space' in keys:
            if not self.immune[0]:
                self.shoot()

        self.vel = (x,y)
        self.thrust(self.vel, lastVel, dt)

    def thrust(self,speed, lastVel, dt):
        """
        speed: maximum allowed speed\n
        lastVel: the last velocity (self.vel) calculated before input. Used to check if the player is moving\n
        dt: delta time from pygame.tick()
        """        
        dt= dt/1000

        x,y = speed
        x1,y1 = lastVel

        #check if past max speed
        if (x**2)**0.5 > self.speed[0]:
            x = self.speed[0] * ((x)/(x**2)**0.5)
        if (y**2)**0.5 > self.speed[1]:
            y = self.speed[1] * ((y)/(y**2)**0.5)

        #check if player x is not changing. Then slowly come to stop
        if x == x1 and x != 0:
            sign = ((x**2)**0.5)/x
            val = x

            x-=  val*dt
            
            if x <= 0.1 and x >= -0.1:
                x = 0

        #check if player y is not changing. Then slowly come to stop
        if y == y1 and y != 0:
            sign = ((y**2)**0.5)/y
            val = y

            y-=  val*dt
            if y <= 0.1 and y >= -0.1:
                y = 0

        #update speed, velocity, then move the player
        speed = (x,y)
        self.vel = (x,y)
        self.move(speed)

    def shoot(self):
        if pygame.time.get_ticks() - self.shootTime >= 350:
            self.shootTime = pygame.time.get_ticks()
            a = self.angle

            path = 'imgs/phonyR.png'

            x,y = self.vel

            #calculate velocity
            angle = self.angle
            if angle > 90 and angle < 180:
                angle = 180-angle
            elif angle >= 180 and angle <= 270:
                angle = angle - 180
            elif angle > 270 and angle <= 360:
                angle = 360 - angle

            x = (cos(angle*(3.1415/180)))
            y = (sin(angle*(3.1415/180)))

            if self.angle > 90 and self.angle < 270:
                if x > 0:
                    x = -x
            if self.angle > 0 and self.angle  < 180:
                if y > 0:
                    y = -y
            

            x = bulltet(self.center(),(x,y),a,(100,40))
                

            x.image = pygame.image.load(path)

            x.centerBullet()

            self.bullets.append(x)

    def collision(self, asteroids):
        #check if player is off screen:
        r = self.render().get_rect(center=self.center())
        x,y = self.pos
        w,h = self.size
        if r.bottom < 0 and not self.out[1]:
            self.out[1] = True
            y= size[1]
        elif r.top > size[1] and not self.out[1]:
            self.out[1] = True
            y = -h
        
        if r.right < 0 and not self.out[0]:
            self.out[0] = True
            x= size[0]
        elif r.left > size[0] and not self.out[0]:
            self.out[0] = True
            x = -w

        self.pos = (x,y)
        cx,cy = self.center()
        if cx > 0 and cx < size[0]:
            self.out[0] = False
        if cy > 0 and cy < size[1]:
            self.out[1] = False

        if not self.immune[0]:
            for i in asteroids:
                ar = i.render().get_rect(center=i.center())
                if ar.colliderect(r):
                    self.kill()
                    asteroids.pop(asteroids.index(i))

                    x = explodeParticle(i.center(),5,1000,3)
                    particles.append(x)

                    self.immune = [True,pygame.time.get_ticks(), [pygame.time.get_ticks(), True]]

        self.immunity()

    def immunity(self):
        if self.immune[0]:
            if pygame.time.get_ticks() - self.immune[1] >= 3500:
                self.immune = [False]

    def kill(self):
        if self.lives == 0:
            global mode
            mode = 'death'
            self.deathTime = pygame.time.get_ticks()
            self.immune[False]
        else:
            self.lives -= 1
        
    def renderHealth(self, width, color):
        k = pygame.Surface(((width*2*(self.lives+1)) + width,50))
        k.fill((0,255,0))
        p =width
        for i in range(self.lives + 1):
            pygame.draw.line(k, color, (p+20,0), (p,50), width)
            p += width*2

        k.set_colorkey((0,255,0))
        display.blit(k, (5,5))

class explodeParticle(object):
    def __init__(self,pos,amount,radius,size=1):
        self.pos = pos
        self.num = amount
        self.dis = 0
        self.maxRadius = radius
        self.r = 0
        self.size = size

        self.angle = 360/amount

    def draw(self):
        a = 0
        for i in range(self.num):
            x = (cos(a)*self.r)
            y = (sin(a)*self.r)
            x1,y1 = self.pos
            pygame.draw.circle(display,(90,90,90),(int(x+x1),int(y+y1)),self.size)
            a += self.angle
            self.r += 1

        if self.r >= self.maxRadius:
            global particles
            k = particles.index(self)
            particles.pop(k)

def getKeys():
    current_keys = {'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103, 'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109,
    'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116, 'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122, '[': 91, ']': 93, '\\': 92, '.': 46, '/': 47, ';': 59, "'": 39, 'backspace': 8, 'delete': 127, 'home': 278, 'end': 279, 'return': 13, 'insert': 277, 'page up': 280, 'right shift': 303, 'up': 273, 'page down': 281, 'right': 275, 'down': 274, 'left': 276,
    'right ctrl': 305, 'menu': 319, 'right alt': 307, 'space': 32, 'left alt': 308, 'left ctrl': 306, 'left shift': 304, 'caps lock': 301, 'tab': 301, '`': 301, '1': 301, '2': 301, '3': 301, '4':
    301, '5': 301, '6': 301, '7': 301, '8': 301, '9': 301, '0': 301, '-': 301, '=': 301, 'escape': 301, 'f1': 301, 'f2': 301, 'f3':
    301, 'f4': 301, 'f5': 301, 'f6': 287, 'f7': 301, 'f8': 301, 'f9': 301, 'f10': 301, 'f11': 301, 'f12': 301, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57}
    
    if pygame.key.get_focused() == True:
        bools = pygame.key.get_pressed()
        out = []
        for i in range(0,len(bools)):
            if bools[i] == 1:
                try:
                    out.append(list(current_keys.keys())[list(current_keys.values()).index(i)])
                except(ValueError):
                    pass
        return out
    return []

def update(disp, screen):
    screen.blit(disp, (0,0))
    pygame.display.flip()

def restart():
    global clock
    global dt
    global display
    global asteroids
    global particles
    global mode
    global astNum
    clock = pygame.time.Clock()
    dt = 0
    display.fill((255,255,255))
    p = player((100,100))
    p.image = pygame.image.load('imgs/index.png')
    p.pos = (450,450)


    asteroids = []
    particles = []

    mode = 'game'
    astNum = 3
    return p

ctypes.windll.shcore.SetProcessDpiAwareness(1)
pygame.init()

size = (900,900)
display = pygame.Surface(size)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
dt = 0
mouse = pygame.Rect(0, 0, 2, 2)

display.fill((255,255,255))

p = player((100,100))
p.image = pygame.image.load('imgs/index.png')
p.pos = (450,450)

astNum = 3
asteroids = []
particles = []

mode = 'tutorial'
while True:
    
    xm, ym = pygame.mouse.get_pos()
    mouse.center = (xm,ym)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if mode == 'game':
        #move
        p.input(dt, (xm,ym))

        re = p.render()

        for roid in asteroids:
            display.blit(roid.render(), roid.pos)
            roid.move(dt)
            roid.collision(p)

        display.blit(re, p.pos)

        p.collision(asteroids)

       

        a,b = p.center()
        pygame.draw.circle(display, (0,0,0), (int(a), int(b)), 5)
        for bullet in p.bullets:
            display.blit(bullet.render(), bullet.pos)
            x,y = bullet.center()
            #print(x,y, bullet.pos)
            #pygame.draw.circle(display, (0,0,0), (int(x),int(y)), 5)
            bullet.move(dt)
            bullet.collision()
            if bullet.distance > 800:
                x = explodeParticle(bullet.center(),5,100)
                particles.append(x)
                k = p.bullets.index(bullet)
                del bullet
                p.bullets.pop(k)

        for particle in particles:
            particle.draw()

        #spawn asteroids
        if len(asteroids) == 0:
            astNum += 1
            for i in range(astNum):
                x = asteroid((200,200))
                x.pos = (randint(0,size[0]),randint(0,size[1]))

                v = randint(0,1)
                if v == 0: v -=1
                v1 = randint(0,1)
                if v1 == 0: v-=1

                d = randint(0,100)
                d1 = randint(0,100)

                v = str(v) + '.' + str(d)
                v1 = str(v1) + '.' + str(d1)

                v = float(v)
                v1 = float(v1)

                x.vel = (60*v,60*v1)
                x.image = pygame.image.load('imgs/asteroid.png')

                r = x.render().get_rect(center=x.center())
                pr = p.render().get_rect(center=p.center())

                if not pr.colliderect(r):
                    asteroids.append(x)

       
        p.renderHealth(20, (255,0,0))

    if mode == 'death':
        re = p.render()
        display.blit(re, p.pos)

        for roid in asteroids:
            asteroids.pop(asteroids.index(roid))

            x = explodeParticle(roid.center(),5,1000,3)
            particles.append(x)
        
        for particle in particles:
            particle.draw()

        if pygame.time.get_ticks() - p.deathTime > 1000: #You
            font = pygame.font.SysFont('ArialBold', 200)
            text = font.render('YOU', True, (255,255,255))
            display.blit(text, ((size[0]/2)-(text.get_rect().width/2), 150))
        
        if pygame.time.get_ticks() - p.deathTime > 2000: #Lose
            font = pygame.font.SysFont('ArialBold', 200)
            text = font.render('LOSE', True, (255,255,255))
            display.blit(text, ((size[0]/2)-(text.get_rect().width/2), (size[1]-150-text.get_rect().height)))

        if pygame.time.get_ticks() - p.deathTime > 3000: #restart button
            font = pygame.font.SysFont('ArialBold', 150)
            text = font.render('Restart', True, (255,255,255))

            w,h = text.get_size()
            btn = pygame.Surface((w+50, h+50))

            btnRect = btn.get_rect(center=((size[0]/2), size[1]/2))
            pygame.draw.rect(display, (0,255,0), btnRect)
            if mouse.colliderect(btnRect):
                btn.fill((200,200,200))
                if pygame.mouse.get_pressed()[0] == 1:
                    
                    p = restart()
            else:
                btn.fill((150,150,150))

            x,y = btn.get_rect().center
            btn.blit(text, (x-text.get_width()/2, y-text.get_height()/2))
            
            display.blit(btn,((size[0]/2)-(btn.get_rect().width/2), (size[1]/2-(btn.get_rect().height/2))) )

    if mode == 'tutorial':
        font = pygame.font.SysFont('ArialBold', 100)
        text = font.render('TUTORIAL', True, (255,255,255))
        display.blit(text, ((size[0]/2)-(text.get_rect().width/2), 50))

        font = pygame.font.SysFont('ArialBold', 80)
        a = ['accelerates forward', 'rotates left', 'rotates right', 'shoots bullets']
        d = 150
        w = 0
        c = 20
        for i in ['W', 'A', 'D', 'SPACE']:
            text = font.render(i, True, (255,255,255))
            display.blit(text, (c, d))
            d += 50
            
            if text.get_rect().width > w:
                w = text.get_rect().width

        d = 150
        for i in a:
            i = ': ' + i
            text = font.render(i, True, (255,255,255))
            display.blit(text, (c + w, d))
            d += 50

        d += 50
        
        text = font.render("Break", True, (255,255,255))
        display.blit(text, (c,d))

        x = asteroid((75,75))
        x.image = pygame.image.load('imgs/asteroid.png')
        x.pos = (c + (text.get_rect().width) + 20,d-10)
        display.blit(x.render(), x.pos)

        text = font.render("'s with bullets", True, (255,255,255))
        display.blit(text, (c + x.pos[0] + x.render().get_width()-20,d))



    update(display, screen)
    display.fill((0,255,255))
    dt = clock.tick(60)