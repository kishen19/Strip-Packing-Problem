'''
    Author: Kishen N Gowda
    Implementation of Steinberg's 2-Approximation Algorithm for Strip Packing Problem

'''

from sys import stdin, stdout, setrecursionlimit
from operator import itemgetter
from plot import visual_plot
setrecursionlimit(10**9)


'''For pi (i!=0), if inv=1, p-i is carried out'''


def p1(l, q0, q1, ans, inv=0):  # Procedure P1, P-1
    count = len(l)
    if inv:
        l.sort(key=itemgetter(1), reverse=True)
    for i in range(len(l)):
        if l[i][0+inv] < round((q1[0+inv]-q0[0+inv])/2, 2):
            count = i
            break
    left = q0
    for i in range(count):
        ans[l[i][3]][0], ans[l[i][3]][1] = left, [
            round(left[0]+l[i][0], 2), round(left[1]+l[i][1], 2)]
        left = [round(left[0]+inv*l[i][0], 2),
                round(left[1]+(1-inv)*l[i][1], 2)]
    if count == len(l):
        return ans
    sw = round(sum([l[i][1-inv] for i in range(count)]), 2)
    l = sorted(l[count:], key=itemgetter(1-inv), reverse=True)
    bl, vp = round(l[0][1-inv], 2), round((q1[1-inv]-q0[1-inv])-sw, 2)
    print('vp: ' + str(vp))
    print((round(q1[1-inv]-q0[1-inv])-sw, 2))
    if bl > vp:
        count = len(l)
        for i in range(len(l)):
            if l[i][1-inv] <= vp:
                count = i
                break
        right = q1
        for i in range(count):
            ans[l[i][3]][0], ans[l[i][3]][1] = [
                round(right[0]-l[i][0], 2), round(right[1]-l[i][1], 2)], right
            right = [round(right[0]-(1-inv)*l[i][0], 2),
                     round(right[1]-inv*l[i][1], 2)]
        if count == len(l):
            return ans
        l = l[count:]
        # print(ans)
        return steinberg(l, left, right, ans)
    else:
        # print(ans)
        return steinberg(l, left, q1, ans)


def p2(l, q0, q1, ans, i, j, inv=0):  # Procedure P2, P-2
    # print(l)
    ans[l[i][3]][0] = q0
    ans[l[i][3]][1] = [round(q0[0]+l[i][0], 2), round(q0[1]+l[i][1], 2)]
    ans[l[j][3]][0] = [round(q0[0]+inv*l[i][0], 2),
                       round(q0[1]+(1-inv)*l[i][1], 2)]
    ans[l[j][3]][1] = [round(q0[0]+l[j][0]+inv*l[i][0], 2),
                       round(q0[1]+(1-inv)*l[i][1]+l[j][1], 2)]
    left = [round(q0[0]+(1-inv)*l[i][0], 2), round(q0[1]+inv*l[i][1], 2)]
    l = l[:min(i, j)]+l[min(i, j)+1:max(i, j)]+l[max(j, i)+1:]
    # print(ans)
    if len(l) == 0:
        return ans
    return steinberg(l, left, q1, ans)


def p3(l, q0, q1, ans, m, inv=0):  # Procedure P3, P-3
    # print(l)
    z, u, v = round(sum([l[i][2] for i in range(m)]), 2), round(
        q1[0+inv] - q0[0+inv], 2), round(q1[1-inv]-q0[1-inv], 2)
    print('z: '+str(z))
    up = max(round(u/2, 2), round(2*z/v, 2))
    upp = min(round(u/2, 2), round(u-2*z/v, 2))
    print('up: '+str(up))
    if inv:
        ans = steinberg(l[:m], q0, [q1[0], round(q0[1]+up, 2)], ans)
        # print(ans)
    else:
        ans = steinberg(l[:m], q0, [round(q0[0]+up, 2), q1[1]], ans)
        # print(ans)
    if inv:
        # print(ans)
        return steinberg(l[m:], [q0[0], round(q0[1]+up, 2)], q1, ans)
    else:
        # print(ans)
        return steinberg(l[m:], [round(q0[0]+up, 2), q0[1]], q1, ans)


def p0(l, q0, q1, ans):  # Procedure P0
    # print(l)
    i = l.index(max(l, key=itemgetter(2)))
    ans[l[i][3]][0] = q0
    ans[l[i][3]][1] = [round(q0[0]+l[i][0], 2), round(q0[1]+l[i][1], 2)]
    left = [round(q0[0]+l[i][0], 2), round(q0[1], 2)]
    l = l[:i]+l[i+1:]
    # print(ans)
    if len(l) == 0:
        return ans
    else:
        return steinberg(l, left, q1, ans)


def steinberg(l, q0, q1, ans):  # Steinberg's Recursive algorithm
    print(len(l))
    if len(l) == 0:
        return ans
    al, bl = max(l, key=itemgetter(0))[0], max(l, key=itemgetter(1))[1]
    sl = round(sum([l[i][2] for i in range(len(l))]), 2)
    u, v = round(q1[0]-q0[0], 2), round(q1[1]-q0[1], 2)
    l.sort(key=itemgetter(0), reverse=True)
    print(q0, q1)
    print('u: '+str(u)+' v: '+str(v))
    if al >= round(u/2, 2) or bl >= round(v/2, 2):  # Procedure P1 and P-1
        if (al >= round(u/2, 2)):
            print('P1')
            return p1(l, q0, q1, ans, inv=0)
        else:
            print('P-1')
            return p1(l, q0, q1, ans, inv=1)
    elif al <= round(u/2, 2) and bl <= round(v/2, 2):
        # --------------Procedure P3-------------------
        if len(l) > 1:
            sw, m, lb, rb = 0, -1, round(sl-u*v/4, 2), round(3*u*v/8, 2)
            flag = 0
            for i in range(len(l)-1):
                sw += l[i][2]
                # print(sw)
                if lb <= round(sw, 2) and round(sw, 2) <= rb and l[i+1][0] <= round(u/4, 2):
                    m = i+1
                    break
            if m == -1:
                sw = 0
                l.sort(key=itemgetter(1), reverse=True)
                for i in range(len(l)-1):
                    sw += l[i][2]
                    if lb <= round(sw, 2) and round(sw, 2) <= rb and l[i+1][1] <= round(v/4, 2):
                        m = i
                        flag = 1
                        break
            if m != -1 and not flag:
                print('P3')
                print('m:'+str(m))
                return p3(l, q0, q1, ans, m, inv=flag)
            elif m != -1 and flag:
                print('P-3')
                print('m:'+str(m))
                return p3(l, q0, q1, ans, m, inv=flag)

        # ---------End Procedure P3 -------------------
        # -----------Procedure P0-------------------
        if max(l, key=itemgetter(2))[2] >= round(sl-u*v/4, 2):
            print('P0')
            return p0(l, q0, q1, ans)
        # ---------End Procedure P0 -------------------
        # -----------Procedure P2-------------------
        i1, j1, flag = -1, -1, 0
        for i in range(len(l)):
            if l[i][0] >= round(u/4, 2) and l[i][1] >= round(v/4, 2):
                if flag == 0:
                    i1, flag = i, 1
                elif flag == 1:
                    j1, flag = i, 2
                    break
        if flag == 2 and round(2*(sl-l[i1][2]-l[j1][2]), 2) <= round((u-max(l[i1][0], l[j1][0]))*v, 2):
            print('P2')
            return p2(l, q0, q1, ans, i1, j1)
        if flag == 2 and round(2*(sl-l[i1][2]-l[j1][2]), 2) <= round((v-max(l[i1][1], l[j1][1]))*u, 2):
            if l[i1][1] < l[j1][1]:
                i1, j1 = j1, i1
            print('P-2')
            return p2(l, q0, q1, ans, i1, j1, inv=1)
        # ---------End Procedure P2 -------------------
        print('Wasted')  # just for checking


def main():
    # Input #
    n = int(stdin.readline())
    L = [[round(float(s), 2) for s in stdin.readline().split()]
         for j in range(n)]

    l = [(L[i][0], L[i][1], round(L[i][0]*L[i][1], 2), i) for i in range(n)]

    bl = max(l, key=itemgetter(1))[1]
    print('bl: '+str(bl))
    al = max(l, key=itemgetter(0))[0]
    print('al: '+str(al))
    sl = sum([l[i][2] for i in range(n)])

    h = max(bl, round(2*sl, 2)+max(0, round(2-1/al, 2))
            * max(0, round(bl-sl, 2)))
    print('h: '+str(h))
    ans = [[[], []] for i in range(n)]
    ans = steinberg(l, [0, 0], [1, h], ans)
    visual_plot(ans, 1, h)


if __name__ == '__main__':
    main()
