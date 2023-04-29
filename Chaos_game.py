import pygame
import random
import math
import colorsys
import argparse
from pygame.locals import *
from enum import Enum

points=[]
background_color=(0,0,0)
vertex=[0,0,0]

# args
parser = argparse.ArgumentParser(description="Python Chaos game - David Nuñez Gurrola")
parser.add_argument('-m', '--mode', metavar="Mode", type=int, help='Please press 0 for automatic mode (use geometry to create a regular polygon) or press 1 for manual mode (create a irregular polygon)', default=0)
parser.add_argument('-n', '--nodes', metavar="Nodes", type=int, help='Please enter the number of nodes of the polygon', required=True)
parser.add_argument('-r', '--ratio', metavar="Ratio", type=float, help='Please enter the size of the jump between point and vertex (Between 0-1) the default amount is 0.5', default=0.5)
args = parser.parse_args()

class Mode(Enum):
    AUTOMATIC = 0
    MANUAL = 1


"""
Code Analysis

Objective:
The objective of the function is to modify the color of a pixel on a given surface by adding a fraction of a given color to the current color of the pixel. This is useful for creating visual effects such as shading or highlighting.

Inputs:
- surface: a pygame Surface object representing the surface on which the pixel is located
- pos: a tuple representing the position of the pixel on the surface
- pcol: a tuple representing the color to be added to the current color of the pixel

Flow:
1. Get the current color of the pixel at the given position on the surface.
2. Calculate the new color by adding a fraction of the given color to the current color.
3. Set the color of the pixel at the given position on the surface to the new color.

Outputs:
- None

Additional aspects:
- The function uses the Pygame library to manipulate surfaces and colors.
- The function modifies the color of a single pixel at a time, so it may need to be called multiple times to achieve the desired effect.
- The function ensures that the color values do not exceed 255 by using the min() function.
"""
def mark_pixel(surface, pos, pcol):
    col = surface.get_at(pos)
    surface.set_at(pos, (min(col[0] + pcol[0]/10, 255),
                         min(col[1] + pcol[1]/10, 255),
                         min(col[2] + pcol[2]/10, 255)))

"""
Objective:
The objective of the function is to generate a random vertex 
for a given set of points, with the condition that the vertex 
should not be the same as the previous two indices and the distance 
between the current vertex and the previous vertex should not be 1 or 
the length of the set minus 1.

Inputs:
- p: a set of points

Flow:
1. If the length of the set is less than or equal to 3, return a random vertex between 0 and the length of the set minus 1.
2. Set the global variable vertex[2] to vertex[1] and vertex[1] to vertex[0].
3. Calculate the distance between vertex[1] and vertex[2].
4. Create a set of used indices.
5. Loop until a valid vertex is found:
   a. Generate a random vertex between 0 and the length of the set minus 1.
   b. Calculate the distance between the new vertex and vertex[1].
   c. If the distance between vertex[1] and vertex[2] is 0 and the distance between the new vertex and vertex[1] is 1 or the length of the set minus 1, continue to the next iteration of the loop.
   d. If the new vertex is already in the set of used indices, continue to the next iteration of the loop.
   e. Otherwise, add the new vertex to the set of used indices and break out of the loop.
6. Return the new vertex.

Outputs:
- A random vertex for the given set of points.

Additional aspects:
- The function uses a global variable vertex to keep track of the previous two indices.
- The function ensures that the returned vertex is not the same as the previous two indices 
and the distance between the current vertex and the previous vertex is not 1 or the length of 
the set minus 1. This is to prevent the chaos game from generating points that are too close 
together or overlapping.

"""
def random_point_vertex(p):
    if len(p) <= 3:
        return random.randint(0, len(p) - 1)
    global vertex
    vertex[2] = vertex[1]
    vertex[1] = vertex[0]
    # checks if the two prevously vertices are the same
    distance1 = abs(vertex[1] - vertex[2])
    used_indices = set(vertex)
    while True:
        vertex[0] = random.randint(0, len(p) - 1)
        # distance of the actual point with the last one. If the distance is one, this means
        # they are adjacent
        distance = abs(vertex[0] - vertex[1])
        
        """
        the currently chosen vertex cannot be a neighbor of the previously chosen vertex if the 
        two previously chosen vertices are the same. See more https://en.wikipedia.org/wiki/Chaos_game.
        """
        if distance1 == 0 and (distance == 1 or distance == len(p) - 1):
            continue
        # elif vertex[0] in used_indices:
        #     continue
        else:
            used_indices.add(vertex[0])
            break

    return vertex[0]


"""
Objective:
The objective of the main function is to implement the chaos game algorithm to generate a fractal image. The function takes in the width and height of the surface, the number of nodes of the polygon, the scaling factor, and the mode of the polygon (automatic or manual). The function generates a set of points that define the polygon, and then iteratively generates new points using the chaos game algorithm. The function updates the surface with each new point, creating a fractal image.

Inputs:
- width: an integer representing the width of the surface
- height: an integer representing the height of the surface
- n: an integer representing the number of nodes of the polygon
- r: a float representing the scaling factor for the chaos game algorithm
- mode: an enum representing the mode of the polygon (automatic or manual)

Flow:
1. Initialize the Pygame library and create a surface with the given width and height.
2. If the mode is manual, allow the user to click on the surface to define the points of the polygon.
3. Generate the set of points that define the polygon using the init_polygon function.
4. Loop until the user closes the window:
   a. If the mode is manual and the user has not clicked on all the points of the polygon, wait for the user to click on the surface.
   b. If the mode is automatic or the user has clicked on all the points of the polygon, generate a new point using the random_point_vertex function.
   c. Update the position of the current point using the chaos game algorithm.
   d. Update the surface with the new point using the mark_pixel function.
   e. If a certain number of iterations have passed, display the current iteration number on the surface.
5. When the user closes the window, save the image and quit Pygame.

Outputs:
- None

Additional aspects:
- The function uses the Pygame library to create and manipulate surfaces.
- The function uses the init_polygon function to generate the set of points that define the polygon.
- The function uses the random_point_vertex function to generate a random vertex for the set of points.
- The function uses the chaos game algorithm to generate new points.
- The function uses the mark_pixel function to update the surface with each new point.
- The function displays the current iteration number on the surface every certain number of iterations.
- The function saves the generated image when the user closes the window.

"""
def init_polygon(width, height, n=3, mode=Mode.AUTOMATIC):
    
    delta_angle = 360/n
    r = width/2 - 10
    p = []

    for i in range(0, n):
        angle = (180 + i*delta_angle) * math.pi / 180
        color = colorsys.hsv_to_rgb((i*delta_angle)/360, 0.8, 1)
        # with a regular polygon
        if mode==Mode.AUTOMATIC:
            
            p.append(((width/2 + r*math.sin(angle),
                    height/2 + r*math.cos(angle)),
                    (int(color[0]*255), int(color[1]*255), int(color[2]*255))))
        # manual points
        elif mode==Mode.MANUAL:
            p.append(((points[i][0],
                    points[i][1]),
                    (int(color[0]*255), int(color[1]*255), int(color[2]*255))))
    return p



"""
Objective:
The objective of the main function is to implement the chaos game algorithm to generate a fractal image. The function takes in the width and height of the surface, the number of nodes of the polygon, the scaling factor, and the mode of the polygon (automatic or manual). The function generates a set of points that define the polygon, and then iteratively generates new points using the chaos game algorithm. The function updates the surface with each new point, creating a fractal image.

Inputs:
- width: an integer representing the width of the surface
- height: an integer representing the height of the surface
- n: an integer representing the number of nodes of the polygon
- r: a float representing the scaling factor for the chaos game algorithm
- mode: an enum representing the mode of the polygon (automatic or manual)

Flow:
1. Initialize the Pygame library and create a surface with the given width and height.
2. If the mode is manual, allow the user to click on the surface to define the points of the polygon.
3. Generate the set of points that define the polygon using the init_polygon function.
4. Loop until the user closes the window:
   a. If the mode is manual and the user has not clicked on all the points of the polygon, wait for the user to click on the surface.
   b. If the mode is automatic or the user has clicked on all the points of the polygon, generate a new point using the random_point_vertex function.
   c. Update the position of the current point using the chaos game algorithm.
   d. Update the surface with the new point using the mark_pixel function.
   e. If a certain number of iterations have passed, display the current iteration number on the surface.
5. When the user closes the window, save the image and quit Pygame.
"""
def main(width, height, n, r,mode):
    try:
        Mode(mode)
        pygame.init()
        surface = pygame.display.set_mode((width, height))
        surface.fill(background_color)
        pygame.display.set_caption('Chaos Game')
        x, y = (400, 300)
        step = 0
        if mode==Mode.AUTOMATIC:
            p = init_polygon(width, height, n,mode)
        else:
            pass
        points_clicked = 0
        global points
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.image.save(surface, 'Images/chaos_game_sup_sup.jpg')
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN and mode==Mode.MANUAL:
                    if points_clicked < n:
                        pygame.draw.circle(surface, (0, 0, 255), event.pos, 1 )
                        points_clicked += 1                    
                        points.append((event.pos[0],event.pos[1]))
                        pygame.display.update()
            step = step + 1
            if points_clicked ==n:
                p = init_polygon(width, height, n,mode)
                point_vertex = random_point_vertex(p)
                
            elif mode == Mode.AUTOMATIC:
                point_vertex = random_point_vertex(p)
            else:    
                continue
            # print(point_vertex)
            pos = p[point_vertex][0]
            color = p[point_vertex][1]
            x += (pos[0] - x) * r
            y += (pos[1] - y) * r
            #print(f"position {pos}, color= {color}, x = {x}, y = {y}")
            mark_pixel(surface, (int(x), int(y)), color)
            if step % 1000 == 0:
                font = pygame.font.Font(None, 24)
                text = font.render(f"Iteration: {step}", True, (255,255,255), background_color)
                surface.blit(text, (10, 10))
                pygame.display.update()       
    except ValueError:
        print("Valor de modo invalido. Por favor ingresar 0 por modo automático y 1 para manual")
    
if __name__ == "__main__":
    main(800, 800, args.nodes, args.ratio, Mode(args.mode))
    
    
