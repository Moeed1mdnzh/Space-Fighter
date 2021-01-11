import pygame,time
import random as r


class Player:
	def __init__(self,theme):
		self.theme = theme
		self.player = pygame.image.load(self.theme[0])
		self.key = pygame.key.get_pressed()
		self.shoot_perm = False
		self.bulletX,self.bulletY = [],[]
		self.Xbuttons = {
						pygame.K_a:(5,-10),
						pygame.K_d:(355,10)
						}
		self.playerX,self.playerY = 200,300
		self.Ybuttons = (pygame.K_w,pygame.image.load(self.theme[1]),-20)
		self.health = 200
		self.boost = 150
		self.lives = {"lives" : 10}
		self.score = {"score" : 0}
		self.font = pygame.font.SysFont('MC Sans Comic',40,bold=True)
		self.text_Y = 120
		self.current_gun = None
		self.gunTypes = []
		self.bullet_width = 20
		self.laser_mode = False
		self.laser_perm = False
		self.case = "normal"
		self.cases = ["normal","laser","shot"]
		self.deathFonts = [pygame.font.SysFont('agencyfb',80,bold=True),
							pygame.font.SysFont('MC Sans Comic',25,bold=True),
							pygame.font.SysFont('MC Sans Comic',25,bold=True)]
		self.deathTexts = {
							"YOU DIED" : (220,60),
							"press R to return to menu" : (230,260),
							"press C to lose a live and continue" : (190,190)
							}
		self.deathExp = pygame.image.load("explosion.png")
		self.skeleton = pygame.image.load("skeleton.jpg")
		self.shoot_sound = pygame.mixer.Sound("Laser_gun1.mp3")
		self.shotGun_sound = pygame.mixer.Sound("Laser_gun2.mp3")
		self.laser_sound = pygame.mixer.Sound("Laser_gun3.mp3")
		self.launch_sound = pygame.mixer.Sound("spaceShip.mp3")
		self.boost_sound = pygame.mixer.Sound("speed_sound.mp3")
		self.switch_sound = pygame.mixer.Sound("select_sound.mp3")
		self.explosion_sound = pygame.mixer.Sound("Explosion.mp3")

	def display_details(self,win_obj):
		for detail in [self.score,self.lives]:
			for k,v in detail.items():
				rendered = self.font.render(f"{k} : {v}",True,(255,255,255))
				win_obj.blit(rendered,(5,self.text_Y))
			self.text_Y += 30
		self.text_Y = 120

	def Events(self):
		self.key = pygame.key.get_pressed()
		self.Xbuttons = {
						pygame.K_a:(5,-30),
						pygame.K_d:(355,30)
						}
		for index,(event,details) in enumerate(self.Xbuttons.items()):
			if self.key[event]:
				if self.key[pygame.K_s] and self.boost > 0:
					self.boost_sound.play()
					self.boost -= 10
					self.player = pygame.image.load(self.theme[2])
					self.playerY += self.Ybuttons[2]*2
				if index == 0:
					if self.playerX > -80:
						self.playerX += details[1]
				if index == 1:
					if self.playerX+300 < 780:
						self.playerX += details[1]
				return details[0]
			else:
				if index != 0:
					return 0

	def display_player(self,win_obj,degree):
		win_obj.blit(pygame.transform.rotate(self.player,degree),(self.playerX,self.playerY))

	def launch(self,current_player):
		self.key = pygame.key.get_pressed()
		self.Ybuttons = (pygame.K_w,pygame.image.load(self.theme[2]),-30)
		if self.key[self.Ybuttons[0]]:
			self.launch_sound.play()
			if self.key[pygame.K_s] and self.boost > 0:
				self.boost_sound.play()
				self.boost -= 10
				self.playerY += self.Ybuttons[2]*2
				return self.Ybuttons[1]
			else:
				self.playerY += self.Ybuttons[2]
				return pygame.image.load(self.theme[1])
		else:
			return current_player

	def Score(self):
		self.score["score"] += 1

	def laser(self):
		self.key = pygame.key.get_pressed()
		if self.key[pygame.K_SPACE]:
			self.laser_sound.play()
			self.laser_perm = True
			pygame.draw.line(self.win,(170,0,170),(self.playerX+132,self.playerY+90),(self.playerX+132,10),5)
		self.laser_mode = True


	def shotGun(self):
		if self.shoot_perm:
			if self.bulletX != [] or self.bulletY != []:
				for i,y in enumerate(self.bulletY):
					pygame.draw.line(self.win,(255,255,0),(self.bulletX[i],y),(self.bulletX[i],y-10),4)
					pygame.draw.line(self.win,(0,240,240),(self.bulletX[i]-self.bullet_width,y),(self.bulletX[i]-self.bullet_width-5,y-10),4)
					pygame.draw.line(self.win,(0,240,240),(self.bulletX[i]+self.bullet_width,y),(self.bulletX[i]+self.bullet_width+5,y-10),4)
					self.bulletY[i] -= 60
					if self.bulletY[i] <= 20:
						self.bulletY.remove(self.bulletY[i])
						self.bulletX.remove(self.bulletX[i])
			else: 
				self.shoot_perm = False

	def gunIcon(self,case):
		pygame.draw.rect(self.win,(0,0,0),[640,5,55,55])
		pygame.draw.rect(self.win,(50,168,149),[640,5,55,55],6)
		if case == "normal":
			pygame.draw.line(self.win,(255,255,0),(668,50),(668,40),3)
			pygame.draw.line(self.win,(255,255,0),(668,20),(668,30),3)
		elif case == "laser":
			pygame.draw.line(self.win,(170,0,170),(668,55),(668,10),5)
		elif case == "shot":
			pygame.draw.line(self.win,(255,255,0),(668,37),(668,27),3)
			pygame.draw.line(self.win,(0,240,240),(675,37),(680,27),3)
			pygame.draw.line(self.win,(0,240,240),(660,37),(655,27),3)

	def switch(self):
		if self.current_gun == None:
			self.current_gun = self.shoot
			self.gunTypes = [self.shoot,self.laser,self.shotGun]
		self.key = pygame.key.get_pressed()
		if self.key[pygame.K_e]:
			self.switch_sound.play()
			for i,gun in enumerate(self.gunTypes):
				if self.current_gun == gun:
					try:
						self.current_gun = self.gunTypes[i+1]
						self.case = self.cases[i+1]
						break
					except IndexError:
						self.current_gun = self.gunTypes[0]
						self.case = self.cases[0]
						break
		if self.current_gun != self.laser:
			self.laser_mode = False

	def shoot(self):
		if self.shoot_perm:
			if self.bulletX != [] or self.bulletY != []:
				for i,y in enumerate(self.bulletY):
					pygame.draw.line(self.win,(255,255,0),(self.bulletX[i],y),(self.bulletX[i],y-20),4)
					self.bulletY[i] -= 50
					if self.bulletY[i] <= 20:
						self.bulletY.remove(self.bulletY[i])
						self.bulletX.remove(self.bulletX[i])
			else: self.shoot_perm = False

	def HealthBar(self,win_obj):
		pygame.draw.rect(win_obj,(0,0,0),[5,10,200,50])
		pygame.draw.rect(win_obj,(255,0,0),[5,10,self.health,50])
		pygame.draw.rect(win_obj,(255,255,255),[5,10,200,50],4)

	def BoostBar(self,win_obj):
		pygame.draw.rect(win_obj,(0,0,0),[5,65,150,50])
		if self.boost > 0:
			pygame.draw.rect(win_obj,(0,255,255),[5,65,self.boost,50])
		pygame.draw.rect(win_obj,(255,255,255),[5,65,150,50],4)
		if self.boost < 150:
			self.boost += r.choices([10,0],weights=[5,100])[0]

	def live_loss(self,perm):
		if perm:
			self.lives["lives"] -= 1

	def deathScreen(self):
		self.win.blit(self.deathExp,(220,180))
		for i,(k,v) in enumerate(self.deathTexts.items()):	
			rendered = self.deathFonts[i].render(k,True,(240,240,240))
			self.win.blit(rendered,v)

	def deathEvents(self):
		self.key = pygame.key.get_pressed()
		if self.key[pygame.K_c]:
			self.health = 200
			self.lives["lives"] -= 1
		elif self.key[pygame.K_r]:
			self.health = 200
			self.dead = True

	def Death(self):
		if self.health <= 0:
			while True:
				self.fill(self.fill_color)
				self.delay(80)
				self.deathScreen()
				self.deathEvents()
				if self.health > 0:
					break
				self.Quit()
				self.update()

	def lossScreen(self):
		self.win.blit(self.skeleton,(170,150))
		rendered = self.deathFonts[0].render("YOU LOST",True,(255,255,255))
		self.win.blit(rendered,(210,50))
		score = self.score["score"]
		rendered = rendered = self.deathFonts[1].render(f"Your final score : {str(score)}",True,(255,255,255))
		self.win.blit(rendered,(250,150))
		rendered = self.deathFonts[1].render("returning to the menu...",True,(255,255,255))	
		self.win.blit(rendered,(230,190))

	def Loss(self,win_obj):
		if self.lives["lives"] <= 0:
			self.fill(self.fill_color)
			self.delay(80)
			self.lossScreen()
			self.Quit()
			self.update()
			time.sleep(5)
			self.dead = True

class Enemies:
	def __init__(self,speed,difficultyType):
		self.difficultyType = difficultyType
		self.normal_enemy = [pygame.image.load("enemy1.png") for _ in range(5)]
		self.shoot_enemy = [pygame.image.load("enemy2.png") for _ in range(2)]
		self.boost_enemy = [pygame.image.load("enemy3.png") for _ in range(2)]
		self.enemy_coordinates = [
								[[r.randint(50,500),r.randint(-2400,-600)] for _ in range(5)],
								[[r.choice([0,500]),r.randint(-14000,-7000)] for _ in range(2)],
								[[r.choice([250,450]),r.randint(-2400,-1800)] for _ in range(2)]
								]
		self.enemy_speed = speed
		self.enemies = [self.normal_enemy,self.boost_enemy,self.shoot_enemy]
		self.normal_health = [50 for _ in range(5)]
		self.shooter_health = [200 for _ in range(2)]
		self.boosted_health = [20 for _ in range(2)]
		self.particles = []
		self.shootX,self.shootY = [],[]

	def Shooter(self,win_obj):
		if self.shootX == []:
			for coordinates in self.enemy_coordinates[-1]:
				self.shootX.append(coordinates[0]+130)
				self.shootY.append(coordinates[1]+80)
		else:
			for i,x in enumerate(self.shootX):
				y = self.shootY[i]
				if y >= -20:
					self.shoot_sound.play()
				pygame.draw.line(win_obj,(255,0,0),(x,y),(x,y+20),4)
				if x in range(self.playerX+90,self.playerX+210) and y in range(self.playerY,self.playerY+300):
					self.health -= 5
				self.shootY[i] += 50
				if self.shootY[i] >= self.enemy_coordinates[-1][i][1]+350:
					self.shootY.remove(self.shootY[i])
					self.shootX.remove(self.shootX[i])

	def create_particles(self):
		for particles in self.particles:
			for particle in particles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.7
				particle[1][1] += 1.5
				pygame.draw.circle(self.win,r.choice([(255,0,0),(255,255,0),(252,148,3)]),[int(particle[0][0]),int(particle[0][1])],int(particle[2]))
				if particle[2] <= 0:
					particles.remove(particle)
		if self.particles != []:
			if self.particles[0] == []:
				self.particles.remove([])
 
	def display_enemies(self,win_obj,enemyType,coordinates):
		win_obj.blit(enemyType,coordinates)

	def shooter_boosted(self,win_obj):
		for i,enemy in enumerate(self.enemy_coordinates[1]):
			pygame.draw.rect(win_obj,(0,255,0),[enemy[0]+115,enemy[1],self.boosted_health[i],10])
			pygame.draw.rect(win_obj,(255,255,255),[enemy[0]+115,enemy[1],20,10],5)
			pygame.draw.rect(win_obj,(255,0,0),[self.enemy_coordinates[2][i][0]+25,self.enemy_coordinates[2][i][1],self.shooter_health[i],10])
			pygame.draw.rect(win_obj,(255,255,255),[self.enemy_coordinates[2][i][0]+25,self.enemy_coordinates[2][i][1],200,10],5)

	def normal(self,win_obj):
		for i,enemy in enumerate(self.enemy_coordinates[0]):
			pygame.draw.rect(win_obj,(255,255,0),[enemy[0]+100,enemy[1],self.normal_health[i],10])
			pygame.draw.rect(win_obj,(255,255,255),[enemy[0]+100,enemy[1],50,10],5)


	def move(self,win_obj):
		for i,coordinates in enumerate(self.enemy_coordinates):
			for j,coordinate in enumerate(coordinates):
				if i == 2: self.enemy_coordinates[i][j] = [coordinate[0]+r.randint(-5,5),coordinate[1]+self.enemy_speed[i]]
				else : self.enemy_coordinates[i][j] = [coordinate[0],coordinate[1]+self.enemy_speed[i]]
				self.display_enemies(win_obj,self.enemies[i][j],self.enemy_coordinates[i][j])
				if i == 0:
					self.Return("normal",i,j)
				if i == 1:
					self.Return("boosted",i,j)
				if i == 2:
					self.Return("shooter",i,j)
		self.laser_perm = False

	def kill(self,enemyType,i,j):
		"""Had to copy and paste the code for
			different bullet types"""
		if self.current_gun != self.laser:
			for index,bullet in enumerate(list(zip(self.bulletX,self.bulletY))):
				if ((bullet[0] in range(self.enemy_coordinates[i][j][0]+90,self.enemy_coordinates[i][j][0]+150)) and (
				bullet[1] in range(self.enemy_coordinates[i][j][1],self.enemy_coordinates[i][j][1]+270))):
					if enemyType == "normal":
						self.normal_health[j] -= 10
						self.bulletX.remove(self.bulletX[index-1])
						self.bulletY.remove(self.bulletY[index-1])
						if self.normal_health[j] < 10:
							self.Score()
							self.normal_health[j] = 50
							times = r.randint(15,30)
							particles = []
							for _ in range(times):
								particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-20,20),
									self.enemy_coordinates[i][j][1]+r.randint(-20,20)], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
							self.explosion_sound.play()
							self.particles.append(particles)
							self.enemy_coordinates[i][j] = [r.randint(50,500),r.randint(-2400,-600)]
					if enemyType ==  "boosted":
						self.Score()
						self.boosted_health[j] -= 10
						self.bulletX.remove(self.bulletX[index-1])
						self.bulletY.remove(self.bulletY[index-1])
						if self.boosted_health[j] < 10:
							self.boosted_health[j] = 20
							times = r.randint(5,10)
							particles = []
							for _ in range(times):
								particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-20,20),
									self.enemy_coordinates[i][j][1]+r.randint(-20,20)-70], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
							self.explosion_sound.play()
							self.particles.append(particles)
							self.enemy_coordinates[i][j] = [r.choice([0,500]),r.randint(-14000,-7000)]
					if enemyType == "shooter":
						self.Score()
						if self.difficultyType == "Hard": self.shooter_health[j] -= 5
						else: self.shooter_health[j] -= 10
						self.bulletX.remove(self.bulletX[index-1])
						self.bulletY.remove(self.bulletY[index-1])
						if self.shooter_health[j] < 20:
							self.shooter_health[j] = 200
							times = r.randint(25,50)
							particles = []
							for _ in range(times):
								particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-50,50),
									self.enemy_coordinates[i][j][1]+r.randint(-50,50)-70], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
							self.explosion_sound.play()
							self.enemy_coordinates[i][j] = [r.choice([250,450]),r.randint(-2400,-1800)]
							self.particles.append(particles)
				else:
					if self.current_gun == self.shotGun:
						if (bullet[0]-self.bullet_width in range(self.enemy_coordinates[i][j][0]+90,self.enemy_coordinates[i][j][0]+150) and (
							bullet[1] in range(self.enemy_coordinates[i][j][1],self.enemy_coordinates[i][j][1]+150))) or ((bullet[0]+self.bullet_width in range(
							self.enemy_coordinates[i][j][0]+90,self.enemy_coordinates[i][j][0]+150)) and (bullet[1] in range(
							self.enemy_coordinates[i][j][1],self.enemy_coordinates[i][j][1]+150))):
							if enemyType == "normal":
								self.normal_health[j] -= 10
								self.bulletX.remove(self.bulletX[index-1])
								self.bulletY.remove(self.bulletY[index-1])
								if self.normal_health[j] < 10:
									self.Score()
									self.normal_health[j] = 50
									times = r.randint(15,30)
									particles = []
									for _ in range(times):
										particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-20,20),
											self.enemy_coordinates[i][j][1]+r.randint(-20,20)], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
									self.explosion_sound.play()
									self.particles.append(particles)
									self.enemy_coordinates[i][j] = [r.randint(50,500),r.randint(-2400,-600)]
							if enemyType ==  "boosted":
								self.Score()
								self.boosted_health[j] -= 10
								self.bulletX.remove(self.bulletX[index-1])
								self.bulletY.remove(self.bulletY[index-1])
								if self.boosted_health[j] < 10:
									self.boosted_health[j] = 20
									times = r.randint(5,10)
									particles = []
									for _ in range(times):
										particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-20,20),
											self.enemy_coordinates[i][j][1]+r.randint(-20,20)-70], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
									self.explosion_sound.play()
									self.particles.append(particles)
									self.enemy_coordinates[i][j] = [r.choice([0,500]),r.randint(-14000,-7000)]
							if enemyType == "shooter":
								self.Score()
								if self.difficultyType == "Hard": self.shooter_health[j] -= 5
								else: self.shooter_health[j] -= 10
								self.bulletX.remove(self.bulletX[index-1])
								self.bulletY.remove(self.bulletY[index-1])
								if self.shooter_health[j] < 20:
									self.shooter_health[j] = 200
									times = r.randint(25,50)
									particles = []
									for _ in range(times):
										particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-50,50),
											self.enemy_coordinates[i][j][1]+r.randint(-50,50)-70], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
									self.explosion_sound.play()
									self.enemy_coordinates[i][j] = [r.choice([250,450]),r.randint(-2400,-1800)]
									self.particles.append(particles)
		else:
			if self.laser_perm:
				if self.playerX+132 in range(self.enemy_coordinates[i][j][0]+100,self.enemy_coordinates[i][j][0]+150) and (
					self.enemy_coordinates[i][j][1] in range(0,500)):
					if enemyType == "normal":
						self.normal_health[j] -= 5
						if self.normal_health[j] < 5:
							self.Score()
							self.normal_health[j] = 50
							times = r.randint(15,30)
							particles = []
							for _ in range(times):
								particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-20,20),
									self.enemy_coordinates[i][j][1]+r.randint(-20,20)], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
							self.explosion_sound.play()
							self.particles.append(particles)
							self.enemy_coordinates[i][j] = [r.randint(50,500),r.randint(-2400,-600)]
					if enemyType ==  "boosted":
						self.Score()
						self.boosted_health[j] -= 5
						if self.boosted_health[j] < 5:
							self.Score()
							self.boosted_health[j] = 20
							times = r.randint(5,10)
							particles = []
							for _ in range(times):
								particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-20,20),
									self.enemy_coordinates[i][j][1]+r.randint(-20,20)-70], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
							self.explosion_sound.play()
							self.particles.append(particles)
							self.enemy_coordinates[i][j] = [r.choice([0,500]),r.randint(-14000,-7000)]
					if enemyType == "shooter":
						if self.difficultyType == "Hard": self.shooter_health[j] -= 5
						else: self.shooter_health[j] -= 10
						if self.shooter_health[j] < 10:
							self.Score()
							self.shooter_health[j] = 200
							times = r.randint(25,50)
							particles = []
							for _ in range(times):
								particles.append([[self.enemy_coordinates[i][j][0]+120+r.randint(-50,50),
									self.enemy_coordinates[i][j][1]+r.randint(-50,50)-70], [r.randint(0, 20) / 10 - 1, -2], r.randint(4, 6)])
							self.explosion_sound.play()
							self.enemy_coordinates[i][j] = [r.choice([250,450]),r.randint(-2400,-1800)]
							self.particles.append(particles)
															

	def Return(self,enemyType,indexI,indexJ):
		if self.enemy_coordinates[indexI][indexJ][1] >= 600:
			self.live_loss(True)
			if enemyType == "normal":
				self.enemy_coordinates[indexI][indexJ] = [r.randint(50,500),r.randint(-2400,-600)]
				self.normal_health[indexJ] = 50
			if enemyType == "boosted":
				self.enemy_coordinates[indexI][indexJ] = [r.choice([0,500]),r.randint(-14000,-7000)]
				self.boosted_health[indexJ] = 20
				if self.difficultyType == "Hard":
					self.lives["lives"] -= 1 
			if enemyType == "shooter":
				self.shooter_health = 200
				self.enemy_coordinates[indexI][indexJ] = [r.choice([250,450]),r.randint(-2400,-1800)]
				if self.difficultyType == "Hard":
					self.lives["lives"] -= 1
		else: 
			self.kill(enemyType,indexI,indexJ)

class GameLoop(Player,Enemies):
	def __init__(self,speed,difficultyType,theme):
		super().__init__(theme)
		Enemies.__init__(self,speed,difficultyType)
		self.caption = pygame.display.set_caption("Space Fighter")
		self.W,self.H = 700,600
		self.win = pygame.display.set_mode((self.W,self.H))
		self.fill_color = (0,0,0)
		self.dead = False
		self.backGrounds = {
							pygame.image.load("starbg1.png"):[0,0],
							pygame.image.load("starbg2.png"):[0,200],
							pygame.image.load("starbg3.png"):[0,400]
							}

	def display_backGround(self):
		for background,coordinates in self.backGrounds.items():
			coordinates[1] += 50
			self.backGrounds[background] = coordinates
			self.win.blit(background,coordinates)
			if coordinates[1] == 600:
				self.backGrounds[background] = [0,-100]

	def fill(self,fill_color):
		self.win.fill(fill_color)

	def update(self):
		pygame.display.update()

	def Quit(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					self.shoot_perm = True
					self.bulletX.append(self.playerX+130)
					self.bulletY.append(self.playerY)
					if self.current_gun == self.shoot: self.shoot_sound.play()
					if self.current_gun == self.shotGun: self.shotGun_sound.play()

	def delay(self,delay_time):
		pygame.time.delay(delay_time)

	def main(self):
		while not self.dead:
			self.fill(self.fill_color)
			self.delay(43)
			self.display_backGround()
			degree = self.Events()
			if self.current_gun != None:
				self.current_gun()
			self.player = self.launch(self.player)
			if self.difficultyType != "Easy":
				self.Shooter(self.win)
			self.move(self.win)
			self.normal(self.win)
			self.shooter_boosted(self.win)
			self.switch()
			self.create_particles()
			self.display_player(self.win,degree)
			self.HealthBar(self.win)
			self.BoostBar(self.win)
			self.gunIcon(self.case)
			self.display_details(self.win)
			self.Quit()
			self.update()
			if self.playerY <= 390:   
				self.playerY += 10
			self.player = pygame.image.load(self.theme[0])
			self.Death()
			self.Loss(self.win)