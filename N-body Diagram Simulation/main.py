import random, pygame as pg

G = 1
BLACK = (0,0,0)
WHITE = (255,255,255)
BODIES = []

class mass():
      global G, BODIES
      def __init__(self,mass,position,dx=0,dy=0,radius=None,stable=False):
            self.m = mass
            self.r = mass**0.5
            self.x = position[0]
            self.y = position[1]
            self.dx = dx
            self.dy = dy
            self.trail = []
            self.stable=stable
            self.deactivated = False
            if radius != None:
                  self.r = radius

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

      def get_dist(self, other):
            return(((self.x-other.x)**2+(self.y-other.y)**2)**0.5)

      def step(self):
            if self.deactivated:
                  return
            dx = self.get_acceleration()[0]
            dy = self.get_acceleration()[1]
            
            self.dx += dx
            self.dy += dy

            self.trail.append((self.x,self.y))
            if len(self.trail) > 300:
                  del self.trail[0]

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

def main():
      global BLACK, WHITE, BODIES

      N = 10 # number of bodies
      for i in range(N-1):
            rand = random.randrange(40,100)
            temp = mass(50,(random.randrange(300,700),random.randrange(300,700)),random.random()-0.5,random.random()-0.5)
            BODIES.append(temp)
      # balance
      bdx = 0
      bdy = 0
      massX=0
      massY=0
      for b in BODIES:
            bdx -= b.dx
            bdy -= b.dy
            massX+=b.x
            massY+=b.y
      print(bdx,bdy)
      BODIES.append(mass(50,(500*N-massX,500*N-massY),bdx,bdy))
      #BODIES = [mass(500,(500,500),0,-.2),mass(100,10,(700,500),0,1)

      pg.init()
      
      # pygame window settings
      size = (1000,1000)
      screen = pg.display.set_mode(size)
      pg.display.set_caption("N-Body Simulation")
      clock = pg.time.Clock()

      # show count
      font = pg.font.Font('freesansbold.ttf', 32)
      text = font.render(str(len(BODIES)), True, WHITE, BLACK)
      textRect = text.get_rect()
      textRect.center = (50,50)
      
      while True:
            clock.tick(60)
            screen.fill(BLACK)
            text = font.render(str(len(BODIES)), True, WHITE, BLACK)
            screen.blit(text, textRect)
            massx = 0
            massy = 0
            total = 0
            for b in BODIES:
                  b.step()
                  pg.draw.circle(screen,WHITE,(int(b.x),int(b.y)),int(b.r),int(b.r))
                  for t in b.trail:
                        pg.draw.circle(screen,(0,100,255),(int(t[0]),int(t[1])),1,1)
                  
                  # center of mass
                  total+=b.m
                  massx+=b.x*b.m
                  massy+=b.y*b.m
            while b.check_collisions():
                  pass
            for b in range(len(BODIES)-1,-1,-1):
                  BODIES[b].check_collisions()
            for b in BODIES:
                  if not b.stable:
                        b.x += b.dx
                        b.y += b.dy
            pg.draw.circle(screen,(255,100,100),(int(massx/total),int(massy/total)),2,2)
            #pg.draw.circle(screen,(255,50,50),(500,500),3,3)

            
            for event in pg.event.get():
                  if event.type == pg.QUIT:
                        pg.quit()
                        quit()
      
            pg.display.update()

if __name__== "__main__":
      main()
