# _*_ coding=utf-8 _*_
import pygame
import random

"""
    创建敌机
"""
class SmallEnemy(pygame.sprite.Sprite):
    """
        小型敌机
    """
    # 初始化
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./source/image/enemy1.png")  # 加载敌机图片
        self.rect = self.image.get_rect()  # 获取飞机图片尺寸
        self.width, self.height = bg_size[0], bg_size[1]  # 背景尺寸
        self.speed = 3 # 设置飞机速度
        self.mask = pygame.mask.from_surface(self.image)  # 获取飞机图像的掩膜
        self.rect.left,self.rect.top = random.randint(0,self.width-self.rect.width),random.randint(-5 * self.rect.height, -5) # 保证敌机不会在游戏开始立即出现
        self.active = True
        self.destroy_images = [pygame.image.load("./source/image/enemy1_down1.png"),
                                pygame.image.load("./source/image/enemy1_down2.png"),
                                pygame.image.load("./source/image/enemy1_down3.png"),
                                pygame.image.load("./source/image/enemy1_down4.png")]  # 加载飞机损毁图片

    # 移动
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    # 位置重置
    def reset(self):  # 当敌机向下移动出屏幕时
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width),random.randint(-5 * self.rect.height, 0)
        self.active = True


class MidEnemy(pygame.sprite.Sprite):
    """
       中型敌机
    """
    life = 5 # 初始血量值
    # 初始化
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./source/image/enemy2.png")  # 加载敌机图片
        self.image_hit = pygame.image.load("./source/image/enemy2_hit.png")  # 加载中型敌机中弹图片
        self.rect = self.image.get_rect()  # 获取飞机图片尺寸
        self.width, self.height = bg_size[0], bg_size[1]  # 背景尺寸
        self.speed = 2  # 设置飞机速度
        self.mask = pygame.mask.from_surface(self.image)  # 获取飞机图像的掩膜
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(
            -10 * self.rect.height, -self.rect.height)  # 保证敌机不会在游戏开始立即出现
        self.active = True
        self.life = MidEnemy.life # 设置初始血量
        self.hit = False  # 是否被击中标志位
        self.destroy_images = [pygame.image.load("./source/image/enemy2_down1.png"),
                               pygame.image.load("./source/image/enemy2_down2.png"),
                               pygame.image.load("./source/image/enemy2_down3.png"),
                               pygame.image.load("./source/image/enemy2_down4.png")]  # 加载飞机损毁图片

    # 移动
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    # 位置和重置
    def reset(self):  # 当敌机向下移动出屏幕时
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(
            -10 * self.rect.height, self.rect.height)
        self.active = True
        self.life = MidEnemy.life
        self.hit = False  # 是否被击中标志位


class BigEnemy(pygame.sprite.Sprite):
    """
        大型敌机
    """
    life = 15  # 初始血量值
    # 初始化
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("./source/image/enemy3_n1.png")  # 加载敌机图片
        self.image2 = pygame.image.load("./source/image/enemy3_n2.png")
        self.image_hit = pygame.image.load("./source/image/enemy3_hit.png")  # 加载大型敌机中弹图片
        self.rect = self.image1.get_rect()  # 获取飞机图片尺寸
        self.width, self.height = bg_size[0], bg_size[1]  # 背景尺寸
        self.speed = 1 # 设置飞机速度
        self.mask = pygame.mask.from_surface(self.image1)  # 获取飞机图像的掩膜
        self.switch_image = False
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(
            -15 * self.rect.height, -5 * self.rect.height)  # 保证敌机不会在游戏开始立即出现
        self.active = True
        self.life = BigEnemy.life  # 设置初始血量
        self.hit = False # 是否被击中标志位
        self.destroy_images = [pygame.image.load("./source/image/enemy3_down1.png"),
                               pygame.image.load("./source/image/enemy3_down2.png"),
                               pygame.image.load("./source/image/enemy3_down3.png"),
                               pygame.image.load("./source/image/enemy3_down4.png"),
                               pygame.image.load("./source/image/enemy3_down5.png"),
                               pygame.image.load("./source/image/enemy3_down6.png")]  # 加载飞机损毁图片

    # 移动
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    # 位置和血量重置
    def reset(self):  # 当敌机向下移动出屏幕时
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), random.randint(
            -15 * self.rect.height, -5 * self.rect.height)
        self.active = True
        self.life = BigEnemy.life
        self.hit = False  # 是否被击中标志位