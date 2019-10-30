#####################
# IMPORT STATEMENTS #
#####################
import pygame
assert pygame.init() == (6, 0)
from pygame.locals import *
from random import random, randint
import webbrowser

##########
# IMAGES  #
##########
load = pygame.image.load
screen1 = load("img/screen1.png")

opioidEpidemic = load("img/opioidepidemic.png")
iraqWar = load("img/iraqwar.png")
wildfires = load("img/wildfires.png")

spinner = load("img/spinner.png")
cont = load("img/continue.png")
info = load("img/info.png")

p_bar = load("img/progress_bar.png")

#################
# INSTANTIATING   #
#################
FONT = pygame.font.Font("img/PressStart2P-Regular.ttf", 30)
SPINNERS = [(50, 165), (250, 165), (475, 165), (715, 165), (75, 275), (400, 275), (675, 275)]
values = [14, 14, 14, 14, 14, 14, 15]
txt = []
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Congressional Budget Manager -- MM Olde Games")
tot = [0, 0, 0]
av = [0, 0, 0]

# National Threat Safety, Emergency Services, Public Happiness
metrics = [0, 0, 0]

# Military, Education, Healthcare, Transportation, Public Welfare, Employment, Foreign Relations

events = [
        [opioidEpidemic, [(5, 5, 5, 5, 5, 5, 5), (5, 5, 35, 80, 15, 5, 5), (5, 30, 95, 20, 30, 25, 5)], "https://www.drugabuse.gov/drugs-abuse/opioids/opioid-overdose-crisis"],
        [iraqWar, [(95, 5, 5, 20, 30, 15, 50), (5, 5, 15, 10, 10, 5, 5), (25, 10, 21, 10, 23, 15, 10)], "https://en.wikipedia.org/wiki/Iraq_War"],
        [wildfires, [(5, 5, 5, 5, 5, 5, 5), (5, 7, 60, 80, 45, 25, 5), (5, 7, 75, 75, 55, 7, 5)], "https://en.wikipedia.org/wiki/2019_California_wildfires"]
    ]

for i in range(len(values)):
    txt.append(FONT.render(str(values[i]), False, (0, 0, 0)))

def checkSpinner(spinner):
    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] >= spinner[0] and pygame.mouse.get_pos()[0] <= spinner[0] + 42 and pygame.mouse.get_pos()[1] >= spinner[1] and pygame.mouse.get_pos()[1] <= spinner[1] + 38:
        return "up"
    elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] >= spinner[0] and pygame.mouse.get_pos()[0] <= spinner[0] + 42 and pygame.mouse.get_pos()[1] >= spinner[1] + 38 and pygame.mouse.get_pos()[1] <= spinner[1] + 76:
        return "down"
    return ""

def checkContinue():
    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pos()[1] >= 450:
        return True
    return False

def checkInfo():
    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] <= 50 and pygame.mouse.get_pos()[1] <= 50:
        return True
    return False

def blitSpinners():
    for i in range(len(SPINNERS)):
        screen.blit(spinner, SPINNERS[i])
        screen.blit(txt[i], (SPINNERS[i][0] + 50, SPINNERS[i][1] + 25))
    screen.blit(cont, (0, 450))
    screen.blit(info, (0, 0))
    #screen.blit(cursor, pygame.mouse.get_pos())
    pygame.display.flip()

##################
# MAIN FUNCTION  #
##################
initScr = True
while initScr:
    screen.blit(screen1, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            initScr = False

for i in range(3): # three events will be simulated
    eventID = randint(0, len(events) - 1)
    screen.blit(events[eventID][0], (0, 0))
    blitSpinners()
    settingBudget = True
    while settingBudget:
        for event in pygame.event.get():
            for i in range(len(SPINNERS)):
                if checkSpinner(SPINNERS[i]) == "up" and values[i] < 99:
                    values[i] += 1
                    txt[i] = FONT.render(str(values[i]), False, (0, 0, 0))
                elif checkSpinner(SPINNERS[i]) == "down" and values[i] > 0:
                    values[i] -= 1
                    txt[i] = FONT.render(str(values[i]), False, (0, 0, 0))
                screen.blit(events[eventID][0], (0, 0))
                blitSpinners()
            if checkContinue() and sum(values) == 100:
                settingBudget = False
            elif checkContinue() and sum(values) != 100:
                if sum(values) < 100:
                    screen.blit(FONT.render("Need " + str(100 - sum(values)) + " more!", False, (255, 255, 255)), (50, 400))
                    pygame.display.flip()
                else:
                    screen.blit(FONT.render("Need " + str(sum(values) - 100) + " less!", False, (255, 255, 255)), (50, 400))
                    pygame.display.flip()
            if checkInfo():
                webbrowser.open(events[eventID][2])
            if event.type == pygame.QUIT:
                pygame.display.quit()
    for j in range(len(metrics)):
        for k in range(len(values)):
            metrics[j] += (values[k] * events[eventID][1][j][k]) // 100
            tot[j] += events[eventID][1][j][k]
        av[j] = tot[j] // 7
    #print(metrics)
    viewingScore = True
    screen.fill((0, 0, 0))
    for i in range(len(metrics)):
        if metrics[i] > av[i]:
            metrics[i] = av[i]
    screen.blit(FONT.render("Foreign Threat Safety: " + str(metrics[0]) + "/" + str(av[0]), False, (255, 255, 255)), (20, 20))
    screen.blit(FONT.render("#" * (metrics[0] // 5), False, (50, 255, 50)), (20, 60))
    screen.blit(FONT.render("Emergency Services: " + str(metrics[1]) + "/" + str(av[1]), False, (255, 255, 255)), (20, 160))
    screen.blit(FONT.render("#" * (metrics[1] // 5), False, (50, 255, 50)), (20, 200))
    screen.blit(FONT.render("Public Happiness: " + str(metrics[2]) + "/" + str(av[2]), False, (255, 255, 255)), (20, 300))
    screen.blit(FONT.render("#" * (metrics[2] // 5), False, (50, 255, 50)), (20, 340))
    screen.blit(cont, (0, 450))
    pygame.display.flip()
    while viewingScore:
        pygame.event.clear()
        for event in pygame.event.get():
            if checkContinue():
                viewingScore = False
    del events[eventID]
screen.fill((0, 0, 0))
finalScore = int(sum(metrics) / sum(av) * 100)
color = (int(abs(100 - finalScore) / 100 * 255), int(finalScore / 100 * 255), 0)
screen.blit(FONT.render("Final Score: " + str(finalScore) + "/100", False, color), (20, 100))
screen.blit(cont, (0, 450))
pygame.display.flip()
viewingScore = True
while viewingScore:
    pygame.event.clear()
    for event in pygame.event.get():
        if checkContinue() and sum(values) == 100:
            viewingScore = False
pygame.display.quit()
