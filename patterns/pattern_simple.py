# patterns/pattern_simple.py
# Python code, uploaded by Giteesome, 2025-11-29
# A Mimic Program Manager for Drone-Light-Show Items , beta v0.9
# tested pass on Windows 11 platform
# work with drone-light-show-main.py and other code pieces in the bundle

import pygame
import random
import math


class PatternSimple:
    """简单测试图案"""

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

        # 简单图案的变量
        self.circles = []
        self.setup_circles()

    def setup_circles(self):
        """设置圆圈"""
        for i in range(10):
            self.circles.append({
                'x': random.randint(50, self.width - 50),
                'y': random.randint(50, self.height - 50),
                'radius': random.randint(10, 40),
                'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                'speed': random.uniform(0.5, 2.0),
                'angle': random.uniform(0, 2 * math.pi)
            })

    def initialize(self):
        """初始化"""
        print("简单图案初始化完成")

    def update(self, dt):
        """更新逻辑"""
        self.frame_count += 1

        # 移动圆圈
        for circle in self.circles:
            circle['x'] += math.cos(circle['angle']) * circle['speed']
            circle['y'] += math.sin(circle['angle']) * circle['speed']

            # 边界检测
            if circle['x'] < circle['radius'] or circle['x'] > self.width - circle['radius']:
                circle['angle'] = math.pi - circle['angle']
            if circle['y'] < circle['radius'] or circle['y'] > self.height - circle['radius']:
                circle['angle'] = -circle['angle']

        return self.frame_count < 300  # 运行5秒（60fps * 5）

    def draw_basic_elements(self, surface):
        """绘制基础元素"""
        surface.fill((0, 0, 0, 0))  # 透明背景

        # 绘制所有圆圈
        for circle in self.circles:
            pygame.draw.circle(surface, circle['color'],
                               (int(circle['x']), int(circle['y'])),
                               circle['radius'])

    def apply_effects(self, surface):
        """应用特效"""
        # 简单的光晕效果
        glow_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        for circle in self.circles:
            pygame.draw.circle(glow_surface, (*circle['color'], 50),
                               (int(circle['x']), int(circle['y'])),
                               circle['radius'] + 10)
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
            f"图案: Simple",
            f"帧数: {self.frame_count}",
            f"调试模式: {self.debug_mode}",
            f"圆圈数量: {len(self.circles)}"
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            surface.blit(text, (10, 10 + i * 25))

    def get_duration(self):
        """返回图案建议持续时间"""
        return 5.0

    def should_continue(self):
        """判断是否应该继续运行"""
        return self.frame_count * 0.016 < self.get_duration()

    def stop(self):
        """停止图案运行"""
        self.running = False