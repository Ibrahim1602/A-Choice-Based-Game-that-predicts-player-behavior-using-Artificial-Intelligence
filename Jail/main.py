import pygame
from button import Button
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

pygame.init()
pygame.mixer.init()
beep = pygame.mixer.Sound('sfx/beep.ogg')
channel1 = pygame.mixer.Channel(0)
font1 = pygame.font.Font('font/digital-7.ttf',24)
screen = pygame.display.set_mode([800,500])
timer = pygame.time.Clock()

postext = ''
negtext = ''
state = 0
postextoptions = ['Tell her','I don\'t know','Attack guards','Look for brown objects']
negtextoptions = ['Don\'t tell her','Respond differently','Ask them to stop','Make something up']
# Choice 1: 1 = Extrovert / 0 = Introvert
# Choice 2: 1 = Judging / 0 = Percieving
# Choice 3: 1 = Feeling / 0 = Thinking


story = [['Two guards drag an unconscious person across a dark prison hallway...','Warden: \"Lock him up with the rest of the non workers.\"','An elderly female prisoner looks at the unconcious person who is bleeding.','Old woman: \"Oh poor boy... what have they done to you?\"', 'The guards slam the gate shut.','The old woman turns to the wounded prisoner who had started moving.','"You stay still, young man.", The old woman says to the prisoner.', '"Why did they do this to you?"       [Note: You are playing as the Prisoner]'],
         ['Old woman: \"It\'s okay.. You should really take some rest. Atleast for now.\"','You rest your head on the concrete floor and slowly fall asleep.','Many hours pass by...','Old woman: "Wake up!, the guards will be here soon!"','"I need you to do me a favor", She says hiding from the camera\'s sight.','"Hide this piece of paper in your bandages"','Old woman: "If they ask, just say you don\'t know where it is. Ok?"','You: "But, why?"','"That piece of paper is actually-"', 'The gates open with a loud metallic roar and guards come through it.','The Warden of the prison begins to speak.','Warden: "Okay listen up everyone!"','Warden: "If any of you lie to me, you will regret it."',"Warden: \"How about we start with you?\", The warden points towards you.","Where is it?"],
         ['Warden: "Listen everyone ! We\'re looking for a brown piece of paper!"','"If any of you see it, don\'t look at it, don\'t read it..."','"Just hand it over to us."','If you fail to cooperate, you WILL be punished','One of the guards whispers something in the warden\'s ear' ,'He then points to the old woman','The warden orders the guards to arrest her.','Old woman: "I didn\'t do anything."','A guard slaps the old woman.','Guard: "I saw it in your hand, you old hag!"'],
         ['You: "Leave her alone, she\'s innocent"','Warden: "Okay, then what did the guard see in her hand?"'],
         ['Guard: "How did you know that?"','Warden: "We\'ll find out... Take him back to the factory"','The guards grab you by your arms', 'and push you along the hallway towards the factory.','You notice a light blinking from the warden\'s neck','The guards and the warden were humanoid robots of the german army.','The army had invaded poland and turned the civilians into prisoners of war','They set up various labour camps across poland and this was one of them','The camp was controlled by a robot called Prime Command or PrimeCom for short','It monitored everyone through cameras and controlled all the robot guards from its room.','The guards take you to a different factory and throw you at the floor']]

pos = [['You: "They took my brother away."', '"They started beating me when I asked them where they were taking him."','"I mean, he\'s just a little boy. What did he ever do to anybody?"','"This war has taken everything from me..."','Old woman: "I know it must be really tough for you."','You: "I should go and look for him."'],
       ['You: "I don\'t know."',"Warden: \"How did you know what I was talking about?\"","You: \"I- I just- I don\'t know...\"",'Warden: \"I\'ll be keeping an eye on you.\"'],
       ['You PUSH the guard away.','Two other guards grab you and the guard you pushed walks towards you.','He starts punching you in your wound and the bandage loosens a little.'],
       ['You look around the room and see a brown handkerchief','You: "Maybe it was this napkin."','The warden looks towards the guard and the guard shrugs his shoulders.']]

neg = [['You: "It was nothing."','Old woman: "Nothing?"','You: "I don\'t want to talk about it."'],
       ['You: "What are you talking about?"','Warden: "Fair enough."'],
       ['You: "Hey stop it!"'],
       ['You: "Maybe it was a handkerchief"', 'Warden says to the old woman: "Show us your handkerchief"','The old woman picks up a handkerchief which is actually brown']]

playerDecisions = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

messages = story[state]
snip = font1.render('', True, 'dark green')
counter = 0
speed = 1
b = 0
pflag = 0
nflag = 0
sflag = 1
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

    POSITIVE = Button(image=pygame.image.load("assets/Pos Rect.png"), pos=(135, 445), 
                            text_input=postext, font=font1, base_color="dark green", hovering_color="green")
    NEGATIVE = Button(image=pygame.image.load("assets/Pos Rect.png"), pos=(390, 445), 
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
                if active_message == len(messages)-1 and sflag == 1:
                    postext = postextoptions[state]
                    negtext = negtextoptions[state]


        if event.type == pygame.MOUSEBUTTONDOWN:
                if (POSITIVE.checkForInput(MOUSE_POS) or NEGATIVE.checkForInput(MOUSE_POS)) and active_message == len(messages)-1:
                    if POSITIVE.checkForInput(MOUSE_POS) and nflag != 1:
                        postext = ''
                        negtext = ''
                        pflag = 1
                        sflag = 0
                        messages = pos[state]
                        playerDecisions[state]=1
                    if NEGATIVE.checkForInput(MOUSE_POS) and pflag != 1:
                        postext = ''
                        negtext = ''
                        nflag = 1
                        sflag = 0
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