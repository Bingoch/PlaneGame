# _*_ coding=utf-8 _*_
import pygame

"""
    定义子弹类
"""
class GeneralBullet(pygame.sprite.Sprite):
    # 初始化
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./source/image/bullet1.png") # 加载图片
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position # 子弹位置
        self.speed = 8
        self.active = True
        self.position =position
        self.mask = pygame.mask.from_surface(self.image)

    # 移动
    def move(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.active = False

    # 位置重置
    def reset(self,position):
        self.rect.left, self.rect.top = position
        self.active = True

class DoubleBullet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./source/image/bullet2.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 12
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < 0:
            self.active = False
        else:
            self.rect.top -= self.speed

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True