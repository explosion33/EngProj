import pygame

pygame.init()
size = (900,900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('C.I.T.R Game')
screen.fill((255,255,255))
pygame.display.flip()

mouse = pygame.Rect(0, 0, 2, 2)
enableInput = True
mode = 'game'

bckg = pygame.image.load('imgs/bckg.png')

class level(object):
    def __init__(self, scrollSpeed, bckg, platformList):
        self.scrlSpeed = scrollSpeed
        self.platformData = platformList

        self.scrlAmount = 0
        self.maxScroll = bckg.get_width()
        
        self.platforms = self.createPlatforms(self.platformData)

    
    def createPlatforms(self, platforms):
        lst = []
        for i in platforms:
            x = pygame.Rect(i[0]-self.scrlAmount, i[1], i[2], i[3])
            lst.append(x)
        return lst

    def update(self):
        self.platforms = self.createPlatforms(self.platformData)

    def drawBckg(self):
        x = self.scrlAmount
        screen.blit(bckg,(0-x,0))


    def drawPlatforms(self, color):
        for i in self.platforms:
            pygame.draw.rect(screen, color, i)

    def scroll(self):
        if self.scrlAmount + size[0] < self.maxScroll:
            self.scrlAmount += self.scrlSpeed
        self.update()
        
class player(object):
    def __init__(self, playersize):
        self.pos = (0,0)
        self.rect = pygame.Rect(self.pos, playersize)
        self.size = playersize
        self.velocity = (0,0)

        self.jumpx = 0
        self.jumping = False
        self.c = True

        self.x = 0
        self.y = 0
    
    def move(self, vel):
        x,y = vel

        self.pos = (self.pos[0] + x, self.pos[1] + y)

    def jump(self, height, speed):
        p = -256
        if self.jumping:
            if self.c:
                self.last = 0
                p = -((height/speed)**0.5)
                self.jumpx = p
                self.c = False

            y = -speed*((self.jumpx)**2) + height
            self.move((0,-(y-self.last)))
            self.last = y

            if self.jumpx >= 0:
                self.jumping = False
                self.c = True
            
            self.jumpx += 0.1


    def update(self):
        #update collision
        self.rect.topleft = (self.pos)

        #limit speed
        if self.x > 8: self.x = 8
        if self.x < -8: self.x = -8

        if self.y > 20: self.y = 20
        if self.y < -20: self.y = -20

        #check for jump
        self.jump(250,60)

        #check out of box
        if self.pos[1] + self.size[1] > size[1]: self.pos = (self.pos[0], size[1] - self.size[1])



    def collisionVert(self, platforms):
        for rect in platforms:
            if self.rect.colliderect(rect):
                print('True')
                if self.pos[1] + self.size[1] >= rect.top and self.pos[1] + self.size[1] <= rect.bottom:
                    if self.pos[1] + self.size[1] != rect.top + 1: self.pos = (self.pos[0], (rect.top +1) - self.size[1])

                    return 'platform'
        if self.pos[1] + self.size[1] >= size[1]:
            #x,y = self.pos
            #self.pos = (x,size[1] - self.size[1])
            #x,y = self.velocity
            #self.velocity = (x,0)
            return 'ground'
        return False

    def collisionHor(self, platforms):
        for rect in platforms:
            if self.rect.colliderect(rect):
                if self.pos[0] + self.size[0] >= rect.left and self.pos[0] + self.size[0] <= rect.right and self.collisionVert(platforms) != 'platform': # to the right of platfrom  but not on the other side of it and not on top of it
                    return 'right'
                if self.pos[0] <= rect.right and self.collisionVert(platforms) != 'platform':
                    return 'left'

    def draw(self, color):
        player = pygame.Surface(self.size)
        player.fill(color)
        screen.blit(player, self.pos)

        #pygame.draw.rect(screen, (255,0,0), self.rect)

    def getKeys(self):
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



platforms = [
    [800, 600, 400, 50]
]
level1 = level(1,bckg,platforms)
player1 = player((50,120))

while True:
    xm, ym = pygame.mouse.get_pos()
    mouse.center = (xm,ym)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #draw level
    level1.drawBckg()
    level1.drawPlatforms((0,0,255))

    #draw player
    player1.draw((0,255,0))

    #gravity
    if not player1.collisionVert(level1.platforms) and not player1.jumping:
        player1.y += 1
        player1.move((0,player1.y))
    
    else: player1.y = 0
    print(player1.pos, player1.collisionVert(level1.platforms))

    #move
    if 'd' in player1.getKeys() and player1.collisionHor(level1.platforms) != 'right':
        player1.x += 2
        player1.move((player1.x,0))
    elif 'a' in player1.getKeys() and player1.collisionHor(level1.platforms) != 'left':
        player1.x -= 2
        player1.move((player1.x,0))
    else:
        player1.x = -level1.scrlSpeed
        player1.move((player1.x, 0))

    #jump
    if 'space' in player1.getKeys() and (player1.collisionVert(level1.platforms) == 'platform' or player1.collisionVert(level1.platforms) == 'ground'):
            player1.jumping = True

    #update
    player1.update()

    #scroll level
    level1.scroll()
    

    pygame.display.flip()
    screen.fill((255,255,255))