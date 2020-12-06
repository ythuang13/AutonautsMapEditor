import PySimpleGUI as sg
import os
from AmeSettings import BUTTON_SIZE, THEMES

class Menu:

    def __init__(self, theme="BlueMono", unlock=False, newLocation=(1420, 880)):
        self.theme = theme
        sg.theme(self.theme)

        self.toolsTabLayout = self.toolbarTabSetup()
        self.settingsTabLayout = self.settingsTabSetup()
        self.menuWindowLayout = [
            [sg.TabGroup([[sg.Tab("settings", self.settingsTabLayout, key="-settingsTab-"),
                           sg.Tab("tools", self.toolsTabLayout, disabled=not unlock, key="-toolTab-")]])],
        ]

        self.menuWindow = sg.Window("AME Menu", self.menuWindowLayout, keep_on_top=True, alpha_channel=0.9, location=newLocation, icon=os.path.join("assets", "AME.ico"))


    def toolbarTabSetup(self):
        toolsLayout = [
            [sg.Combo(["brush", "bucket"], key="-toolsSelect-", default_value="brush", readonly=True, tooltip="list of tools"),
             sg.Button("fill", tooltip="fill the whole map with one tile", k="-fill-", size=BUTTON_SIZE),
             sg.Button("reset", tooltip="reset back to original", k="-reset-", size=BUTTON_SIZE),
             sg.Button("Undo", tooltip="undo one time", key="-undo-", disabled=True, size=BUTTON_SIZE),
             sg.Button("Redo", tooltip="redo one time", key="-redo-", disabled=True, size=BUTTON_SIZE)
            ],
            [sg.Text("Brush Size:"),
             sg.Slider(range=(1, 10), default_value=2, orientation="h", k="-brushSize-", relief="raised", size=(15, 15), tooltip="change brush size"),
             sg.Button("Screenshot", tooltip="save a screenshot to your desktop (F12)", k="-screenshot-")
            ]
        ]
        colorLayout = [
            [sg.Combo(["0 grass", "1 dirt", "6 coast", "7 ocean", "8 lake", "9 shallow water", "10 sand", "12 swamp", "14 metal ore", "19 clay"], default_value="0 grass", key="-tileTypeSelect-", readonly=True, tooltip="list of all possible tile type")],
        ]

        temp = [[sg.Frame("Tools", toolsLayout, k="-toolsFR-"), sg.VerticalSeparator(), sg.Frame("Tile types", colorLayout, k="-colorFR-")]]
        return temp

    
    def settingsTabSetup(self):
        setting = [
            [sg.Button("load", k="-load-", tooltip="load world file from file directory", size=BUTTON_SIZE),
             sg.Button("template", k="-template-", tooltip="quick load a template world"),
             sg.Button("export", disabled=True, k="-export-", tooltip="export world to desktop", size=BUTTON_SIZE) ,
             sg.Button("help", k="-help-", tooltip="quick launch help guide", size=BUTTON_SIZE),
             sg.Button("quick launch", k="-quick-", tooltip="quick launch game")
            ],
            [sg.Checkbox("world visibility", default=True, k="-visibility-", tooltip="change export setting so world visibility are on"),
             sg.Combo(["0. colonize", "1. free", "2. creative"], k="-gamemode-", default_value="0. colonize", readonly=True, tooltip="change export setting for in-game gamemode")
            ],
            [sg.Text("time:"),
             sg.Slider((0, 126000), resolution=1000, k="-time-", orientation="h", size=(30, 10), relief=sg.RELIEF_RIDGE, tooltip="change export setting for in-game time")
            ]
        ]

        theme_swap = [
            [sg.Combo(THEMES, key="-theme-", default_value=self.theme, readonly=True, tooltip="list of themes")],
            [sg.Button("submit", k="-themeSubmit-", tooltip="submit to change theme")]
        ]

        return [[sg.Frame("Settings", setting, k="-settingsFR-"), sg.VerticalSeparator(), sg.Frame("Themes", theme_swap, k="-themeFR-")]]
    

    def quit(self):
        self.menuWindow.close()
