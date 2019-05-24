'''
    Author: Kishen N Gowda
    Implementation of Steinberg's 2-Approximation Algorithm for Strip Packing Problem

'''

from sys import stdin, stdout, setrecursionlimit
from operator import itemgetter
from plot import visual_plot
setrecursionlimit(10**9)


'''For Pi (i!=0), if inv=1, p-i is carried out'''


def p1(l, q0, q1, ans, inv=0):  # Procedure P1, P-1
    count = len(l)
    if inv:
        l.sort(key=itemgetter(1), reverse=True)
    for i in range(len(l)):
        if l[i][0+inv] < round((q1[0+inv]-q0[0+inv])/2, 8):
            count = i
            break
    left = q0
    for i in range(count):
        ans[l[i][3]][0], ans[l[i][3]][1] = left, [
            round(left[0]+l[i][0], 8), round(left[1]+l[i][1], 8)]
        left = [round(left[0]+inv*l[i][0], 8),
                round(left[1]+(1-inv)*l[i][1], 8)]
    if count == len(l):
        return ans
    sw = round(sum([l[i][1-inv] for i in range(count)]), 8)
    l = sorted(l[count:], key=itemgetter(1-inv), reverse=True)
    bl, vp = round(l[0][1-inv], 8), round((q1[1-inv]-q0[1-inv])-sw, 8)
    print('vp: ' + str(vp))
    if bl > vp:  # To place blocks on right top
        count = len(l)
        for i in range(len(l)):
            if l[i][1-inv] <= vp:
                count = i
                break
        right = q1
        for i in range(count):
            ans[l[i][3]][0], ans[l[i][3]][1] = [
                round(right[0]-l[i][0], 8), round(right[1]-l[i][1], 8)], right
            right = [round(right[0]-(1-inv)*l[i][0], 8),
                     round(right[1]-inv*l[i][1], 8)]
        if count == len(l):
            return ans
        l = l[count:]
        return steinberg(l, left, right, ans)
    else:
        return steinberg(l, left, q1, ans)


def p2(l, q0, q1, ans, i, j, inv=0):  # Procedure P2, P-2
    ans[l[i][3]][0] = q0
    ans[l[i][3]][1] = [round(q0[0]+l[i][0], 8), round(q0[1]+l[i][1], 8)]
    ans[l[j][3]][0] = [round(q0[0]+inv*l[i][0], 8),
                       round(q0[1]+(1-inv)*l[i][1], 8)]
    ans[l[j][3]][1] = [round(q0[0]+l[j][0]+inv*l[i][0], 8),
                       round(q0[1]+(1-inv)*l[i][1]+l[j][1], 8)]
    left = [round(q0[0]+(1-inv)*l[i][0], 8), round(q0[1]+inv*l[i][1], 8)]
    l = l[:min(i, j)]+l[min(i, j)+1:max(i, j)]+l[max(j, i)+1:]
    if len(l) == 0:
        return ans
    return steinberg(l, left, q1, ans)


def p3(l, q0, q1, ans, m, inv=0):  # Procedure P3, P-3
    z, u, v = round(sum([l[i][2] for i in range(m)]), 8), round(
        q1[0+inv] - q0[0+inv], 8), round(q1[1-inv]-q0[1-inv], 8)
    print('z: '+str(z))
    up = max(round(u/2, 8), round(2*z/v, 8))
    upp = min(round(u/2, 8), round(u-2*z/v, 8))
    print("u': "+str(up)+" u'': "+str(upp))
    if inv:
        ans = steinberg(l[:m], q0, [q1[0], round(q0[1]+up, 8)], ans)
    else:
        ans = steinberg(l[:m], q0, [round(q0[0]+up, 8), q1[1]], ans)
    if inv:
        return steinberg(l[m:], [q0[0], round(q0[1]+up, 8)], q1, ans)
    else:
        return steinberg(l[m:], [round(q0[0]+up, 8), q0[1]], q1, ans)


def p0(l, q0, q1, ans):  # Procedure P0
    i = l.index(max(l, key=itemgetter(2)))
    ans[l[i][3]][0] = q0
    ans[l[i][3]][1] = [round(q0[0]+l[i][0], 8), round(q0[1]+l[i][1], 8)]
    left = [round(q0[0]+l[i][0], 8), round(q0[1], 8)]
    l = l[:i]+l[i+1:]
    if len(l) == 0:
        return ans
    else:
        return steinberg(l, left, q1, ans)


def steinberg(l, q0, q1, ans):  # Steinberg's Recursive algorithm
    print('No. of rectangles = ' + str(len(l)))
    if len(l) == 0:
        return ans
    al, bl = max(l, key=itemgetter(0))[0], max(l, key=itemgetter(1))[1]
    sl = round(sum([l[i][2] for i in range(len(l))]), 8)
    u, v = round(q1[0]-q0[0], 8), round(q1[1]-q0[1], 8)
    l.sort(key=itemgetter(0), reverse=True)
    print(q0, q1)
    print('al: ' + str(al) + ', bl: ' + str(bl))
    print('u: ' + str(u) + ' v: ' + str(v))
    if al >= u/2 or bl >= v/2:  # Procedure P1 and P-1
        if (al >= round(u/2, 8)):
            print('P1')
            return p1(l, q0, q1, ans, inv=0)
        else:
            print('P-1')
            return p1(l, q0, q1, ans, inv=1)
    elif al <= u/2 and bl <= v/2:
        # -----------Procedure P0-------------------
        if max(l, key=itemgetter(2))[2] >= round(sl-u*v/4, 8):
            print('P0')
            return p0(l, q0, q1, ans)
        # ---------End Procedure P0 -------------------
        # -----------Procedure P2-------------------
        i1, j1, flag = -1, -1, 0
        for i in range(len(l)):
            if l[i][0] >= round(u/4, 8) and l[i][1] >= round(v/4, 8):
                if flag == 0:
                    i1, flag = i, 1
                elif flag == 1:
                    j1, flag = i, 2
                    break
        if flag == 2 and round(2*(sl-l[i1][2]-l[j1][2]), 8) <= round((u-max(l[i1][0], l[j1][0]))*v, 8):
            print('P2')
            return p2(l, q0, q1, ans, i1, j1)
        if flag == 2 and round(2*(sl-l[i1][2]-l[j1][2]), 8) <= round((v-max(l[i1][1], l[j1][1]))*u, 8):
            if l[i1][1] < l[j1][1]:
                i1, j1 = j1, i1
            print('P-2')
            return p2(l, q0, q1, ans, i1, j1, inv=1)
        # ---------End Procedure P2 -------------------
        # --------------Procedure P3-------------------
        if len(l) > 1:
            sw, m, lb, rb = 0, -1, sl-u*v/4, 3*u*v/8
            flag = 0
            for i in range(len(l)-1):
                sw += l[i][2]
                if lb <= sw and sw <= rb and l[i+1][0] <= u/4:
                    m = i+1
                    break
            if m == -1:
                sw = 0
                l.sort(key=itemgetter(1), reverse=True)
                for i in range(len(l)-1):
                    sw += l[i][2]
                    if lb <= sw and sw <= rb and l[i+1][1] <= v/4:
                        m = i+1
                        flag = 1
                        break
            if m != -1 and not flag:
                print('P3')
                print('m:' + str(m))
                return p3(l, q0, q1, ans, m, inv=flag)
            elif m != -1 and flag:
                print('P-3')
                print('m:' + str(m))
                return p3(l, q0, q1, ans, m, inv=flag)

        # ---------End Procedure P3 -------------------
        print('Wasted')  # just for checking


def main():
    # Input #
    n = int(stdin.readline())
    L = [[round(float(s), 8) for s in stdin.readline().split()]
         for j in range(n)]

    l = [(L[i][0], L[i][1], round(L[i][0]*L[i][1], 8), i) for i in range(n)]

    bl = max(l, key=itemgetter(1))[1]
    print('bl: '+str(bl))
    al = max(l, key=itemgetter(0))[0]
    print('al: '+str(al))
    sl = sum([l[i][2] for i in range(n)])

    h = max(bl, round(2*sl, 8)+max(0, round(2-1/al, 8))
            * max(0, round(bl-sl, 8)))
    print('h: '+str(h))
    ans = [[[], []] for i in range(n)]
    ans = steinberg(l, [0, 0], [1, h], ans)
    visual_plot(ans, 1, h)


if __name__ == '__main__':
    main()
