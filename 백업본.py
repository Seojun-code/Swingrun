import pygame as p
import math as m

# 초기화 및 기본설정
p.init()
background=p.display.set_mode((480,360))
p.display.set_caption('Swing&Run')
fps=p.time.Clock()

# 변수
gravity_on=True
swing_on=False
ground=300
gravity_power=0.5
jump_power=-10
now_stage=None
start_time=p.time.get_ticks()

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
    def __init__(self,name):
        self.name=name
        self.obstacles=[0,0]
        self.obstacles_red=[0,0]
        self.start_point=None
        self.end_point=None
        self.next=None
    def stage_complete(self):
        global now_stage,overswing_speed,character_pos
        now_stage=self.next
        overswing_speed=p.Vector2(0,0)
        character_pos=p.Vector2(self.next.start_point.center)

# 스테이지1
stage_1=stage('stage 1')
stage_1.obstacles=[
    p.Rect(40,200,100,30)
]
stage_1.obstacles_red=[
    p.Rect(0,300,480,60)
]
stage_1.start_point=p.Rect(70,100,40,40)
stage_1.end_point=p.Rect(400,150,40,40)

# 스테이지2
stage_2=stage('stage 2')
stage_2.obstacles=[
    p.Rect(40,200,100,30)
]
stage_2.obstacles_red=[
    p.Rect(0,300,480,60),
    p.Rect(220,100,40,270)
]
stage_2.start_point=p.Rect(70,100,40,40)
stage_2.end_point=p.Rect(400,260,40,40)

# 스테이지3
stage_3=stage('stage 3')
stage_3.obstacles=[
    p.Rect(30,120,100,30),
    p.Rect(30,270,150,30)
]
stage_3.obstacles_red=[
    p.Rect(0,150,360,30),
    p.Rect(0,300,480,60)
]
stage_3.start_point=p.Rect(70,10,40,40)
stage_3.end_point=p.Rect(70,200,40,40)

# 스테이지4
stage_4=stage('stage 4')
stage_4.obstacles=[
    p.Rect(0,200,100,30),
    p.Rect(360,140,100,30)
]
stage_4.obstacles_red=[
    p.Rect(0,300,480,60),
    p.Rect(160,130,40,240),
    p.Rect(280,0,40,170)
]
stage_4.start_point=p.Rect(30,130,40,40)
stage_4.end_point=p.Rect(390,70,40,40)

# 스테이지5
stage_5=stage('stage 5')
stage_5.obstacles=[
    p.Rect(0,270,100,30),
    p.Rect(360,140,100,30)
]
stage_5.obstacles_red=[
    p.Rect(0,300,480,60),
    p.Rect(150,130,50,50),
    p.Rect(0,0,200,130),
    p.Rect(290,130,40,170)
]
stage_5.start_point=p.Rect(30,220,40,40)
stage_5.end_point=p.Rect(390,70,40,40)

# 스테이지6
stage_6=stage('stage 6')
stage_6.obstacles=[
    p.Rect(0,270,100,30),
    p.Rect(360,270,100,30)
]
stage_6.obstacles_red=[
    p.Rect(0,300,480,60),
    p.Rect(100,100,30,240),
    p.Rect(100,80,270,30),
    p.Rect(210,180,270,30)
]
stage_6.start_point=p.Rect(30,220,40,40)
stage_6.end_point=p.Rect(390,220,40,40)

# 스테이지 순서설정
stage_1.next=stage_2
stage_2.next=stage_3
stage_3.next=stage_4
stage_4.next=stage_5
stage_5.next=stage_6
stage_6.next=None

# 1스테이지부터 시작
now_stage=stage_1
character_pos=p.Vector2(stage_1.start_point.center)

# 텍스트 추가a
Font=p.font.Font(None,50)
message=Font.render(now_stage.name,True,(255,255,255))
message_location=message.get_rect(center=(background.get_width()//2,40))
time=p.time.get_ticks()
timer=Font.render(str(time//1000),True,(255,255,255))
timer_location=timer.get_rect(center=(400,340))

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

# 스윙 끝내기 함수
def swing_end():
    global overswing_speed,swing_on,gravity_on
    if swing_on==True:
        overswing_speed = p.Vector2(m.cos(angle), -m.sin(angle)) * 속도 * 100
        swing_on = False
        gravity_on = True

# 물체 충돌 함수
def colliding(rect):
    closest_x=max(rect.left,(min(character_pos.x,rect.right)))
    closest_y=max(rect.top,(min(character_pos.y,rect.bottom)))
    distance=m.sqrt((character_pos.x-closest_x)**2+(character_pos.y-closest_y)**2)
    return distance<=15

# 게임리셋
def game_reset():
    global point,r,angle,속도,가속도,overswing_speed,now_stage,character_pos,start_time,swing_on,gravity_on,ground,pressed_keys
    point=None
    r=None
    angle=None
    속도=0
    가속도=0
    overswing_speed=p.Vector2(0,0)
    now_stage=stage_1
    character_pos=p.Vector2(stage_1.start_point.center)
    start_time=p.time.get_ticks()
    swing_on=False
    gravity_on=True
    ground=300
    pressed_keys={p.K_a:False,p.K_d:False}

# 메인루프
play=True
while True:
    while play:

        # 창종료 및 방향키 입력
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    swing_start()
            if event.type == p.KEYDOWN:
                if event.key in pressed_keys:
                    pressed_keys[event.key]=True
                if event.key == p.K_w and character_pos.y==ground:
                    overswing_speed[1]=jump_power
                if event.key == p.K_s:
                    swing_end()
                if event.key == p.K_r:
                    game_reset()
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

        # 벽뚫 방지
        if character_pos.x+15>480:
            character_pos.x=480-15
            swing_end()
        if character_pos.x-15<0:
            character_pos.x=0+15
            swing_end()
        if character_pos.y-15<0:
            character_pos.y=0+15
            swing_end()

        # 스테이지 클리어
        if colliding(now_stage.end_point):
            if now_stage.next==None:
                swing_end()
                play=False
            else:
                swing_end()
                now_stage.stage_complete()

        # 스테이지 텍스트 변경
        message=Font.render(now_stage.name,True,(255,255,255))

        # 시간추가
        time=p.time.get_ticks()-start_time
        timer=Font.render(str(time//1000),True,(255,255,255))

        # 지정된 위치에 그리기
        background.fill((0,0,0))
        
        for Rect in now_stage.obstacles:
            p.draw.rect(background,(100,100,100),Rect)
        for Rect in now_stage.obstacles:
            if colliding(Rect):
                if Rect.top-character_pos.y>=0:
                    swing_end()
                    ground=Rect.top-15
                    break
        else:
            ground=300 #이게 되네 역시 갓 GPT 갓 for-else문
                
        for Rect_red in now_stage.obstacles_red:
            p.draw.rect(background,(255,0,0),Rect_red)
            if colliding(Rect_red):
                swing_end()
                overswing_speed=p.Vector2(0,0)
                character_pos=p.Vector2(now_stage.start_point.center)

        p.draw.rect(background,(0,0,255),now_stage.end_point)
        p.draw.rect(background,(240,240,255),now_stage.start_point)
        p.draw.circle(background,(255,255,255),(int(character_pos.x),int(character_pos.y)),15)
        
        if swing_on:
            p.draw.circle(background,(255,255,255),point,7)
            p.draw.line(background,(255,255,255),point,(int(character_pos.x),int(character_pos.y)),3)

        background.blit(message,message_location)
        background.blit(timer,timer_location)
        p.display.update()

        # 프레임 유지
        fps.tick(60)

    # 클리어메시지
    background.fill((0,0,0))
    clear_message_1=Font.render('clear!',True,(255,255,255))
    clear_message_2=Font.render(f'your record is {(time)//1000} second',True,(255,255,255))
    clear_message_location_1=clear_message_1.get_rect(center=(background.get_width()//2,150))
    clear_message_location_2=clear_message_2.get_rect(center=(background.get_width()//2,200))
    background.blit(clear_message_1,clear_message_location_1)
    background.blit(clear_message_2,clear_message_location_2)
    p.display.update()

    # 게임종료및 재시작
    while not play:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_r:
                    game_reset()
                    play=True
                    start_time=p.time.get_ticks()