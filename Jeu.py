import pyxel

CIEL = [0,0]
DRAPEAU = [3,21]
casesSol =[] 
pos = [64,0]
prevPos = pos
grav = 3.5
speed = 3
frameCount = 0
chute = False
enSaut = 0
enMouvement = False

niveau = 0

drapeau = [
    {"num":1, "valide": False, "pos":[0,88], "scroll": [25*8, 72*8]},
    {"num":2, "valide": False, "pos": [0, 32], "scroll": [24, 232*8]},
    {"num":3, "valide": False, "pos": [15*8, 40], "scroll": [96*8, 56*8]},
    {"num":4, "valide": False, "pos": [15*8, 11*8], "scroll": [96*8, 120*8]}
    ]

sprites = [[40,16], [8,16], [16, 16]]

scroll_x = 0
scroll_y = 0

def case(x, y):
    if niveau == 0:
        return list(pyxel.tilemap(0).pget(72 + x//8, y//8))
    else:
        return list(pyxel.tilemap(0).pget( (scroll_x+x)//8, (scroll_y+y)//8))
    
def setCases():
    global scroll_x, scroll_y
    sol = []
    for i in range(0,128,8):
        for j in range(0,128,8):
            if  case(i,j) != CIEL and case(i,j) != DRAPEAU:
                sol.append([i,j])
    return sol
    
def mouvement(s):
    global chute, enSaut
    vel = [0, 0]
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
        vel[0] +=s
        vel[0] = colMurR(vel[0])
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
        vel[0] +=-s
        vel[0] = colMurL(vel[0])
    if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and not chute:
       enSaut = 30
    if enSaut:
        enSaut += -2
        vel[1] = -enSaut/2.5
        if case(pos[0], pos[1]) != CIEL:
            vel[1]=0
    if chute:
        vel[1] += grav
   
    return vel
    
def colMurR(vel):
    global casesSol
    # while [pos[0]+7 + vel -(pos[0]+7 + vel)%8, pos[1]] in casesSol:
    #     vel += -1 
    if case(pos[0]+8, pos[1]) == CIEL or case(pos[0]+8, pos[1]) == DRAPEAU:
        vel += 1
    else:
        vel=0
    return vel
        
def colMurL(vel):
    global casesSol
    # while [pos[0] + vel -(pos[0] + vel)%8, pos[1]] in casesSol:
    #     vel += 1
    if case(pos[0]-8, pos[1]) == CIEL or case(pos[0]-8, pos[1]) == DRAPEAU:
        vel += -1
    else:
        vel=0
    return vel
    
def changement_de_niveau():
    global niveau, drapeau, scroll_x, scroll_y, pos, casesSol
    for i in range(4):
        if pos == drapeau[i]["pos"]:
            niveau = drapeau[i]["num"]
            scroll_x = drapeau[i]["scroll"][0]
            scroll_y = drapeau[i]["scroll"][1] 
            pos = [0,128-32]
            casesSol = setCases()  
                
def animation(pos, prev):
    global sprites, m, chute, enMouvement, casesSol
    if chute :
        pyxel.blt(pos[0], pos[1], 0, sprites[2][0], sprites[2][1], 8, 8, colkey = 5)
    elif enMouvement:
        pyxel.blt(pos[0], pos[1], 0, sprites[1][0], sprites[1][1], 8, 8, colkey = 5)
    else:
        pyxel.blt(pos[0], pos[1], 0, sprites[0][0], sprites[0][1], 8, 8, colkey = 5)
        
def update():
    global pos, prevPos, frameCount, chute, enMouvement,scroll_x,scroll_y
    mouv = mouvement(speed)
    if mouv != [0,0]:
        enMouvement = True
    else:
        enMouvement = False
    
    
    pos[0] += mouv[0] 
    pos[1] += mouv[1]
    
    if niveau == 0:
        if pos[0]+mouv[0] <= 0 : 
            pos[0] = 0
        if pos[0]+mouv[0] >= 120:
            pos[0] = 120
    else:
        if pos[1]+mouv[1] < 0 : 
            scroll_y = scroll_y - 64
            pos[1]=pos[1]+64
            casesSol = setCases()
        if pos[1]+mouv[1] > 120 : 
            scroll_y = scroll_y + 64
            pos[1]=pos[1]-64
            casesSol = setCases()
        if pos[0]+mouv[0] < 0 : 
            scroll_x = scroll_x - 64
            pos[0]=pos[0]+64
            casesSol = setCases()
        if pos[0]+mouv[0] > 120:
            scroll_x = scroll_x + 64
            pos[0]=pos[0]-64
            casesSol = setCases()
            
    frameCount += 1
    
    if case(pos[0], pos[1]+8) == CIEL or case(pos[0], pos[1]+8) == DRAPEAU:
        chute = True
    else:
        chute = False
        pos[1] = pos[1] - pos[1]%8
    
    casesSol = setCases()    
        
    if niveau == 0:
        changement_de_niveau()
        
def draw():
    global pos, prevPos
    pyxel.cls(0)
    if niveau == 0:
        pyxel.bltm(0, 0, 0, 72*8, 0*8, 128, 128)
    else:
        pyxel.bltm(0, 0, 0, scroll_x, scroll_y, 128, 128)
    animation(pos, prevPos)
    
pyxel.init(128, 128, title="temporaire")
pyxel.load("42.pyxres")
casesSol = setCases()
print(casesSol)
pyxel.run(update, draw)