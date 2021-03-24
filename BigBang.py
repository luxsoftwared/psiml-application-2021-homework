
import math
import copy

class Point:
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.collision=0
    def forward_collide(self,S):#vraca broj kolizija
        self.x+=self.vx
        self.y+=self.vy
        if abs(self.x)>S:
            self.x+=2*(-self.x+math.copysign(1,self.x)*S)
            self.collision+=1
            self.vx=-self.vx
        if abs(self.y)>S:
            self.y+=2*(-self.y+math.copysign(1,self.y)*S)
            self.collision+=1
            self.vy=-self.vy
        
    def backward(self):
        self.x-=self.vx
        self.y-=self.vy
    def print(self):
        print(self.x," ",self.y," ",self.vx," ",self.vy)
    def dist_from_zero(self):
        return math.sqrt(self.x**2+self.y**2)
    

def distance(p1,p2):
    return math.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)



inp=input().split()
N=int(inp[0])
S=int(inp[1])
T=int(inp[2])
P=float(inp[3])

points=[]
for i in range(N):
    inp=input().split()
    points.append(Point(float(inp[0]),float(inp[1]),float(inp[2]),float(inp[3])))

points2=copy.deepcopy(points)

####PRVI DEO
t=0
sum_dist_new=0
for point in points:
    sum_dist_new+=point.dist_from_zero()
sum_dist_old=sum_dist_new+1

while sum_dist_old>sum_dist_new:                              #>=?
    sum_dist_old=sum_dist_new
    sum_dist_new=0
    for point in points:
        point.backward()
        sum_dist_new+=point.dist_from_zero()
    t+=1
t-=1

#print(t)

##DRUGI DEO

for i in range(T):
    for point in points2:
        point.forward_collide(S)

result2=0
result3=0
for point in points2:
    result2+=point.collision
    result3+=P**point.collision


print(t," ",result2," ",result3)

