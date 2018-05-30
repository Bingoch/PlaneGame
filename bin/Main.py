# _*_ coding=utf-8 _*_
import os
import sys
from random import choice

from pygame.locals import *
import traceback
from bin.Enemy import *
from bin.HeroPlane import HeroPlane
from bin.Bullet import *
from bin.Supply import *

"""
    资源的初始化
"""
# ==========初始化=========
pygame.init()
pygame.mixer.init() # 混音的初始化
bg_size = width,height = 480,800 # 背景大小
screen = pygame.display.set_mode(bg_size) # 设置主界面
pygame.display.set_caption("PlaneShutGame") #设置主界面标题
background = pygame.image.load("./source/image/background.png") #加载背景图片
clock = pygame.time.Clock()  # 设置帧率
delay = 60 # 设置延时

# ==========载入游戏音乐====================
pygame.mixer.music.load("./source/sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("./source/sound/bullet.wav")
bullet_sound.set_volume(0.2)
big_enemy_flying_sound = pygame.mixer.Sound("./source/sound/big_spaceship_flying.wav")
big_enemy_flying_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("./source/sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("./source/sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("./source/sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("./source/sound/game_over.wav")
me_down_sound.set_volume(0.2)
button_down_sound = pygame.mixer.Sound("./source/sound/button.wav")
button_down_sound.set_volume(0.2)
level_up_sound = pygame.mixer.Sound("./source/sound/achievement.wav")
level_up_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("./source/sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("./source/sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("./source/sound/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)


# 生成小型飞机
def add_small_enemies(small_enemys,enemys,num):
    for i in range(num):
        small_enemy = SmallEnemy(bg_size)
        small_enemys.add(small_enemy)
        enemys.add(small_enemy)


# 生成中型敌机
def add_mid_enemies(mid_enemys, enemys, num):
    for i in range(num):
        mid_enemy = MidEnemy(bg_size)
        mid_enemys.add(mid_enemy)
        enemys.add(mid_enemy)


# 生成大型敌机
def add_big_enemies(big_enemys, enemys, num):
    for i in range(num):
        big_enemy = BigEnemy(bg_size)
        big_enemys.add(big_enemy)
        enemys.add(big_enemy)

def increase_speed(enemys,increase):
    for each in enemys:
        each.speed += increase

def main():
    score = 0  # 统计用户得分
    score_font = pygame.font.Font(os.path.join('.\\source\\font', "TORK____.ttf"), 30)  # 定义分数字体
    game_over_font = pygame.font.Font(os.path.join('.\\source\\font', "TORK____.ttf"), 60)
    color_white = (255, 255, 255) # 白色
    color_black = (0,0,0)

    is_double_bullet = False  # 是否强化火力标志位

    level = 1 # 难度等级
    bomb_num = 3  # 初始为三个炸弹
    bomb_front = score_font
    bomb_image = pygame.image.load("./source/image/bomb.png")  # 加载全屏炸弹图标
    bomb_rect = bomb_image.get_rect()

    # ====================飞机损毁图像索引====================
    enemy1_destroy_index = 0
    enemy2_destroy_index = 0
    enemy3_destroy_index = 0
    heroPlane_destroy_index = 0

    # 加载游戏界面
    pygame.mixer.music.play(-1) # 循环播放音乐
    hero_plane = HeroPlane(bg_size, screen)

    enemies = pygame.sprite.Group()  # 敌方飞机组
    small_enemies = pygame.sprite.Group()  # 敌方小型飞机组
    add_small_enemies(small_enemies, enemies, 3)  # 生成若干敌方小型飞机
    mid_enemies = pygame.sprite.Group()  # 敌方中型飞机组
    add_mid_enemies(mid_enemies, enemies, 1)  # 生成若干敌方中型飞机
    big_enemies = pygame.sprite.Group()  # 敌方大型飞机组
    add_big_enemies(big_enemies, enemies, 1)  # 生成若干敌方大型飞机

    # ====================生成普通子弹====================
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 9  # 定义子弹实例化个数
    for i in range(bullet1_num):
        bullet1.append(GeneralBullet(hero_plane.rect.midtop))

    # ===================强化子弹=========================
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 20
    for i in range(bullet2_num//2):
        bullet2.append(DoubleBullet((hero_plane.rect.centerx - 30,hero_plane.rect.centery)))
        bullet2.append(DoubleBullet((hero_plane.rect.centerx + 30, hero_plane.rect.centery)))

    # ====================实例化补给包====================
    bullet_supply = BulletSupply(bg_size)
    bomb_supply = BombSupply(bg_size)
    supply_timer = USEREVENT  # 补给包发放定时器
    pygame.time.set_timer(supply_timer, 30 * 1000)  # 定义每30秒发放一次补给包
    double_bullet_timer = USEREVENT + 1  # 强化火力持续时间定时器

    # ====================初始化飞机生命值=================
    life_image = pygame.image.load("./source/image/life.png")
    life_rect = life_image.get_rect()
    life_num = 3
    invincible_timer = USEREVENT + 2  # 重生无敌时间定时器

    # ====================游戏暂停=======================
    paused = False  # 标志是否暂停游戏
    pause_nor_image = pygame.image.load("./source/image/game_pause_nor.png")  # 加载暂停相关按钮
    pause_pressed_image = pygame.image.load("./source/image/game_pause_pressed.png")
    resume_nor_image = pygame.image.load("./source/image/game_resume_nor.png")
    resume_pressed_image = pygame.image.load("./source/image/game_resume_pressed.png")
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 36  # 设置暂停按钮位置
    paused_image = pause_nor_image  # 设置默认显示的暂停按钮

    # ==================游戏结束==================
    gameover_image = pygame.image.load("./source/image/game_over.png")  # 游戏结束背景图片
    gameover_rect = gameover_image.get_rect()
    flag_recorded = False
    game_over_flag = False

    while True:
        if life_num and (not paused):
            clock.tick(60)  # 设置帧数为60
            screen.blit(background, (0, 0))  # 加载主背景
            score_text = score_font.render("Score : %s" % str(score), True, color_white)
            screen.blit(score_text, (10, 10))  # 加载分数
            for i in range(life_num):
                screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, 10))

            bomb_text = bomb_front.render("x %d" % bomb_num, True, color_black)
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 10 - bomb_text_rect.height))

            # ====================定义难度递进操作====================
            if level == 1 and score > 2000:  # 如果达到第二难度等级，则增加3架小型敌机，2架中型敌机，1架大型敌机,并提升小型敌机速度
                level = 2
                level_up_sound.play()
                add_small_enemies(small_enemies,enemies,3)
                add_mid_enemies(mid_enemies,enemies,2)
                add_big_enemies(big_enemies,enemies,1)
                increase_speed(small_enemies,1)
            elif level == 2 and score > 6000:  # 如果达到第三难度等级
                level = 3
                level_up_sound.play()
                add_small_enemies(small_enemies, enemies, 3)
                add_mid_enemies(mid_enemies, enemies, 2)
                add_big_enemies(big_enemies, enemies, 1)
                increase_speed(small_enemies, 1)
                increase_speed(mid_enemies,1)
            elif level == 3 and score > 12000:  # 如果达到第四难度等级
                level = 4
                level_up_sound.play()
                add_small_enemies(small_enemies, enemies, 3)
                add_mid_enemies(mid_enemies, enemies, 2)
                add_big_enemies(big_enemies, enemies, 1)
                increase_speed(small_enemies, 1)
                increase_speed(mid_enemies,1)
                increase_speed(big_enemies,1)

            global delay
            if not delay % 3:
                hero_plane.switch_image = not hero_plane.switch_image # 更换标志位,使飞机在两张图片之间切换
            hero_plane.display() # 加载英雄飞机

            if not (delay % 10):  # 每十帧发射一颗移动的子弹
                bullet_sound.play()
                if not is_double_bullet:
                    bullets = bullet1
                    bullets[bullet1_index].reset(hero_plane.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num
                else:
                    bullets = bullet2
                    bullets[bullet2_index].reset((hero_plane.rect.centerx - 30,hero_plane.rect.centery))
                    bullets[bullet2_index + 1].reset((hero_plane.rect.centerx + 30,hero_plane.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num

            for b in bullets:
                if b.active:  # 只有激活的子弹才可能击中敌机
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemies_hit:  # 如果子弹击中敌机
                        b.active = False  # 子弹损毁
                        for e in enemies_hit:
                            if e in mid_enemies or e in big_enemies: # 中型机和大型机被击中血量减一
                                e.life -= 1
                                e.hit = True
                                if e.life == 0:
                                    e.active = False  # 敌机损毁
                            else:
                                e.active = False # 小型机被击中直接损毁

            for each in small_enemies:  # 加载小型敌机并自动移动
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if enemy1_destroy_index == 0:
                        enemy1_down_sound.play()
                    if not (delay % 3):
                        screen.blit(each.destroy_images[enemy1_destroy_index], each.rect)
                        enemy1_destroy_index = (enemy1_destroy_index + 1) % 4
                        if enemy1_destroy_index == 0:
                            score += 50
                            each.reset()

            for each in mid_enemies:  # 加载中型敌机并自动移动
                if each.active:
                    each.move()
                    if not each.hit:
                        screen.blit(each.image, each.rect)
                    else:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False

                else:
                    if enemy2_destroy_index == 0:
                        enemy2_down_sound.play()
                    if not (delay % 3):
                        screen.blit(each.destroy_images[enemy2_destroy_index], each.rect)
                        enemy2_destroy_index = (enemy2_destroy_index + 1) % 4
                        if enemy2_destroy_index == 0:
                            score += 100
                            each.reset()

            for each in big_enemies:  # 加载大型敌机并自动移动
                if each.active:
                    each.move()
                    if not delay % 3:
                        each.switch_image = not each.switch_image  # 更换标志位,使飞机在两张图片之间切换
                    if each.switch_image:
                        if not each.hit:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image_hit, each.rect)
                            each.hit = False
                    else:
                        screen.blit(each.image2, each.rect)
                    if each.rect.bottom == -50: # 大型敌机音效
                        big_enemy_flying_sound.play(-1)
                else:
                    big_enemy_flying_sound.stop()
                    if enemy3_destroy_index == 0:
                        enemy3_down_sound.play()  # 播放飞机撞毁音效
                    if not (delay % 3):  # 每三帧播放一张损毁图片
                        screen.blit(each.destroy_images[enemy3_destroy_index], each.rect)
                        enemy3_destroy_index = (enemy3_destroy_index + 1) % 6  # 大型敌机有六张损毁图片
                        if enemy3_destroy_index == 0:  # 如果损毁图片播放完毕，则重置飞机属性
                            score += 150
                            each.reset()

            # 英雄飞机损毁
            if hero_plane.active:  # 绘制我方飞机的两种不同的形式
                plane_hit = pygame.sprite.spritecollide(hero_plane, enemies, False, pygame.sprite.collide_mask)
                if plane_hit and not hero_plane.invincible:  # 如果碰撞检测返回的列表非空，则说明已发生碰撞
                    hero_plane.active = False
                    for e in plane_hit:
                        e.active = False  # 敌机损毁
            else:
                if not (delay % 11):
                    screen.blit(hero_plane.destroy_images[heroPlane_destroy_index], hero_plane.rect)
                    heroPlane_destroy_index = (heroPlane_destroy_index + 1) % 4 # 模4取余
                    if heroPlane_destroy_index == 0:
                        me_down_sound.play() # 播放音效
                        hero_plane.reset()
                        life_num -= 1
                        pygame.time.set_timer(invincible_timer, 2 * 1000)

            # 补给
            if bomb_supply.active:
                screen.blit(bomb_supply.image,bomb_supply.rect)
                bomb_supply.move()
                if pygame.sprite.collide_mask(bomb_supply,hero_plane):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            # 弹药
            if bullet_supply.active:
                screen.blit(bullet_supply.image,bullet_supply.rect)
                bullet_supply.move()
                if pygame.sprite.collide_mask(bullet_supply,hero_plane):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    bullet_supply.active = False
                    pygame.time.set_timer(double_bullet_timer,15*1000) # 开启定时器

            key_pressed = pygame.key.get_pressed()  # 获得用户所有的键盘输入序列
            if key_pressed[K_w] or key_pressed[K_UP]:  # 如果用户通过键盘发出“向上”的指令,其他类似
                hero_plane.move_up()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                hero_plane.move_down()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                hero_plane.move_left()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                hero_plane.move_right()

            if delay == 0:
                delay = 60
            delay -= 1

            pygame.display.flip()

        elif life_num == 0:
            screen.blit(gameover_image, gameover_rect)
            pygame.mixer.music.stop()  # 关闭背景音乐
            pygame.mixer.stop()  # 关闭所有音效
            pygame.time.set_timer(supply_timer, 0)  # 关闭补给机制
            if not flag_recorded:

                with open("./source/score_record.txt", "r") as f:
                    record_score = int(f.read())
                if score > record_score:  # 如果玩家得分大于历史最高分，则将当前分数存档
                    with open("./source/score_record.txt", "w") as f:
                        f.write(str(score))
                flag_recorded = True
                game_over_flag = True
            record_score_text = score_font.render("%d" % record_score, True, color_white)
            screen.blit(record_score_text, (150, 34))
            game_over_score_text = score_font.render("%d" % score, True, color_white)
            screen.blit(game_over_score_text, (195, 370))
            game_over_text = game_over_font.render("GAME OVER",True,color_white)
            screen.blit(game_over_text,(50,110))



        for event in pygame.event.get():  # 响应事件
            if event.type == QUIT:  # 关闭
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  # 如果检测到用户按下空格键
                    if bomb_num:  # 如果炸弹数量大于零，则引爆一颗超级炸弹
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:  # 屏幕上的所有敌机均销毁
                                each.active = False
            elif event.type == supply_timer:
                if choice([False, True]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == double_bullet_timer:
                is_double_bullet = False
                pygame.time.set_timer(double_bullet_timer, 0)
            elif event.type == invincible_timer:
                hero_plane.invincible = False
                pygame.time.set_timer(invincible_timer, 0)
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):  # 如果鼠标悬停在按钮区域
                    if paused:  # r如果当前的状态是暂停
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == MOUSEBUTTONDOWN:
                if not game_over_flag:
                    button_down_sound.play()
                    if event.button == 1 and paused_rect.collidepoint(event.pos):  # 如果检测到用户在指定按钮区域按下鼠标左键
                        paused = not paused
                        if paused:  # 如果当前的状态是暂停
                            paused_image = resume_pressed_image
                            pygame.time.set_timer(supply_timer, 0)  # 关闭补给机制以及所有音效
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()

                        else:
                            paused_image = pause_pressed_image
                            pygame.time.set_timer(supply_timer, 30 * 1000)  # 开启补给机制以及所有音效
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()
            else:
                break
        screen.blit(paused_image, paused_rect)
        # 页面刷新
        pygame.display.flip()

if __name__ == '__main__':
    """
        加载飞机大战的主类
    """
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()