import pygame as pg
import math
import time

# Configuration
Max_value = 100000
rect_color = (255, 255, 255)
outline_color = (0, 0, 0)
width, height = 900, 900
RES = width // Max_value
if RES < 3:
    RES = 4
midW, midH = (width - RES) // 2, height // 2 - RES // 2

# Utility Functions
def isprime(value):
    if value < 2:
        return False
    for i in range(2, math.isqrt(value) + 1):
        if value % i == 0:
            return False
    return True

def rules(stepsTo):
    x, y = 0, 0
    if stepsTo % 4 == 1:
        x += 1
    elif stepsTo % 4 == 2:
        y -= 1
    elif stepsTo % 4 == 3:
        x -= 1
    elif stepsTo % 4 == 0:
        y += 1
    return x, y

def draw_spiral(screen, zoom, pan_x, pan_y, paused):
    counter = [1, 1]
    counterOldX = 1
    stepsTo = 1
    current_number = 1
    exit_loops = False

    while not exit_loops and not paused:
        for step in range(1, Max_value + 1):
            if exit_loops:
                break
            for i in range(stepsTo):
                if  isprime(current_number):
                    center_x = midW + RES * (counter[0] - 1) * zoom + pan_x
                    center_y = midH + RES * (counter[1] - 1) * zoom + pan_y

                    if center_x > width or center_y > height or center_x < 0 or center_y < 0:
                        print("I can't do more, please increase the width and height.")
                        print(f"Last number processed: {current_number}")
                        exit_loops = True
                        break

                    circle_radius = RES * zoom // 2
                    pg.draw.circle(screen, rect_color, (int(center_x), int(center_y)), int(circle_radius - 1))
                    pg.display.flip()
                    # time.sleep(0.001)

                counter[0] += rules(step)[0]
                counter[1] += rules(step)[1]

                current_number += 1
                if current_number > Max_value:
                    exit_loops = True
                    break
            if counterOldX != counter[1]:
                stepsTo += 1
            counterOldX = counter[1]
    running = False

def main():
    pg.init()
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption('Ulam Spiral Animation')
    clock = pg.time.Clock()

    zoom = 1.0
    pan_x, pan_y = 0, 0
    paused = False

    running = True
    screen.fill(outline_color)
    while running:

        draw_spiral(screen, zoom, pan_x, pan_y, paused)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:  # Pause/resume with 'p' key
                    paused = not paused
                    if paused:
                        print("Paused")
                    else:
                        print("Resumed")
                        draw_spiral(screen, zoom, pan_x, pan_y, paused)
                elif event.key == pg.K_s:  # Save the current screen with 's' key
                    pg.image.save(screen, 'ulam_spiral.png')
                    print("Screen saved as ulam_spiral.png")
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up to zoom in
                    zoom *= 1.1
                elif event.button == 5:  # Scroll down to zoom out
                    zoom *= 0.9
            elif event.type == pg.MOUSEMOTION:
                if pg.mouse.get_pressed()[0]:  # Drag to pan
                    dx, dy = event.rel
                    pan_x += dx
                    pan_y += dy

        pg.display.flip()
        clock.tick(60)  # Limit the frame rate

    pg.quit()

if __name__ == '__main__':
    main()
