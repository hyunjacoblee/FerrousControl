add_library('serial')

import fluid as Fluid
from easing_functions import *
from random import randint 
from time import sleep, time
import math
import struct
from threading import Thread
from Queue import Queue

#SineWave
xspacing = 1     # How far apart should each horizontal location be spaced
theta = 50       # Start angle at 0
amplitude = 23.0    # Height of wave
period = 300.0      # How many pixels before the wave repeats
dx = (TWO_PI / period) * xspacing # Value for incrementing X, a function of period and xspacing
directionX = 0
directionY = 0
counter = 0
angle = 0
toggle = 1
ccounter = 0 
location_tracker = []

#GLOBAL VARIABLES FOR NAVIER_STOKES
WIDTH = 40
D_RATE = 2
VISCOSITY = 0.7
TIME_SPACE = 0.0005

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

counter = 0

#Serial Connection
magnetPort = None
magnetPort2 = None
magnetPortAddresses = [u'/dev/cu.usbmodem58040401',
               u'/dev/cu.usbmodem49270001',
               u'/dev/cu.usbmodem58130601',
               u'/dev/cu.usbmodem43318101',
               u'/dev/cu.usbmodem43318001']
magnetPorts = []
INITIALIZED = False
MAGNET_CONNECTION = False


STARTING = 0
sf = 20

#TOGGLES
AMOEBA_TOGGLE = False
SNEK_TOGGLE = False

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

def sendSerial(infosend, port):
    global magnetPort, magnetPorts

    if infosend != None:
        # print("sending to", port)
        for i in infosend:
            magnetPorts[port].write(i)
            # magnetPort.write(i)

# Send Queue
# sendQueue = Queue()
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
                    for mag_y in range(4):
                        for mag_x in range(4):
                            index = mag_x + mag_y * 40 + quad_x * 4 + quad_y * 160 + panel_x * 8 + panel_y * 320
                            if len(initial_list) < WIDTH*2:
                                reordered_list.append(initial_list[index])
                            
    return reordered_list
    # return initial_list

def setup():
    global FLUID, GRID, WIDTH, D_RATE, VISCOSITY, TIME_SPACE, sf, w, yvalues
    background(0)
    size(WIDTH * sf, WIDTH * sf)
    
    #Initializing the Navier Stokes grid.
    GRID = makeGrid(WIDTH)
    
    #Sine Wave variables intialization.
    w = WIDTH * sf / 3
    yvalues = [0.0] * (w / xspacing)
     
    #Generating coordinates for snake movements.
    snake(WIDTH)

def draw():
    global s_tracker, MAGNET_CONNECTION, INITIALIZED, magnetPort, randposX, randposY, npcounter, counter, GRID, WIDTH, D_RATE, VISCOSITY, TIME_SPACE, VEL_H, VEL_HPREV, VEL_V, VEL_VPREV, DENS, DENS_PREV, STARTING, BUBBLE_TOGGLE, SNEK_TOGGLE, AMOEBA_TOGGLE, directionX, directionY, amplitude, xspacing, yvalues, toggle, ccounter, theta, location_tracker, sf, angle, period, sendThread, busyCount, openCount, startTime, startFrame
    
    background(0)
    
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

                bright = 90
                DENS[FLUID.xy_coordinate(WIDTH, x + 1, y + 1)] += bright
                
            for i in range(snake_length, 0, -1):
                x = int(s_tracker[st - i][0])
                y = int(s_tracker[st - i][1])
                
                DENS[FLUID.xy_coordinate(WIDTH, x + 1, y + 1)] -= bright / (snake_length + 1 - i)
  
    #AMOEBA movements generation
    if AMOEBA_TOGGLE:
        directionX += randint(-4,4) * 4
        directionY -= randint(-1,1)
        calcWave()
        renderWave()
        generate_amoeba()
    
    if(frameCount % 100 == 0):
        VEL_H, VEL_V, VEL_HPREV, VEL_VPREV = FLUID.velocity_step(WIDTH, VEL_H, VEL_V, VEL_HPREV, VEL_VPREV, VISCOSITY, TIME_SPACE)
    
        if AMOEBA_TOGGLE:
            for i in location_tracker[:200]:
                center_x = i[0]
                center_y = i[1]
                
                bright = 90 
                DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y + 1)] += bright
                DENS[FLUID.xy_coordinate(WIDTH, center_x, center_y + 1)] += bright
                # DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y)] += bright
                # DENS[FLUID.xy_coordinate(WIDTH, center_x + 2, center_y + 1)] += bright
                # DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y + 2)] += bright
            
            location_tracker = []
        
    DENS, DENS_PREV = FLUID.density_step(WIDTH, DENS, DENS_PREV, VEL_H, VEL_V, D_RATE, TIME_SPACE) 
    
    for i in xrange(WIDTH):
        for j in xrange(WIDTH):
            num = FLUID.xy_coordinate(WIDTH, i, j)
            wind = PVector(VEL_H[num], VEL_V[num])   
            
    reset_gridcells()
    display_grid()
    
    #Write to Arduino
    if MAGNET_CONNECTION:
        if not INITIALIZED:
            initialize_port()
            
        carr = count()
                
        reordered_list = reordinator(carr)
        
        # byte message to send
        byteMessage = ''
        # for idx, i in enumerate(carr):
        for idx, i in enumerate(reordered_list):
            try:
                byteMessage+=chr(int(round(i)))
            except:
                print("BAD NUMBER", i, idx)
                byteMessage+=chr(int(round(0.0)))
        # print(carr)
        # print(carr[820],mouseX, mouseY)
        
        # dummy values to prove sending
        # changes every 1000 frames (~3.3 seconds @ 30 fps)
        # values sent to each arduino alternates by 1
        byteMessage = ''
        msg_check = []
        dween_num = 0
        entry_num = 0
    
        for dweeners in range(5):
            for entries in range(320):
                val = dween_num * 25 + ((frameCount % 30) / 3)
                val = 120 + (frameCount % 30) / 2
                # if val > 127:
                #     val = val / 2
                #     stringByte = ""
                #     for i in range(7):
                #         stringByte = chr(val % 2) + stringByte;
                #         val = val / 2;
                #     stringByte = "-" + stringByte;
                #     byteMessage += stringByte
                # else:
                #     byteMessage += chr(val)
                # if entry_num % 2 == 0:
                #     val+=1                
                msg_check.append(val)
                byteMessage += chr(val)
                entry_num+=1
                # magnetPort.write(val)
            dween_num+=1
        # print(msg_check, len(msg_check), frameCount)
        # print(byteMessage)
        # print(msg_check[1])
        t0 = Thread(target=sendSerial, args=[msg_check[0:320], 0])
        t1 = Thread(target=sendSerial, args=[msg_check[320:640], 1])
        t2 = Thread(target=sendSerial, args=[msg_check[640:960], 2])
        t3 = Thread(target=sendSerial, args=[msg_check[960:1280], 3])
        t4 = Thread(target=sendSerial, args=[msg_check[1280:1600], 4])

        t0.start()
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t0.join()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        
        # sendSerial(msg_check[0:320], 0)
        # sendSerial(byteMessage)
        nowTime = time()
        if nowTime - startTime >= 1.0:
            print(nowTime - startTime, frameCount - startFrame, frameCount, msg_check[1])
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
    global DENS, DENS_PREV, VEL_H, VEL_V, VEL_HPREV, VEL_VPREV, BUBBLE_TOGGLE, SNEK_TOGGLE, D_RATE, AMOEBA_TOGGLE, MAGNET_CONNECTION
    
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
        
    if ((key == 'A') or (key == 'a')):
        D_RATE = 0.6
        AMOEBA_TOGGLE = not AMOEBA_TOGGLE
        if AMOEBA_TOGGLE:
            print("AMOEBA ON")
        else:
            print("AMOEBA OFF")
        
    if ((key == 'M') or (key == 'm')):
        center_x = mouseX // sf
        center_y = mouseY // sf

        for i in easelist():
            DENS[FLUID.xy_coordinate(WIDTH, center_x + 1, center_y + 1)] = i

def ratio(x):
    # return (x / 2)
    if(x < 0):
        return 0
    elif (x * 128 / 32) > 127:
        return 127
    else:
        return (x * 128 / 32)
    
def count():
    global DENS, WIDTH, FLUID 
    counter = []
    
    # original counter - appeared to be top to bottom, then left to right
    # when using 'F' as tester
    # for i in range(WIDTH):
    #     for j in range(WIDTH):
    #         counter.append(ratio(DENS[FLUID.xy_coordinate(WIDTH, i + 1, j + 1)]))
     
    # current counter - goes left to right, then top to bottom
    # when using 'F' as tester
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
        fill(0, self.tempDens, 0)
        rect(self.x,self.y,self.w,self.h)
        
def calcWave():
    global theta, directionxSWITCH
        
    theta += 0.5
    
    # For every x varlue, calculate a y value with sine function
    x = theta
    for i in range(len(yvalues)):
        yvalues[i] = sin(x) * amplitude
        x += dx

def renderWave():
    global counter, angle, sf, location_tracker, randposX, randposY
    noStroke()
    fill(255)
        
    for x in range(len(yvalues)):
        val_x = x * xspacing + directionX
        val_y = (height/2 + yvalues[x]) + directionY
        
        val_x = ((val_x) * (cos(angle)) - (val_y) * (sin(angle))) // sf
        val_y = ((val_x) * (sin(angle)) + (val_y) * (cos(angle))) // sf

        location_tracker.append((val_x, val_y))
        
def generate_amoeba():
    global angle, period, xspacing
    angle -= ((TWO_PI / period) * xspacing)*25

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
