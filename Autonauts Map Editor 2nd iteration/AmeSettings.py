import pygame
import os

# assets loading
TURF = pygame.image.load(os.path.join("assets", "turf.png"))
SOIL = pygame.image.load(os.path.join("assets", "soil.png"))
TILLED_SOIL = pygame.image.load(os.path.join("assets", "tilled soil.png"))
SAND = pygame.image.load(os.path.join("assets", "sand.png"))
STONE_DEPOSITS = pygame.image.load(os.path.join("assets", "stone deposits.png"))
RICH_STONE_DEPOSITS = pygame.image.load(os.path.join("assets", "rich stone deposits.png"))
CLAY_DEPOSITS = pygame.image.load(os.path.join("assets", "clay deposits.png"))
RICH_CLAY_DEPOSITS = pygame.image.load(os.path.join("assets", "rich clay deposits.png"))
TRACE_METAL_ORE_DEPOSITS = pygame.image.load(os.path.join("assets", "trace metal ore deposits.png"))
METAL_ORE_DEPOSITS = pygame.image.load(os.path.join("assets", "metal ore deposits.png"))
TRACE_COAL_DEPOSITS = pygame.image.load(os.path.join("assets", "trace coal deposits.png"))
COAL_DEPOSITS = pygame.image.load(os.path.join("assets", "coal deposits.png"))
FRESH_WATER = pygame.image.load(os.path.join("assets", "fresh water.png"))
FRESH_WATER_DEEP = pygame.image.load(os.path.join("assets", "fresh water deep.png"))
SEA_WATER = pygame.image.load(os.path.join("assets", "sea water.png"))
SEA_WATER_DEEP = pygame.image.load(os.path.join("assets", "sea water deep.png"))
SWAMP = pygame.image.load(os.path.join("assets", "swamp.png"))
DEFAULT = pygame.image.load(os.path.join("assets", "default.png"))


LIGHTGREY = (100, 100, 100)
TILES_TYPE_DICT = {0: TURF, # Turf
                 1: SOIL, # Soil
                 2: TILLED_SOIL, # Tilled Soil
                 3: DEFAULT, # Hole
                 6: FRESH_WATER, # Fresh Water
                 7: FRESH_WATER_DEEP, # Fresh Water (Deep)
                 8: SEA_WATER, # Sea Water
                 9: SEA_WATER_DEEP, # Sea Water (Deep)
                 10: SAND, # Sand
                 12: SWAMP, # Swamp
                 14: TRACE_METAL_ORE_DEPOSITS, # Trace Metal Ore Deposits
                 19: CLAY_DEPOSITS, # Clay Deposits
                 23: TRACE_COAL_DEPOSITS, # Trace Coal Deposits
                 29: STONE_DEPOSITS, # Stoned Deposit
                 }
GAME_MODES = {0: "0. colonize", 1: "1. free", 2: "2. creative"}
THEMES = ["BlueMono", "Black", "DarkBlue", "DarkGreen4", "GreenTan", "LightGreen", "TealMono"]

# game settings
ENLARGE = TILESIZE = 5
FPS = 60
WINDOW_WIDTH = 420 * ENLARGE
WINDOW_HEIGHT = 210 * ENLARGE
TITLE = "Autonauts Map Editor"
BUTTON_SIZE = (5, 0)

