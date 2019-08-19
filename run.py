'''
    Implementation of Steinberg's 2-approximation recursive algorithm.
    Author: Kishen N Gowda
    Feel free to tweak the Steinberg class to make things more convenient to you.

    Input Format:
    - First line contains space separated one integer and one float, denoting the no. of rectangles and width of the strip respectively.
    - This is followed by 7 space separated integers, a permutation of [-1,1,0,-2,2,-3,3]. This denotes the order in which Steinberg's 
      algorithm will check satisfiability of the corresponding conditions. Default is [1, -1, 0, 2, -2, 3, -3]. If you want to use default,
      enter "-1"(without quotes).
    - This is followed by a single line containing two space separated floats, denoting the bottom left coordinate of your strip. Default is
      [0,0]. If you want to use default, enter "-1"(without quotes).
    - This is followed by n lines where each line should contain two space separated floats, width and height of the ith rectangle.

'''
from steinberg import Steinberg

# A driver program
def main():
    no_rect, strip_width = (float(s) for s in input().split())
    n, w = int(no_rect), strip_width
    procedurelist = [s for s in input().split()] # Procedure order to be followed in each iteration
    left_bottom = [float(s) for s in input().split()]
    if len(procedurelist) == 1:
        procedurelist = ['1', '-1', '0', '2', '-2', '3', '-3']
    if len(left_bottom) == 1:
        left_bottom = [0,0]
    rectangles = [[float(s) for s in input().split()] for j in range(n)]
    s = Steinberg(rectangles= rectangles, width_of_strip=w, procedurelist=procedurelist, left_bottom=left_bottom)
    s.run()


if __name__ == '__main__':
    main()
