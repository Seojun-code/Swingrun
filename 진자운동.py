import pygame as p
import math as m

# 초기화 및 기본설정
p.init()
background=p.display.set_mode((480,360))
p.display.set_caption('진자운동')
clock=p.time.Clock()

# 변수설정
center=[background.get_size()[0]//2,background.get_size()[1]//2]
r=100
angle=m.radians(0)
pressed_keys={p.K_LEFT:False,p.K_RIGHT:False}
속도=0
가속도=0
중력가속도=0.005
공기저항=0.98
최대속도=0.2

play=True
while play:
    # 창종료 및 방향키 입력
    for event in p.event.get():
        if event.type == p.QUIT:
            play=False
        if event.type == p.KEYDOWN:
            if event.key in pressed_keys:
                pressed_keys[event.key]=True
        if event.type == p.KEYUP:
            if event.key in pressed_keys:
                pressed_keys[event.key]=False
    if pressed_keys[p.K_LEFT]:
        속도-=0.003
    if pressed_keys[p.K_RIGHT]:
        속도+=0.003

    # 물리엔진 계산
    가속도=-중력가속도*m.sin(angle)
    속도+=가속도
    if 속도>최대속도:
        속도=최대속도
    elif 속도<-최대속도:
        속도=-최대속도
    angle+=속도
    속도*=공기저항
    x=center[0]+r*m.sin(angle)
    y=center[1]+r*m.cos(angle)
    background.fill((0,200,100))

    # 그리기
    p.draw.circle(background,(0,0,0),center,7)
    p.draw.line(background,(0,0,0),center,(int(x),int(y)),3)
    p.draw.circle(background,(255,255,255),(int(x),int(y)),15)
    p.display.update()

    # 초당 프레임 유지
    clock.tick(60)

    
p.quit()