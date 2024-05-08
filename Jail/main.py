import pygame
from button import Button

pygame.init()
pygame.mixer.init()
beep = pygame.mixer.Sound('sfx/beep.ogg')
channel1 = pygame.mixer.Channel(0)
font1 = pygame.font.Font('font/digital-7.ttf',24)
screen = pygame.display.set_mode([800,500])
timer = pygame.time.Clock()

postext = 'Respond Positively'
negtext = 'Respond Negatively'
state = 0
postextoptions = ['Tell her','POSITIVE THING']
negtextoptions = ['Don\'t tell her','NEGATIVE THING']

story = [['Two guards drag an unconscious person across a dark prison hallway...','Captain: \"Lock him up with the rest of the non workers.\"','An elderly female prisoner looks at the unconcious person who is bleeding.','Old woman: \"Oh poor boy... what have they done to you?\"','The old woman turns to her son and says: \"Timmy! Give me the bandage!\"', 'The guards slam the gate shut.','The old woman turns to the wounded prisoner who had started moving.','"You stay still, young man.", The old woman says to the prisoner.', '"Why did they do this to you?"       [Note: You are playing as the Prisoner]'],
         ['Old woman: \"It\'s okay.. You should really take some rest. Atleast for now.\"','You rest your head on the concrete floor and slowly fall asleep.','TEST QUESTION']]

pos = [['You: "They took my brother away."', '"All I did was ask them where they were taking him."','"I mean, he\'s just a little boy. What did he ever do to anybody?"','" It\'s so wrong.. All of this is so wrong..."','Old woman: "I know it must be really tough for you."','You: "I should go and look for him."'],
       ['POSITIVE ANSWER']]
neg = [['You: "It was nothing."','Old woman: "Nothing?"','Prisoner: "I don\'t want to talk about it."'],
       ['NEGATIVE ANSWER']]

playerDecisions = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

messages = story[state]
snip = font1.render('', True, 'dark green')
counter = 0
speed = 1
b = 0
pflag = 0
nflag = 0
done = False
run = True
active_message = 0
message = messages[active_message]
while run:
    screen.fill('dark green')
    timer.tick(60)
    pygame.draw.rect(screen, 'black', [0, 380, 800, 500-380])
    if counter < speed * len(message):
        counter += 1
        if b == 0:
            channel1.play(beep)
            b = 1
        elif b < 4:
            b += 1
        if b == 4:
            channel1.pause()
            b = 0

    elif counter >= speed * len(message):
        done = True
        channel1.stop(

        )

    MOUSE_POS = pygame.mouse.get_pos()

    POSITIVE = Button(image=pygame.image.load("assets/Pos Rect.png"), pos=(115, 445), 
                            text_input=postext, font=font1, base_color="dark green", hovering_color="green")
    NEGATIVE = Button(image=pygame.image.load("assets/Pos Rect.png"), pos=(330, 445), 
                            text_input=negtext, font=font1, base_color="dark green", hovering_color="green") 

    for button in  [POSITIVE, NEGATIVE]:
            button.changeColor(MOUSE_POS)
            button.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and done:
                if  active_message < len(messages)-1:
                    active_message += 1
                    done = False
                    message = messages[active_message]
                    counter = 0

                    if active_message == len(messages)-1:
                        postext = postextoptions[state]
                        negtext = negtextoptions[state]

                elif active_message == len(messages)-1 and (nflag == 1 or pflag == 1):
                    pflag = 0
                    nflag = 0
                    state += 1
                    messages=story[state]
                    active_message = 0
                    done = False
                    message = messages[active_message]
                    counter = 0
            elif done:
                if active_message == len(messages)-1:
                    postext = postextoptions[state]
                    negtext = negtextoptions[state]


        if event.type == pygame.MOUSEBUTTONDOWN:
                if (POSITIVE.checkForInput(MOUSE_POS) or NEGATIVE.checkForInput(MOUSE_POS)) and active_message == len(messages)-1:
                    if POSITIVE.checkForInput(MOUSE_POS) and nflag != 1:
                        pflag = 1
                        messages = pos[state]
                        playerDecisions[state]=1
                    if NEGATIVE.checkForInput(MOUSE_POS) and pflag != 1:
                        nflag = 1
                        messages = neg[state]
                        playerDecisions[state]=0
                    active_message = 0
                    done = False
                    message = messages[active_message]
                    counter = 0
                    
        
    snip = font1.render(message[0:counter//speed], True, 'dark green')
    screen.blit(snip, (10, 390))
    pygame.display.flip()
pygame.quit()