import pygame as p
import math as m

# 초기화 및 기본설정
p.init()
background=p.display.set_mode((480,360))
p.display.set_caption('Swing&Run')
clock=p.time.Clock()

# 변수
gravity_on=True
swing_on=False
jump=False
ground=300
gravity_power=0.5
jump_power=-10
now_stage=None

# 스윙변수
point=None
r=None
angle=None
속도=0
가속도=0
중력가속도=0.003
공기저항=0.98
최대속도=0.2

# 기타 자료형
pressed_keys={p.K_a:False,p.K_d:False}
point=[0,0]
character_pos=p.Vector2(70,300)
overswing_speed=p.Vector2(0,0)

# 클래스 스테이지
class stage:
    def __init__(self):
        self.obstacles=[0,0]
        self.obstacles_red=[0,0]

# 스테이지1
stage_1=stage()
stage_1.obstacles=[
    p.Rect(100,270,100,30)
]
stage_1.obstacles_red=[
    p.Rect(200,270,100,30)
]
now_stage=stage_1


    


# 스윙 초기설정 함수
def swing_start():
    global point,r,angle,swing_on,gravity_on,속도,가속도
    gravity_on=False
    point=p.mouse.get_pos()
    r=m.dist(character_pos,point)
    angle=m.atan2(character_pos.x - point[0], character_pos.y - point[1])
    swing_on=True
    속도=0
    가속도=0

def colliding():
    closest_x=max(Rect.left,(min(character_pos.x,Rect.right)))
    closest_y=max(Rect.top,(min(character_pos.y,Rect.bottom)))
    distance=m.sqrt((character_pos.x-closest_x)**2+(character_pos.y-closest_y)**2)
    return distance<=15

def colliding_red():
    closest_x=max(Rect_red.left,(min(character_pos.x,Rect_red.right)))
    closest_y=max(Rect_red.top,(min(character_pos.y,Rect_red.bottom)))
    distance=m.sqrt((character_pos.x-closest_x)**2+(character_pos.y-closest_y)**2)
    return distance<=15

# 메인루프
play=True
while play:

     # 창종료 및 방향키 입력
    for event in p.event.get():
        if event.type == p.QUIT:
            play=False
        if event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1:
                swing_start()
        if event.type == p.KEYDOWN:
            if event.key in pressed_keys:
                pressed_keys[event.key]=True
            if event.key == p.K_w and character_pos.y==ground:
                overswing_speed[1]=jump_power
            if event.key == p.K_e:
                overswing_speed = p.Vector2(m.cos(angle), -m.sin(angle)) * 속도 * 100
                swing_on = False
                gravity_on = True
        if event.type == p.KEYUP:
            if event.key in pressed_keys:
                pressed_keys[event.key]=False

    # 중력적용중
    if gravity_on:

        # 좌우이동
        if pressed_keys[p.K_a]:
            character_pos.x-=5
        if pressed_keys[p.K_d]:
            character_pos.x+=5

        # 캐릭터 위치설정
        character_pos.x+=overswing_speed.x
        character_pos.y+=overswing_speed.y
        if character_pos.y<ground:
            overswing_speed[1]+=gravity_power
        else:
            character_pos.y=ground
            overswing_speed=p.Vector2(0,0)

    # 스윙중
    if swing_on:

        # 스윙중에 방향키 입력으로 속도 변화
        if pressed_keys[p.K_a]:
            속도-=0.003
        if pressed_keys[p.K_d]:
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
        character_pos.x=point[0]+r*m.sin(angle)
        character_pos.y=point[1]+r*m.cos(angle)

    # 지정된 위치에 그리기
    background.fill((0,0,0))
    
    for Rect in now_stage.obstacles:
        p.draw.rect(background,(100,100,100),Rect)
        if colliding():
            print('충돌')
    for Rect_red in now_stage.obstacles_red:
        p.draw.rect(background,(255,0,0),Rect_red)
        if colliding_red():
            print('빨강충돌')
    p.draw.circle(background,(255,255,255),(int(character_pos.x),int(character_pos.y)),15)
    
        
    if swing_on:
        p.draw.circle(background,(255,255,255),point,7)
        p.draw.line(background,(255,255,255),point,(int(character_pos.x),int(character_pos.y)),3)
    p.display.update()

    

    # 프레임 유지
    clock.tick(60)

p.quit()