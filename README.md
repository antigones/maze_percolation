# Mazes by Percolation

**MazeSitePercolationModel**

A maze generator to create mazes with site percolation.

**Initializing a maze**

    import  maze_site_percolation
    pm = maze_site_percolation.MazeSitePercolationModel(p=0.6, size=25)
Initializes a maze as a porous material with p, probability of having an hollow cell.

**Determining if maze percolates**


    does_maze_percolate = pm.does_percolate()
Determines if player could get to the end of the maze (i.e. the line in the bottom) starting from an hollow cell at the top.

**Saving the original grid image for the maze**

    pm.output_grid_image('site_percolation_maze_grid.gif')

![grid simulating a porous material](https://github.com/antigones/maze_percolation/blob/main/imgs/site_percolation_maze_grid.gif?raw=true)

**Saving a pretty image for the maze**

    pm.pretty_output_grid_image('site_percolation_maze_nowalls.gif', add_walls=False)
    pm.pretty_output_grid_image('site_percolation_maze_walls.gif', add_walls=True)

![generated maze (without walls)](https://github.com/antigones/maze_percolation/blob/main/imgs/site_percolation_maze_nowalls.gif?raw=true)

![generated maze (with walls)](https://github.com/antigones/maze_percolation/blob/main/imgs/site_percolation_maze_walls.gif?raw=true)

**Getting a random percolation path**

    rand_perc_path = pm.get_random_percolation_path()

Finds a random percolation path from the top of maze down to the bottom.

![enter image description here](https://github.com/antigones/maze_percolation/blob/main/imgs/maze_percolation_path.gif?raw=true)
