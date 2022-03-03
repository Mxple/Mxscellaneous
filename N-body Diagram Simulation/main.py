import random, pickle, copy, pygame as pg

G = 6
BLACK = (0,0,0)
WHITE = (255,255,255)
BODIES = []
SAVETMP = None
ZOOM = 1
TIME = 0
PERSPECTIVE = -1

class mass():
      global G, BODIES, SAVETMP
      # mass object
      def __init__(self,mass,position,dx=0,dy=0,radius=None,stable=False):
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
            if radius != None:
                  self.r = radius

      # uses newton's law of gravitation, sums all forces acting upon it
      def get_acceleration(self):
            xAccel = 0
            yAccel = 0
            for body in BODIES:
                  xDist = self.x - body.x
                  yDist = self.y - body.y

                  if xDist == 0 and yDist == 0:
                        continue
                  
                  dist = self.get_dist(body)
                  accel = (G*body.m)/((dist)**2)

                  xAccel -= accel*xDist/dist
                  yAccel -= accel*yDist/dist

            return ( (xAccel,yAccel) )

      # pythagorean distance formula
      def get_dist(self, other):
            return(((self.x-other.x)**2+(self.y-other.y)**2)**0.5)

      # performs one step/frame of the system, sets new dx and dy and trail
      def step(self):
            dx = self.get_acceleration()[0]
            dy = self.get_acceleration()[1]
            
            self.dx += dx
            self.dy += dy

            if TIME%5 == 0:
                  self.trail.append((self.x,self.y))
                  if len(self.trail) > 255:
                        del self.trail[0]

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

def main():
      global BLACK, WHITE, BODIES, ZOOM, TIME, SAVETMP, PERSPECTIVE

      init_bodies(10)

      with open("N-body Diagram Simulation/save","rb") as file:
            BODIES = pickle.load(file)

      pg.init()

      # pygame window settings
      size = (1000,1000)
      screen = pg.display.set_mode(size)
      pg.display.set_caption("N-Body Simulation")
      clock = pg.time.Clock()

      # show count
      font = pg.font.Font('freesansbold.ttf', 32)
      text = font.render(str(len(BODIES))+"  "+str(round(100*ZOOM,2))+"%", True, WHITE, BLACK)
      textRect = text.get_rect()
      textRect.center = (100,50)
      
      while True:
            ZOOM = max(ZOOM,0.001)
            ZOOM = min(ZOOM,4)
            clock.tick(120)
            TIME+=1
            screen.fill(BLACK)
            text = font.render(str(len(BODIES))+"  "+str(round(100*ZOOM,2))+"%", True, WHITE, BLACK)
            screen.blit(text, textRect)
            massx = 0
            massy = 0
            total = 0

            if PERSPECTIVE == -1:
                  transformx = 0
                  transformy = 0
            else:
                  try:
                        transformx = int(BODIES[PERSPECTIVE].x*ZOOM*-1)
                        transformy = int(BODIES[PERSPECTIVE].y*ZOOM*-1)
                  except:
                        PERSPECTIVE = min(PERSPECTIVE,len(BODIES)-1)

            for b in BODIES:
                  b.step()
                  pg.draw.circle(screen,WHITE,(int(b.x*ZOOM)+transformx+500,int(b.y*ZOOM)+transformy+500),int(ZOOM*b.r),int(ZOOM*b.r))
                  for t in range(len(b.trail)):
                        pg.draw.circle(screen,(min(t,255),min(t,255),min(t,255)),(int(b.trail[t][0]*ZOOM)+transformx+500,int(b.trail[t][1]*ZOOM)+transformy+500),1,1)
                  
                  # center of mass
                  total+=b.m
                  massx+=b.x*b.m
                  massy+=b.y*b.m

            for b in range(len(BODIES)-1,-1,-1):
                  BODIES[b].check_collisions()
            for b in BODIES:
                  if not b.stable:
                        b.x += b.dx
                        b.y += b.dy

            if total == 0:
                  total = 1
            pg.draw.circle(screen,(255,100,100),(int(ZOOM*massx/total)+transformx+500,int(ZOOM*massy/total)+transformy+500),4,2)
            
            keys = pg.key.get_pressed()
            ZOOM += (keys[pg.K_UP]-keys[pg.K_DOWN]) * ZOOM/100
            for event in pg.event.get():
                  if event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:
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

                  if event.type == pg.QUIT:
                        pg.quit()
                        quit()
      
            pg.display.update()

if __name__== "__main__":
      main()