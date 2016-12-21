import pygame
import sys
from museum import Museum, Vector2
from pygame.locals import *
import numpy as np

screen_x = 1024
screen_y = 768

n = 20
guards_percentage = 5
visitors_percentage = 20


y_res = screen_y / n
x_res = screen_x / n

square = min(x_res, y_res)
field = np.zeros([n, n])

scale = 1.

pygame.init()

wnd = pygame.display.set_mode((screen_x, screen_y), RESIZABLE)
caption = "Thief: %dx%d Guards %.2f%% Visitors %2.f%%" % (n, n, guards_percentage, visitors_percentage)
pygame.display.set_caption(caption)

gc = int(guards_percentage / 100. * n * n)
vc = int(visitors_percentage / 100. * n * n)
#museum = Museum(n, treasurePos=Vector2.random(n), guards_count=gc,visitors_count=vc)
museum = Museum(n, guards_count=gc,visitors_count=vc)
print 'stealing'
museum.steal()
print 'stolen'
def draw(h, w):
	global wnd
	wnd = pygame.display.set_mode((h, w), RESIZABLE)

	surf = pygame.Surface((n * 2, n * 2))
	max_cost = museum.max_cost
	surf.fill((0, 0, 0))
	for y in range(n):
		for x in range(n):
			x_pos = x * 2
			y_pos = y * 2
			val = museum.matrix[y][x]
			if val == -1:
				blue = 255
				red = 0
				green = 0
			elif val == -2:
				blue = 0
				red = 255
				green = 0
			#start
			elif val == -3:
				blue = 0
				red = 0
				green = 255
			#treasure
			elif val == -4:
				blue = 255
				red = 255
				green = 0
			elif val == -5:
				blue = 0
				red = 0
				green = 255
			else:
				val *= 1.
				blue = 0
				assert (val >= 0)
				red = int(val / (max_cost) * 255)
				green = 0
			pygame.draw.rect(surf, (red, green, blue), (x_pos, y_pos, 2, 2))

	wnd.fill((0, 0, 0))
	# noinspection PyUnboundLocalVariable
	aspect = 1. * x / y
	# ^ I have completely no idea what is going here, but it seems working
	if w < h:
		h = int(w / aspect)
	else:
		w = int(h * aspect)

	wnd.blit(pygame.transform.scale(surf, (h, w)), (0, 0))
	pygame.display.flip()


def handle_events(events):
	for event in events:
		if event.type == QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == VIDEORESIZE:
			draw(event.w, event.h)
		else:
			#print event
			pass


draw(screen_x, screen_y)
#pygame.draw.rect(wnd, (255,0,0), (50,50,100,100))

while True:
	handle_events(pygame.event.get())
	pygame.display.flip()
