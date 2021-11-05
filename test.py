import percolation
import maze_site_percolation
import random
import numpy as np

def calculate_tipping_point():
    # ratio of percolating mazes 
    tries = 5000
    stats = {}
    for p in np.arange(0.0,0.5,0.1):
        print(str(p))
        p_c = []
        for i in range(tries):
            pm = maze_site_percolation.MazeSitePercolationModel(p=p, size=25)
            does_maze_percolate = pm.does_percolate()
            p_c.append(does_maze_percolate)
        stats[p] = p_c

    for p in np.arange(0.5,0.7,0.0125):
        print(str(p))
        p_c = []
        for i in range(tries):
            pm = maze_site_percolation.MazeSitePercolationModel(p=p, size=25)
            does_maze_percolate = pm.does_percolate()
            p_c.append(does_maze_percolate)
        stats[p] = p_c

    for p in np.arange(0.7,1.0,0.1):
        print(str(p))
        p_c = []
        for i in range(tries):
            pm = maze_site_percolation.MazeSitePercolationModel(p=p, size=25)
            does_maze_percolate = pm.does_percolate()
            p_c.append(does_maze_percolate)
        stats[p] = p_c
        
    for p in stats:
        print(str(p)+";"+str(np.mean(stats[p])))


def main():
    pm = maze_site_percolation.MazeSitePercolationModel(p=0.6, size=25)
    does_maze_percolate = pm.does_percolate()
    print('does_maze_percolate: ',does_maze_percolate)
    pm.output_grid_image('site_percolation_maze_grid.gif')
    pm.pretty_output_grid_image('site_percolation_maze_nowalls.gif',add_walls=False)
    pm.pretty_output_grid_image('site_percolation_maze_walls.gif',add_walls=True)
    rand_perc_path = pm.get_random_percolation_path()
    pm.output_pretty_percolation_path_image(rand_perc_path,'maze_percolation_path.gif')

    #calculate_tipping_point()

if __name__ == '__main__':
    main()
    