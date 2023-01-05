from pygame import *
from math import *
from random import randint
from pprint import pprint
init()
x = mixer.music.load("Pics//winterTheme.wav")
mixer.music.play(-1)
res, xBlock, yBlock = 72, 14, 10
width, height = res * xBlock, res * yBlock
screen = display.set_mode((width, height))
# Creates a list with same dimensions as screen and all of its borders are marked
fileList = [['D' if int(yBlock / 2) == i or int(yBlock / 2) - 1 == i else 'B' for i in range(yBlock)]
            if j == 0 or j == xBlock - 1 else ['-' if 0 < i < yBlock - 1 else 'D'
if int(xBlock / 2) == j or int(xBlock / 2) - 1 == j else 'B' for i in range(yBlock)] for j in range(xBlock)]
# Creates list with empty middle, borders around and doorways in the middle of the borders
drawTemp = []  # Stores location of places where mouse has placed an object in file creation to make creating files
# easier
RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
myClock = time.Clock()
# rocks = [transform.scale(image.load('Pics//rock0' + str(i) + ".png"), (res, res)) for i in range(1, 2)]
rock1 = transform.scale(image.load("Pics//rock1.png"), (res, res))
rock2 = transform.scale(image.load("Pics//rock2.png"), (res, res))
rock3 = transform.scale(image.load("Pics//rock3.png"), (res, res))
rock4 = transform.scale(image.load("Pics//rock4.png"), (res, res))
iceCorner = transform.scale(image.load("Pics/IceCorner01.png"), (res, res))
iceWall = transform.scale(image.load("Pics/IceWall01.png"), (res, res))
gameOver = image.load("Pics/gameOver.png")
winText = image.load("Pics/winText.png")
counter = 0
blob1 = image.load("Pics//chaserSpriteList//sprite_0.png")
blob2 = image.load("Pics//chaserSpriteList//sprite_1.png")
blob3 = image.load("Pics//chaserSpriteList//sprite_2.png")
blob4 = image.load("Pics//chaserSpriteList//sprite_3.png")
blob = (blob1, blob2, blob3, blob4)
class Object:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sprite = iceCorner
        self.rect = Rect(x, y, w, h)

    def drawObject(self):
        #draw.rect(screen, RED, (self.x, self.y, self.w, self.h))
        screen.blit(self.sprite, Rect(self.x, self.y, self.w, self.h))


class Entity(Object):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.xVel = 0
        self.yVel = 0

    def trig(self, mx, my):
        self.rise = self.y - my
        self.run = self.x - mx
        self.angle = atan2(self.rise, self.run)
        # print(self.angle)
        draw.line(screen, GREEN, (mx, my), (self.x + self.w/2, self.y + self.h/2))


class ShooterEnemy(Entity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.health = 3

    def moveShooterEnemy(self, player):
        speed = 1.25
        if dist_collision(self, player, 300):
            if self.x > player.x:  # If enemy is further than 300 pixels, have it chase player
                self.x -= speed
            if self.x < player.x:
                self.x += speed
            if self.y > player.y:
                self.y -= speed
            if self.y < player.y:
                self.y += speed
        elif not dist_collision(self, player, 300):
            if self.x > player.x:  # If enemy is closer than 300 pixels, have it run from player
                self.x += speed
            if self.x < player.x:
                self.x -= speed
            if self.y > player.y:
                self.y += speed
            if self.y < player.y:
                self.y -= speed

    def shooterEnemyBullet(self, enemy_bullet_list, mx, my):
        # print(self.x, self.y)
        if counter % 60 == 0:
            enemy_bullet_list.append(Bullets(self.x, self.y, mx, my, (0, 255, 255)))


class Player(Entity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.ammo = 6
        self.counter = 20
        self.health = 12

    def movePlayer(self):
        velCap = 3.55
        velReduce = 0.01
        # print(self.xVel, self.yVel)
        self.xVel = round(self.xVel, 2)
        self.yVel = round(self.yVel, 2)
        self.x += self.xVel
        self.y += self.yVel
        if self.xVel > 0:
            self.xVel -= velReduce
        if self.xVel < 0:
            self.xVel += velReduce
        if self.yVel > 0:
            self.yVel -= velReduce
        if self.yVel < 0:
            self.yVel += velReduce
        if self.xVel >= velCap:
            self.xVel = velCap
        if self.yVel >= velCap:
            self.yVel = velCap
        if self.xVel <= -velCap:
            self.xVel = -velCap
        if self.yVel <= -velCap:
            self.yVel = -velCap

    def key_input(self, mx, my, mb, vel_increase, player_bullet_list, bullCount):
        keys = key.get_pressed()
        #fileWriting(keys, mx, my)
        if keys[K_w]:
            self.yVel -= vel_increase
        if keys[K_s]:
            self.yVel += vel_increase
        if keys[K_a]:
            self.xVel -= vel_increase
        if keys[K_d]:
            self.xVel += vel_increase
        if mb[0] and self.ammo > 0 and bullCount % 30 == 0:
            player_bullet_list.append(Bullets(self.x, self.y, mx, my, (0, 255, 255)))
            # self.ammo -= 1

    def drawPlayer(self, mx, my):
        # print(degrees(self.angle))
        draw.ellipse(screen, (255, 255, 255), (self.x, self.y, self.w, self.w))
        draw.ellipse(screen, (0, 0, 0), (self.x + self.w / 2 - 15, self.y + self.h/2 - 5, 2, 2))
        draw.ellipse(screen, (0, 0, 0), (self.x + self.w / 2 + 15, self.y + self.h/2 - 11, 2, 2))
        draw.arc(screen, (0, 0, 0), (self.x +5, self.y - 15, self.w - 10, self.w), pi * 4 / 3, 11 * pi / 6)
        # draw.polygon(screen, (175, 24, 25), ((self.x, self.y), (self.x+15, self.y), (self.w*cos(degrees(self.angle)), self.w*sin(degrees(self.angle)))))
    # def playerCollision(self, ene):
    #     for bullet in bulletList


class Bullets:
    def __init__(self, x, y, mx, my, col):
        self.x, self.y = x, y
        self.w, self.h = 25, 25
        self.col = col
        self.mx, self.my = mx, my
        self.bullet_speed = 15
        # self.bullet_speed_slowed = bullet_speed_slowed
        # if self.mx - x == 0:
        #     return
        self.angle = atan2((self.my - self.y), (self.mx - self.x))
        self.rise = sin(self.angle)
        self.run = cos(self.angle)

    def draw_bullets(self):
        draw.ellipse(screen, (255,255,255), (self.x, self.y, self.w, self.w))
        self.x += self.run * self.bullet_speed
        self.y += self.rise * self.bullet_speed


class Doorways(Object):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def drawDoorway(self):
        draw.rect(screen, (0,0,0), (self.x, self.y, self.w, self.h))

class Rock(Object):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.sprite = eval("rock" + str(randint(1, 4)))


class IceWalls(Object):
    def __init__(self, x, y, w, h, sprite):
        super().__init__(x, y, w, h)
        self.sprite = sprite


# ------------------------------------ Global functions ------------------------------------
def generateRooms(roomList, check):  # Creates
    check += 1
    if check > 500: # HOw many times the function recurses to determine length of rooms
        # print(roomList)
        return roomList
    xCode, yCode = 0, 0
    if randint(2, 3) % 2 == 0:
        xCode = randint(-2, -1)
        if xCode == -2:
            xCode = 1
    else:
        yCode = randint(-2, -1)
        if yCode == -2:
            yCode = 1
    roomList.append((roomList[-1][0] + xCode, roomList[-1][1] + yCode))
    for i in range(len(roomList)):
        if i == len(roomList) - 1:
            break
        if roomList[i] == roomList[-1]:
            roomList.pop() # basically a list of unique codes, and the difference in code determines where the doorways
            # are. If roomList[0] = (0,0) and roomlist[1] == (1,0) then theres a door to the right since its 1 + on
            # the x coordinate
    return generateRooms(roomList, check)


def doorWayRoute(rooms, doorways, playerDoorwayLocations):
    tempList = []
    backList = [] # Assigns all the doors and return doorways from the room list
    # Reverse doorway is the opposite of the previous room. This Fn assigns it as opposite and when its referencfed
    # elsewhere its always roomNum - 1.
    for i in range(1, len(rooms)):
        if rooms[i][0] > rooms[i - 1][0]:
            tempList.append((doorways.get("right"), playerDoorwayLocations.get("right")))
            backList.append((doorways.get("left"), playerDoorwayLocations.get("left")))
            # print("Right")
        elif rooms[i][0] < rooms[i - 1][0]:
            tempList.append((doorways.get("left"), playerDoorwayLocations.get("left")))
            backList.append((doorways.get("right"), playerDoorwayLocations.get("right")))
            # print("left")
        if rooms[i][1] > rooms[i - 1][1]:
            tempList.append((doorways.get("up"), playerDoorwayLocations.get("up")))
            backList.append((doorways.get("down"), playerDoorwayLocations.get("down")))
            # print("Up")
        elif rooms[i][1] < rooms[i - 1][1]:
            tempList.append((doorways.get("down"), playerDoorwayLocations.get("down")))
            backList.append((doorways.get("up"), playerDoorwayLocations.get("up")))
            # print("Down")
    return tempList, backList


def doorwayCollision(player, roomNum, doorRoute, backdoorRoute):
    if object_collision(player, doorRoute[roomNum][0]):  # If collides with a front door
        player.x = doorRoute[roomNum][1][0]  # Send the player to the right location
        player.y = doorRoute[roomNum][1][1]
        return roomNum + 1  # Increase room number
    if object_collision(player, backdoorRoute[roomNum - 1][0]) and roomNum > 0:  # If collides with back door
        player.x = backdoorRoute[roomNum - 1][1][0]  # Sends the player to the right location
        player.y = backdoorRoute[roomNum - 1][1][1]  # -1 since its the last rooms reverse door, not the current reverse
        return roomNum - 1  # Decreases room number
    return roomNum  # If neither then just return room number


def detect_object_collision(obj_1, obj_2):  # Quick func to check if 2 objects collide
    obj_1_rect = Rect(obj_1.x, obj_1.y, obj_1.w, obj_1.h)
    obj_2_rect = Rect(obj_2.x, obj_2.y, obj_2.w, obj_2.h)
    if Rect.colliderect(obj_1_rect, obj_2_rect):
        return True


def object_collision(obj_1, obj_2):  # Checks rect to rect collision of 2 objects, and prevents them from moving
    obj_1_rect = Rect(obj_1.x, obj_1.y, obj_1.w, obj_1.h)  # into one another
    obj_left_border = Rect(obj_2.x, obj_2.y + 2, 2, obj_2.h - 4)
    obj_right_border = Rect(obj_2.x + obj_2.w - 2, obj_2.y + 2, 2, obj_2.h - 4)
    obj_up_border = Rect(obj_2.x, obj_2.y, obj_2.w, 2)  # Narrow borders of the second object
    obj_down_border = Rect(obj_2.x, obj_2.y + obj_2.h - 2, obj_2.w, 2)
    # borders = [(obj_up_border, GREEN), (obj_down_border, GREEN), (obj_left_border, BLUE), (obj_right_border, BLUE)]
    # draw.rect(screen, BLACK, obj_down_border)
    # for i in range(len(borders)):  # Testing
    #     draw.rect(screen, borders[i][1], borders[i][0], 6)
    if Rect.colliderect(obj_1_rect, obj_left_border):
        obj_1.xVel = 0
        obj_1.x = obj_2.x - obj_1.w
        return True
    if Rect.colliderect(obj_1_rect, obj_right_border):
        obj_1.xVel = 0
        obj_1.x = obj_2.x + obj_2.w
        return True
    if Rect.colliderect(obj_1_rect, obj_up_border):
        obj_1.yVel = 0
        obj_1.y = obj_2.y - obj_1.h
        return True
    if Rect.colliderect(obj_1_rect, obj_down_border):
        obj_1.yVel = 0
        obj_1.y = obj_2.y + obj_2.h
        return True


# def cirToRectColl(circle, rect):
#     tempList = []
#     x, y, itr = 0, 0, 0
#     if rect.w == itr:
#         for i in tempList:
#             pass#if dist_collision(c)


def push_object(obj_1, obj_2):
    obj_1_rect = Rect(obj_1.x, obj_1.y, obj_1.w, obj_1.h)
    obj_left_border = Rect(obj_2.x, obj_2.y + 2, 2, obj_2.h - 4)
    obj_right_border = Rect(obj_2.x + obj_2.w - 2, obj_2.y + 2, 2, obj_2.h - 4)
    obj_up_border = Rect(obj_2.x, obj_2.y, obj_2.w, 2)
    obj_down_border = Rect(obj_2.x, obj_2.y + obj_2.h - 2, obj_2.w, 2)
    if Rect.colliderect(obj_1_rect, obj_left_border):
        obj_2.x += obj_1.xVel
    elif Rect.colliderect(obj_1_rect, obj_right_border):
        obj_2.x += obj_1.xVel
    elif Rect.colliderect(obj_1_rect, obj_up_border):
        obj_2.y += obj_1.yVel
    elif Rect.colliderect(obj_1_rect, obj_down_border):
        obj_2.y += obj_1.yVel


def dist_collision(obj_1, obj_2, rad):
    dist = sqrt((obj_1.x - obj_2.x) ** 2 + (obj_1.y - obj_2.y) ** 2)
    if dist > rad:
        return True
    if dist < rad:
        return False


def blitCorners():
    screen.blit(iceCorner, (0, 0))
    screen.blit(transform.rotate(iceCorner, 90), (0, height - res))
    screen.blit(transform.rotate(iceCorner, 180), (width - res, height - res))
    screen.blit(transform.flip(iceCorner, True, False), (width - res, 0))
    for i in range(1, xBlock - 1):
        screen.blit(iceWall, (i * res, 0))
        screen.blit(transform.flip(iceWall, False, True), (i * res, height - res))
    for i in range(1, yBlock - 1):
        screen.blit(transform.rotate(iceWall, 90), (0, i * res))
        screen.blit(transform.rotate(iceWall, 270), (width - res, i * res))


def gridDisplay():  # Temp to help create levels
    for i in range(0, height, res):
        draw.line(screen, RED, (0, i), (width, i))
    for i in range(0, width, res):
        draw.line(screen, RED, (i, 0), (i, height))
    # draw.rect(screen, BLUE, Rect(0,0,255,255))


def fileWriting(keys, mx, my):
    global fileList
    global drawTemp
    # Func to make creating rooms easier
    row, col = int(mx / res), int(my / res)
    # print(row, col)
    for box in drawTemp:
        draw.rect(screen, box[1], box[0])
    if keys[K_r]:
        fileList[row][col] = "r"
        drawTemp.append((Rect(row * res, col * res, res, res), BLUE))
    if keys[K_s]:
        fileList[row][col] = "s"
        drawTemp.append((Rect(row * res, col * res, res, res), RED))
    # pprint(fileList)
    if keys[K_SPACE]:
        newFile = open("Levels/updown1.txt", "w")
        pprint(fileList)
        for row in fileList:
            for col in row:
                newFile.write(f"{col},")
            newFile.write(f"\n")
        newFile.close()
        quit()
    #gridDisplay()


def readFile(file, blocks):
    returnList = []
    text = file.readlines()
    for i in range(len(text)):
        text[i] = text[i].split(",")
        text[i].pop()
    # pprint(text)
    # Reads flies and then generates a list of objects from what is read
    for r in range(len(text)):
        for c in range(len(text[r])):
            for key in blocks.keys():
                if text[r][c] == key:
                    # print(blocks.get(key))
                    returnList.append((blocks.get(key)(r * res, c * res, res, res)))
                    # print(returnList)
    return returnList


def findRoomObjects(roomNum, doorRoute, backdoorRoute, blocks, doorways):
    # print(f"Door Route{doorRoute}")
    # return readFile(open("Levels/lvl_0" + str(0) + ".txt"), blocks)
    # print(f"backDoorRoute{backdoorRoute}")
    if roomNum == 0:
        return readFile(open("Levels/lvl_00.txt"), blocks)
    for i in doorways:
        if doorRoute[roomNum][0] == doorways.get(i):
            for j in doorways:
                if backdoorRoute[roomNum - 1][0] == doorways.get(j):
                    try:
                        return readFile(open("Levels/" + str(j) + str(i) + str(randint(0,1)) + ".txt"), blocks)
                    except:
                        return readFile(open("Levels/" + str(i) + str(j) + str(randint(0,1)) + ".txt"), blocks)
                    # return readFile(open("Levels/lvl_0" + str(1) + ".txt"), blocks)
    return readFile(open("Levels/lvl_0" + str(1) + ".txt"), blocks)
    # if doorRoute[roomNum] == doorways.get("up") and backdoorRoute[roomNum - 1] == doorways.get("down"):
    #     return readFile(open("Levels/lvl_0" + str(roomNum) + ".txt"), blocks)

def checkBorder(player):
    n = 10
    if player.x < res - n:
        player.x = res - n
    if player.x + player.w > width - res - n:
        player.x = width - res - n
    if player.y + player.h > height - res - n:
        player.y = height - res - n
    if player.y < res - n:
        player.y = res - n

def main():
    global counter
    player_bullet_list = []
    enemy_bullet_list = []
    player = Player(150, 150, res, res)
    #enemy = ShooterEnemy(50, 50, 90, 90)
    running = True
    bullCount = 0
    roomNum, oldRoomNum = 0, 0
    rooms = generateRooms([(0, 0)], 0)
    win = len(rooms) - 2
    doorways = {"up": Doorways(width / 2 - res, 0, 2 * res, res),
                "down": Doorways(width / 2 - res, height - res, 2 * res, res),
                "left": Doorways(0, height / 2 - res, res, 2 * res),
                "right": Doorways(width - res, height / 2 - res, res, 2 * res)}
    playerDoorwayLocation = {"up": (width / 2, height - 2 * res),  # Where player is warped once they enter a doorway
                             "down": (width / 2, res * 2),  # Same keys as doorways to make it easier
                             "left": (width - res * 2, height / 2),  # to link with both
                             "right": (res * 2, height / 2)}
    borders = [Object(0, 0, res*6, res), Object(res*8, 0, res*6, res),
               Object(0, height - res, res*6, res), Object(res*8, height - res, res*6, res),
               Object(0, res, res, res*3), Object(0, res*6, res, res*3),
               Object(width-res, res, res, res*3), Object(width-res, res*6, res, res*3)]
    blocks = {"r": Rock,
              "s": ShooterEnemy}
    # print(roomObjects)
    doorRoute, backdoorRoute = doorWayRoute(rooms, doorways, playerDoorwayLocation)[0], \
                               doorWayRoute(rooms, doorways, playerDoorwayLocation)[1]
    roomObjects = findRoomObjects(roomNum, doorRoute, backdoorRoute, blocks,
                                  doorways)
    gameMode = "game"
    counts = width / 1.2
    blobtime = 0
    while running:
        # print(roomNum)
        blobtime += 0.2
        if blobtime > 3: # Spaghetti
            blobtime = 0
        counter += 1
        bullCount += 1
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                player_bullet_list.append(Bullets(player.x, player.y, mx, my, (255, 0, 255)))
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        if player.health <= 0:
            gameMode = "dead"
            print("GameOver")
        if roomNum == win:
            print("wee")
            gameMode = "win"
        if gameMode == 'dead':
            mixer.music.stop()
            counts -= 5
            draw.circle(screen, (0, 0, 0), (width / 2, height / 2), counts, 5)
            if counts < 0:
                screen.blit(gameOver, (200, height - 500))
        if gameMode == "win":
            mixer.music.stop()
            counts -= 5
            draw.circle(screen, (255, 255, 255), (width / 2, height / 2), counts, 5)
            if counts < 0:
                screen.blit(winText, (300, height - 450))
        if gameMode == "game":
            screen.fill((200, 200, 255))

            # screen.blit(rocks[0], (0, 0, res, res))
            #  ----- Drawing -----
            blitCorners()
            for i in borders:
                object_collision(player,i)
            # readFile(open("Levels/lvl_0" + str(roomNum) + ".txt", 'r'), blocks)
            roomNum = doorwayCollision(player, roomNum, doorRoute, backdoorRoute)
            if roomNum != oldRoomNum:
                roomObjects = findRoomObjects(roomNum, doorRoute, backdoorRoute, blocks,
                                              doorways)
            for i in roomObjects:
                if isinstance(i, ShooterEnemy):
                    ShooterEnemy.shooterEnemyBullet(i, enemy_bullet_list, player.x, player.y)
                    # ShooterEnemy.drawObject(i)
                    print(blobtime)
                    screen.blit(blob[int(blobtime)], (i.x, i.y))
                    ShooterEnemy.moveShooterEnemy(i, player)
                    checkBorder(i)
                    for j in roomObjects:
                        if isinstance(j, Rock):
                            object_collision(i, j)
                    for j in player_bullet_list:
                        if detect_object_collision(i, j):
                            i.health -= 1
                            player_bullet_list.pop(player_bullet_list.index(j))
                            if i.health <= 0:
                                roomObjects.pop(roomObjects.index(i))
                if isinstance(i, Rock): # checks if item in room object mathces class, then does respective Fns
                    Object.drawObject(i)
                    object_collision(player, i)
                    for j in player_bullet_list:
                        if detect_object_collision(i, j):
                            player_bullet_list.pop(player_bullet_list.index(j))
                    for j in enemy_bullet_list:
                        if detect_object_collision(i, j):
                            enemy_bullet_list.pop(enemy_bullet_list.index(j))
            for i in borders:
                for j in player_bullet_list:
                    if detect_object_collision(i, j):
                        player_bullet_list.pop(player_bullet_list.index(j))
                for j in enemy_bullet_list:
                    if detect_object_collision(i, j):
                        enemy_bullet_list.pop(enemy_bullet_list.index(j))
            # print(doorRoute[roomNum][0])
            Doorways.drawDoorway(doorRoute[roomNum][0])
            if roomNum > 0:
                Doorways.drawDoorway(backdoorRoute[roomNum - 1][0])
            # for i in doorways.keys():
            #     Object.drawObject(doorways.get(i))

            for i in player_bullet_list:
                Bullets.draw_bullets(i)
            for i in enemy_bullet_list:
                Bullets.draw_bullets(i)
                if detect_object_collision(player, i):
                    player.health -= 1
                    enemy_bullet_list.pop(enemy_bullet_list.index(i))
            player.trig(mx, my)
            player.movePlayer()
            player.drawPlayer(mx, my)
            player.key_input(mx, my, mb, 0.5, player_bullet_list, bullCount)
            #checkBorder(player)
            oldRoomNum = roomNum
            # print(roomNum, win)
            # for i in borders:
            #     Object.drawObject(i)
            # player.health = 10
        myClock.tick(60)
        display.flip()


main()
quit()
