from re import X
import numpy as np
import matplotlib.pyplot as plt

class stick(): 
    def __init__(self,point1,point2,v):
        self.point1 = np.array(point1,dtype=np.float64)
        self.point2 = np.array(point2,dtype=np.float64)
        self.v = np.array(v,dtype=np.float64)
    def update(self):
        self.point1 += self.v
        self.point2 += self.v
class gate():
    def __init__(self,point1,point2,v):
        self.point1 = np.array(point1,dtype=np.float64)
        self.point2 = np.array(point2,dtype=np.float64)
        self.v = np.array(v,dtype=np.float64)
    def update(self):
        self.point1 += self.v*self.v[3]
        self.point2 += self.v*self.v[3]
class LorenzTransLib(): # only for x axis
    def __init__(self,v):
        self.c = 3e8
        self.v = v
        self.beta = self.v/self.c
        self.gamma = 1/np.sqrt(1-np.square(self.beta))
    def positive_trans(self,a): # output a'
        trans_matrix = np.array([[ self.gamma, -self.v*self.gamma ],
                        [ (-self.v/(self.c**2))*self.gamma, self.gamma ]],dtype=np.float64)
        return np.dot(trans_matrix,a)
    def negative_trans(self,a):
        trans_matrix = [[ self.gamma, self.v*self.gamma ],
                        [ (self.v/(self.c**2))*self.gamma, self.gamma ]]
        return np.dot(trans_matrix,a)
def drew_base(axes,stick_left,stick_right,gate_left,gate_right):
    stick_left = np.array(stick_left)
    stick_right = np.array(stick_right)
    gate_right = np.array(gate_right)
    gate_left = np.array(gate_left)
    axes.plot(stick_left[:,0],stick_left[:,1],color="pink",marker="o")
    axes.plot(stick_right[:,0],stick_right[:,1],color="pink",marker="o")
    axes.plot(gate_left[:,0],gate_left[:,1],color="blue",marker="o")
    axes.plot(gate_right[:,0],gate_right[:,1],color="blue",marker="o")
    for x,y in zip(stick_left[:,0],stick_left[:,1]):
        axes.annotate("({:.2e})".format(x,y),xy=(x-1.5e8,y+0.1),fontsize=3,color="red",alpha=0.9)
    for x,y in zip(stick_right[:,0],stick_right[:,1]):
        axes.annotate("({:.2e})".format(x,y),xy=(x+1.5e8,y+0.1),fontsize=3,color="red",alpha=0.9)
    for x,y in zip(gate_left[:,0],gate_left[:,1]):
        axes.annotate("({:.2e})".format(x,y),xy=(x-1.5e8,y+0.1),fontsize=3,color="blue",alpha=0.9)
    for x,y in zip(gate_right[:,0],gate_right[:,1]):
        axes.annotate("({:.2e})".format(x,y),xy=(x+1.5e8,y+0.1),fontsize=3,color="blue",alpha=0.9)
    axes.fill(np.concatenate([stick_left[:,0],stick_right[::-1,0]]),np.concatenate([stick_left[:,1],stick_right[::-1,1]]),color="pink",alpha=0.2)
    axes.fill(np.concatenate([gate_left[:,0],gate_right[::-1,0]]),np.concatenate([gate_left[:,1],gate_right[::-1,1]]),color="blue",alpha=0.2)
    
def drew_ground(axes,stick_v,time):
    # axes.set_xlim([-30,30])
    # axes.set_ylim([0,50])
    axes.set_xlim([-1e9,1e9])
    axes.set_ylim([-1,5.5])
    s = stick((-3e8,0,0,0),(-3e8+1e8,0,0,0),(stick_v,0,0,1))
    g = gate((-0.4e8,0,0,0),(0.4e8,0,0,0),(0,0,0,1))
    lorenz = LorenzTransLib(stick_v)
    stick_right = []
    stick_left = []
    gate_right = []
    gate_left = []
    for _ in range(0,time):
        trans2ground_point1 = lorenz.negative_trans([s.point1[0],s.point1[3]])
        trans2ground_point2 = lorenz.negative_trans([s.point2[0],s.point2[3]])
        stick_left.append(trans2ground_point1)
        stick_right.append(trans2ground_point2)
        gate_right.append([g.point1[0],g.point1[3]])
        gate_left.append([g.point2[0],g.point2[3]])
        g.update()
        s.update()
    drew_base(axes,stick_left,stick_right,gate_left,gate_right)
def drew_stick(axes,stick_v,time):
    # axes.set_xlim([-30,30])
    # axes.set_ylim([0,50])
    axes.set_xlim([-1e9,1e9])
    axes.set_ylim([-1,5.5])
    s = stick((-3e8,0,0,0),(-3e8+1e8,0,0,0),(0,0,0,1))
    g = gate((-0.4e8,0,0,0),(0.4e8,0,0,0),(-stick_v,0,0,1))
    lorenz = LorenzTransLib(stick_v)
    stick_right = []
    stick_left = []
    gate_right = []
    gate_left = []
    for _ in range(0,time):
        trans2stick_point1 = lorenz.positive_trans([g.point1[0],g.point1[3]])
        trans2stick_point2 = lorenz.positive_trans([g.point2[0],g.point2[3]])
        gate_left.append(trans2stick_point1)
        gate_right.append(trans2stick_point2)
        stick_right.append([s.point1[0],s.point1[3]])
        stick_left.append([s.point2[0],s.point2[3]])
        g.update()
        s.update()
    drew_base(axes,stick_left,stick_right,gate_left,gate_right)
if __name__ == "__main__":
    stick_v = 0.6*3e8
    time = 4
    fig = plt.figure(dpi=200)
    axes1 = fig.add_subplot(1,2,1)
    axes1.set_title("Ground")
    axes1.set_xlabel("x")
    axes1.set_ylabel("t")
    axes2 = fig.add_subplot(1,2,2)
    axes2.set_title("Stick")
    axes2.set_xlabel("x")
    axes2.set_ylabel("t")
    drew_ground(axes1,stick_v,time)
    drew_stick(axes2,stick_v,time)
    fig.savefig("1.png")