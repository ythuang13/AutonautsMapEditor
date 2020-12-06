import sys, math, os, copy
import pygame as pg
import PySimpleGUI as sg
from pathlib import Path
from datetime import datetime as dt
from AmeSettings import *
from World import World
from Menu import Menu

sys.setrecursionlimit(1000000)

class Map:
    def __init__(self):
        # initialize menu
        self.menu = Menu()

        # initialize pygame
        pg.init()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        self.firstTime = True
        self.canUndo = False
        self.canRedo = False

        #gameIcon
        gameIcon = pygame.image.load(os.path.join("assets", "AME.png"))
        pygame.display.set_icon(gameIcon)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.running = True
        self.clicking = False
        # boolean for if a world is loaded
        self.isWorldLoaded = False

        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.isWorldLoaded:
                self.draw()
    

    def loadWorld(self, template=False):
        if template:
            filePath = "templateWorld.txt"
        else:
            filePath = sg.popup_get_file("Import World.txt", initial_folder=str(Path.home()) + r"\AppData\LocalLow\Denki Ltd\Autonauts\Saves", keep_on_top=True)
        if filePath in (None, ""):
            return

        self.world = World(filePath)
        self.TILESIZE = WINDOW_WIDTH // self.world.wide
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.isWorldLoaded = True
        self.undoState = copy.deepcopy(self.world.tile2DMap)
        self.drawMap()
        self.menu.menuWindow["-time-"].update(value=self.world.timeOfDay)
        self.menu.menuWindow["-gamemode-"].update(value=GAME_MODES[self.world.gameMode])


    def colorPicker(self, num):
        if num not in TILES_TYPE_DICT:
            return DEFAULT # default
        else:
            return TILES_TYPE_DICT[num]

    
    def drawMap(self):
        currentTile, lastTile = 0, -1
        self.screen.fill((0, 0, 0))
        for y in range(self.world.wide):
            for x in range(self.world.high):
                currentTile = self.world.tile2DMap[x][y]
                if currentTile != lastTile:
                    tileColor = self.colorPicker(self.world.tile2DMap[x][y])
                lastTile = self.world.tile2DMap[x][y]
                self.screen.blit(pygame.transform.scale(tileColor, (self.TILESIZE, self.TILESIZE)), (y * self.TILESIZE, x * self.TILESIZE))
                #pygame.draw.rect(self.screen, tileColor, [y * self.TILESIZE, x * self.TILESIZE, self.TILESIZE, self.TILESIZE])


    def drawGrid(self):
        for x in range(0, WINDOW_WIDTH, self.TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, self.TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WINDOW_WIDTH, y))


    # bucket tool
    def bucket(self, x, y):
        def neighbours(x, y):
            return [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]

        def bucketHelper(x, y, oldTileType):
            if x < 0 or y < 0 or x >= self.world.wide or y >= self.world.high:
                return
            elif self.world.tile2DMap[y][x] != oldTileType:
                return
            elif [x, y] in visitedTile:
                return

            visitedTile.append([x, y])
            self.world.tile2DMap[y][x] = self.tileTypeValue
            neighboringTiles = neighbours(x, y)
            for neighbor in neighboringTiles:
                bucketHelper(neighbor[0], neighbor[1], oldTileType)



        currentTileType = self.world.tile2DMap[y][x]
        visitedTile = []
        # recursion helper function to visit all neighboring tile to change them
        bucketHelper(x, y, currentTileType)

        self.drawMap()


    # brush tool
    def brush(self, x, y):
        w = len(self.world.tile2DMap[0])
        h = len(self.world.tile2DMap)

        for i in range(0 - self.brushSize // 2, self.brushSize // 2):
            for j in range(0 - self.brushSize // 2, self.brushSize // 2):
                if math.sqrt(i ** 2 + j ** 2) < (self.brushSize // 2) and 0 <= x + i < w and 0 <= y + j < h:
                    self.world.tile2DMap[y + j][x + i] = self.tileTypeValue
                    self.screen.blit(pygame.transform.scale(self.colorPicker(self.tileTypeValue), (self.TILESIZE, self.TILESIZE)), ((x + i) * self.TILESIZE, (y + j) * self.TILESIZE))
                    #pygame.draw.rect(self.screen, self.colorPicker(self.tileTypeValue), [(x + i) * self.TILESIZE, (y + j) * self.TILESIZE, self.TILESIZE, self.TILESIZE])


    def fill(self):
        self.world.tile2DMap = [[self.tileTypeValue for x in range(self.world.wide)] for x in range(self.world.high)]
        self.drawMap()


    def draw(self):
        self.drawGrid()
        #update the canvas
        pg.display.flip()


    def menuEvents(self):
        event, values = self.menu.menuWindow.read(timeout=10)

        # take data from menu
        try:
            self.tooltype = values["-toolsSelect-"]
            self.brushSize = int(values["-brushSize-"]) * 2
            self.tileTypeValue = int(values["-tileTypeSelect-"][0:2])
        except TypeError:
            self.quit()

        # unlock menu when loaded world
        if self.isWorldLoaded and self.firstTime:
            self.menu.menuWindow["-toolTab-"].update(disabled=False)
            self.menu.menuWindow["-settingsTab-"].update(disabled=False)
            self.menu.menuWindow["-export-"].update(disabled=False)
            self.menu.menuWindow.Refresh()
            self.firstTime = False
        
        if event == sg.WIN_CLOSED:
            self.quit()
        elif event == "-load-":
            self.loadWorld()
        elif event == "-template-":
            self.loadWorld(True)
        elif event == "-reset-":
            self.undoState = copy.deepcopy(self.world.tile2DMap)
            self.world.tile2DMap = copy.deepcopy(self.world.original)
            self.menu.menuWindow["-undo-"].update(disabled=False)
            self.drawMap()
        elif event == "-screenshot-":
            self.screenshot()
        elif event == "-fill-":
            self.undoState = copy.deepcopy(self.world.tile2DMap)
            self.menu.menuWindow["-undo-"].update(disabled=False)
            self.fill()
        elif event == "-export-":
            self.world.exportWorld(values["-visibility-"],
                                   int(values["-gamemode-"][0]),
                                   int(values["-time-"]))
        elif event == "-undo-":
            self.undo()
        elif event == "-redo-":
            self.redo()
        elif event == "-help-":
            self.help()
        elif event == "-textExport-":
            self.world.printTileMapToTxt()
        elif event == "-quick-":
            self.quickLaunch()
        elif event == "-themeSubmit-":
            self.themeSwap(values["-theme-"])
        


    def pygameEvents(self):
        # events for pygame
        mx, my = pygame.mouse.get_pos()
        if self.clicking:
            if not self.canUndo:
                self.undoState = copy.deepcopy(self.world.tile2DMap)
                self.menu.menuWindow["-undo-"].update(disabled=False)
                self.canUndo = True
            if self.canRedo:
                self.menu.menuWindow["-redo-"].update(disabled=True)
                

            if self.tooltype == "brush":
                xPos = mx // self.TILESIZE
                yPos = my // self.TILESIZE
                self.brush(xPos, yPos)
            elif self.tooltype == "bucket":
                xPos = mx // self.TILESIZE
                yPos = my // self.TILESIZE
                self.bucket(xPos, yPos)
                self.clicking = False


        # event checking 
        for event in pg.event.get(pump=True):
            # exit
            if event.type == pg.QUIT:
                self.quit()
            # keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_F12:
                    self.screenshot()
                if event.key == pg.K_z:
                    if self.canUndo:
                        self.undo()
                        self.menu.menuWindow["-undo-"].update(disabled=True)
                        self.canUndo = False
                if event.key == pg.K_y:
                    if self.canRedo:
                        self.redo()
                    
            # mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                    self.canUndo = False
            


    def events(self):
        # events for menu
        self.menuEvents()
        # events for pygame
        if self.isWorldLoaded:
            self.pygameEvents()


    # Take a screenshot
    def screenshot(self):
        now = dt.now()
        formattedTime = now.strftime("%Y-%m-%d_%I.%M.%S")
        pygame.image.save(self.screen, str(Path.home()) + r"\Desktop\\" + formattedTime + ".png")

    
    # undo
    def undo(self):
        self.redoState = copy.deepcopy(self.world.tile2DMap)
        self.world.tile2DMap = copy.deepcopy(self.undoState)
        self.drawMap()
        self.canUndo = False
        self.canRedo = True
        self.menu.menuWindow["-redo-"].update(disabled=False)
        self.menu.menuWindow["-undo-"].update(disabled=True)

    # redo
    def redo(self):
        self.undoState = copy.deepcopy(self.world.tile2DMap)
        self.world.tile2DMap = copy.deepcopy(self.redoState)
        self.drawMap()
        self.canUndo = True
        self.canRedo = False
        self.menu.menuWindow["-redo-"].update(disabled=True)
        self.menu.menuWindow["-undo-"].update(disabled=False)
    
    #swap theme
    def themeSwap(self, newTheme):
        location = self.menu.menuWindow.CurrentLocation();
        self.menu.quit()
        unlock = True
        self.menu = Menu(newTheme, unlock, location)


    #launch help
    def help(self):
        os.startfile(r"help.txt")        
    

    #quick launch game
    def quickLaunch(self):
        os.startfile(r"D:\SteamLibrary\steamapps\common\Autonauts\Autonauts.exe")


    #quit
    def quit(self):
        pg.quit()
        self.menu.quit()    
        self.running = False
        sys.exit(0)


if __name__ == "__main__":    
    ameMap = Map()
    ameMap.run()
