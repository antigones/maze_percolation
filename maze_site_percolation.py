import numpy as np
import random as rd
from collections import defaultdict
from PIL import Image, ImageDraw
import imageio


class MazeSitePercolationModel:

    def __init__(self, p, size):
        #np.random.seed(100)
        n = 1
        self.p = p
        self.size = size
        self.horz_edges = np.random.binomial(n,self.p, size=(self.size*self.size))
        self.vert_edges = np.random.binomial(n,self.p, size=(self.size*self.size))
        #print(self.horz_edges)
        #print(self.vert_edges)
        self.percolation_path = None
    
    def pretty_output_grid_image(self, img_uri:str, add_walls=False)->Image:
        output_image = Image.new("RGB", (10*self.size, 10*self.size), "white")
        draw = ImageDraw.Draw(output_image)

        # draw horz bonds
        for i in range(len(self.horz_edges)):
            if self.horz_edges[i]:
                x0 = (i % self.size)*10
                x1 = x0 + 10
                y = (i//self.size)*10
                #print(str(x0)+":"+str(y))
                draw.line((x0,y,x1,y),fill="black")

        # draw vert bonds
        for i in range(len(self.horz_edges)):
            if self.horz_edges[i]:
                x0 = (i % self.size)*10
                x1 = x0
                y0 = (i//self.size)*10
                y1 = y0 + 10
                #print(str(x0)+":"+str(y0))
                draw.line((x0,y0,x1,y1),fill="black")
        # draw points lattice
        for (i,j) in [(i,j) for i in range(self.size*10) for j in range(self.size*10)]:
            draw.point((i*10,j*10), fill="black")
        output_image.save(img_uri)