# _*_ coding=utf-8 _*_
import pygame


"""
    英雄飞机
"""
class HeroPlane(pygame.sprite.Sprite):
    # 初始化
    def __init__(self,bg_size,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image1 = pygame.image.load("./source/image/hero1.png") # 加载飞机图片
        self.image2 = pygame.image.load("./source/image/hero2.png")  # 加载飞机图片
        self.rect = self.image1.get_rect() #获取飞机图片尺寸
        self.width,self.height = bg_size[0],bg_size[1] # 背景尺寸
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, (self.height - self.rect.height - 60) # 初始化飞机位置
        self.speed = 3 # 设置飞机速度
        self.switch_image = False # 控制飞机图片切换的标志位（用以模拟发动机喷火效果）
        self.mask = pygame.mask.from_surface(self.image1) # 获取飞机图像的掩膜
        self.active = True
        self.invincible = False  # 飞机初始化时有两秒的无敌时间
        self.destroy_images = [pygame.image.load("./source/image/hero_blowup_n1.png"),
                                pygame.image.load("./source/image/hero_blowup_n2.png"),
                                pygame.image.load("./source/image/hero_blowup_n3.png"),
                                pygame.image.load("./source/image/hero_blowup_n4.png")]  # 加载飞机损毁图片

    # 向上移动
    def move_up(self):
        if self.rect.top > 0: # 向上移动没有越出边界
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    # 向下移动
    def move_down(self):
        if self.rect.bottom < self.height - 10:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 10

    # 向左移动
    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    # 向右移动
    def move_right(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    # 显示飞机
    def display(self):
        if self.switch_image:
            self.screen.blit(self.image1, self.rect)  # 绘制我方飞机的两种不同的形式
        else:
            self.screen.blit(self.image2, self.rect)

    # 重置
    def reset(self):
        # 初始化飞机
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, (self.height - self.rect.height - 60)
        # 重置飞机的存活状态
        self.active = True
        # 重生两秒无敌
        self.invincible = True
