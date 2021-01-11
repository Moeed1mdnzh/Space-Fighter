import pygame,time
import random as r


class Menu:
	def __init__(self):
		pygame.init()
		self.W,self.H = 700,600
		self.caption_name = "Space Fighter"
		self.caption = pygame.display.set_caption(self.caption_name)
		self.win = pygame.display.set_mode((self.W,self.H))
		self.selectFont = pygame.font.SysFont("monospace",30,bold=True) 
		self.fill_color = (10,10,10)
		self.text_details = {

		"start":(pygame.font.SysFont('monospace',40,bold=True,italic=True),(0,130))
		,"difficulty":(pygame.font.SysFont('monospace',30,bold=True,italic=True),(0,130+60))
		,"themes":(pygame.font.SysFont('monospace',30,bold=True,italic=True),(0,130+120))
		,"guide":(pygame.font.SysFont('monospace',30,bold=True,italic=True),(0,130+180))
		,"quit":(pygame.font.SysFont('monospace',30,bold=True,italic=True),(0,130+240))

		}
		self.font = pygame.font.SysFont('agencyfb',80,'light')
		self.pos = None
		self.begin = [False,None]
		self.backgrounds =[ 

		[pygame.image.load("menu_bg (1).png"),(0,0)],
		[pygame.image.load("menu_bg (2).png"),(0,200)],
		[pygame.image.load("menu_bg (3).png"),(0,400)]

		]
		self.selection_sound = pygame.mixer.Sound("select_sound.mp3")

	def backGround(self):
		for background in self.backgrounds:			
			self.win.blit(background[0],background[1])

	def select(self,task):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					self.selection_sound.play()
					time.sleep(1)
					if task == "start":
						self.begin = (True,task)
					elif task == "difficulty":
						self.begin = (True,task)
					elif task == "themes":
						self.begin = (True,task)
					elif task == "guide":
						self.begin = (True,task)
					elif task == "quit":
						pygame.quit()
						quit()

	def click(self):
		self.pos = pygame.mouse.get_pos()
		if self.pos[0] in range(0,130) and self.pos[1] in range(130,130+60):
			pygame.draw.rect(self.win,(170,0,170),(0,130,130,50),5)
			self.select("start")
		elif self.pos[0] in range(0,190) and self.pos[1] in range(130+60,130+120):
			pygame.draw.rect(self.win,(170,0,170),(0,130+60,190,40),5)
			self.select("difficulty")
		elif self.pos[0] in range(0,120) and self.pos[1] in range(130+120,130+180):
			pygame.draw.rect(self.win,(170,0,170),(0,130+120,120,40),5)
			self.select("themes")
		elif self.pos[0] in range(0,100) and self.pos[1] in range(130+180,130+240):
			pygame.draw.rect(self.win,(170,0,170),(0,130+180,100,40),5)
			self.select("guide")
		elif self.pos[0] in range(0,80) and self.pos[1] in range(130+180,130+300):
			pygame.draw.rect(self.win,(170,0,170),(0,130+240,80,40),5)
			self.select("quit")

	def Quit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			

	def Caption(self,font,name):
		rendered = font.render(name,True,(220,220,220))
		self.win.blit(rendered,(0,20))
		pygame.draw.line(self.win,(220,220,220),(0,110),(450,110),10)

	def display_text(self,text,font,coordinates):
		rendered = font.render(text,True,(200,200,200))
		self.win.blit(rendered,coordinates)

	def stop(self,delay):
		pygame.time.delay(delay)

	def refresh(self):
		pygame.display.update()

	def fill(self,fill_color):
		self.win.fill(fill_color)

	def menu(self):
		while True:
			self.fill(self.fill_color)
			self.stop(50)
			self.backGround()
			self.click()
			self.Caption(self.font,"Space Fighter")
			for text,details in self.text_details.items():
				self.display_text(text,details[0],details[1])
			if self.begin[0]:
				return self.begin[1]
			self.Quit()
			self.refresh()

class Difficulty(Menu):
	def __init__(self):
		super().__init__()
		self.difficulties = ["Easy","Normal","Hard"]
		self.diffFont = pygame.font.SysFont("monospace",50,bold=True)
		self.selected = False
		self.textX,self.textY = 270,250
		self.pos = None
		self.switch_sound = pygame.mixer.Sound("select_sound2.mp3")
		self.index = 0

	def Shapes(self):
		pygame.draw.polygon(self.win,(255,255,255),[(200,300),(160,280),(200,260)])
		pygame.draw.polygon(self.win,(255,255,255),[(460,300),(500,280),(460,260)])
		self.pos = pygame.mouse.get_pos()
		if self.pos[0] in range(280,390) and self.pos[1] in range(110,140):
			pygame.draw.rect(self.win,(170,0,170),[280,110,110,30],4)

	def Texts(self,text):
		rendered = self.diffFont.render(text,True,(250,250,250))
		self.win.blit(rendered,(self.textX,self.textY))
		rendered = self.selectFont.render("select",True,(250,250,250))
		self.win.blit(rendered,(280,110))		

	def switch(self):
		self.pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					if True:
						if self.pos[0] in range(160,200) and self.pos[1] in range(260,300):
							self.switch_sound.play()
							pygame.draw.polygon(self.win,(0,0,0),[(200,300),(160,280),(200,260)])
							if self.index != 0:
								self.index -= 1
							else:
								self.index = 2
					if True:
						if self.pos[0] in range(460,500) and self.pos[1] in range(260,300):
							self.switch_sound.play()
							pygame.draw.polygon(self.win,(0,0,0),[(460,300),(500,280),(460,260)])
							if self.index != 2:
								self.index += 1
							else:
								self.index = 0
					if True:
						if self.pos[0] in range(280,390) and self.pos[1] in range(110,140):
							self.selection_sound.play()
							self.selected = True

	def DiffMenu(self):
		while True:
			self.fill((20,20,20))
			self.stop(100)
			if self.index == 1:
				self.textX = 250
			else:
				self.textX = 270
			self.Texts(self.difficulties[self.index])
			self.Shapes()
			self.switch()
			self.Quit()
			self.refresh()
			if self.selected:
				return self.difficulties[self.index]



class Themes(Menu):
	def __init__(self):
		super().__init__()
		self.themes = ["charc.png","charc2.png","charc3.png","charc4.png"]
		self.current_theme = pygame.image.load(self.themes[0])
		self.theme_cooridnate = (70,60)
		self.selected = False
		self.pos = None
		self.switch_sound = pygame.mixer.Sound("select_sound2.mp3")
		self.index = 0

	def choice(self):
		pass

	def resize(self):
		self.current_theme = pygame.transform.scale(self.current_theme,(600,600))

	def skip(self):
		self.pos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					if True:
						if self.pos[0] in range(160,200) and self.pos[1] in range(260,300):
							self.switch_sound.play()
							pygame.draw.polygon(self.win,(0,0,0),[(200,300),(160,280),(200,260)])
							if self.index != 0:
								self.index -= 1
							else:
								self.index = 2
					if True:
						if self.pos[0] in range(460,500) and self.pos[1] in range(260,300):
							self.switch_sound.play()
							pygame.draw.polygon(self.win,(0,0,0),[(470,300),(510,280),(470,260)])
							if self.index != 3:
								self.index += 1
							else:
								self.index = 0
					if True:
						if self.pos[0] in range(280,390) and self.pos[1] in range(110,140):
							self.selection_sound.play()
							self.selected = True

	def switch_button(self):
		pygame.draw.polygon(self.win,(255,255,255),[(200,300),(160,280),(200,260)])
		pygame.draw.polygon(self.win,(255,255,255),[(470,300),(510,280),(470,260)])
		self.pos = pygame.mouse.get_pos()
		if self.pos[0] in range(280,390) and self.pos[1] in range(110,140):
			pygame.draw.rect(self.win,(170,0,170),[280,110,110,30],4)
	def display(self):
		self.win.blit(self.current_theme,self.theme_cooridnate)
		rendered = self.selectFont.render("select",True,(250,250,250))
		self.win.blit(rendered,(280,110))

	def Theme(self):
		while True:
			self.fill((20,20,20))
			self.stop(100)
			self.resize()
			self.display()
			self.switch_button()
			self.skip()
			self.Quit()
			self.refresh()
			self.current_theme = pygame.image.load(self.themes[self.index])
			if self.selected:
				name = self.themes[self.index]
				name = name[:name.index(".")]
				return [f"{name}.png",f"fired_{name}.png",f"boosted_{name}.png"]