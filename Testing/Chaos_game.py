import pygame
import random
import math
import colorsys
from pygame.locals import *
from enum import Enum
index = [0, 0, 0]
points=[]
background_color=(0,0,0)

class Mode(Enum):
    AUTOMATIC = 0
    MANUAL = 1

def mark_pixel(surface, pos, pcol):
    col = surface.get_at(pos)
    surface.set_at(pos, (min(col[0] + pcol[0]/10, 255),
                         min(col[1] + pcol[1]/10, 255),
                         min(col[2] + pcol[2]/10, 255)))


def random_point_index(p):
    if len(p) <= 3:
        return random.randint(0, len(p) - 1)

    global index
    index[2] = index[1]
    index[1] = index[0]
    dst1 = abs(index[1] - index[2])

    used_indices = set(index)
    while True:
        index[0] = random.randint(0, len(p) - 1)
        dst = abs(index[0] - index[1])
        if dst1 == 0 and (dst == 1 or dst == len(p) - 1):
            continue
        elif index[0] in used_indices:
            continue
        else:
            used_indices.add(index[0])
            break

    return index[0]


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

def main(width, height, n, r,mode):
    try:
        Mode(mode)
        pygame.init()
        surface = pygame.display.set_mode((width, height))
        surface.fill(background_color)
        pygame.display.set_caption('Chaos Game')
        x, y = (400, 300)
        step = 0
        points_clicked = 0
        global points
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.image.save(surface, 'chaos_game_example.jpg')
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN and mode==Mode.MANUAL:
                    if points_clicked < n:
                        pygame.draw.circle(surface, (0, 0, 255), event.pos, 1 )
                        points_clicked += 1                    
                        points.append((event.pos[0],event.pos[1]))
                        pygame.display.update()
            if points_clicked == n or mode==Mode.AUTOMATIC:
                step = step + 1
                p = init_polygon(width, height, n,mode)
                point_idx = random_point_index(p)
                pos = p[point_idx][0]
                color = p[point_idx][1]
                x += (pos[0] - x) * r
                y += (pos[1] - y) * r
                mark_pixel(surface, (int(x), int(y)), color)
                print(step)
                if step % 1000 == 0:
                    font = pygame.font.Font(None, 24)
                    text = font.render(f"Iteration: {step}", True, (255,255,255), background_color)
                    surface.blit(text, (10, 10))
                    pygame.display.update()
                    pygame.display.update()

    except ValueError:
        print("Valor de modo invalido. Por favor ingresar 0 por modo automático y 1 para manual")


if __name__ == "__main__":
    n=6;mode=Mode.AUTOMATIC; main(800, 800, n, 0.45, mode)
    
