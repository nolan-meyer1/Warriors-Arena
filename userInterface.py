import simpleGE,pygame,game,time
"""
User interface for the start screen. This allows you to 
select your character's then start the game. All citing for
images/sound is located in the game file source code.

Nolan Meyer

Novemeber 28, 2023
"""

#Class that controls the user interface
class UserInterface(simpleGE.Scene):

    def __init__(self):
        
        super().__init__()

        #Setup the screen
        self.setCaption("Start Screen")
        self.background = pygame.Surface((self.screen.get_size()))
        self.background.fill("black")

        #Logo
        self.logo = simpleGE.SuperSprite(self)
        self.logo.imageMaster = pygame.image.load("UI/logo.png")
        self.logo.setPosition((320,200))
        self.logo.setSize(300,300)

        #Start Button
        self.startButton = simpleGE.Button()
        self.startButton.fgColor = (0,0,0)
        self.startButton.bgColor = (225,225,0)
        self.startButton.center = (320,375)
        self.startButton.text = "START"

        #Fight button that will start fight sequence
        self.fightButton = simpleGE.Button()
        self.fightButton.fgColor = (0,0,0)
        self.fightButton.bgColor = (225,225,0)
        self.fightButton.center = (320,70)
        self.fightButton.text = "FIGHT"
        self.fightButton.hide()

        #Knight Headshot
        self.knightHeadshot = simpleGE.SuperSprite(self)
        self.knightHeadshot.imageMaster = pygame.image.load("Knight/knight_headshot.png")
        self.knightHeadshot.setSize(75,75)
        self.knightHeadshot.setPosition((50,400))
        self.knightHeadshot.hide()

        self.knightHotSpot = HotSpot(self,50,400,"knight")

        #Minotuar HeadShot
        self.minotaurHeadshot = simpleGE.SuperSprite(self)
        self.minotaurHeadshot.imageMaster = pygame.image.load("Minotaur/minotaur_headshot.png")
        self.minotaurHeadshot.setSize(75,75)
        self.minotaurHeadshot.setPosition((590,400))
        self.minotaurHeadshot.hide()

        self.minotaurHotSpot = HotSpot(self,590,400,"minotaur")

        #Talos Headshot
        self.talosHeadshot = simpleGE.SuperSprite(self)
        self.talosHeadshot.imageMaster = pygame.image.load("Talos/talos_headshot.png")
        self.talosHeadshot.setSize(75,75)
        self.talosHeadshot.setPosition((320,400))
        self.talosHeadshot.hide()

        self.talosHotSpot = HotSpot(self,320,400,"talos")
        self.talosHotSpot.hide()

        #P1 control label
        self.P1control = simpleGE.MultiLabel()
        self.P1control.textLines = ["Player 1 Controls: Hit- W KEY Block- Q KEY Left Walk- A KEY", 
                                    "Right Walk- D KEY, Jump- S KEY"]
        self.P1control.size = (600,80)
        self.P1control.bgColor = ("orange")
        self.P1control.hide()

        #P2 control label
        self.P2control = simpleGE.MultiLabel()
        self.P2control.textLines = ["Player 2 Controls: Hit- I KEY Block- O KEY Left Walk- J KEY", 
                                    "Right Walk- L KEY, Jump- K KEY"]
        self.P2control.size = (600,80)
        self.P2control.bgColor = ("orange")
        self.P2control.hide()

        #Sounds
        self.player1Sound = simpleGE.Sound("UI/player_1.wav")
        self.player2Sound = simpleGE.Sound("UI/player_2.wav")
        self.chooseCharacter = simpleGE.Sound("UI/choose_your_character.wav")
        self.selectSound = simpleGE.Sound("UI/click.wav")

        self.selectionTurn = 1

        #Background music
        pygame.mixer.music.load("UI/loadingScreenSound.mp3")
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play(-1)

        #Variables that will contain the selections
        self.player1 = ""
        self.player2 = ""

        self.sprites = [self.fightButton,self.knightHeadshot,self.knightHotSpot,self.minotaurHeadshot,
                        self.minotaurHotSpot,self.logo,self.startButton,self.P1control,self.P2control,
                        self.talosHeadshot,self.talosHotSpot]


    #Checks that both characters have selected a character and ready to fight
    def update(self):

        if self.startButton.clicked:

            self.logo.hide()
            self.startButton.hide()
            self.fightButton.show((320,70))
            self.knightHeadshot.show()
            self.minotaurHeadshot.show()
            self.talosHeadshot.show()
            self.talosHotSpot.show()
            self.P1control.show((320,150))
            self.P2control.show((320,250))

            self.player1Sound.play()
            time.sleep(1)
            self.chooseCharacter.play()

        if self.fightButton.clicked:

            if self.selectionTurn == 3:
                pygame.mixer.music.stop()
                self.stop()
                


#Class that creates hotspots to be clicked on
class HotSpot(simpleGE.BasicSprite):
    
    def __init__(self, scene,x,y,character):
        super().__init__(scene)
        self.image = pygame.Surface((75, 75), pygame.SRCALPHA)
        self.image.fill(pygame.Color(0,0,0,0))
        self.rect = self.image.get_rect()
        self.active = False
        self.clicked = False
        self.transparent = False
        self.x = x
        self.y = y
        self.hitTimes = 0
        self.character = character
        
    def checkEvents(self):
        #check for clicked and active                
        
        self.clicked = False

        #check for mouse input
        if pygame.mouse.get_pressed() == (1, 0, 0):
            
            if self.rect.collidepoint(pygame.mouse.get_pos()):
               
                #Selection for the knight character
                if (self.scene.selectionTurn == 1) and self.character == "knight":
                    self.scene.selectSound.play()
                    self.scene.knightHeadshot.imageMaster = pygame.image.load("Knight/knight_headshotSelected.png")
                    self.scene.knightHeadshot.setSize(75,75)
                    self.scene.selectionTurn += 1 
                    self.scene.player1 = "knight"
                    self.scene.player2Sound.play()
                    time.sleep(1)
                    self.scene.chooseCharacter.play()
                    self.hide()
                    
                elif (self.scene.selectionTurn == 2) and self.character == "knight":
                    self.scene.selectSound.play()
                    self.scene.knightHeadshot.imageMaster = pygame.image.load("Knight/knight_headshotSelected.png")
                    self.scene.knightHeadshot.setSize(75,75)
                    self.scene.selectionTurn += 1 
                    self.scene.player2 = "knight"
                    self.hide()
                    
                #Minotaur selection
                if (self.scene.selectionTurn == 1) and self.character == "minotaur":
                    self.scene.selectSound.play()
                    self.scene.minotaurHeadshot.imageMaster = pygame.image.load("Minotaur/minotaur_headshotSelected.png")
                    self.scene.minotaurHeadshot.setSize(75,75)
                    self.scene.selectionTurn += 1 
                    self.scene.player1 = "minotaur"
                    self.scene.player2Sound.play()
                    time.sleep(1)
                    self.scene.chooseCharacter.play()
                    self.hide()
                    
                elif (self.scene.selectionTurn == 2) and self.character == "minotaur":
                    self.scene.selectSound.play()
                    self.scene.minotaurHeadshot.imageMaster = pygame.image.load("Minotaur/minotaur_headshotSelected.png")
                    self.scene.minotaurHeadshot.setSize(75,75)
                    self.scene.selectionTurn += 1 
                    self.scene.player2 = "minotaur"
                    self.hide()
                
                #Talos Selection
                if (self.scene.selectionTurn == 1) and self.character == "talos":
                    self.scene.selectSound.play()
                    self.scene.talosHeadshot.imageMaster = pygame.image.load("Talos/talos_headshotSelected.png")
                    self.scene.talosHeadshot.setSize(75,75)
                    self.scene.selectionTurn += 1 
                    self.scene.player1 = "talos"
                    self.scene.player2Sound.play()
                    time.sleep(1)
                    self.scene.chooseCharacter.play()
                    self.hide()
                    
                elif (self.scene.selectionTurn == 2) and self.character == "talos":
                    self.scene.selectSound.play()
                    self.scene.talosHeadshot.imageMaster = pygame.image.load("Talos/talos_headshotSelected.png")
                    self.scene.talosHeadshot.setSize(75,75)
                    self.scene.selectionTurn += 1 
                    self.scene.player2 = "talos"
                    self.hide()


        #check for mouse release
        if self.active == True:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.active = False
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked = True


#Main function that declares the scene
def main():
   
    UI = UserInterface()
    UI.start()

    player1 = UI.player1
    player2 = UI.player2

    gameplay = game.Game(player1,player2)
    gameplay.start()


#Calls the main function
if __name__ == "__main__":

    main()