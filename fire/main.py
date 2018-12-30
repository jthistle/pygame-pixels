#!/usr/bin/env python3

import pygame, math, sys, os, random
from colours import *

def drawPixel(surface, color, pos):
    pygame.draw.line(surface, color, pos, pos)

def draw4Pixels(surface, color, pos):
	#points = [pos, (pos[0]+1, pos[1]), (pos[0]+1, pos[1]+1), (pos[0], pos[1]+1)]
	#pygame.draw.polygon(surface, color, points)
    pygame.draw.line(surface, color, pos, (pos[0]+1, pos[1]), 2)

def main():
	pygame.init()
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 600

	DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	CLOCK = pygame.time.Clock()
	totalTime = 0

	maxFire = len(FIRE)-1
	minFire = 0

	pixelMap = []

	fireWidth = 150
	fireHeight = 80

	doGenerate = True

	wind = -5	# -5 to 5
	decaySpeed = 1

	for i in range(fireHeight):
		pixelMap.append([minFire for j in range(fireWidth)])

	fireBoxStart = (SCREEN_WIDTH//2-fireWidth, SCREEN_HEIGHT-fireHeight*2)

	while True:
		DISPLAY.fill(BLACK)
		deltaT = CLOCK.get_time()/1000
		totalTime += deltaT

		heldKeys = pygame.key.get_pressed()
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()

			elif e.type == pygame.KEYDOWN:
				heldKeys = pygame.key.get_pressed()
				if (heldKeys[pygame.K_RCTRL] or heldKeys[pygame.K_LCTRL]) and\
					(heldKeys[pygame.K_w] or heldKeys[pygame.K_q]):
					pygame.quit()

				if e.key == pygame.K_SPACE:
					doGenerate = not doGenerate
					if not doGenerate:
						pixelMap[-1] = [0 for j in range(fireWidth)]
				elif e.key == pygame.K_a:
					wind -= 1
					if wind < -5:
						wind = -5
				elif e.key == pygame.K_d:
					wind += 1
					if wind > 5:
						wind = 5

		if doGenerate:
			pixelMap[-1] = [maxFire for j in range(fireWidth)]

		for row in range(len(pixelMap)):
			for p in range(len(pixelMap[row])):
				windRand = random.randint(1,10)
				hor = 0
				if windRand <= wind+3:
					hor = 1
				elif windRand > wind+6:
					hor = -1

				if row > 0 and p+hor < len(pixelMap[row]) and p+hor >= 0:
					pixelMap[row-1][p+hor] = pixelMap[row][p] - (random.randint(2, 9)//3)
					if pixelMap[row-1][p+hor] < 0:
						pixelMap[row-1][p+hor] = 0
				
		for row in range(len(pixelMap)):
			for p in range(len(pixelMap[row])):
				val = pixelMap[row][p]
				draw4Pixels(DISPLAY, FIRE[val], (fireBoxStart[0]+p*2, fireBoxStart[1]+row*2))

		pygame.display.update()
		CLOCK.tick(24)

if __name__ == "__main__":
	main()