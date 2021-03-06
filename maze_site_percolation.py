import numpy as np
from collections import defaultdict
from PIL import Image, ImageDraw
import imageio
import random


class MazeSitePercolationModel:

    def __init__(self, p, size):
        # np.random.seed(100)
        n = 1
        self.p = p
        self.size = size
        self.grid = np.random.binomial(n, self.p, size=(self.size, self.size))
        self.neighbours_map = self.build_adjacency_map(self.grid)
        self.percolation_paths = self.try_to_percolate()

    def assess_neighbours(
            self,
            grid: np.ndarray,
            neighbours_map: dict,
            size: int,
            i: int,
            j: int) -> dict:
        # n,nw,w,sw,s,se,e,ne
        # 0,1 ,2, 3,4, 5,6,7
        can_visit = [
            1,  # w
            1,  # s
            1,  # e
        ]
        can_visit_idx = [
            (i, j-1),  # w
            (i+1, j),  # s
            (i, j+1),  # e
        ]
        if j == 0:
            # first column
            can_visit[0] = 0
        if i == size-1:
            # last row
            can_visit[1] = 0
        if j == size-1:
            # last column
            can_visit[2] = 0
        for k in range(len(can_visit)):
            if can_visit[k] == 1:
                # can go there and check
                k_i, k_j = can_visit_idx[k]
                if grid[k_i, k_j] == 1:
                    key = (i, j)
                    neighbours_map[key].append((k_i, k_j))

    def build_adjacency_map(self, grid: np.ndarray) -> dict:
        neighbours_map = defaultdict(list)
        for (i, j) in [(i, j) for i in range(self.size) for j in range(self.size)]:
            if grid[i, j] == 1:
                self.assess_neighbours(grid, neighbours_map, self.size, i, j)
        return neighbours_map

    def find_percolation_path(self, from_cell: set) -> list:
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
                for succ in self.neighbours_map[(cur_i, cur_j)]:
                    if succ not in visited:
                        new_path = list(path)
                        new_path.append(succ)
                        queue.append(new_path)
                visited.add(succ)
        return queue

    def get_grid(self) -> np.ndarray:
        return self.grid

    def does_percolate(self) -> bool:
        result = False
        for key in self.percolation_paths.keys():
            result = result or len(self.percolation_paths[key]) > 0
        return result

    def try_to_percolate(self) -> dict:
        # returns a dict with roots (keys) and eventual percolation path (value)
        # fluid can percolate from any of the upper cells
        filtered_dictionary = {(a, b): value for (a, b), value in self.neighbours_map.items() if a == 0}
        percolation_results = {}
        for key in filtered_dictionary.keys():
            root = key
            percolation_path_for_root = self.find_percolation_path(from_cell=root)
            percolation_results.update({root: percolation_path_for_root})
        return percolation_results

    def get_random_percolation_path(self) -> list:
        # choose a random percolating root
        roots_with_path = {k: v for k, v in self.percolation_paths.items() if len(v) > 0}
        if len(roots_with_path) > 0:
            rand_root = random.choice(list(roots_with_path.keys()))
            return self.get_percolation_path(rand_root)
        else:
            # no percolable root, return empty path (no path here)
            return []

    def get_percolation_path(self, root) -> list:
        return self.percolation_paths[root]

    # printing functions

    def output_grid_image(self, img_uri: str) -> Image:
        img_grid = self.grid.copy()
        img_grid[img_grid == 0] = 0
        img_grid[img_grid == 1] = 255
        im = Image.fromarray(img_grid)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        imageio.imsave(img_uri, im)

    def pretty_output_grid_image(self, img_uri: str, add_walls: bool) -> Image:
        output_image = Image.new("RGB", (10*self.size, 10*self.size), "white")
        draw = ImageDraw.Draw(output_image)
        self.draw_empty_cells(draw)
        self.draw_full_cells(draw)
        if add_walls:
            self.draw_walls(draw)
        # draw points lattice
        self.draw_lattice(draw)
        output_image.save(img_uri)

    def output_percolation_path_image(self, percolation_path: list, img_uri: str):
        img_grid = self.grid.copy()
        img_grid[img_grid == 0] = 255
        img_grid[img_grid == 1] = 0
        for (cell_i, cell_j) in percolation_path:
            img_grid[cell_i, cell_j] = 50
        im = Image.fromarray(img_grid)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        imageio.imsave(img_uri, im)

    def draw_walls(self, draw: ImageDraw):
        # additional horz lines
        for (i, j) in [(i, j) for i in range(1, self.size-1) for j in range(1, self.size-1)]:
            if self.grid[i-1, j-1] and self.grid[i-1, j] and self.grid[i-1, j+1] and self.grid[i, j-1] and self.grid[i, j] and self.grid[i, j+1]:
                draw.line((j*10, i*10, (j*10)+10, i*10), fill="black")
        # additional vert lines
        for (i, j) in [(i, j) for i in range(0, self.size-1) for j in range(0, self.size-1)]:
            if self.grid[i, j-1] and self.grid[i-1, j-1] and self.grid[i-1, j] and self.grid[i, j] and self.grid[i+1, j-1] and self.grid[i+1, j]:
                draw.line((j*10, i*10, j*10, (i*10)+10), fill="black")
        # last row is special
        for j in range(1, self.size-1):
            i = self.size-2
            if self.grid[i, j-1] and self.grid[i, j] and self.grid[i, j+1] and self.grid[i+1, j-1] and self.grid[i+1, j] and self.grid[i+1, j+1]:
                draw.line((j*10, i*10+10, j*10+10, i*10+10), fill="black")
        # last column is special
        for i in range(0, self.size-1):
            j = self.size-2
            if self.grid[i-1, j] and self.grid[i-1, j+1] and self.grid[i, j] and self.grid[i, j+1] and self.grid[i+1, j] and self.grid[i+1, j+1]:
                draw.line((j*10+10, i*10, j*10+10, i*10+10), fill="black")

    def draw_empty_cells(self, draw: ImageDraw):
        for (i, j) in [(i, j) for i in range(self.size) for j in range(self.size)]:
            if self.grid[j, i] == 1:
                draw.rectangle((i*10, j*10, i*10+10, j*10+10), fill="white")

    def draw_full_cells(self, draw: ImageDraw):
        for (i, j) in [(i, j) for i in range(self.size) for j in range(self.size)]:
            if self.grid[j, i] == 0:
                draw.rectangle((i*10, j*10, i*10+10, j*10+10), outline="black", width=1)

    def draw_lattice(self, draw: ImageDraw):
        for (i, j) in [(i, j) for i in range(self.size*10) for j in range(self.size*10)]:
            draw.point((i*10, j*10), fill="black")

    def draw_path(self, draw: ImageDraw, percolation_path: list):
        for (cell_j, cell_i) in percolation_path:
            draw.rectangle((cell_i*10, cell_j*10, cell_i*10+10, cell_j*10+10), fill="gray")

    def output_pretty_percolation_path_image(self, percolation_path: list, img_uri: str) -> Image:
        output_image = Image.new("RGB", (10*self.size, 10*self.size), "white")
        draw = ImageDraw.Draw(output_image)
        self.draw_empty_cells(draw)
        self.draw_path(draw, percolation_path)
        self.draw_full_cells(draw)
        self.draw_lattice(draw)
        output_image.save(img_uri)
