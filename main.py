import pygame
from guide import Texts
from menu import Menu,Difficulty,Themes
from gameLoop import GameLoop

difficulty = "Normal"
speed = [5,20,3]
theme = ["charc.png","fired_charc.png","boosted_charc.png"]
def main():
	global difficulty,speed,theme
	m = Menu()
	m = m.menu()
	if m == "difficulty":
		d = Difficulty()
		difficulty = d.DiffMenu()
		main()
	if m == "themes":
		t = Themes()
		theme = t.Theme()
		main()
	if m == "guide":
		g = Texts(["How to play","Controls","Enemies"])
		g.main()
		main()
	if m == "start":
		if difficulty == "Easy":
			speed = [3,10,1]
		if difficulty == "Normal":
			speed = [5,20,3]
		if difficulty == "Hard":
			speed = [10,25,5]
		g = GameLoop(speed,difficulty,theme)
		g.main()
		main()



if __name__ == "__main__":
	pygame.init()
	main()
