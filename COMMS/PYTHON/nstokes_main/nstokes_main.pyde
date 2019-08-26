add_library('serial')
add_library('opencv_processing')

import fluid as Fluid
from easing_functions import *
from random import randint 
from time import sleep, time
import math
import struct
from threading import Thread

#GLOBAL VARIABLES FOR NAVIER_STOKES
WIDTH = 40
D_RATE = 0.05
VISCOSITY = 0.8
TIME_SPACE = 0.0001

#GLOBAL GRID 
GRID =[]
FLUID = Fluid.fluid(WIDTH, D_RATE, VISCOSITY, TIME_SPACE)

#Velocity and Density Fields
SIZE = (WIDTH+2)**2
VEL_HPREV = [0] * SIZE
VEL_H = [0 for _ in xrange(SIZE)]
VEL_VPREV = [0] * SIZE
VEL_V = [0 for _ in xrange(SIZE)]
DENS = [0 for _ in xrange(SIZE)]
DENS_PREV = [0] * SIZE

#Serial Connection
magnetPort = None
magnetPort2 = None
# Macbook
# magnetPortAddresses = [u'/dev/cu.usbmodem58040401',
#                u'/dev/cu.usbmodem49270001',
#                u'/dev/cu.usbmodem58130601',
#                u'/dev/cu.usbmodem43318101',
#                u'/dev/cu.usbmodem43318001']
# Mac Mini
magnetPortAddresses = [u'/dev/cu.usbmodem5804040',
               u'/dev/cu.usbmodem4927000',
               u'/dev/cu.usbmodem5813060',
               u'/dev/cu.usbmodem4331810',
               u'/dev/cu.usbmodem4331800']
magnetPorts = []
INITIALIZED = False
MAGNET_CONNECTION = False

STARTING = 0
sf = 1

#TOGGLES
SNEK_TOGGLE = False
EASING_TOGGLE = False
TEST_TOGGLE = False
ON_TOGGLE = False
MORPH_TOGGLE = True
BLACK_OUT = False
testIndex = WIDTH + 1

def genrandi(maxn, num):
    newi = randint(0, maxn)
    while(newi == num):
        newi = randint(0, maxn)
    return newi

#Snake Globals
fcx = randint(0, WIDTH)
fcy = randint(0, WIDTH)
nax = genrandi(WIDTH, fcx)
nay = genrandi(WIDTH, fcy)
scx = randint(0, WIDTH)
scy = randint(0, WIDTH)
nax1 = randint(0, WIDTH)
nay1 = randint(0, WIDTH)

s_tracker = []

#Morphing
render = []
shape0 = []
shape1 = []

state = False
morph_refresh = True

pset_0 = None
cset_0 = None
pset_1 = None
cset_1 = None

img_idx = 0
rand_lt = [0.003, 0.005, 0.0008]
randspeed = 0.001 

#EASING Globals
FadeBox = [0 for _ in range(SIZE)]
ease_range = easelist()
FrameIndex = 0
ease_initiated = False 
sign = -1

def sendSerial(infosend, port):
    global magnetPorts

    # print(infosend,port)
    if infosend != None:
        # print("sending to", port)
        try:
            # as byte message
            msg = byteConverter(infosend)
            magnetPorts[port].write(msg)
            
            # as single sends
            # for i in infosend:
            #     magnetPorts[port].write(i)

            magnetPorts[port].write(255)
        except:
            print("error in send", port)
            
def byteConverter(inlist):
    byteMessage = ''
    for idx, i in enumerate(inlist):
        try:
            byteMessage+=chr(int(round(i)))
        except:
            print("BAD NUMBER", i, idx)
            byteMessage+=chr(int(round(0.0)))
            
    return byteMessage

# Send
# sendThread = Thread(target = sendSerial, args = [None])
busyCount = 0
openCount = 0
startTime = time()
startFrame = 0

def reordinator(initial_list):
    reordered_list = []
    
    for panel_y in range(5):
        for panel_x in range(5):
            for quad_y in range(2):
                for quad_x in range(2):
                    for mag_y in  range(4):
                        for mag_x in range(4):
                            index = mag_x + mag_y * 40 + quad_x * 4 + quad_y * 160 + panel_x * 8 + panel_y * 320
                            reordered_list.append(initial_list[index])
                            
    return reordered_list
    # return initial_list

def setup():
    global FLUID, GRID, WIDTH, D_RATE, VISCOSITY, TIME_SPACE, sf, w, yvalues
    background(0)
    size(WIDTH + 2, WIDTH + 2)

    #Initializing the Navier Stokes grid.
    GRID = makeGrid(WIDTH)
     
    #Generating coordinates for snake movements.
    snake(WIDTH)
    frameRate(30)
    strokeWeight(0)
    smooth(2)

ramp_up = True
power = 0

timer = randint(750, 1500)
state = 0

def draw():
    global BLACK_OUT, state, timer, FrameIndex, sign, ease_initiated, EASING_TOGGLE, MORPH_TOGGLE, rand_lt, randspeed, img_idx, morph_refresh, src, state, render, shape0, shape1, pset_0, cset_0, pset_1, pset_1, src_cv, det_cv, ramp_up, power, testIndex, TEST_TOGGLE, s_tracker, MAGNET_CONNECTION, INITIALIZED, magnetPort, randposX, randposY, GRID, WIDTH, D_RATE, VISCOSITY, TIME_SPACE, VEL_H, VEL_HPREV, VEL_V, VEL_VPREV, DENS, DENS_PREV, STARTING, BUBBLE_TOGGLE, SNEK_TOGGLE, AMOEBA_TOGGLE, sf, sendThread, busyCount, openCount, startTime, startFrame
    
    background(0)
    
    if timer <= 0:
        if SNEK_TOGGLE or MORPH_TOGGLE:
            EASING_TOGGLE = True
            
        if BLACK_OUT:
            BLACK_OUT = False
            
            if state:
                MORPH_TOGGLE = True
                # this.surface.setSize(WIDTH + 2, WIDTH + 2)   
            else:
                SNEK_TOGGLE = True
                # this.surface.setSize(WIDTH + 2, WIDTH + 2)
                
        timer += randint(750, 1500)
    
    if SNEK_TOGGLE == True:
        timer -= 2
     
    if MORPH_TOGGLE == True:
        timer -= 1
    
    if BLACK_OUT == True:
        timer -= 4
    
    if EASING_TOGGLE:
        if SNEK_TOGGLE:
            SNEK_TOGGLE = False
            state = 1
            
        if MORPH_TOGGLE:
            MORPH_TOGGLE = False
            state = 0

        if not ease_initiated:
            print("Easing Initiated")
            for i in range(WIDTH):
                for j in range(WIDTH):
                    a = QuadEaseInOut(start=DENS[FLUID.xy_coordinate(WIDTH, i + 1, j + 1)], end= 0, duration= 15)

                    y0 = list(map(a.ease, ease_range))
                    y0.reverse()
                    # y0.extend(reversed(y0))
                    # print(y0)
                    
                    FadeBox[FLUID.xy_coordinate(WIDTH, i + 1, j + 1)] =  y0
            
            FrameIndex = len(ease_range) - 1
            
            ease_initiated = True
            
        if FrameIndex:
            # print("Easing in Process")
            for i in range(WIDTH):
                for j in range(WIDTH):
                    DENS[FLUID.xy_coordinate(WIDTH, i + 1, j + 1)] =  FadeBox[FLUID.xy_coordinate(WIDTH, i + 1, j + 1)][FrameIndex]
            
            FrameIndex -= 1
           
        else:
            ease_initiated = False
            EASING_TOGGLE = not EASING_TOGGLE
            BLACK_OUT = True
    
    print("Timer: %d, SNEK: %d, MORPH: %d, BLACK: %d, EASE: %d " % (timer, SNEK_TOGGLE, MORPH_TOGGLE, BLACK_OUT, EASING_TOGGLE))
        
    if MORPH_TOGGLE:
        translate(1, 1)
        totalDistance = 0
        
        if morph_refresh:
            set_morphing()
            randspeed = rand_lt[randint(0, len(rand_lt) - 1)]

        for i in range(len(render)):
            # Are we lerping to the circle or square?
            if state:
                v1 = shape0[i]
                render = shape1
            else:
                v1 = shape1[i]
                render = shape0
            
            # Get the vertex we will draw.
            v2 = render[i]
            
            # Lerp to the target
            # print(v1, v2)
            v2.lerp(v1, randspeed)
    
            # Check how far we are from target.
            totalDistance += PVector.dist(v1, v2)
    
        # # If all the vertices are close, switch shape.
        if totalDistance < 100:
            img_idx += 1
            morph_refresh = True
            
        print(totalDistance)
    
        # Draw a polygon that makes up all the vertices
        beginShape()
        fill(127)
        for vector in render:
            vertex(vector.x, vector.y)
        endShape()
        
        loadPixels()
        
        DENS = [(p & 255) / float(255) for p in pixels]
        
    #Snake movement Generation: when the toggle is on, the position coordinates for the snake are generated based on bezier curves stitching. 
    if SNEK_TOGGLE:
        snake_length = 3
        st = frameCount % (len(s_tracker) - snake_length)
        
        if st == 0:
            s_tracker = []
            snake(WIDTH)
            
        else:
            for i in range(snake_length):
                x = int(s_tracker[st + i][0])
                y = int(s_tracker[st + i][1])

                bright = 1
                DENS[FLUID.xy_coordinate(WIDTH, x + 1, y + 1)] += bright
                
            # for i in range(snake_length, 0, -1):
            #     x = int(s_tracker[st - i][0])
            #     y = int(s_tracker[st - i][1])
                
            #     DENS[FLUID.xy_coordinate(WIDTH, x + 1, y + 1)] -= bright / (snake_length + 1 - i)
    
    if TEST_TOGGLE:
        if frameCount % 2 == 0:
            # print("Index %d On" % testIndex)
            DENS[testIndex - 1] = 0
            DENS[testIndex] = 1
            testIndex+=1
            
    # if(frameCount % 100 == 0):
    #     VEL_H, VEL_V, VEL_HPREV, VEL_VPREV = FLUID.velocity_step(WIDTH, VEL_H, VEL_V, VEL_HPREV, VEL_VPREV, VISCOSITY, TIME_SPACE)
        
    DENS, DENS_PREV = FLUID.density_step(WIDTH, DENS, DENS_PREV, VEL_H, VEL_V, D_RATE, TIME_SPACE) 
    
    # if frameCount % 1 == 0 :
        
    if not MORPH_TOGGLE:   
        for i in xrange(WIDTH):
            for j in xrange(WIDTH):
                DENS[FLUID.xy_coordinate(WIDTH, i + 1, j + 1)] -= 0.002
                
        reset_gridcells()
        display_grid()
        
    #Write to Arduino
    if MAGNET_CONNECTION:
        if not INITIALIZED:
            initialize_port()
        
        carr = count()
        # reordered_list = reordinator(carr)
        
        # testing
        iterator = ((frameCount / 3) %  64)
        reordered_list = []
        for i in range(5):
            for i in range(40):
                appender = [i]*8
                reordered_list.extend(appender)
        # reordered_list.extend([0]*(320*4))
        # reordered_list[iterator] = 127
        # print(len(reordered_list))
        # print(reordered_list)
        print(frameCount, frameRate)
        
        sendSerial(reordered_list[0:320], 0)
        sendSerial(reordered_list[320:640], 1)
        sendSerial(reordered_list[640:960], 2)
        sendSerial(reordered_list[960:1280], 3)
        sendSerial(reordered_list[1280:1600], 4)
        
        # t0 = Thread(target=sendSerial, args=[reordered_list[0:320], 0])
        # t1 = Thread(target=sendSerial, args=[reordered_list[320:640], 1])
        # t2 = Thread(target=sendSerial, args=[reordered_list[640:960], 2])
        # t3 = Thread(target=sendSerial, args=[reordered_list[960:1280], 3])
        # t4 = Thread(target=sendSerial, args=[reordered_list[1280:1600], 4])

        # t0.start()
        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        # t0.join()
        # t1.join()
        # t2.join()
        # t3.join()
        # t4.join()
        
        # sendSerial(msg_check[0:320], 0)
        # sendSerial(byteMessage)
        nowTime = time()
        if nowTime - startTime >= 1.0:
            # print(nowTime - startTime, frameCount - startFrame, frameCount, reordered_list[0])
            startTime = nowTime
            startFrame = frameCount
        # magnetPort.clear()
        # print(frameCount)
        # thread logic
        # if sendThread.isAlive():
        #         busyCount += 1
        #         openCount = 0
        #         print("Thread BUSY", busyCount)
        #         pass
        # else:
        #     # print("regular")
        #     sendThread = Thread(target = sendSerial, args = [byteMessage])
        #     sendThread.start()
        #     busyCount = 0
        #     openCount += 1
        #     print("OPEN Thread", openCount)
        #     # print("Thread GOOD!", busyCount)

def keyPressed():
    global testIndex, MORPH_TOGGLE, ON_TOGGLE, TEST_TOGGLE, DENS, DENS_PREV, VEL_H, VEL_V, VEL_HPREV, VEL_VPREV, BUBBLE_TOGGLE, SNEK_TOGGLE, D_RATE, MAGNET_CONNECTION
    
    if ((key == 'R') or (key == 'r')):
        DENS = [0 for _ in xrange(SIZE)]
        DENS_PREV = [0 for _ in xrange(SIZE)]
        VEL_H = [0 for _ in xrange(SIZE)]
        VEL_HPREV = [0 for _ in xrange(SIZE)]
        VEL_V = [0 for _ in xrange(SIZE)]
        VEL_VPREV = [0 for _ in xrange(SIZE)]
        
    if ((key == 'D') or (key == 'd')):
        center_x = mouseX // sf
        center_y = mouseY // sf
        
        DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y + 1)] = 100
        
    if ((key == 'F') or (key == 'f')):
        center_x = mouseX // sf
        center_y = mouseY // sf
        
        bval = 100
        DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y + 1)] += bval
        DENS[FLUID.xy_coordinate(WIDTH, center_x, center_y + 1)] += bval
        DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y)] += bval
        DENS[FLUID.xy_coordinate(WIDTH, center_x + 2, center_y + 1)] += bval
        DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y + 2)] += bval
          
    if ((key == 'S') or (key == 's')):
        D_RATE = 0.05
        SNEK_TOGGLE = not SNEK_TOGGLE
        
        if SNEK_TOGGLE:
            print("SNAKE ON")
        else:
            print("SNAKE OFF")
    
    if ((key == 'C') or (key == 'c')):
        MAGNET_CONNECTION = not MAGNET_CONNECTION
        
        if MAGNET_CONNECTION:
            print("MAGNET CONNECTION ON")
        else:
            print("MAGNET CONNECTION OFF")
    
    if ((key == 'M') or (key == 'm')):
        MORPH_TOGGLE = not MORPH_TOGGLE
        
        if MORPH_TOGGLE:
            print("MORPH ON")
        else:
            print("MORPH OFF")
    
    if ((key == 'N') or (key == 'n')):
        center_x = mouseX // sf
        center_y = mouseY // sf

        for i in easelist():
            DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y + 1)] = i
            
    if ((key == 'T') or (key == 't')):
        TEST_TOGGLE = not TEST_TOGGLE
        testIndex = WIDTH + 1 
        D_RATE = 0.0
        
        if TEST_TOGGLE:
            print("TESTING ON")
        else:
            DENS = [0 for _ in xrange(SIZE)]
            print("TESTING OFF")
            
    if ((key == 'O') or (key == 'o')):
        ON_TOGGLE = not ON_TOGGLE
        D_RATE = 0.0
        
        if ON_TOGGLE:
            DENS = [1 for _ in xrange(SIZE)]
            print("ALL MAGNETS ON")
        else:
            DENS = [0 for _ in xrange(SIZE)]
            print("ALL MAGNETS OFF")

def ratio(x):
    # return (x / 2)
    if(x < 0):
        return 0
    elif (x * 128) > 127:
        return 127
    else:
        return int(x * 128)
    
def count():
    global DENS, WIDTH, FLUID 
    counter = []
    
    # current counter - goes left to right, then top to bottom
    for j in range(WIDTH):
        for i in range(WIDTH):
            counter.append(ratio(DENS[FLUID.xy_coordinate(WIDTH, i + 1, j + 1)]))

    return counter

def reset_gridcells():
    global DENS, WIDTH, GRID
    for i in xrange(WIDTH):
        for j in xrange(WIDTH):
            GRID[i][j] = Cell(i*sf,j*sf,sf, sf, DENS[FLUID.xy_coordinate(WIDTH, i + 1, j + 1)])
    
def makeGrid(wth):
    global GRID 
    for i in xrange(wth):
        # Create an empty list for each row
        GRID.append([])
        for j in xrange(wth):
            # Pad each column in each row with a 0
            GRID[i].append(0)
            
    return GRID

def display_grid():
    global GRID, WIDTH
    for i in xrange(WIDTH):
        for j in xrange(WIDTH):
            if GRID[i][j].tempDens > 0.1:
                GRID[i][j].display()

class Cell():
    def __init__(self, tempX, tempY, tempW, tempH, tempDens):
        self.x = tempX
        self.y = tempY
        self.w = tempW
        self.h = tempH
        self.tempDens = tempDens
        
    def display(self):
        noStroke()
        fill(0, self.tempDens * 255, 0)
        rect(self.x,self.y,self.w,self.h)

#Port Initialization
def initialize_port():
    global INITIALIZED, magnetPort, magnetPort2, magnetPortAddresses, magnetPorts
    print(Serial.list())
    # arduinoPort = Serial.list()[3]
    # magnetPort = Serial(this, arduinoPort, 1000000)
    # magnetPort = Serial(this, u'/dev/cu.usbmodem58040401', 1000000)
    # magnetPort = Serial(this, magnetPortAddresses[1], 1000000)

    # magnetPort2 = Serial(this, Serial.list()[4], 1000000)
    # magnetPort = Serial(this, arduinoPort, 115200)
    for each in magnetPortAddresses:
        serialPort = Serial(this, each, 1000000)
        magnetPorts.append(serialPort)

    
    INITIALIZED = True

def snake(w):
    global nax, nay, fcx, fcy, scx, scy, nax1, nay1, s_tracker
    
    m = (float(nay) - fcy) / (float(nax) - fcx)
    b = nay - (m * nax)
    scx = nax - (fcx - nax)
    scy = m * scx + b
    
    fcx = randint(0, w) 
    fcy = randint(0, w)
    nax1 = genrandi(w, fcx)
    nay1 = genrandi(w, fcy)
    
    steps = 200
    
    for i in range(0, steps):
        t = i / float(steps)
        x = bezierPoint(nax, scx, fcx, nax1, t)
        y = bezierPoint(nay, scy, fcy, nay1, t)
        
        s_tracker.append((x, y))
        
    nax = nax1
    nay = nay1
    
def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a)/(n - 1)
    return [diff * i + a  for i in range(n)]

def set_morphing():
    global img_idx, morph_refresh, render, shape0, shape1, pset_0, cset_0, pset_1, pset_1, src_cv, det_cv
    
    render = []
    shape0 = []
    shape1 = []

    src = loadImage("data/" + str(img_idx % 8) + ".png")
    det = loadImage("data/" + str((img_idx + 1) % 8) + ".png")
    
    # src.resize(500, 500)
    # det.resize(500, 500)
    
    src_cv = OpenCV(this, src)
    det_cv = OpenCV(this, det)
    
    tnum = 40
    src_cv.threshold(tnum)
    det_cv.threshold(tnum)

    clist = [len(c.getPoints()) for c in src_cv.findContours()]
    clist1 = [len(c.getPoints()) for c in det_cv.findContours()]
    
    mi = clist.index(max(clist))
    mi1 = clist1.index(max(clist1))
    
    pset_0 = src_cv.findContours()[mi].getPoints()
    cset_0 = src_cv.findContours()[mi]
    
    pset_1 = det_cv.findContours()[mi1].getPoints()
    cset_1 = det_cv.findContours()[mi1]
    
    lt1 = linspace(0, len(pset_0) - 1, 200)
    lt2 = linspace(0, len(pset_1) - 1, 200)
    
    for i in lt1:
        shape0.append(pset_0[int(i)])

    for i in lt2:
        shape1.append(pset_1[int(i)])
        
        render.append(pset_1[int(i)])
    
    morph_refresh = False
