from pygame import *
from math import *
from random import randint
from pprint import pprint

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
rocks = transform.scale(image.load("Pics//IceCorner01.png"), (res, res))
iceCorner = transform.scale(image.load("Pics/IceCorner01.png"), (res, res))
iceWall = transform.scale(image.load("Pics/IceWall01.png"), (res, res))


class Object:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sprite = iceCorner
        self.rect = Rect(x, y, w, h)

    def drawObject(self):
        draw.rect(screen, RED, (self.x, self.y, self.w, self.h))
        screen.blit(self.sprite, Rect(self.x, self.y, self.w, self.h))


class Entity(Object):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.xVel = 0
        self.yVel = 0

    def trig(self, mx, my):
        self.rise = my - self.y
        self.run = mx - self.x
        self.angle = atan2(self.rise, self.run)
        draw.line(screen, BLUE, (mx, my), (self.x, self.y))


class ShooterEnemy(Entity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

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


class Player(Entity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.ammo = 6
        self.counter = 20

    def movePlayer(self):
        velCap = 1.55
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
        fileWriting(keys, mx, my)
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

    def drawPlayer(self):
        draw.circle(screen, (255, 255, 255), (self.x, self.y), self.w)

    # def playerCollision(self, ene):
    #     for bullet in bulletList


class Bullets:
    def __init__(self, x, y, mx, my, col):
        self.x, self.y = x, y
        self.width, self.height = 25, 25
        self.col = col
        self.mx, self.my = mx, my
        self.bullet_speed = 25
        # self.bullet_speed_slowed = bullet_speed_slowed
        # if self.mx - x == 0:
        #     return
        self.angle = atan2((self.my - self.y), (self.mx - self.x))
        self.rise = sin(self.angle)
        self.run = cos(self.angle)

    def draw_bullets(self):
        draw.rect(screen, self.col, (self.x, self.y, self.width, self.height))
        self.x += self.run * self.bullet_speed
        self.y += self.rise * self.bullet_speed


def remove_bullets(enemy_list, player_bullet_list, entity_list):
    for player_bullet in player_bullet_list:
        for enemy in enemy_list:
            if object_collision(player_bullet, enemy):
                player_bullet_list.pop(player_bullet_list.index(player_bullet))
                enemy_list.pop(enemy_list.index(enemy))
        for lists in entity_list:
            for objects in lists:
                if detect_object_collision(player_bullet, objects):
                    player_bullet_list.pop(player_bullet_list.index(player_bullet))


class Doorways(Object):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)


class Rock(Object):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.sprite = rocks


class IceWalls(Object):
    def __init__(self, x, y, w, h, sprite):
        super().__init__(x, y, w, h)
        self.sprite = sprite


# ------------------------------------ Global functions ------------------------------------
def generateRooms(roomList):
    if len(roomList) > 10:
        print(roomList)
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
            roomList.pop()
    return generateRooms(roomList)


def doorWayRoute(rooms,doorways):
    tempList = []
    for i in range(1, len(rooms)):
        if rooms[i][0] > rooms[i - 1][0]:
            tempList.append(doorways.get("right"))
            print("Right")
        elif rooms[i][0] < rooms[i - 1][0]:
            tempList.append(doorways.get("left"))
            print("left")
        if rooms[i][1] > rooms[i - 1][1]:
            tempList.append(doorways.get("up"))
            print("Up")
        elif rooms[i][1] < rooms[i - 1][1]:
            tempList.append(doorways.get("down"))
            print("Down")
    return tempList

def doorwayCollision(player, doorways, roomNum, playerDoorwayLocation, rooms):
    for i in doorways:
        if object_collision(player, doorways.get(i)):
            player.x = playerDoorwayLocation.get(i)[0]
            player.y = playerDoorwayLocation.get(i)[1]
            return roomNum + 1
    return roomNum


def detect_object_collision(obj_1, obj_2):
    obj_1_rect = Rect(obj_1.x, obj_1.y, obj_1.w, obj_1.h)
    obj_2_rect = Rect(obj_2.x, obj_2.y, obj_2.w, obj_2.h)
    if Rect.colliderect(obj_1_rect, obj_2_rect):
        return True


def object_collision(obj_1, obj_2):
    obj_1_rect = Rect(obj_1.x, obj_1.y, obj_1.w, obj_1.h)
    obj_left_border = Rect(obj_2.x, obj_2.y + 2, 2, obj_2.h - 4)
    obj_right_border = Rect(obj_2.x + obj_2.w - 2, obj_2.y + 2, 2, obj_2.h - 4)
    obj_up_border = Rect(obj_2.x, obj_2.y, obj_2.w, 2)
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
    row, col = int(mx / res), int(my / res)
    # print(row, col)
    for box in drawTemp:
        draw.rect(screen, box[1], box[0])
    if keys[K_r]:
        fileList[row][col] = "r"
        drawTemp.append((Rect(row * res, col * res, res, res), BLUE))
    # pprint(fileList)
    if keys[K_SPACE]:
        newFile = open("Levels/new.txt", "w")
        pprint(fileList)
        for row in fileList:
            for col in row:
                newFile.write(f"{col},")
            newFile.write(f"\n")
        newFile.close()
        quit()
    gridDisplay()


def readFile(file, blocks):
    returnList = []
    text = file.readlines()
    for i in range(len(text)):
        text[i] = text[i].split(",")
        text[i].pop()
    pprint(text)
    for r in range(len(text)):
        for c in range(len(text[r])):
            for key in blocks.keys():
                if text[r][c] == key:
                    returnList.append(Object(r * res, c * res, res, res))
    return returnList


def main():
    player_bullet_list = []
    player = Player(50, 50, 30, 30)
    enemy = ShooterEnemy(50, 50, 90, 90)
    running = True
    bullCount = 0
    roomNum = 0
    rooms = generateRooms([(0, 0)])
    doorways = {"up": Object(width / 2 - res, 0, 2 * res, res),
                "down": Object(width / 2 - res, height - res, 2 * res, res),
                "left": Object(0, height / 2 - res, res, 2 * res),
                "right": Object(width - res, height / 2 - res, res, 2 * res)}
    playerDoorwayLocation = {"up": (width / 2, height - 2 * res),  # Where player is warped once they enter a doorway
                             "down": (width / 2, res * 2),  # Same keys as doorways to make it easier
                             "left": (width - res * 2, height / 2),  # to link with both
                             "right": (res * 2, height / 2)}
    blocks = {"r": Rock(0, 0, res, res),
              }
    roomObjects = readFile(open("Levels/new.txt", 'r'), blocks)
    # print(roomObjects)
    doorRoute = doorWayRoute(rooms, doorways)
    while running:
        # print(roomNum)
        bullCount += 1
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                player_bullet_list.append(Bullets(player.x, player.y, mx, my, (255, 0, 255)))
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.fill((0, 0, 0))
        # screen.blit(rocks[0], (0, 0, res, res))
        #  ----- Drawing -----
        # blitCorners()
        for i in roomObjects:
            print(i.x, i.y)
        Object.drawObject(doorRoute[roomNum])
        roomNum = doorwayCollision(player, doorways, roomNum, playerDoorwayLocation, rooms)
        # for i in doorways.keys():
        #     Object.drawObject(doorways.get(i))
        # Object.drawObject()
        player.drawPlayer()
        enemy.drawObject()
        enemy.moveShooterEnemy(player)
        for i in player_bullet_list:
            Bullets.draw_bullets((i))

        player.trig(mx, my)
        player.movePlayer()
        player.key_input(mx, my, mb, 0.5, player_bullet_list, bullCount)

        myClock.tick(60)
        display.flip()


main()
quit()
