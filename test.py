import percolation
import maze_percolation
import random

def main():
    
    pm = maze_percolation.MazePercolationModel(p=0.7, size=8)
    (percolation_path_root_list,does_maze_percolate) = pm.does_percolate()
    
    print(does_maze_percolate)
    pm.output_grid_image('maze_grid.gif')
    pm.pretty_output_grid_image('maze_percolation.gif')
    if does_maze_percolate:
        percolation_path_root = random.choice(percolation_path_root_list)
        perc_path = pm.get_percolation_path(percolation_path_root)
        #pm.output_percolation_path_image('maze_percolation.gif')
        pm.output_pretty_percolation_path_image('maze_percolation_path.gif')
    

    """
    p = percolation.PercolationModel(p=0.7, size=30)
    does_it_percolate = p.does_percolate()
    print(does_it_percolate)
    p.output_grid_image('percolation.gif')
    perc_path = p.get_percolation_path()
    if len(perc_path) > 0:
        p.output_percolation_path_image('percolation_path.gif')
    """

if __name__ == '__main__':
    main()
    