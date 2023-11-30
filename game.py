import simpleGE,random,pygame,time
"""
An arcade style fighting game.

Background: https://www.vecteezy.com/photo/26844400-2d-hero-battle-pvp-arena-background-casual-game-art-design-ai-generative
Health Bar: https://opengameart.org/content/long-red-health-bar
Sword Swinging Sounds: https://opengameart.org/content/rpg-sound-pack
Characters Generated through: https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator/#?body=Body_color_light&head=Human_male_light
Loading Screen sound: By Grand_Project from Pixbay
Victory Sound: https://opengameart.org/content/cant-stop-winning-rpg-orchestral-essentials-battle-victory-music
Fight sound: https://opengameart.org/content/boss-battle-3-8-bit-re-upload
Voicer over Audios: https://www.kenney.nl/assets/voiceover-pack-fighter
Logo Image: https://www.freepik.com/free-vector/spartan-helmet-logo-design_41600786.htm#query=spartan%20head&position=12&from_view=keyword&track=ais&uuid=1b12b60d-5eea-4ff6-b011-2d215fc65643
Kapow Image: https://pixabay.com/illustrations/kapow-comic-comic-book-fight-1601675/
Hit Sound effect Created by: https://pixabay.com/users/universfield-28281460/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=140236
Selection Sound Effect : Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=37979">Pixabay</a>
Player 1 and 2 Wins: Image created by me
Character Headshots: Image created by me
Minotaur Authors: Authors: bluecarrot16, Benjamin K. Smith (BenCreating), Evert, Eliza Wyatt (ElizaWy), TheraHedwig, MuffinElZangano, Durrani, Johannes Sj?lund (wulax), Stephen Challener (Redshrike), Nila122, Daniel Eddeland (daneeklu), David Conway Jr. (JaidynReiman), Johannes Sjölund (wulax), Matthew Krohn (makrohn), Joe White, Pierre Vigier and DCSS artists (see https://github.com/crawl/tiles/blob/master/ARTISTS.md)
Knight Authors: Authors: bluecarrot16, Benjamin K. Smith (BenCreating), Evert, Eliza Wyatt (ElizaWy), TheraHedwig, MuffinElZangano, Durrani, Johannes Sj?lund (wulax), Stephen Challener (Redshrike), Manuel Riecke (MrBeast), Michael Whitlock (bigbeargames), Matthew Krohn (makrohn), Johannes Sjölund (wulax), Nila122

Nolan Meyer

November 13, 2023
"""

#Classes that holds all the attributes in game such as characters, and all graphical elements
class Game(simpleGE.Scene):

    def __init__(self,player1,player2):
        super().__init__()

        #setup background
        self.setCaption("Warriors Arena")
        self.background = pygame.image.load("UI/background.jpeg")
        self.background = self.background.convert_alpha()
        self.background = pygame.transform.scale(self.background, ((self.screen.get_size())))

        #Player1 Character Selection
        if player1 == "knight":
            
            self.player1 = Knight(self,1)

            self.player1HB = [Hitbox(self,self.player1,"head"),Hitbox(self,self.player1,"mace")]
            self.p1HitboxGroup = self.makeSpriteGroup(self.player1HB)

        elif player1 == "minotaur":

            self.player1 = Minotaur(self,1)

            self.player1HB = [Hitbox(self,self.player1,"head"),Hitbox(self,self.player1,"katana")]
            self.p1HitboxGroup = self.makeSpriteGroup(self.player1HB)

        #Player2 Character selection
        if player2 == "knight":

            self.player2 = Knight(self,2)

            self.player2HB = [Hitbox(self,self.player2,"head"),Hitbox(self,self.player2,"mace")]
            self.p2HitboxGroup = self.makeSpriteGroup(self.player2HB)

        elif player2 == "minotaur":
        
            self.player2 = Minotaur(self,2)

            self.player2HB = [Hitbox(self,self.player2,"head"),Hitbox(self,self.player2,"katana")]
            self.p2HitboxGroup = self.makeSpriteGroup(self.player2HB)


        #Player 1 Health bar
        self.player1HealthBar = HealthBar(self,self.player1,0,0,(7, 245, 19))
        self.player1HealthBarU = HealthBar(self,self.player1,0,0,(250,245,245))
        self.player1HealthBarO = HealthBar(self,self.player1,10,10,(119, 128, 124))

        #Player 1 Text
        self.player1Text = simpleGE.Label()
        self.player1Text.text = "PLAYER 1"
        self.player1Text.center = (125,60)
        self.player1Text.bgColor = (0,0,0)
        self.player1Text.fgColor = ("red")

        #Player 2 Text
        self.player2Text = simpleGE.Label()
        self.player2Text.text = "PLAYER 2"
        self.player2Text.center = (518,60)
        self.player2Text.bgColor = (0,0,0)
        self.player2Text.fgColor = ("red")

        #Player 2 Health bar
        self.player2HealthBar = HealthBar(self,self.player2,0,0,(7, 245, 19))
        self.player2HealthBarU = HealthBar(self,self.player2,0,0,(250,245,245))
        self.player2HealthBarO = HealthBar(self,self.player2,10,10,(119, 128, 124))

        #Player 1 Wins Image
        self.player1Wins = simpleGE.SuperSprite(self)
        self.player1Wins.setImage("UI/player1Wins.png")
        self.player1Wins.setSize(300,300)
        self.player1Wins.setPosition((315,200))
        self.player1Wins.hide()
        self.player1Sound = simpleGE.Sound("UI/player_1.wav")

        #Player 2 Wins Image
        self.player2Wins = simpleGE.SuperSprite(self)
        self.player2Wins.setImage("UI/player2Wins.png")
        self.player2Wins.setSize(300,300)
        self.player2Wins.setPosition((315,200))
        self.player2Wins.hide()
        self.player2Sound = simpleGE.Sound("UI/player_2.wav")
        
        #Voice over sounds
        self.youWinSound = simpleGE.Sound("UI/you_win.wav")
        self.comboSound = simpleGE.Sound("UI/combo.wav")
        
        #Keeps track of fighting attributes
        self.playTimes = 0
        self.P1collisionTimes = 0
        self.P1hitTimes = 0
        self.P2collisionTimes = 0 
        self.P2hitTimes = 0
        self.comboTimes = 0
        self.gameStatus = True
        self.P1comboTimes = random.randint(5,20)
        self.P2comboTimes = random.randint(5,20)

        #Play again with same character SC-Same characters
        self.playAgainSCButton = simpleGE.Button()
        self.playAgainSCButton.fgColor = (0,0,0)
        self.playAgainSCButton.bgColor = (225,225,0)
        self.playAgainSCButton.text = "Restart With Same Characters"
        self.playAgainSCButton.size = (300,30)
        self.playAgainSCButton.hide()

        #Quit button
        self.quitButton = simpleGE.Button()
        self.quitButton.fgColor = (0,0,0)
        self.quitButton.bgColor = (225,225,0)
        self.quitButton.text = "Quit"
        self.quitButton.hide()

        #Kapow Image
        self.kapow = simpleGE.SuperSprite(self)
        self.kapow.imageMaster = pygame.image.load("UI/kapow.png")
        self.kapow.setSize(150,150)
        self.kapow.hide()

        #Countdown sequence
        self.three_sound = simpleGE.Sound("UI/3.wav")
        self.two_sound = simpleGE.Sound("UI/2.wav")
        self.one_sound = simpleGE.Sound("UI/1.wav")
        self.begin_sound = simpleGE.Sound("UI/begin.wav")
        
        self.three_image = simpleGE.SuperSprite(self)
        self.three_image.imageMaster = pygame.image.load("UI/3.png")
        self.three_image.setSize(100,100)
        self.three_image.setPosition((320,30))
        self.three_image.hide()

        self.two_image = simpleGE.SuperSprite(self)
        self.two_image.imageMaster = pygame.image.load("UI/2.png")
        self.two_image.setSize(100,100)
        self.two_image.setPosition((320,30))
        self.two_image.hide()

        self.one_image = simpleGE.SuperSprite(self)
        self.one_image.imageMaster = pygame.image.load("UI/1.png")
        self.one_image.setSize(100,100)
        self.one_image.setPosition((320,30))
        self.one_image.hide()

        self.begin_image = simpleGE.SuperSprite(self)
        self.begin_image.imageMaster = pygame.image.load("UI/begin.png")
        self.begin_image.setSize(100,100)
        self.begin_image.setPosition((320,30))
        self.begin_image.hide()

        #Background music for fight sequence
        pygame.mixer.music.load("UI/fightSong.ogg")
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play(-1)
        
        self.runTimes = 0

        #Puts everything on the screen
        self.sprites = [self.player1HealthBarO,self.player1HealthBarU,self.player1HealthBar,
                        self.player1Text,self.player2HealthBarO,self.player2HealthBarU,
                        self.player2HealthBar,self.player2Text,self.player1,self.p1HitboxGroup,
                        self.player2,self.p2HitboxGroup,self.player1Wins,self.playAgainSCButton,
                        self.quitButton,self.player2Wins,self.kapow,self.three_image,self.two_image,
                        self.one_image,self.begin_image]
        

    #Update method controls the game
    def update(self):

        self.checkCollision()
        self.countdown()

        if self.playAgainSCButton.clicked:

            self.reset()
        
        if self.quitButton.clicked:

            self.stop()

    
    #Method to check for collisions. This is the combat system
    def checkCollision(self):

        if self.player1HB[1].collidesWith(self.player2HB[0]):

            if self.player1.hitMotion == True:

                self.P1collisionTimes += 1
                
                if self.P1collisionTimes == 1:
                    if self.player2.block == False:

                        self.P1hitTimes += 1
                        self.player1.hitSound.play()
                        self.player2.health -= self.player1.maxDamage
                        self.player2.ratio = self.player2.health / 100
                        self.player2HealthBar.updateLabel(self.player2)

                        if self.P1hitTimes == self.P1comboTimes:

                            self.player2.canMove = True
                            self.P2hitTimes = 0 
                            self.P1comboTimes = random.randint(5,20)
                            self.kapow.show()
                            self.kapow.x = self.player1.x
                            self.kapow.y = (self.player1.y) - 200
                            self.comboSound.play()
                            self.player2.kickBack()
                    
                    else:
                        self.player1.blockSound.play()
                
        if self.player2HB[1].collidesWith(self.player1HB[0]):

            if self.player2.hitMotion == True:

                self.P2collisionTimes += 1

                if self.P2collisionTimes == 1:
                    if self.player1.block == False:

                        self.P2hitTimes +=1 
                        self.player2.hitSound.play()
                        self.player1.health -= self.player2.maxDamage
                        self.player1.ratio = self.player1.health / 100
                        self.player1HealthBar.updateLabel(self.player1)
                    
                        if self.P2hitTimes == self.P2comboTimes:
                
                                self.player1.canMove = True
                                self.P2hitTimes = 0 
                                self.P2comboTimes = random.randint(5,20)
                                self.kapow.x = self.player2.x
                                self.kapow.y = (self.player1.y) - 200
                                self.comboSound.play()
                                self.player1.kickBack()
                        
                    else:
                        self.player2.blockSound.play()
                
                
        if self.player1.health <= 0:
            self.playTimes += 1
            self.player1.canMove = False
            self.player2.canMove = False

            if self.playTimes == 1:
                self.player2Wins.show()
                self.player2Wins.x = 315
                self.player2Wins.y = 200
                self.playAgainSCButton.show((300,375))
                self.quitButton.show((300,420))
                time.sleep(1)
                self.player2Sound.play()
                time.sleep(1)
                self.youWinSound.play()


        if self.player2.health <= 0:

            self.playTimes += 1
            self.player1.canMove = False
            self.player2.canMove = False

            if self.playTimes == 1:
                self.player1Wins.show()
                self.player1Wins.x = 315
                self.player1Wins.y = 200
                self.playAgainSCButton.show((300,375))
                self.quitButton.show((300,420))
                time.sleep(1)
                self.player1Sound.play()
                time.sleep(1)
                self.youWinSound.play()
        
    #Resets everything
    def reset(self):

        self.player1.health = 100
        self.player2.health = 100
        self.player1.setPosition((50,400))
        self.player2.setPosition((590,400))
        self.player1.lastKey = "d"
        self.player2.lastKey = "j"
        self.playAgainSCButton.hide()
        self.player1Wins.hide()
        self.player2Wins.hide()
        self.kapow.hide()
        self.playTimes = 0
        self.player1HealthBar.reset(self.player1)
        self.player2HealthBar.reset(self.player2)
        self.quitButton.hide()
        self.runTimes = 0
        self.P1hitTimes = 0
        self.P2hitTimes = 0
        self.player1.imageMaster = self.player1.rightImages["right1"]
        self.player2.imageMaster = self.player2.leftImages["left1"]
    
    #Countdown sequence
    def countdown(self):

        self.runTimes += 1

        if self.runTimes == 2:
        
            self.three_image.show()
            self.three_sound.play()
        
        if self.runTimes == 3:
            time.sleep(1)
            self.three_image.hide()
            self.two_image.show()
            self.two_sound.play()
        
        if self.runTimes == 4:
            time.sleep(1)
            self.two_image.hide()
            self.one_image.show()
            self.one_sound.play()
        
        if self.runTimes == 5:
            time.sleep(1)
            self.one_image.hide()
            self.begin_image.show()
            self.begin_sound.play()
        
        if self.runTimes  == 6:
            time.sleep(1)
            self.begin_image.hide()
            self.player1.canMove = True
            self.player2.canMove = True
    
        

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Health Bar Classes. Health bar is the class that will have a check events to change the health. All the others are just layers. 
class HealthBar(simpleGE.SuperSprite):

    def __init__(self,scene,player,offsetx,offsety,color):
        super().__init__(scene)
        self.imageMaster = pygame.Surface(((200*player.ratio+(offsetx)),(offsety + 30)))
        self.imageMaster.fill(pygame.Color(color))
        self.P1interval = 125
        self.P2interval = 518
        self.color = color

        if player.playerID == 1:
            self.setPosition((125,25))
        
        else:
            self.setPosition((518,25))

    #Work on update of the healthbars. Below is the idea update.
    def updateLabel(self,player):

        try:
            self.imageMaster = pygame.Surface((200*player.ratio,30))
            self.imageMaster.fill(pygame.Color(((7, 245, 19))))

            if player.playerID == 1:
                self.P1interval -= self.scene.player2.maxDamage
                self.setPosition((self.P1interval,25))

            if player.playerID == 2:
                self.P2interval += self.scene.player1.maxDamage
                self.setPosition((self.P2interval,25))

        except pygame.error:
            self.imageMaster = pygame.Surface((0,30))
            self.imageMaster.fill(pygame.Color(((7, 245, 19))))
            
    
    #Resets Label
    def reset(self,player):
        player.ratio = player.health / 100

        self.imageMaster = pygame.Surface((200*player.ratio,30))
        self.imageMaster.fill(pygame.Color((7, 245, 19)))

        if player.playerID == 1:

            self.setPosition((125,25))
            self.P1interval = 125
        
        elif player.playerID == 2:
            self.setPosition((518,25))
            self.P2interval = 518
            
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Creates hitboxes that will be attatched to the character's and move with the characters
class Hitbox(simpleGE.SuperSprite):

    def __init__(self,scene,character,type):
        super().__init__(scene)
        self.character = character
        self.type = type

        if type == "head":
    
            self.imageMaster = pygame.Surface((50,50),pygame.SRCALPHA)
            self.imageMaster.fill("red")
            self.setPosition((character.x,(character.y)-35))
                
        if type == "mace":
            if character.playerID == 1:

                self.imageMaster = pygame.Surface((30,50),pygame.SRCALPHA)
                self.imageMaster.fill("red")
                self.setPosition(((character.x)+40, (character.y)+40))
                self.rotateBy(70)
            
            if character.playerID == 2:

                self.imageMaster = pygame.Surface((30,50),pygame.SRCALPHA)
                self.imageMaster.fill("red")
                self.setPosition(((character.x)-40, (character.y)+40))
                self.rotateBy(70)
            
        if type == "katana":
            if character.playerID == 1:
                self.imageMaster = pygame.Surface((30,80),pygame.SRCALPHA)
                self.imageMaster.fill("red")
                self.setPosition(((character.x)+40, (character.y)+40))
                self.rotateBy(70)
            
            if character.playerID == 2:
                self.imageMaster = pygame.Surface((30,80),pygame.SRCALPHA)
                self.imageMaster.fill("red")
                self.setPosition(((character.x)-40, (character.y)+40))
                self.rotateBy(70)

    
    def checkEvents(self):

        if self.type == "head":

            self.x = self.character.x

            if self.character.jumpMotion == True:

                self.y = (self.character.y)-35
        
        if self.type in ("mace", "katana"):

            if self.character.hitMotion == False:

                if self.character.lastKey == "d":
                    self.x = (self.character.x)+40
                    self.y = (self.character.y)+40
                
                if self.character.lastKey == "a":
                    self.x = (self.character.x)-40
                    self.y = (self.character.y)+40
                
                if self.character.lastKey == "j":
                    self.x = (self.character.x)-40
                    self.y = (self.character.y)+40
                
                if self.character.lastKey == "l":
                    self.x = (self.character.x)+40
                    self.y = (self.character.y)+40

            if self.character.hitMotion == True:

                self.y -= 10
                self.hitTimes = 1

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Knight character class
class Knight(simpleGE.SuperSprite):

    def __init__(self,scene,playerID):
        super().__init__(scene)
        self.playerID = playerID
        self.canMove = False
        self.imageNum = 2
        self.lastKey = ""
        self.index = 0
        self.sound = simpleGE.Sound("Knight/swing2.wav")
        self.blockSound = simpleGE.Sound("Knight/sword-unsheathe2.wav")
        self.hitSound = simpleGE.Sound("Minotaur/hitSound.wav")
        self.hitMotion = False
        self.jumpMotion = False
        self.block = False
        self.kickBackMotion = False
        self.maxDamage = 5
        self.armor = 3
        self.health = 100
        self.ratio = self.health / 100

        self.rightImages = {

            "right1": pygame.image.load("Knight/knight_rightWalk1.png"),
            "right2": pygame.image.load("Knight/knight_rightWalk2.png"),
            "right3": pygame.image.load("Knight/knight_rightWalk3.png"),
            "right4":pygame.image.load("Knight/knight_rightWalk4.png"),
            "right5":pygame.image.load("Knight/knight_rightWalk5.png"),
            "right6": pygame.image.load("Knight/knight_rightWalk6.png"),
            "right7":pygame.image.load("Knight/knight_rightWalk7.png"),
            "right8": pygame.image.load("Knight/knight_rightWalk8.png"),
            "right9": pygame.image.load("Knight/knight_rightWalk9.png"),
            "rightSwing1": pygame.image.load("Knight/knight_rightSwing1.png"),
            "rightSwing2": pygame.image.load("Knight/knight_rightSwing2.png"),
            "rightSwing3": pygame.image.load("Knight/knight_rightSwing3.png"),
            "rightSwing4": pygame.image.load("Knight/knight_rightSwing4.png"),
            "rightSwing5": pygame.image.load("Knight/knight_rightSwing5.png"),
            "rightSwing6": pygame.image.load("Knight/knight_rightSwing6.png"),
            "rightBlock": pygame.image.load("Knight/knight_rightBlock.png"),
        
        }

        self.leftImages = {
            
            "left1": pygame.image.load("Knight/knight_leftWalk1.png"),
            "left2": pygame.image.load("Knight/knight_leftWalk2.png"),
            "left3": pygame.image.load("Knight/knight_leftWalk3.png"),
            "left4": pygame.image.load("Knight/knight_leftWalk4.png"),
            "left5": pygame.image.load("Knight/knight_leftWalk5.png"),
            "left6": pygame.image.load("Knight/knight_leftWalk6.png"),
            "left7": pygame.image.load("Knight/knight_leftWalk7.png"),
            "left8": pygame.image.load("Knight/knight_leftWalk8.png"),
            "left9": pygame.image.load("Knight/knight_leftWalk9.png"),
            "leftSwing1": pygame.image.load("Knight/knight_leftSwing1.png"),
            "leftSwing2": pygame.image.load("Knight/knight_leftSwing2.png"),
            "leftSwing3":pygame.image.load("Knight/knight_leftSwing3.png"),
            "leftSwing4": pygame.image.load("Knight/knight_leftSwing4.png"),
            "leftSwing5":pygame.image.load("Knight/knight_leftSwing5.png"),
            "leftSwing6":pygame.image.load("Knight/knight_leftSwing6.png"),
            "leftBlock": pygame.image.load("Knight/knight_leftBlock.png"),
        }

        for name,image in self.rightImages.items():

            self.rightImages[name] = pygame.transform.scale(image,(175,175))
        
        for name,image in self.leftImages.items():

            self.leftImages[name] = pygame.transform.scale(image,(175,175))


        if self.playerID == 1:
            self.imageMaster = self.rightImages["right1"]
            self.lastKey = "d"
            self.x = 50
            self.y = 400
        
        elif self.playerID == 2:
            self.imageMaster = self.leftImages["left1"]
            self.lastKey = "j"
            self.x = 590
            self.y = 400
        

    def checkEvents(self):

        if self.canMove == True:

            if self.playerID == 1:
                self.block = False
                if self.lastKey == "d":
                    self.imageMaster = self.rightImages["right1"]
                
                elif self.lastKey == "a":
                    self.imageMaster = self.leftImages["left1"]
                
                else:
                    self.imageMaster = self.rightImages["right1"]
                
                
                if self.scene.isKeyPressed(pygame.K_d):
                    
                    self.x += 5
                    self.imageMaster = self.rightImages[f"right{self.imageNum}"]
                    self.imageNum += 1
                    self.lastKey = "d"
            
                    if self.imageNum == 9:
                        self.imageNum = 2
                
                if self.scene.isKeyPressed(pygame.K_a):
                    
                    self.x -= 5
                    self.imageMaster = self.leftImages[f"left{self.imageNum}"]
                    self.imageNum += 1
                    self.lastKey = "a"

                    if self.imageNum == 9:
                        self.imageNum = 2
                
                if self.scene.isKeyPressed(pygame.K_w):
                    
                    if self.hitMotion == False:
                        self.hitMotion = True
                        self.sound.play()
                
                if self.scene.isKeyPressed(pygame.K_s):
                    
                    if self.jumpMotion == False:
                        self.jumpMotion = True
                        self.addForce(4,90)
                        self.y += 10
                
                if self.scene.isKeyPressed(pygame.K_q):
                    
                    if not(self.scene.isKeyPressed(pygame.K_d) or (self.scene.isKeyPressed(pygame.K_a))):
                        self.block = True

                        if self.lastKey == "d":
                            self.imageMaster = self.rightImages["rightBlock"]
                
                        if self.lastKey == "a":
                            self.imageMaster = self.leftImages["leftBlock"]
                
    
            #Controlls if it is player 2:
            if self.playerID == 2:
                self.block = False
                if self.lastKey == "l":
                    self.imageMaster = self.rightImages["right1"]
                
                elif self.lastKey == "j":
                    self.imageMaster = self.leftImages["left1"]
                
                else:
                    self.imageMaster = self.leftImages["left1"]
                
                if self.scene.isKeyPressed(pygame.K_l):
                    
                    self.x += 5
                    self.imageMaster = self.rightImages[f"right{self.imageNum}"]
                    self.imageNum += 1
                    self.lastKey = "l"
            
                    if self.imageNum == 9:
                        self.imageNum = 1
                
                if self.scene.isKeyPressed(pygame.K_j):
                    
                    self.x -= 5
                    self.imageMaster = self.leftImages[f"left{self.imageNum}"]
                    self.imageNum += 1
                    self.lastKey = "j"

                    if self.imageNum == 9:
                        self.imageNum = 1
                
                if self.scene.isKeyPressed(pygame.K_i):
                    
                    if self.hitMotion == False:
                        self.hitMotion = True
                        self.sound.play()
                
                if self.scene.isKeyPressed(pygame.K_k):
                
                    if self.jumpMotion == False:
                        self.jumpMotion = True
                        self.addForce(4,90)
                        self.y += 10
                
                if self.scene.isKeyPressed(pygame.K_o):
                    
                    if not(self.scene.isKeyPressed(pygame.K_j) or (self.scene.isKeyPressed(pygame.K_l))):
                        self.block = True
                        
                        if self.lastKey == "l":
                            self.imageMaster = self.rightImages["rightBlock"]
                    
                        if self.lastKey == "j":
                            self.imageMaster = self.leftImages["leftBlock"] 
                
        #Checks states of character

        #Hit state
        if self.hitMotion == True:
            self.hit()
            
        #Jump State
        if self.jumpMotion == True:
            self.jump()
        
        #Check's kicknotion state
        if self.kickBackMotion == True:
            
            if self.y < 350:
                self.setDY(0)
                self.addForce(3,270)
            
            if self.y > 400:
                self.y = 400
                self.kickBackMotion = False
                self.canMove = True
                self.setDY(0)
                self.setDX(0)
                self.scene.kapow.hide()
                
                if self.lastKey == "d":
                    self.rotateBy(-90)
            
                if self.lastKey == "a":
                    self.rotateBy(-270)
            
                if self.lastKey == "j":
                    self.rotateBy(-270)
            
                if self.lastKey == "l":
                    self.rotateBy(-90)
    
    #Hit method
    def hit(self):

        self.canMove = False
        self.index += 1
            
        if self.lastKey == "d":
            self.imageMaster = self.rightImages[f"rightSwing{self.index}"]
            time.sleep(0.01)
            
        elif self.lastKey == "a":
            self.imageMaster = self.leftImages[f"leftSwing{self.index}"]
            time.sleep(0.01)
            
        elif self.lastKey == "j":
            self.imageMaster = self.leftImages[f"leftSwing{self.index}"]
            time.sleep(0.01)
            
        elif self.lastKey == "l":
            self.imageMaster = self.rightImages[f"rightSwing{self.index}"]
            time.sleep(0.01)
    
        if self.index == 6:
            self.canMove = True
            self.hitMotion = False
            self.index = 0
            self.scene.P1collisionTimes = 0
            self.scene.P2collisionTimes = 0
            time.sleep(0.1)
    
    #Jump Method
    def jump(self):

        self.canMove = False

        if self.lastKey == "d":
            self.imageMaster = self.rightImages["right2"]
            
        if self.lastKey == "a":
            self.imageMaster = self.leftImages["left2"]
            
        if self.lastKey == "j":
            self.imageMaster = self.leftImages["left2"]
            
        if self.lastKey == "l":
            self.imageMaster = self.rightImages["right2"]

        self.addForce(0.2,270)
            
        if self.y > 410:
            self.setDY(0)
            self.canMove = True
            self.jumpMotion = False
            self.y = 400
            
        if self.playerID == 1:

            if self.scene.isKeyPressed(pygame.K_d):
                self.x += 5
                
            if self.scene.isKeyPressed(pygame.K_a):
                self.x -= 5
                
        if self.playerID == 2:

            if self.scene.isKeyPressed(pygame.K_j):
                self.x -= 5
                
            if self.scene.isKeyPressed(pygame.K_l):
                self.x += 5
        
    #This will make the player fly back after getting combo
    def kickBack(self):

        self.canMove = False
        self.kickBackMotion = True

        if self.lastKey == "d":
            self.imageMaster = self.rightImages["right1"]
            self.rotateBy(90)
            self.addForce(5,135)
            
        if self.lastKey == "a":
            self.imageMaster = self.leftImages["left1"]
            self.rotateBy(270)
            self.addForce(5,45)
            
        if self.lastKey == "j":
            self.imageMaster = self.leftImages["left1"]
            self.rotateBy(270)
            self.addForce(5,45)
            
        if self.lastKey == "l":
            self.imageMaster = self.rightImages["right1"]
            self.rotateBy(90)
            self.addForce(5,135)

    #Checks the bounds of the character
    def checkBounds(self):

        if self.x > 640:
            self.x = 590

        if self.x < 0:
            self.x = 50

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Minotaur Class. Inherits from the knight class. Changes Images and has two more health than the knight class.
class Minotaur(Knight):

    def __init__(self,scene,playerID):
        super().__init__(scene,Knight)
        self.playerID = playerID
        self.canMove = False
        self.imageNum = 2
        self.lastKey = ""
        self.index = 0
        self.sound = simpleGE.Sound("Knight/swing2.wav")
        self.blockSound = simpleGE.Sound("Knight/sword-unsheathe2.wav")
        self.hitSound = simpleGE.Sound("Minotaur/hitSound.wav")
        self.hitMotion = False
        self.jumpMotion = False
        self.block = False
        self.kickBackMotion = False
        self.maxDamage = 6
        self.armor = 3
        self.health = 100
        self.ratio = self.health / 100

        self.rightImages = {
            "right1": pygame.image.load("Minotaur/minotaur_rightWalk1.png"),
            "right2": pygame.image.load("Minotaur/minotaur_rightWalk2.png"),
            "right3": pygame.image.load("Minotaur/minotaur_rightWalk3.png"),
            "right4":pygame.image.load("Minotaur/minotaur_rightWalk4.png"),
            "right5":pygame.image.load("Minotaur/minotaur_rightWalk5.png"),
            "right6": pygame.image.load("Minotaur/minotaur_rightWalk6.png"),
            "right7":pygame.image.load("Minotaur/minotaur_rightWalk7.png"),
            "right8": pygame.image.load("Minotaur/minotaur_rightWalk8.png"),
            "right9": pygame.image.load("Minotaur/minotaur_rightWalk9.png"),
            "rightSwing1": pygame.image.load("Minotaur/minotaur_rightSwing1.png"),
            "rightSwing2": pygame.image.load("Minotaur/minotaur_rightSwing2.png"),
            "rightSwing3": pygame.image.load("Minotaur/minotaur_rightSwing3.png"),
            "rightSwing4": pygame.image.load("Minotaur/minotaur_rightSwing4.png"),
            "rightSwing5": pygame.image.load("Minotaur/minotaur_rightSwing5.png"),
            "rightSwing6": pygame.image.load("Minotaur/minotaur_rightSwing6.png"),
            "rightBlock": pygame.image.load("Minotaur/minotaur_blockRight.png"),
        }

        self.leftImages = {
            "left1": pygame.image.load("Minotaur/minotaur_leftWalk1.png"),
            "left2": pygame.image.load("Minotaur/minotaur_leftWalk2.png"),
            "left3": pygame.image.load("Minotaur/minotaur_leftWalk3.png"),
            "left4": pygame.image.load("Minotaur/minotaur_leftWalk4.png"),
            "left5": pygame.image.load("Minotaur/minotaur_leftWalk5.png"),
            "left6": pygame.image.load("Minotaur/minotaur_leftWalk6.png"),
            "left7": pygame.image.load("Minotaur/minotaur_leftWalk7.png"),
            "left8": pygame.image.load("Minotaur/minotaur_leftWalk8.png"),
            "left9": pygame.image.load("Minotaur/minotaur_leftWalk9.png"),
            "leftSwing1": pygame.image.load("Minotaur/minotaur_leftSwing1.png"),
            "leftSwing2": pygame.image.load("Minotaur/minotaur_leftSwing2.png"),
            "leftSwing3":pygame.image.load("Minotaur/minotaur_leftSwing3.png"),
            "leftSwing4": pygame.image.load("Minotaur/minotaur_leftSwing4.png"),
            "leftSwing5":pygame.image.load("Minotaur/minotaur_leftSwing5.png"),
            "leftSwing6":pygame.image.load("Minotaur/minotaur_leftSwing6.png"),
            "leftBlock": pygame.image.load("Minotaur/minotaur_leftBlock.png")
        }

        for name,image in self.rightImages.items():

            self.rightImages[name] = pygame.transform.scale(image,(175,175))
        
        for name,image in self.leftImages.items():

            self.leftImages[name] = pygame.transform.scale(image,(175,175))


        if self.playerID == 1:
            self.imageMaster = self.rightImages["right1"]
            self.lastKey = "d"
            self.x = 50
            self.y = 400
        
        elif self.playerID == 2:
            self.imageMaster = self.leftImages["left1"]
            self.lastKey = "j"
            self.x = 590
            self.y = 400
#-----------------------------------------------------------------------------------------------------------------------------------------------------


#Main function that starts the game
def main(player1,player2):

    scene = Game(player1,player2)
    scene.start() 


#Calls main 
if __name__ == "__main__":

    #Variables for testing purposes
    test1 = "minotaur"
    test2 = "knight"

    main(test1,test2)