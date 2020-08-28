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
color_light = (80,80,80)
color_dark = (100,100,100)
no_color = (255,255,255)
playerd = pygame.image.load('playerd.png')
players = pygame.image.load('players.png')
playera = pygame.image.load('playera.png')
playerw = pygame.image.load('playerw.png')
player = playerd
screen = pygame.display.set_mode((700,600))
pygame.display.set_caption('WUMPUS GAME')
return_home = False
#use in logic
visited = list()
safe = list()
unsafe = list()

def canMove(x,y):
    global graph
    if x >= width[0] or x < 0:
        return False
    if y >= height[0] or y < 0:
        return False
    return True

def menu():
    font2 = pygame.font.SysFont("arial", 36)
    input1 = font2.render('input1', True, no_color)
    input2 = font2.render('input2', True, no_color)
    input3 = font2.render('input3', True, no_color)
    input4 = font2.render('input4', True, no_color)
    input5 = font2.render('input5', True, no_color)
    pygame.display.update()
    while True:
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get(): 
            if ev.type == pygame.QUIT: 
                pygame.quit() 
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 80 <= mouse[0] <= 80 + 110 and 100 <= mouse[1] <= 100 +40:
                    return 'map/input1.txt'
                if 80 <= mouse[0] <= 80 + 110 and 200 <= mouse[1] <= 200 +40:
                    return 'map/input2.txt'
                if 80 <= mouse[0] <= 80 + 110 and 300 <= mouse[1] <= 300 +40:
                    return 'map/input3.txt'
                if 80 <= mouse[0] <= 80 + 110 and 400 <= mouse[1] <= 400 +40:
                    return 'map/input4.txt'
                if 80 <= mouse[0] <= 80 + 110 and 500 <= mouse[1] <= 500 +40:
                    return 'map/input5.txt'
        if 80 <= mouse[0] <= 80 + 110 and 100 <= mouse[1] <= 100 +40: 
            pygame.draw.rect(screen,color_light,[80,100,110,40])  
        else: 
            pygame.draw.rect(screen,color_dark,[80,100,110,40])
        screen.blit(input1 , (80 + 10, 100))
        if 80 <= mouse[0] <= 80 + 110 and 200 <= mouse[1] <= 200 +40: 
            pygame.draw.rect(screen,color_light,[80,200,110,40])  
        else: 
            pygame.draw.rect(screen,color_dark,[80,200,110,40])
        screen.blit(input2 , (80 + 10, 200))
        if 80 <= mouse[0] <= 80 + 110 and 300 <= mouse[1] <= 300 +40: 
            pygame.draw.rect(screen,color_light,[80,300,110,40])  
        else: 
            pygame.draw.rect(screen,color_dark,[80,300,110,40])
        screen.blit(input3 , (80 + 10, 300))
        if 80 <= mouse[0] <= 80 + 110 and 400 <= mouse[1] <= 400 +40: 
            pygame.draw.rect(screen,color_light,[80,400,110,40])  
        else: 
            pygame.draw.rect(screen,color_dark,[80,400,110,40])
        screen.blit(input4 , (80 + 10, 400))
        if 80 <= mouse[0] <= 80 + 110 and 500 <= mouse[1] <= 500 +40: 
            pygame.draw.rect(screen,color_light,[80,500,110,40])  
        else: 
            pygame.draw.rect(screen,color_dark,[80,500,110,40])
        screen.blit(input5 , (80 + 10, 500))
        
        pygame.display.update()
def input_graph(file_input):
    file = open(file_input,'r')
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
def renderMapNotFog():
    global player
    global Agent
    global graph2
    screen.fill((103, 100, 112))
    wumpus = pygame.image.load('wumpus.png')
    gold = pygame.image.load('gold.png')
    hole = pygame.image.load('hole.png')
    door = pygame.image.load('door.png')
    yellow = pygame.image.load('yellow.png')
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if 'W' in graph[i][j]:
                screen.blit(wumpus, (j* square,i * square))
            if 'G' in graph[i][j]:
                screen.blit(gold, (j* square,i * square))
            if 'P' in graph[i][j]:
                screen.blit(hole, (j* square,i * square))
            if 'D' in graph[i][j]:
                screen.blit(door, (j* square,i * square))
            if 'S' in graph[i][j]:
                font1 = pygame.font.SysFont("arial", 12)
                text1 = font1.render("Stench", True, green, blue)
                textRect1 = text1.get_rect()
                textRect1.center = (j* square,i * square + 5)
                screen.blit(text1, textRect1.center)
            if 'B' in graph[i][j]:
                font1 = pygame.font.SysFont("arial", 12)
                text1 = font1.render("Breeze", True, green, blue)
                textRect1 = text1.get_rect()
                textRect1.center = (j* square,i * square + 18)
                screen.blit(text1, textRect1.center)
    screen.blit(player, (Agent[0]* square,Agent[1] * square))
    pygame.display.update()
    font1 = pygame.font.SysFont("arial", 26)
    text1 = font1.render("SCORE: " + str(score[0]), True, green, blue)
    textRect1 = text1.get_rect()
    textRect1.center = (0, height[0] * square + 3)
    screen.blit(text1, textRect1.center)
    pygame.display.update()
    
def renderMap():
    global player
    global Agent
    global graph2
    screen.fill((103, 100, 112))
    wumpus = pygame.image.load('wumpus.png')
    gold = pygame.image.load('gold.png')
    hole = pygame.image.load('hole.png')
    door = pygame.image.load('door.png')
    yellow = pygame.image.load('yellow.png')
    if 'F' in graph2[Agent[1]][Agent[0]]:
        graph2[Agent[1]][Agent[0]] = graph2[Agent[1]][Agent[0]].replace('F','')
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if 'F' not in graph2[i][j]:
                graph2[i][j] = graph[i][j]
                screen.blit(yellow, (j* square,i * square))
            if 'W' in graph2[i][j]:
                screen.blit(wumpus, (j* square,i * square))
            if 'G' in graph2[i][j]:
                screen.blit(gold, (j* square,i * square))
            if 'P' in graph2[i][j]:
                screen.blit(hole, (j* square,i * square))
            if 'D' in graph2[i][j]:
                screen.blit(door, (j* square,i * square))
            if 'S' in graph2[i][j]:
                font1 = pygame.font.SysFont("arial", 12)
                text1 = font1.render("Stench", True, green, blue)
                textRect1 = text1.get_rect()
                textRect1.center = (j* square,i * square + 5)
                screen.blit(text1, textRect1.center)
            if 'B' in graph2[i][j]:
                font1 = pygame.font.SysFont("arial", 12)
                text1 = font1.render("Breeze", True, green, blue)
                textRect1 = text1.get_rect()
                textRect1.center = (j* square,i * square + 18)
                screen.blit(text1, textRect1.center)
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
def getAdj(node):
    adj = []
    x,y = node[0],node[1]
    buf = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    while len(buf) > 0:
        temp = buf.pop(0)
        if canMove(temp[0],temp[1]) == True:
            adj.append(temp)
    return adj

def logic():
    global Agent
    global visited
    global safe
    global unsafe
    global num
    if Agent not in visited:
        visited.append((Agent[0],Agent[1]))
        if (Agent[0],Agent[1]) in safe:
            safe.remove((Agent[0],Agent[1]))
    else:
        return
    for it in getAdj(Agent):
        if 'S' in graph2[Agent[1]][Agent[0]] or 'B' in graph2[Agent[1]][Agent[0]]:
            unsafe.append(it)
        else:
            if it not in visited and it not in safe:
                safe.append(it)
            if it in unsafe:
                unsafe.remove(it)
    for it in unsafe:
        num1 = 0
        num2 = 0
        for it1 in getAdj(it):
            if 'S' in graph2[it1[1]][it1[0]] and 'B' not in graph2[it1[1]][it1[0]]:
                num1 += 1
            if 'B' in graph2[it1[1]][it1[0]] and 'S' not in graph2[it1[1]][it1[0]]:
                num2 += 1
        if num1 >= 1 and num2 >= 1:
            unsafe.remove(it)
            if it not in safe and it not in visited:
                safe.append(it)
    
def find_path():
    global visited
    global safe
    global unsafe
    global return_home
    global graph2
    explored = []
    fqueue = [[(Agent[0],Agent[1])]]
    while len(fqueue)>0:
        temp = fqueue.pop(0)
        last_node = temp[-1]
        if return_home == False and last_node in safe:
            if len(temp) == 1:
                return temp[0]
            else:
                return temp[1]
        if return_home == True and 'D' in graph2[last_node[1]][last_node[0]]:
            if len(temp) == 1:
                return temp[0]
            else:
                return temp[1]
        for it in getAdj(last_node):
            path_ = temp.copy()
            path_.append(it)
            if (it in visited or it in safe) and it not in explored and canMove(it[0],it[1]) == True:
                fqueue.append(path_)
                explored.append(it)
    return []

def agent_play():
    global Agent
    global return_home
    logic()
    if return_home == False:
        #bfs
        temp = find_path()
        if len(temp) == 0:
            return_home = True
            temp = find_path()
    else:
        temp = find_path()
    direct_ = 'O'
    if temp[0] == Agent[0] + 1 and temp[1] == Agent[1]:
        direct_ = 'D'
    if temp[0] == Agent[0] - 1 and temp[1] == Agent[1]:
        direct_ = 'A'
    if temp[0] == Agent[0] and temp[1] == Agent[1] + 1:
        direct_ = 'S'
    if temp[0] == Agent[0] and temp[1] == Agent[1] - 1:
        direct_ = 'W'
    if temp == (Agent[0],Agent[1]):
        return direct_,True
    return direct_,False

def change_direct(direct_):
    global player
    global Agent
    if direct_ == 'O':
        return 0
    if direct[0] == direct_:
        temp = Agent.copy()
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
            return 0
        return 10
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
    return 0
        
def play():
    global Agent
    global graph
    global graph2
    for i in range(len(graph)):
        graph2.append([])
        for j in range(len(graph[0])):
            graph2[i].append('F')
    #find agent
    numW = 0
    numG = 0
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if 'A' in graph[i][j]:
                Agent = [j,i]
                graph[i][j] = graph[i][j].replace('A', 'D')
            if 'W' in graph[i][j]:
                numW +=1
            if 'G' in graph[i][j]:
                numG +=1
    if Agent[0] == -1 and Agent[1] == -1:
        print('File no agent')
        exit(0)
    renderMap()
    #renderMapNotFog()
    run = True
    while run == True:
        if numW == 0 and numG == 0:
            font = pygame.font.SysFont("arial", 36)
            text = font.render('Game end', True, green, blue)
            textRect = text.get_rect()
            textRect.center = (0, (height[0] + 1) * square + 3)
            screen.blit(text, textRect.center)
            pygame.display.update()
            time.sleep(0.3)
            return
        direct_,shot = agent_play()
        #direct_,shot = human_play()
        move = False
        if shot == False:
            score[0] -= change_direct(direct_)
        if 'P' in graph[Agent[1]][Agent[0]] or 'W' in graph[Agent[1]][Agent[0]]:
            score[0] -= 10000
            run = False
        if 'G' in graph[Agent[1]][Agent[0]]:
            numG -= 1
            renderMap()
            time.sleep(0.2)
            score[0] += 100
            graph[Agent[1]][Agent[0]] = graph[Agent[1]][Agent[0]].replace('G', '')   
        if shot == True :
            if 'D' in graph[Agent[1]][Agent[0]]:
                score[0] += 10
                renderMap()
                font = pygame.font.SysFont("arial", 36)
                text = font.render('Game end', True, green, blue)
                textRect = text.get_rect()
                textRect.center = (0, (height[0] + 1) * square + 3)
                screen.blit(text, textRect.center)
                pygame.display.update()
                time.sleep(0.3)
                return
            else:
                score[0] -= 100
                temp = Agent.copy()
                change_direct(direct_)
                if 'W' in graph[Agent[1]][Agent[0]]:
                    numW -= 1
                    graph[Agent[1]][Agent[0]] = graph[Agent[1]][Agent[0]].replace('W','')
                    x,y = Agent[0],Agent[1]
                    buf = [(x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                    while len(buf) > 0:
                        x2,y2 = buf.pop(0)
                        if canMove(y2,x2) == False:
                            continue
                        buf2 = [(x2+1,y2),(x2-1,y2),(x2,y2+1),(x2,y2-1)]
                        flag = False
                        while len(buf2) > 0:
                            x3,y3 = buf2.pop(0)
                            if canMove(y3,x3) == False:
                                continue
                            if 'W' in graph[y3][x3]:
                                if 'S' not in graph[y2][x2]:
                                    graph[y2][x2] += 'S'
                                flag = True
                            if 'P' in graph[y3][x3]:
                                if 'B' not in graph[y2][x2]:
                                    graph[y2][x2] += 'B'
                            if len(buf2) == 0 and flag == False:
                                graph[y2][x2] = graph[y2][x2].replace('S','')
                Agent = temp
        renderMap()
        
    font = pygame.font.SysFont("arial", 36)
    text = font.render('GAME OVER', True, green, blue)
    textRect = text.get_rect()
    textRect.center = (0, (height[0] + 1) * square + 3)
    screen.blit(text, textRect.center)
    pygame.display.update()
    time.sleep(1)
            
if __name__ == '__main__':
    file_input = menu()
    input_graph(file_input)
    play()
