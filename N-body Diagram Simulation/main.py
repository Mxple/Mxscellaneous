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
            for body in BODIES:
                  # if same body as itself
                  if self == body:
                        continue

                  if ((self.x-body.x)**2+(self.y-body.y)**2) < (max(self.r,body.r))**2:
                        # combine
                        body.m+=self.m
                        body.r=body.m**0.5
                        body.dx=((body.dx*body.m)+(self.m*(self.dx+dx)))/(body.m+self.m)
                        body.dy=((body.dy*body.m)+(self.m+(self.dy+dy)))/(body.m+self.m)
                        body.x = ((body.x*body.m)+(self.x*self.m))/(body.m+self.m)
                        body.y = ((body.y*body.m)+(self.y*self.m))/(body.m+self.m)
                        self.m=0
                        self.r=0
                        self.dx=0
                        self.dy=0
                        self.deactivated = True
                        return
            
            self.dx += dx
            self.dy += dy

            self.trail.append((self.x,self.y))
            if len(self.trail) > 300:
                  del self.trail[0]

def main():
      global BLACK, WHITE, BODIES

      N = 5 # number of bodies
      for i in range(N-1):
            rand = random.randrange(40,100)
            temp = mass(50,(random.randrange(300,700),random.randrange(300,700)),random.random()-0.5,random.random()-0.5)
            BODIES.append(temp)
      # balance
      bdx = 0
      bdy = 0
      for b in BODIES:
            bdx -= b.dx
            bdy -= b.dy
      print(bdx,bdy)
      BODIES.append(mass(50,(random.randrange(300,700),random.randrange(300,700)),bdx,bdy))
      #BODIES = [mass(500,(500,500),0,-.2),mass(100,10,(700,500),0,1)
      pg.init()
      
      size = (1000,1000)
      screen = pg.display.set_mode(size)

      pg.display.set_caption("N-Body Simulation")
      clock = pg.time.Clock()

      while True:
            clock.tick(60)
            pg.event.get()
            screen.fill(BLACK)

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
            for b in BODIES:
                  if not b.stable:
                        b.x += b.dx
                        b.y += b.dy
            pg.draw.circle(screen,(255,100,100),(int(massx/total),int(massy/total)),2,2)

            pg.display.update()
      

if __name__== "__main__":
      main()
