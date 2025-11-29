# patterns/pattern_star.py
# Python code, uploaded by Giteesome, 2025-11-29
# A Mimic Program Manager for Drone-Light-Show Items , beta v0.9
# tested pass on Windows 11 platform
# work with drone-light-show-main.py and other code pieces in the bundle

import pygame
import math
import random


class PatternStar:
    """星星图案"""

    def __init__(self, width, height, debug_mode=False):
        self.width = width
        self.height = height
        self.debug_mode = debug_mode
        self.is_first_call = True
        self.frame_count = 0
        self.running = True

        # 创建绘制表面
        if self.debug_mode:
            self.buffer_surface = pygame.Surface((width // 2, height))
            self.final_surface = pygame.Surface((width // 2, height))
        else:
            self.buffer_surface = pygame.Surface((width, height))
            self.final_surface = pygame.Surface((width, height))

        # 透明度支持
        self.buffer_surface = self.buffer_surface.convert_alpha()
        self.final_surface = self.final_surface.convert_alpha()

        # 星星相关变量
        self.star_points = []
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = min(width, height) // 3
        self.rotation = 0

    def initialize(self):
        """初始化星星点阵"""
        # 创建8角星的点
        self.star_points = []
        for i in range(16):  # 16个点（8个外角，8个内角）
            angle = 2 * math.pi * i / 16
            if i % 2 == 0:
                # 外点
                radius = self.radius
            else:
                # 内点
                radius = self.radius * 0.4

            x = self.center_x + radius * math.cos(angle)
            y = self.center_y + radius * math.sin(angle)
            self.star_points.append((x, y))

        print("星星图案初始化完成")

    def update(self, dt):
        """更新星星旋转"""
        self.rotation += dt * 0.5  # 缓慢旋转
        self.frame_count += 1
        return self.frame_count < 480  # 运行8秒（60fps * 8）

    def draw_basic_elements(self, surface):
        """绘制基础星星图形"""
        surface.fill((0, 0, 0, 0))  # 透明背景

        # 绘制星星轮廓
        rotated_points = []
        for x, y in self.star_points:
            # 计算旋转后的位置
            dx = x - self.center_x
            dy = y - self.center_y
            rotated_x = self.center_x + dx * math.cos(self.rotation) - dy * math.sin(self.rotation)
            rotated_y = self.center_y + dx * math.sin(self.rotation) + dy * math.cos(self.rotation)
            rotated_points.append((rotated_x, rotated_y))

        # 绘制连线
        if len(rotated_points) > 2:
            pygame.draw.lines(surface, (255, 255, 255), True, rotated_points, 2)

        # 绘制顶点
        for x, y in rotated_points:
            pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), 2)

    def apply_effects(self, surface):
        """应用星星特效"""
        # 添加光晕效果
        glow_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        # 在星星位置添加光晕
        for x, y in self.star_points:
            dx = x - self.center_x
            dy = y - self.center_y
            rotated_x = self.center_x + dx * math.cos(self.rotation) - dy * math.sin(self.rotation)
            rotated_y = self.center_y + dx * math.sin(self.rotation) + dy * math.cos(self.rotation)

            # 绘制光晕
            for radius in range(10, 30, 5):
                alpha = 100 - radius * 3
                if alpha > 0:
                    pygame.draw.circle(glow_surface, (255, 255, 255, alpha),
                                       (int(rotated_x), int(rotated_y)), radius)

        surface.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)

    def draw_debug(self, surface):
        """调试模式下的绘制"""
        if not self.debug_mode:
            return

        # 左侧：基础图形
        self.buffer_surface.fill((0, 0, 0, 0))
        self.draw_basic_elements(self.buffer_surface)

        # 右侧：基础图形 + 特效
        self.final_surface.fill((0, 0, 0, 0))
        self.final_surface.blit(self.buffer_surface, (0, 0))
        self.apply_effects(self.final_surface)

        # 合并到主surface
        surface.blit(self.buffer_surface, (0, 0))
        surface.blit(self.final_surface, (self.width // 2, 0))

        # 绘制调试信息
        self._draw_debug_info(surface)

    def draw_final(self, surface):
        """被调用模式下的最终绘制"""
        self.final_surface.fill((0, 0, 0, 0))
        self.draw_basic_elements(self.final_surface)
        self.apply_effects(self.final_surface)
        surface.blit(self.final_surface, (0, 0))

    def _draw_debug_info(self, surface):
        """绘制调试信息"""
        # 显示当前图案信息
        try:
            # 使用系统中文字体
            font_path = "C:/Windows/Fonts/simhei.ttf"
            font = pygame.font.Font(font_path, 16)
        except:
            # 备用方案
            font = pygame.font.Font(None, 26)

        # font = pygame.font.Font(None, 24)

        info_lines = [
            f"图案: Star",
            f"帧数: {self.frame_count}",
            f"调试模式: {self.debug_mode}",
            f"旋转角度: {self.rotation:.2f}"
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            surface.blit(text, (10, 10 + i * 25))

    def get_duration(self):
        """返回图案建议持续时间"""
        return 8.0

    def should_continue(self):
        """判断是否应该继续运行"""
        return self.frame_count * 0.016 < self.get_duration()

    def stop(self):
        """停止图案运行"""
        self.running = False