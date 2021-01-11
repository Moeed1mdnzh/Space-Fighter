import pygame,time

pygame.init()

class Texts:
	def __init__(self,Captions):
		self.captions = Captions
		self.cap_coordinates = [(230,-10),(260,130),(260,300)]
		self.caption = pygame.display.set_caption("Space Fighter")
		self.win = pygame.display.set_mode((700,600))
		self.cap_font = pygame.font.SysFont('agencyfb',40,'light')
		self.texts = [open("Guide1.txt","r"),open("Guide2.txt","r"),open("Guide3.txt","r")]
		self.text_font = pygame.font.SysFont('arial',13,'light')
		self.R_font = pygame.font.SysFont('arial',20,'light')
		self.text_y = 35
		self.bottom = 260
		self.enemyX = [450,450,450]
		self.enemies = [
		pygame.image.load("enemy1.png"),
		pygame.image.load("enemy2.png"),
		pygame.image.load("enemy3.png")
		]
		self.return_text = "press R to return"
		self.key = None
		self.R_key = None
		self.returning = False
		self.wasd_buttons = pygame.transform.scale(pygame.image.load("wasd.png"),(140,90))
		self.return_sound = pygame.mixer.Sound("select_sound.mp3")

	def Quit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

	def display_exp(self):
		self.win.blit(self.wasd_buttons,(400,200))
		rendered = self.R_font.render(self.return_text,True,(255,255,0))
		self.win.blit(rendered,(30,10))
		self.key = pygame.key.get_pressed()
		self.R_key = pygame.K_r
		if self.key[self.R_key]:
			self.returning = True
			self.return_sound.play()
			time.sleep(1)
		self.text_y = 35
		self.bottom = 260
		self.texts = [open("Guide1.txt","r"),open("Guide2.txt","r"),open("Guide3.txt","r")]
		for texts in self.texts:
			for text in texts.readlines():
				rendered = self.text_font.render(text[:len(text)-1],True,(255,255,255))
				self.win.blit(rendered,(0,self.text_y))
				self.text_y += 20
			self.text_y += 70
			if self.text_y == 665:
				for i,enemy in enumerate(self.enemies):
					self.win.blit(enemy,(self.enemyX[i],self.bottom))
					self.bottom += 100

	def display_captions(self):
		for i,caption in enumerate(self.captions):
			rendered = self.cap_font.render(caption,True,(230,230,230))
			self.win.blit(rendered,self.cap_coordinates[i])			
				
	def refresh(self):
		pygame.display.update()
		
	def delay(self):
		pygame.time.delay(50)

	def fill(self):
		self.win.fill((0,0,0))					

	def main(self):
		while True:
			self.fill()
			self.delay()
			self.display_captions()
			self.display_exp()
			if self.returning:
				return "Return"
			self.Quit()
			self.refresh()