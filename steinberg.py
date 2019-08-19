'''
    Author: Kishen N Gowda
    This is the Steinberg class that I defined. It has mainly 4 functions, others are just aiding functions.
    steinberg() - Is the recursive function which checks the conditions according to procedurelist, and calls 
    the corresponding algo. 
    P1, P2, P3, P0 - Are the implementations of the different procedures of Steinberg's algorithm.
    plot() - A function to visualize the plot

    Important attributes:
    self.packing - list of coordinates of the rectangles in the final packing.
'''

class Steinberg:
    def __init__(self, rectangles, width_of_strip, procedurelist=['1', '-1', '0', '2', '-2', '3', '-3'], left_bottom = [0,0]):
        self.n = len(rectangles)
        self.width = width_of_strip
        self.input = rectangles
        self.procedurelist = procedurelist
        self.rectangles = self.create_input(rectangles)
        self.packing = [[[], []] for i in range(self.n)]
        self.q0 = left_bottom
        self.sheight = 0

    def create_input(self, rectangles):
        return [[i, rectangles[i][0], rectangles[i][1], rectangles[i][0]*rectangles[i][1]] for i in range(self.n)]

    def run(self):
        from operator import itemgetter
        from sys import exit
        if self.width < max(self.rectangles, key=itemgetter(1))[1]:
            print('Invalid Width of Strip!')
            exit(1)

        al, bl, sl = max(self.rectangles, key=itemgetter(1))[1], max(self.rectangles, key=itemgetter(2))[
            2], sum([self.rectangles[i][3] for i in range(self.n)])
        self.sheight = max(bl, round(2*sl/self.width, 8)+max(0,
                                                            round(2-self.width/al, 8)) * max(0, round(bl-sl/self.width, 8)))
        print('al: '+str(al) + ', bl: '+str(bl) + '\nSteinberg Calculated Height h: ' + str(self.sheight))
        print('#------------- Packing Starts ------------#')
        self.steinberg(self.rectangles, self.q0, [self.q0[0]+self.width, self.q0[1]+self.sheight])
        print('#------------- Packing Ends ------------#')
        print('#------------- Visualizing Packing ------------#')
        self.plot()
        print('Bye!')

    def steinberg(self, rectangles, lower, upper):
        from operator import itemgetter
        print('No. of rectangles = ' + str(len(rectangles)))
        if len(rectangles) == 0:
            return
        al, bl, sl = max(rectangles, key=itemgetter(1))[1], max(rectangles, key=itemgetter(2))[
            2], round(sum([rectangles[i][3] for i in range(len(rectangles))]), 8)
        u, v = round(upper[0]-lower[0], 8), round(upper[1]-lower[1], 8)
        rectangles.sort(key=itemgetter(1), reverse=True)
        print(lower, upper)
        print('al: ' + str(al) + ', bl: ' + str(bl))
        print('u: ' + str(u) + ' v: ' + str(v))
        for procedure in self.procedurelist:
            if procedure=='1':
                if (al >= round(u/2, 8)):
                    print('P1')
                    return self.p1(rectangles, lower, upper, inv=0)
            elif procedure=='-1':
                if bl>=round(v/2, 8):
                    print('P-1')
                    return self.p1(rectangles, lower, upper, inv=1)
            elif procedure=='2' or procedure=='-2':
                if al <= u/2 and bl <= v/2:
                    # -----------Procedure P2-------------------
                    i1, j1, flag = -1, -1, 0
                    for i in range(len(rectangles)):
                        if rectangles[i][1] >= round(u/4, 8) and rectangles[i][2] >= round(v/4, 8):
                            if flag == 0:
                                i1, flag = i, 1
                            elif flag == 1:
                                j1, flag = i, 2
                                break
                    if flag == 2 and round(2*(sl-rectangles[i1][3]-rectangles[j1][3]), 8) <= round((u-max(rectangles[i1][1], rectangles[j1][1]))*v, 8) and procedure=='2':
                        print('P2')
                        return self.p2(rectangles, lower, upper, i1, j1)
                    if flag == 2 and round(2*(sl-rectangles[i1][3]-rectangles[j1][3]), 8) <= round((v-max(rectangles[i1][2], rectangles[j1][2]))*u, 8) and procedure=='-2':
                        if rectangles[i1][2] < rectangles[j1][2]:
                            i1, j1 = j1, i1
                        print('P-2')
                        return self.p2(rectangles, lower, upper, i1, j1, inv=1)
                    # ---------End Procedure P2 -------------------
            elif procedure == '3' or procedure=='-3':
                if al <= u/2 and bl <= v/2:
                    # --------------Procedure P3-------------------
                    if len(rectangles) > 1:
                        sw, m, lb, rb = 0, -1, sl-u*v/4, 3*u*v/8
                        flag = 0
                        for i in range(len(rectangles)-1):
                            sw += rectangles[i][3]
                            if lb <= sw and sw <= rb and rectangles[i+1][1] <= u/4:
                                m = i+1
                                break
                        if m == -1:
                            sw = 0
                            rectangles.sort(key=itemgetter(2), reverse=True)
                            for i in range(len(rectangles)-1):
                                sw += rectangles[i][3]
                                if lb <= sw and sw <= rb and rectangles[i+1][2] <= v/4:
                                    m = i+1
                                    flag = 1
                                    break
                        if m != -1 and not flag and procedure=='3':
                            print('P3')
                            print('m:' + str(m))
                            return self.p3(rectangles, lower, upper, m, inv=flag)
                        if m != -1 and flag and procedure=='-3':
                            print('P-3')
                            print('m:' + str(m))
                            return self.p3(rectangles, lower, upper, m, inv=flag)
                    # ---------End Procedure P3 -------------------
            elif procedure=='0':
                if al <= u/2 and bl <= v/2:
                    # -----------Procedure P0-------------------
                    if max(rectangles, key=itemgetter(3))[3] >= round(sl-u*v/4, 8):
                        print('P0')
                        return self.p0(rectangles, lower, upper)
                    # ---------End Procedure P0 -------------------    
        print('Wasted')  # just for checking

    def p1(self, rectangles, lower, upper, inv=0):  # Procedure P1, P-1
        from operator import itemgetter
        if inv:
            rectangles.sort(key=itemgetter(2), reverse=True)
        count = len(rectangles)
        for i in range(len(rectangles)):
            if rectangles[i][1+inv] < round((upper[0+inv]-lower[0+inv])/2, 8):
                count = i
                break
        left, right = lower, upper
        for i in range(count):
            self.packing[rectangles[i][0]][0], self.packing[rectangles[i][0]][1] = left, [
                round(left[0]+rectangles[i][1], 8), round(left[1]+rectangles[i][2], 8)]
            left = [round(left[0]+inv*rectangles[i][1], 8),
                    round(left[1]+(1-inv)*rectangles[i][2], 8)]
        if count == len(rectangles):
            return
        hw = round(sum([rectangles[i][2-inv] for i in range(count)]), 8)
        rectangles = sorted(rectangles[count:],
                            key=itemgetter(2-inv), reverse=True)
        bl, vp = round(rectangles[0][2-inv],
                       8), round((upper[1-inv]-lower[1-inv])-hw, 8)
        print('vp: ' + str(vp))
        if bl > vp:  # To place blocks on right top
            count = len(rectangles)
            for i in range(len(rectangles)):
                if rectangles[i][2-inv] <= vp:
                    count = i
                    break
            for i in range(count):
                self.packing[rectangles[i][0]][0], self.packing[rectangles[i][0]][1] = [
                    round(right[0]-rectangles[i][1], 8), round(right[1]-rectangles[i][2], 8)], right
                right = [round(right[0]-(1-inv)*rectangles[i][1], 8),
                         round(right[1]-inv*rectangles[i][2], 8)]
            if count == len(rectangles):
                return self.packing
            rectangles = rectangles[count:]
        return self.steinberg(rectangles, left, right)

    def p2(self, rectangles, lower, upper, i, j, inv=0):  # Procedure P2, P-2
        self.packing[rectangles[i][0]][0] = lower
        self.packing[rectangles[i][0]][1] = [
            round(lower[0]+rectangles[i][1], 8), round(lower[1]+rectangles[i][2], 8)]
        self.packing[rectangles[j][0]][0] = [round(lower[0]+inv*rectangles[i][1], 8),
                                             round(lower[1]+(1-inv)*rectangles[i][2], 8)]
        self.packing[rectangles[j][0]][1] = [round(lower[0]+rectangles[j][1]+inv*rectangles[i][1], 8),
                                             round(lower[1]+(1-inv)*rectangles[i][2]+rectangles[j][2], 8)]
        left = [round(lower[0]+(1-inv)*rectangles[i][1], 8),
                round(lower[1]+inv*rectangles[i][2], 8)]
        rectangles = rectangles[:min(
            i, j)]+rectangles[min(i, j)+1:max(i, j)]+rectangles[max(j, i)+1:]
        if len(rectangles) == 0:
            return
        return self.steinberg(rectangles, left, upper)

    def p3(self, rectangles, lower, upper, m, inv=0):  # Procedure P3, P-3
        z, u, v = round(sum([rectangles[i][3] for i in range(m)]), 8), round(
            upper[0+inv] - lower[0+inv], 8), round(upper[1-inv]-lower[1-inv], 8)
        print('z: '+str(z))
        up, upp = max(round(u/2, 8), round(2*z/v, 8)
                      ), min(round(u/2, 8), round(u-2*z/v, 8))
        print("u': "+str(up)+" u'': "+str(upp))
        self.steinberg(rectangles[:m], lower, [(1-inv)*round(lower[0]+up, 8) + inv*upper[0], inv*round(lower[1]+up, 8)+(1-inv)*upper[1]])
        return self.steinberg(
            rectangles[m:], [(1-inv)*round(lower[0]+up, 8)+inv*lower[0], (1-inv)*lower[1]+inv*round(lower[1]+up, 8)], upper)

    def p0(self, rectangles, lower, upper):  # Procedure P0
        from operator import itemgetter
        i = rectangles.index(max(rectangles, key=itemgetter(3)))
        self.packing[rectangles[i][0]][0] = lower
        self.packing[rectangles[i][0]][1] = [
            round(lower[0]+rectangles[i][1], 8), round(lower[1]+rectangles[i][2], 8)]
        left = [round(lower[0]+rectangles[i][1], 8), round(lower[1], 8)]
        rectangles = rectangles[:i]+rectangles[i+1:]
        if len(rectangles) == 0:
            return
        return self.steinberg(rectangles, left, upper)

    def plot(self):  # Function for Visualization of Packing
        import matplotlib.patches as patches
        import matplotlib.pyplot as plt
        w, h = self.width, self.sheight
        fig, ax = plt.subplots(1)
        ax.set_xlim(self.q0[0], self.q0[0]+w)
        ax.set_ylim(self.q0[1], self.q0[1]+ h)
        for i in range(self.n):
            ax.add_patch(patches.Rectangle(
                tuple(self.packing[i][0]), self.packing[i][1][0]-self.packing[i][0][0], self.packing[i][1][1]-self.packing[i][0][1], linewidth=0.5, edgecolor='black', facecolor='none'
            ))
            ax.text(self.packing[i][1][0]-0.5*(self.packing[i][1][0]-self.packing[i][0][0]), self.packing[i][1][1]-0.5 *
                    (self.packing[i][1][1]-self.packing[i][0][1]), str(i), horizontalalignment='center')
        print('Actual Height: ' + str(max(self.packing, key=lambda x: x[1][1])[1][1]))
        plt.show()
