import random, pickle, copy, pygame as pg
from numpy import show_config
from pyparsing import White

G = 6
BLACK = (0,0,0)
WHITE = (255,255,255)
BODIES = []
ZOOM = .01
TIME = 0
PERSPECTIVE = -1
SPEED = 1
BLOWUP = False
SOLARSYSTEM = True
SHOWCONTROLS = True

class mass():
      global G, BODIES, PE
      # mass object
      def __init__(self,mass,position,dx=0,dy=0,brad=None,color = WHITE,stable=False):
            self.m = mass
            self.r = mass**0.5
            self.x = position[0]
            self.y = position[1]
            self.dx = dx
            self.dy = dy
            self.trail = []
            for i in range(255):
                  self.trail.append( (self.x, self.y) )
            self.stable=stable
            if brad == None:
                  self.brad = self.r
            else:
                  self.brad = brad
            self.color = color
            
      # pythagorean distance formula
      def get_dist(self, other):
            return(((self.x-other.x)**2+(self.y-other.y)**2)**0.5)

      # uses newtonian gravitation laws
      # a = Gm/r^2
      # splits into components
      # sums all "relevant forces", discards miniscule forces from moons
      def get_acceleration(self):
            xAccel = 0
            yAccel = 0
            gpe = 0
            for body in BODIES:
                  xDist = self.x - body.x
                  yDist = self.y - body.y

                  if xDist == 0 and yDist == 0:
                        continue

                  if body.m < 10:
                        continue
                  
                  dist = self.get_dist(body)
                  accel = (G*body.m)/((dist)**2)

                  xAccel -= accel*xDist/dist
                  yAccel -= accel*yDist/dist
                  
            return ( (xAccel,yAccel) )

      # performs one step/frame of the system, sets new dx and dy and trail
      def step(self):
            accels = self.get_acceleration()
            dx = accels[0]
            dy = accels[1]
            
            self.dx += dx
            self.dy += dy

            if TIME%50 == 0:
                  self.trail.append((self.x,self.y))
                  if len(self.trail) > 255:
                        del self.trail[0]

      # checks for collisions and combines collided particles
      def check_collisions(self):
            global SOLARSYSTEM

            if SOLARSYSTEM:
                  return False

            for b in range(len(BODIES)):
                  # if same body as itself
                  if self == BODIES[b]:
                        continue

                  if ((self.x-BODIES[b].x)**2+(self.y-BODIES[b].y)**2) < (self.r+BODIES[b].r+4)**2:
                        # combine
                        self.dx = (((BODIES[b].dx)*BODIES[b].m)+(self.m*(self.dx)))/(BODIES[b].m+self.m)
                        self.dy = (((BODIES[b].dy)*BODIES[b].m)+(self.m*(self.dy)))/(BODIES[b].m+self.m)
                        self.x = ((BODIES[b].x*BODIES[b].m)+(self.x*self.m))/(BODIES[b].m+self.m)
                        self.y = ((BODIES[b].y*BODIES[b].m)+(self.y*self.m))/(BODIES[b].m+self.m)
                        self.m+=BODIES[b].m
                        self.r=self.m**0.5
                        del BODIES[b]
                        return True
            return False

# initializes N-1 bodies at random and 1 body to stabilize the system
def init_bodies(N=10,clear=True,multi=1):
      global BODIES, SOLARSYSTEM
      SOLARSYSTEM = False

      # restart vs add new
      if clear:
            BODIES.clear()

      for i in range(N):
            BODIES.append(mass(random.randrange(50,300),(random.randrange(-10000,10000),random.randrange(-10000,10000)),0,0))

def main():
      global BLACK, WHITE, BODIES, ZOOM, TIME, PERSPECTIVE, SPEED, BLOWUP, SOLARSYSTEM, SHOWCONTROLS
      speedtmp = None

      # open save file
      # with open("N-body Diagram Simulation/save","rb") as file:
      #       BODIES = pickle.load(file)

      '''
      SOLAR SYSTEM MODEL
      '''
      solarbodies = {
            0:"Sun",
            1:"Mercury",
            2:"Venus",
            3:"Earth",
            4:"Mars",
            5:"Jupiter",
            6:"Saturn",
            7:"Uranus",
            8:"Neptune",
            9:"Pluto",
            10:"Moon (moon)",
            11:"Phobos (moon)",
            12:"Deimos (moon)",
            13:"Ganymede (moon)",
            14:"Io (moon)",
            15:"Europa (moon)",
            16:"Callisto (moon)",
            17:"Titan (moon)",
            18:"Titania (moon)",
            19:"Triton (moon)",
      }

      BODIES = []

      # sun + planets
      BODIES.extend([
            mass(33000000,(0,0),0,0,22,(255,200,100) ),     # sun
            mass(5.5,(72975,0),0,52.1,2,(180,150,140) ),    # mercury
            mass(81.5,(136274,0),0,38.1,4,(210,180,80) ),   # venus
            mass(100,(188435,0),0,32.4,4,(10,220,255) ),    # earth
            mass(10.7,(287034,0),0,26.3,3,(255,230,10) ),   # mars
            mass(31780,(982500,0),0,14.2,15,(255,150,10) ), # jupiter
            mass(9520,(1795155,0),0,10.5,12,(255,240,10) ), # saturn
            mass(1450,(3605664.4,0),0,7.4,8,(10,250,170) ), # uranus
            mass(1710,(5638997.8,0),0,5.9,9,(10,170,250) ), # neptune
            mass(0.22,(7436118.8,0),0,5.2,1,(20,100,255) )  # pluto (yes.)
      ])
      
      # moons 
      BODIES.extend([
            mass(1.23,(188435,486),-1.12,32.4,1,(175,155,155) ),              # moon
            mass(1.78477e-7,(287034,11.82),-2.33,26.3,1,(175,155,155) ),      # phobos (mars)
            mass(0.247179e-7,(287034,29.6),-1.47266,26.3,1,(175,155,155) ),   # deimos (mars)
            mass(2.5,(982500,1352.77),-11.88,14.2,2,(175,155,155) ),          # ganymede (jupiter)
            mass(1.5,(982500,532.72),-18.9,14.2,2,(220,200,155) ),            # io (jupiter)
            mass(0.8,(982500,847.68),-14.998,14.2,1,(220,200,190) ),          # europa (jupiter)
            mass(1.8,(982500,2378.356),-8.954,14.2,2,(155,155,200) ),         # callisto (jupiter)
            mass(2.25,(1795155,1543.8),-6.08,10.5,2,(235,240,10) ),           # titan (saturn)
            mass(0.05685,(3605664,550.7),-3.9,7.4,1,(175,155,155) ),          # titania (uranus)
            mass(0.359,(5638997.8,448.77),-4.7873,5.9,1,(175,155,155) ),      # triton (neptune)
      ])

      # pygame window settings
      pg.init()
      size = (1000,1000)
      screen = pg.display.set_mode(size)
      pg.display.set_caption("N-Body Simulation")
      clock = pg.time.Clock()
      font = pg.font.SysFont('Times New Roman', 24)
      
      # main loop
      while True:
            ms = clock.tick(30) # 30 FPS by default

            # render
            ZOOM = max(ZOOM,0.00001)
            ZOOM = min(ZOOM,4)
            screen.fill(BLACK)

            # simulation
            for i in range(int(SPEED)):
                  TIME+=1
                  for b in BODIES:
                        b.step() # do step

                  # collisions
                  for b in range(len(BODIES)-1,-1,-1):
                        BODIES[b].check_collisions()
                  for b in BODIES:
                        if not b.stable:
                              b.x += b.dx
                              b.y += b.dy

            # center of mass
            massx = 0
            massy = 0
            total = 0

            for b in BODIES:
                  total+=b.m
                  massx+=b.x*b.m
                  massy+=b.y*b.m

            # camera centering 
            if PERSPECTIVE == -1:
                  transformx = int(ZOOM*massx/total)*-1
                  transformy = int(ZOOM*massy/total)*-1
            else:
                  try:
                        transformx = int(BODIES[PERSPECTIVE].x*ZOOM*-1)
                        transformy = int(BODIES[PERSPECTIVE].y*ZOOM*-1)
                  except:
                        PERSPECTIVE = min(PERSPECTIVE,len(BODIES)-1)

            # drawing
            # bodies
            for b in BODIES:
                  if BLOWUP:
                        pg.draw.circle(screen,b.color,(int(b.x*ZOOM)+transformx+500,int(b.y*ZOOM)+transformy+500),int(max(b.r*ZOOM,b.brad)),int(max(b.r*ZOOM,b.brad))) # draw circle
                  else:
                        pg.draw.circle(screen,b.color,(int(b.x*ZOOM)+transformx+500,int(b.y*ZOOM)+transformy+500),int(ZOOM*b.r),int(ZOOM*b.r)) # draw circle
                  for t in range(len(b.trail)):
                         pg.draw.circle(screen,(min(t,255),min(t,255),min(t,255)),(int(b.trail[t][0]*ZOOM)+transformx+500,int(b.trail[t][1]*ZOOM)+transformy+500),1,1) # draw trail
                  #pg.draw.lines(screen,WHITE,False,[(int(c[0]*ZOOM)+transformx+500,int(c[1]*ZOOM)+transformy+500) for c in b.trail],1)

            # center of mass
            if total == 0:
                  total = 1
            pg.draw.circle(screen,(255,100,100),(int(ZOOM*massx/total)+transformx+500,int(ZOOM*massy/total)+transformy+500),4,2)

            # stats
            if SOLARSYSTEM and PERSPECTIVE != -1:
                  cam = solarbodies[PERSPECTIVE]
            elif PERSPECTIVE == -1:
                  cam = "Center of mass"
            else:
                  cam = str(PERSPECTIVE)

            stats = [
                  str(len(BODIES))+" Bodies",
                  "Zoom: "+str(round(100*ZOOM,2))+"%",
                  "Speed: "+str(int(SPEED))+"x",
                  "Days: "+str(round(TIME/100)),
                  "Camera: "+cam
            ]
            
            for i in range(len(stats)):
                  c = (255,50,50) if ms > 35 and i == 2 else WHITE
                  text = font.render(stats[i], True, c, BLACK)
                  screen.blit(text, (20,30*i+20))

            # tips
            tips = [
                  "UP and DOWN to zoom in and out",
                  "= and - to speed up and down",
                  "Hold SHIFT/CTRL to go change faster",
                  "LEFT and RIGHT to change perspective",
                  "B to enlarge",
                  "R to restart",
                  "A to add new bodies",
                  "H to hide this list"
            ]

            if SHOWCONTROLS:
                  for i in range(len(tips)):
                        text = font.render(tips[i], True, WHITE, BLACK)
                        screen.blit(text, (20,200+(i*30)))
            
            # pygame inputs
            keys = pg.key.get_pressed()
            ZOOM += (keys[pg.K_UP]-keys[pg.K_DOWN]) * (ZOOM/100) * (1+9*(keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT])) * (1+24*(keys[pg.K_LCTRL] or keys[pg.K_RCTRL]))
            SPEED += (keys[pg.K_EQUALS]-keys[pg.K_MINUS]) * 0.5 * (1+9*(keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT])) * (1+ 24*(keys[pg.K_LCTRL] or keys[pg.K_RCTRL]))
            SPEED = max(0,SPEED)

            for event in pg.event.get():
                  if event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:
                              TIME = 0
                              init_bodies()

                        if event.key == pg.K_a:
                              init_bodies(4,False)

                        if event.key == pg.K_LEFT:
                              if (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
                                    PERSPECTIVE = -1
                              else:
                                    PERSPECTIVE -= 1
                                    PERSPECTIVE = max(-1,PERSPECTIVE)

                        if event.key == pg.K_RIGHT:
                              if (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
                                    PERSPECTIVE = len(BODIES)-1
                              else:
                                    PERSPECTIVE += 1
                                    PERSPECTIVE = min(PERSPECTIVE,len(BODIES)-1)

                        if event.key == pg.K_s:
                              with open("N-body Diagram Simulation/save","wb") as file:
                                    pickle.dump(BODIES,file)

                        if event.key == pg.K_SPACE:
                              if speedtmp == None:
                                    speedtmp = SPEED
                                    SPEED = 0
                              else:
                                    SPEED = speedtmp
                                    speedtmp = None

                        if event.key == pg.K_b:
                              BLOWUP = not BLOWUP

                        if event.key == pg.K_h:
                              SHOWCONTROLS = not SHOWCONTROLS

                  if event.type == pg.QUIT:
                        pg.quit()
                        quit()
      
            pg.display.update()

if __name__== "__main__":
      main()