# patterns/pattern_circle.py
# Python code, uploaded by Giteesome, 2025-11-29
# A Mimic Program Manager for Drone-Light-Show Items , beta v0.9
# tested pass on Windows 11 platform
# work with drone-light-show-main.py and other code pieces in the bundle

import pygame
import math
import random


class PatternCircle:
    """圆圈波浪图案"""

    def __init__(self, width, height, debug_mode=False):
        self.width = width
        self.height = height
        self.debug_mode = debug_mode
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

        # 圆圈相关变量
        self.center_x = width // 2
        self.center_y = height // 2
        self.max_radius = min(width, height) // 2 - 20
        self.circles = []

    def get_chinese_font(self, size=16):
        """获取支持中文的字体"""
        try:
            font_path = "C:/Windows/Fonts/simhei.ttf"
            return pygame.font.Font(font_path, size)
        except:
            return pygame.font.Font(None, size)

    def initialize(self):
        """初始化"""
        print("圆圈波浪图案初始化完成")

    def update(self, dt):
        """更新逻辑"""
        self.frame_count += 1

        # 生成新的圆圈
        if self.frame_count % 10 == 0:  # 每10帧生成一个新圆圈
            self.circles.append({
                'radius': 5,
                'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                'alpha': 255,
                'growth_speed': random.uniform(1, 3)
            })

        # 更新现有圆圈
        for circle in self.circles[:]:
            circle['radius'] += circle['growth_speed']
            circle['alpha'] -= 2

            # 移除不可见的圆圈
            if circle['alpha'] <= 0 or circle['radius'] > self.max_radius:
                self.circles.remove(circle)

        return self.frame_count < 400  # 运行约6.5秒

    def draw_basic_elements(self, surface):
        """绘制基础圆圈"""
        surface.fill((0, 0, 0, 0))

        # 绘制所有圆圈
        for circle in self.circles:
            color_with_alpha = (*circle['color'], int(circle['alpha']))
            pygame.draw.circle(surface, color_with_alpha,
                               (self.center_x, self.center_y),
                               int(circle['radius']), 2)

    def apply_effects(self, surface):
        """应用特效"""
        # 添加中心光点
        center_glow = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(center_glow, (255, 255, 255, 100), (25, 25), 25)
        surface.blit(center_glow, (self.center_x - 25, self.center_y - 25))

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
        font = self.get_chinese_font(16)

        info_lines = [
            f"图案: 圆圈波浪",
            f"帧数: {self.frame_count}",
            f"调试模式: {self.debug_mode}",
            f"圆圈数量: {len(self.circles)}"
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            surface.blit(text, (10, 10 + i * 25))

    def get_duration(self):
        """返回图案建议持续时间"""
        return 6.5

    def should_continue(self):
        """判断是否应该继续运行"""
        return self.frame_count * 0.016 < self.get_duration()

    def stop(self):
        """停止图案运行"""
        self.running = False

    def set_debug_mode(self, debug_mode):
        """设置调试模式"""
        if self.debug_mode == debug_mode:
            return

        self.debug_mode = debug_mode

        # 重新创建surface
        if self.debug_mode:
            self.buffer_surface = pygame.Surface((self.width // 2, self.height))
            self.final_surface = pygame.Surface((self.width // 2, self.height))
        else:
            self.buffer_surface = pygame.Surface((self.width, self.height))
            self.final_surface = pygame.Surface((self.width, self.height))

        self.buffer_surface = self.buffer_surface.convert_alpha()
        self.final_surface = self.final_surface.convert_alpha()