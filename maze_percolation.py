import numpy as np
import random as rd
from collections import defaultdict
from PIL import Image
import imageio


class MazePercolationModel:

    def __init__(self, p, size):
        #np.random.seed(42)
        n = 1
        self.p = p
        self.size = size
        self.grid = np.random.binomial(n,self.p, size=(self.size,self.size))
        self.percolation_path = None
        self.neighbours_map = self.build_adjacency_map(self.grid)

    def assess_neighbours(self,grid:np.ndarray,neighbours_map:dict,size:int,i:int,j:int) -> int:
        # n,nw,w,sw,s,se,e,ne
        # 0,1 ,2, 3,4, 5,6,7
        can_visit = [
            1, #w
            1, #s
            1, #e
        ]
        can_visit_idx = [
            (i,j-1), # w
            (i+1,j), # s
            (i,j+1), # e
        ]
        

        if j == 0:
            # first column
            can_visit[0] = 0

        if i == size-1:
            # last row
            can_visit[1] = 0

        if j == size-1:
            #last column
            can_visit[2] = 0
     
        for k in range(len(can_visit)):
            if can_visit[k] == 1:   
                # can go there and check
                k_i,k_j = can_visit_idx[k]
                if grid[k_i,k_j] == 1:
                    key = (i,j)
                    neighbours_map[key].append((k_i,k_j))
            
        return neighbours_map

    def build_adjacency_map(self, grid:np.ndarray) -> dict:
        neighbours_map = defaultdict(list)
        for (i,j) in [(i,j) for i in range(self.size) for j in range(self.size)]:
            if grid[i,j] == 1:
                alive_n = self.assess_neighbours(grid,neighbours_map, self.size,i,j)
        return neighbours_map

    def walk(self,from_cell:set)->bool:
        # just a BFS on the adjacency list
        visited = [from_cell]
        succ_list = [from_cell]
        while len(succ_list) > 0:
            (cur_i, cur_j) = succ_list.pop()
            if (cur_i == self.size - 1):
                # we found a path to the end
                return True
            
            for succ in self.neighbours_map[(cur_i, cur_j)]:
                if not succ in visited:
                    visited.append(succ)
                    succ_list.append(succ)
        return False


    def output_grid_image(self,img_uri):
        img_grid = self.grid.copy()
        img_grid[img_grid==0] = 255
        img_grid[img_grid==1] = 0
        im = Image.fromarray(img_grid)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        imageio.imsave(img_uri, im)

    def get_grid(self)->np.ndarray:
        return self.grid
        

    def does_percolate(self)->bool:
        # build adjacency list
        
        root = list(self.neighbours_map.keys())[0]
        result = self.walk(from_cell=root)
        return result

    def find_percolation_path(self, neighbours_map:dict,from_cell:set)->list:
        # just a BFS on the adjacency list, keeping track of the path
        
        visited = set()
        queue = [[from_cell]]
        while len(queue) > 0:
            path = queue.pop()
            cur_i, cur_j = path[-1]
            if (cur_i == self.size - 1):
                # we found a path to the end
                return path
            else:
                for succ in neighbours_map[(cur_i, cur_j)]:
                    if succ not in visited:
                        new_path = list(path)
                        new_path.append(succ)
                        queue.append(new_path)
        
                visited.add(succ)
        
        return queue
        

    def get_percolation_path(self)->list:
        root = list(self.neighbours_map.keys())[0]
        self.percolation_path = self.find_percolation_path(self.neighbours_map,from_cell=root)
        return self.percolation_path

    def output_percolation_path_image(self,img_uri):
        if len(self.percolation_path) > 0:
            img_grid = self.grid.copy()
            
            img_grid[img_grid==0] = 255
            img_grid[img_grid==1] = 0
            for (cell_i, cell_j) in self.percolation_path:
                img_grid[cell_i, cell_j] = 50
            im = Image.fromarray(img_grid)
            if im.mode != 'RGB':
                im = im.convert('RGB')
            imageio.imsave(img_uri, im)
        else:
            print('there is no percolation path to print')

