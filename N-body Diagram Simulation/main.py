import random, pickle, copy, pygame as pg
from pyparsing import White

G = 6
BLACK = (0,0,0)
WHITE = (255,255,255)
BODIES = []
SAVETMP = None
ZOOM = .01
TIME = 0
PERSPECTIVE = -1
KE = 0
PE = 0
SPEED = 1
BLOWUP = False

class mass():
      global G, BODIES, SAVETMP, PE
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
            

      # uses newton's law of gravitation, sums all forces acting upon it
      def get_acceleration(self):
            xAccel = 0
            yAccel = 0
            gpe = 0
            for body in BODIES:
                  xDist = self.x - body.x
                  yDist = self.y - body.y

                  if xDist == 0 and yDist == 0:
                        continue
                  
                  dist = self.get_dist(body)
                  accel = (G*body.m)/((dist)**2)

                  xAccel -= accel*xDist/dist
                  yAccel -= accel*yDist/dist
                  gpe -= G*self.m*body.m/dist
                  
            return ( (xAccel,yAccel, gpe) )

      # pythagorean distance formula
      def get_dist(self, other):
            return(((self.x-other.x)**2+(self.y-other.y)**2)**0.5)

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
            return accels[2]

      # checks for collisions and combines collided particles
      def check_collisions(self):
            for b in range(len(BODIES)):
                   # if same body as itself
                  if self == BODIES[b]:
                        continue

                  if ((self.x-BODIES[b].x)**2+(self.y-BODIES[b].y)**2) < (self.r+BODIES[b].r+4)**2:
                        # combine
                        self.dx=(((BODIES[b].dx)*BODIES[b].m)+(self.m*(self.dx)))/(BODIES[b].m+self.m)
                        self.dy=(((BODIES[b].dy)*BODIES[b].m)+(self.m*(self.dy)))/(BODIES[b].m+self.m)
                        self.x = ((BODIES[b].x*BODIES[b].m)+(self.x*self.m))/(BODIES[b].m+self.m)
                        self.y = ((BODIES[b].y*BODIES[b].m)+(self.y*self.m))/(BODIES[b].m+self.m)
                        self.m+=BODIES[b].m
                        self.r=self.m**0.5
                        del BODIES[b]
                        return True
            return False

# initializes N-1 bodies at random and 1 body to stabilize the system
def init_bodies(N=10,clear=True,multi=1):
      global BODIES,SAVETMP
      if clear:
            BODIES.clear()

      for i in range(N-1):
            rand = random.randrange(40,100)
            temp = mass(50,(random.randrange(-500,500),random.randrange(-500,500)),multi*(random.random()-0.5),multi*(random.random()-0.5))
            BODIES.append(temp)

      # balance
      bdx = 0
      bdy = 0
      massX = 0
      massY = 0
      for b in BODIES:
            bdx -= b.dx
            bdy -= b.dy
            massX += b.x
            massY += b.y
      BODIES.append(mass(50,(-1*massX,-1*massY),bdx,bdy))

      SAVETMP = copy.deepcopy(BODIES)

def get_kinetic_energy():
      global BODIES, KE
      KE = 0
      for b in BODIES:
            KE += 0.5*b.m*(b.dx**2+b.dy**2)
      return KE

def main():
      global BLACK, WHITE, BODIES, ZOOM, TIME, SAVETMP, PERSPECTIVE, KE, PE, SPEED, BLOWUP
      speedtmp = None
      # init_bodies(10)

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
            7:"Saturn",
            8:"Uranus",
            9:"Neptune",
            10:"Pluto",
            11:"Moon"
      }
      BODIES = []
      # planets -uranus -pluto
      BODIES.extend([
      mass(33000000,(0,0),0,0,22,(255,200,100) ),
      mass(5.5,(72975,0),0,52.1,2,(180,150,140) ),
      mass(81.5,(136274,0),0,38.1,4,(210,180,80) ),
      mass(100,(188435,0),0,32.4,4,(10,220,255) ),
      mass(10.7,(287034,0),0,26.3,3,(255,230,10) ),
      mass(31780,(982500,0),0,14.2,15,(255,150,10) ),
      mass(9520,(1795155,0),0,10.5,12,(255,240,10) ),
      mass(1450,(3605664.4,0),0,7.4,8,(10,250,170) ),
      mass(1710,(5638997.8,0),0,5.9,9,(10,170,250) ),
      mass(0.22,(7436118.8,0),0,5.2,1,(20,100,255) )
      ])
      
      # moons 
      BODIES.extend([mass(1.23,(188435,486),-1.12,32.4)])
      pg.init()

      # pygame window settings
      size = (1000,1000)
      screen = pg.display.set_mode(size)
      pg.display.set_caption("N-Body Simulation")
      clock = pg.time.Clock()

      # show count
      font = pg.font.SysFont('Times New Roman', 24)
      
      while True:
            ms = clock.tick(30)
            # render
            ZOOM = max(ZOOM,0.00001)
            ZOOM = min(ZOOM,4)
            screen.fill(BLACK)
            stats = [str(len(BODIES))+" Bodies","Zoom: "+str(round(100*ZOOM,2))+"%","Speed: "+str(int(SPEED)),"Camera: "+str(int(PERSPECTIVE)), "Days: "+str(round(TIME/100))]
            
            for i in range(len(stats)):
                  c = (255,50,50) if ms > 40 and i == 2 else WHITE
                  text = font.render(stats[i], True, c, BLACK)
                  screen.blit(text, (20,30*i+20))

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

            # camera
            if PERSPECTIVE == -1:
                  transformx = int(massx/total)*-1
                  transformy = int(massy/total)*-1
            else:
                  try:
                        transformx = int(BODIES[PERSPECTIVE].x*ZOOM*-1)
                        transformy = int(BODIES[PERSPECTIVE].y*ZOOM*-1)
                  except:
                        PERSPECTIVE = min(PERSPECTIVE,len(BODIES)-1)

            # drawing
            for b in BODIES:
                  if BLOWUP:
                        pg.draw.circle(screen,b.color,(int(b.x*ZOOM)+transformx+500,int(b.y*ZOOM)+transformy+500),int(max(b.r*ZOOM,b.brad)),int(max(b.r*ZOOM,b.brad))) # draw circle
                  else:
                        pg.draw.circle(screen,b.color,(int(b.x*ZOOM)+transformx+500,int(b.y*ZOOM)+transformy+500),int(ZOOM*b.r),int(ZOOM*b.r)) # draw circle
                  for t in range(len(b.trail)):
                         pg.draw.circle(screen,(min(t,255),min(t,255),min(t,255)),(int(b.trail[t][0]*ZOOM)+transformx+500,int(b.trail[t][1]*ZOOM)+transformy+500),1,1) # draw trail
                  #pg.draw.lines(screen,WHITE,False,[(int(c[0]*ZOOM)+transformx+500,int(c[1]*ZOOM)+transformy+500) for c in b.trail],1)

            if total == 0:
                  total = 1

            # center of mass    
            pg.draw.circle(screen,(255,100,100),(int(ZOOM*massx/total)+transformx+500,int(ZOOM*massy/total)+transformy+500),4,2)
            
            # pygame keys
            keys = pg.key.get_pressed()
            ZOOM += (keys[pg.K_UP]-keys[pg.K_DOWN]) * (ZOOM/100) * (1+9*(keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]))
            SPEED += (keys[pg.K_EQUALS]-keys[pg.K_MINUS]) * 0.5 * (1+9*(keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]))
            SPEED = max(0,SPEED)

            for event in pg.event.get():
                  if event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:
                              TIME = 0
                              init_bodies()
                        if event.key == pg.K_a:
                              init_bodies(4,False)
                        if event.key == pg.K_LEFT:
                              PERSPECTIVE -= 1
                              PERSPECTIVE = max(-1,PERSPECTIVE)
                        if event.key == pg.K_RIGHT:
                              PERSPECTIVE += 1
                              PERSPECTIVE = min(PERSPECTIVE,len(BODIES)-1)
                        if event.key == pg.K_s:
                              with open("N-body Diagram Simulation/save","wb") as file:
                                    pickle.dump(SAVETMP,file)
                        if event.key == pg.K_SPACE:
                              if speedtmp == None:
                                    speedtmp = SPEED
                                    SPEED = 0
                              else:
                                    SPEED = speedtmp
                                    speedtmp = None
                        if event.key == pg.K_b:
                              BLOWUP = not BLOWUP

                  if event.type == pg.QUIT:
                        pg.quit()
                        quit()
      
            pg.display.update()

if __name__== "__main__":
      main()