import pygame
import time
graph = []
graph2 = []
height = [0]
width = [0]
square = 40
pygame.init()
Agent = [-1,-1]
score = [0]
direct = ['D']
green = (0, 255, 0) 
blue = (0, 0, 128)
playerd = pygame.image.load('playerd.png')
players = pygame.image.load('players.png')
playera = pygame.image.load('playera.png')
playerw = pygame.image.load('playerw.png')
player = playerd
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('WUMPUS GAME')
def input_graph():
    file = open('input.txt','r')
    temp = list(map(int,file.readline().split()))
    height[0],width[0] = temp[0],temp[1]
    for i in range(height[0]):
        temp = list(map(str,file.readline().split(".")))
        row = []
        for i in temp:
            if '\n' in i:
                i = i.replace('\n', '')   
            row.append(i)
        graph.append(row)
    temp = list(map(int,file.readline().split()))
    screen = pygame.display.set_mode((width[0] * square,(height[0] + 2) * square))
    screen.fill((0,0,0))
    pygame.display.flip()
    
def renderMap():
    global player
    global Agent
    screen.fill((103, 100, 112))
    wumpus = pygame.image.load('wumpus.png')
    gold = pygame.image.load('gold.png')
    hole = pygame.image.load('hole.png')
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if 'W' in graph[i][j]:
                screen.blit(wumpus, (j* square,i * square))
            if 'G' in graph[i][j]:
                screen.blit(gold, (j* square,i * square))
            if 'P' in graph[i][j]:
                screen.blit(hole, (j* square,i * square))
            if 'A' in graph[i][j]:
                Agent = [j,i]
                graph[i][j] = ''
    screen.blit(player, (Agent[0]* square,Agent[1] * square))
    pygame.display.update()
    font1 = pygame.font.SysFont("arial", 26)
    text1 = font1.render("SCORE: " + str(score[0]), True, green, blue)
    textRect1 = text1.get_rect()
    textRect1.center = (0, height[0] * square + 3)
    screen.blit(text1, textRect1.center)
    pygame.display.update()

def human_play():
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == 97 or event.key == pygame.K_LEFT:
                        return 'A',False
                    if event.key == 119 or event.key == pygame.K_UP:
                        return 'W',False
                    if event.key == 115 or event.key == pygame.K_DOWN:
                        return 'S',False
                    if event.key == 100 or event.key == pygame.K_RIGHT:
                        return 'D',False
                    if event.key == pygame.K_SPACE:
                        return direct[0],True
    return '',False

def agent_play():
    return 'W',False

def canMove(x,y):
    if x >= width[0] or x < 0:
        return False
    if y >= height[0] or y < 0:
        return False
    return True

def change_direct(direct_):
    global player
    global Agent
    if direct[0] == direct_:
        temp = Agent
        if direct_ == 'W':
            Agent[1] -= 1
        if direct_ == 'S':
            Agent[1] += 1
        if direct_ == 'D':
            Agent[0] += 1
        if direct_ == 'A':
            Agent[0] -= 1
        if canMove(Agent[0],Agent[1]) == False:
            Agent = temp
    else:
        if direct_ == 'W':
            player = playerw
        if direct_ == 'S':
            player = players
        if direct_ == 'D':
            player = playerd
        if direct_ == 'A':
            player = playera
        direct[0] = direct_
        
def play():
    if Agent[0] == -1 and Agent[1] == -1:
        print('File no agent')
        exit(0)
    run = True
    while run == True:
        #direct_,shot = agent_play()
        direct_,shot = human_play()
        change_direct(direct_)
        if 'P' in graph[Agent[1]][Agent[0]] or 'W' in graph[Agent[1]][Agent[0]]:
            score[0] -= 10000
            run = False
        if 'G' in graph[Agent[1]][Agent[0]]:
            score[0] += 100
            graph[Agent[1]][Agent[0]] = graph[Agent[1]][Agent[0]].replace('G', '')   
        #if shot == True:
        renderMap()
    font = pygame.font.SysFont("arial", 36)
    text = font.render('GAME OVER', True, green, blue)
    textRect = text.get_rect()
    textRect.center = (0, (height[0] + 1) * square + 3)
    screen.blit(text, textRect.center)
    pygame.display.update()
    time.sleep(1)
            
if __name__ == '__main__':
    input_graph()
    renderMap()
    play()
    print(Agent)