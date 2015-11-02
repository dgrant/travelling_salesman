from TSP import *

def main():
    random.seed(100)
    coords = [x for x in randomCoords(100, 1000)]
    tour = solve_greedySimple(coords,1e99)
    #img_file = 'temp.png'
    #write_tour_to_img(coords, tour, img_file)

import cProfile as profile
profile.run('main()', 'TSP.prof')

import pstats
p = pstats.Stats('TSP.prof')
p.strip_dirs().sort_stats('time').print_stats(10)
