import maze_site_percolation

def main():
    pm = maze_site_percolation.MazeSitePercolationModel(p=0.5, size=40)
    pm.pretty_output_grid_image('maze_site_percolation.gif', add_walls=True)

if __name__ == '__main__':
    main()
    