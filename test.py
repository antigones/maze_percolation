import percolation
import maze_percolation


def main():
    pm = maze_percolation.MazePercolationModel(p=0.6, size=30)
    does_it_percolate = pm.does_percolate()
    print(does_it_percolate)
    pm.output_grid_image('percolation.gif')
    perc_path = pm.get_percolation_path()
    if len(perc_path) > 0:
        pm.output_percolation_path_image('percolation_path.gif')


if __name__ == '__main__':
    main()
    