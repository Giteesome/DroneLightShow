# patterns/pattern_stars.py
# Python code, uploaded by Giteesome, 2025-11-29
# A Mimic Program Manager for Drone-Light-Show Items , beta v0.9
# tested pass on Windows 11 platform
# work with drone-light-show-main.py and other code pieces in the bundle

import pygame
import math
import random
import time


class PatternStars:
    """多星星图案 - 修复调试信息和时间问题"""

    def __init__(self, width, height, debug_mode=False):
        self.width = width
        self.height = height
        self.debug_mode = debug_mode
        self.frame_count = 0
        self.running = True
        self.start_time = time.time()
        self.last_update_time = time.time()  # 添加精确时间跟踪

        # 创建绘制表面
        if self.debug_mode:
            self.buffer_surface = pygame.Surface((width // 2, height))
            self.final_surface = pygame.Surface((width // 2, height))
        else:
            self.buffer_surface = pygame.Surface((width, height))
            self.final_surface = pygame.Surface((width, height))

        self.buffer_surface = self.buffer_surface.convert_alpha()
        self.final_surface = self.final_surface.convert_alpha()

        # 星星系统变量
        self.background_stars = []  # 背景恒星
        self.program_stars = []  # 节目星星
        self.star_colors = [
            (255, 255, 255),  # 白色
            (255, 255, 200),  # 暖白
            (200, 200, 255),  # 冷白
            (255, 200, 200),  # 粉白
        ]
        self.program_colors = [
            (255, 50, 50),  # 红色
            (50, 255, 50),  # 绿色
            (50, 50, 255),  # 蓝色
            (255, 255, 50),  # 黄色
            (255, 50, 255),  # 紫色
            (50, 255, 255),  # 青色
        ]

    def get_chinese_font(self, size=24):
        """获取支持中文的字体"""
        try:
            font_path = "C:/Windows/Fonts/simhei.ttf"
            return pygame.font.Font(font_path, size)
        except:
            return pygame.font.Font(None, size)

    def create_star_shape(self, star_type, size, complexity=1.0):
        """创建星星形状"""
        points = []

        if star_type == "background":
            # 背景恒星：不规则多边形
            num_points = random.randint(5, 8)
            base_radius = size
            for i in range(num_points):
                angle = 2 * math.pi * i / num_points
                # 添加随机性使形状不规则
                radius_variation = random.uniform(0.7, 1.3) * complexity
                radius = base_radius * radius_variation
                x = math.cos(angle) * radius
                y = math.sin(angle) * radius
                points.append((x, y))

        else:  # program stars
            # 节目星星：更规则的形状
            num_points = random.choice([5, 6, 7])  # 五角星、六角星、七角星
            base_radius = size
            for i in range(num_points):
                angle = 2 * math.pi * i / num_points
                radius = base_radius
                x = math.cos(angle) * radius
                y = math.sin(angle) * radius
                points.append((x, y))

        return points

    def create_background_star(self):
        """创建背景恒星"""
        return {
            'x': random.uniform(50, self.width - 50),
            'y': random.uniform(50, self.height - 50),
            'size': random.uniform(1.5, 4.0),  # 较小的尺寸
            'base_brightness': random.uniform(0.3, 0.8),
            'flicker_speed': random.uniform(0.5, 2.0),
            'flicker_phase': random.uniform(0, 2 * math.pi),
            'color': random.choice(self.star_colors),
            'shape_points': [],  # 将在initialize中生成
            'type': 'background'
        }

    def create_program_star(self):
        """创建节目星星"""
        # 随机选择进入方向
        side = random.choice(['left', 'right', 'top', 'bottom'])

        if side == 'left':
            x = -20
            y = random.uniform(50, self.height - 50)
            speed_x = random.uniform(1.0, 3.0)
            speed_y = random.uniform(-0.5, 0.5)
        elif side == 'right':
            x = self.width + 20
            y = random.uniform(50, self.height - 50)
            speed_x = random.uniform(-3.0, -1.0)
            speed_y = random.uniform(-0.5, 0.5)
        elif side == 'top':
            x = random.uniform(50, self.width - 50)
            y = -20
            speed_x = random.uniform(-0.5, 0.5)
            speed_y = random.uniform(1.0, 3.0)
        else:  # bottom
            x = random.uniform(50, self.width - 50)
            y = self.height + 20
            speed_x = random.uniform(-0.5, 0.5)
            speed_y = random.uniform(-3.0, -1.0)

        return {
            'x': x,
            'y': y,
            'speed_x': speed_x,
            'speed_y': speed_y,
            'size': random.uniform(5.0, 12.0),  # 较大的尺寸
            'base_brightness': random.uniform(0.7, 1.0),
            'flicker_speed': random.uniform(0.2, 0.8),
            'flicker_phase': random.uniform(0, 2 * math.pi),
            'color': random.choice(self.program_colors),
            'shape_points': [],  # 将在initialize中生成
            'type': 'program',
            'glow_intensity': random.uniform(0.5, 1.0)
        }

    def initialize(self):
        """初始化星星系统"""
        print("多星星图案初始化完成")

        # 重置时间跟踪
        self.start_time = time.time()
        self.last_update_time = time.time()
        self.frame_count = 0

        # 清空现有星星
        self.background_stars = []
        self.program_stars = []

        # 创建背景恒星 (15-25颗)
        num_background = random.randint(15, 25)
        for _ in range(num_background):
            star = self.create_background_star()
            # 生成形状点
            star['shape_points'] = self.create_star_shape('background', star['size'])
            self.background_stars.append(star)

        # 创建节目星星 (8-15颗)
        num_program = random.randint(8, 15)
        for _ in range(num_program):
            star = self.create_program_star()
            # 生成形状点
            star['shape_points'] = self.create_star_shape('program', star['size'])
            self.program_stars.append(star)

    def update(self, dt):
        """更新星星系统 - 使用精确时间计算"""
        current_time = time.time()
        actual_dt = current_time - self.last_update_time
        self.last_update_time = current_time

        self.frame_count += 1

        # 更新背景恒星的闪烁
        for star in self.background_stars:
            # 简单的闪烁效果
            pass  # 闪烁在绘制时计算

        # 更新节目星星的位置
        for star in self.program_stars[:]:
            star['x'] += star['speed_x'] * actual_dt * 60  # 乘以60使速度与帧率无关
            star['y'] += star['speed_y'] * actual_dt * 60

            # 移除屏幕外的星星并创建新的
            if (star['x'] < -50 or star['x'] > self.width + 50 or
                    star['y'] < -50 or star['y'] > self.height + 50):
                self.program_stars.remove(star)
                # 有一定概率创建新星星
                if random.random() < 0.3 and len(self.program_stars) < 20:
                    new_star = self.create_program_star()
                    new_star['shape_points'] = self.create_star_shape('program', new_star['size'])
                    self.program_stars.append(new_star)

        # 确保有一定数量的节目星星
        while len(self.program_stars) < 8:
            new_star = self.create_program_star()
            new_star['shape_points'] = self.create_star_shape('program', new_star['size'])
            self.program_stars.append(new_star)

        return self.should_continue()

    def draw_star(self, surface, star, current_time):
        """绘制单个星星"""
        # 计算闪烁亮度
        flicker = 0.7 + 0.3 * math.sin(current_time * star['flicker_speed'] + star['flicker_phase'])
        brightness = star['base_brightness'] * flicker

        # 计算最终颜色
        base_color = star['color']
        final_color = (
            int(base_color[0] * brightness),
            int(base_color[1] * brightness),
            int(base_color[2] * brightness)
        )

        # 转换形状点到实际位置
        actual_points = []
        for dx, dy in star['shape_points']:
            actual_points.append((
                int(star['x'] + dx),
                int(star['y'] + dy)
            ))

        # 绘制星星主体
        if len(actual_points) > 2:
            pygame.draw.polygon(surface, final_color, actual_points)

        # 为节目星星添加光晕
        if star['type'] == 'program':
            glow_surface = pygame.Surface((int(star['size'] * 4), int(star['size'] * 4)), pygame.SRCALPHA)
            glow_radius = int(star['size'] * 1.5)
            glow_alpha = int(100 * star['glow_intensity'] * brightness)

            # 绘制光晕
            pygame.draw.circle(glow_surface, (*final_color, glow_alpha),
                               (glow_radius * 2, glow_radius * 2), glow_radius)

            # 应用光晕
            surface.blit(glow_surface,
                         (int(star['x'] - glow_radius * 2), int(star['y'] - glow_radius * 2)),
                         special_flags=pygame.BLEND_ALPHA_SDL2)

    def draw_basic_elements(self, surface):
        """绘制基础元素"""
        surface.fill((0, 0, 0, 0))  # 透明背景
        current_time = time.time() - self.start_time

        # 绘制背景恒星
        for star in self.background_stars:
            self.draw_star(surface, star, current_time)

        # 绘制节目星星
        for star in self.program_stars:
            self.draw_star(surface, star, current_time)

    def apply_effects(self, surface):
        """应用特效"""
        if not self.debug_mode:
            # 添加全局星空光晕效果
            glow_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

            # 在节目星星位置添加更强的光晕
            for star in self.program_stars:
                if star['type'] == 'program':
                    current_time = time.time() - self.start_time
                    flicker = 0.7 + 0.3 * math.sin(current_time * star['flicker_speed'] + star['flicker_phase'])
                    brightness = star['base_brightness'] * flicker

                    glow_radius = int(star['size'] * 3)
                    glow_alpha = int(60 * star['glow_intensity'] * brightness)

                    pygame.draw.circle(glow_surface, (255, 255, 255, glow_alpha),
                                       (int(star['x']), int(star['y'])), glow_radius)

            surface.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

    def draw_debug(self, surface):
        """调试模式下的绘制 - 修复信息重叠"""
        if not self.debug_mode:
            return

        # 左侧：基础图形
        self.buffer_surface.fill((20, 20, 40, 255))
        self.draw_basic_elements(self.buffer_surface)

        # 在左侧添加调试信息 - 使用不同位置避免重叠
        font = self.get_chinese_font(14)
        info_lines = [
            "=== 左侧: 基础星星 ===",
            f"背景恒星: {len(self.background_stars)}颗",
            f"节目星星: {len(self.program_stars)}颗",
            "--- 颜色说明 ---",
            "白色系: 背景恒星",
            "彩色: 节目星星"
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            self.buffer_surface.blit(text, (10, 10 + i * 20))

        # 右侧：应用特效
        self.final_surface.fill((10, 10, 30, 255))
        self.draw_basic_elements(self.final_surface)
        self.apply_effects(self.final_surface)

        # 合并到主surface
        surface.blit(self.buffer_surface, (0, 0))
        surface.blit(self.final_surface, (self.width // 2, 0))

        # 绘制调试信息 - 在右侧surface上绘制，避免与左侧重叠
        self._draw_debug_info(surface)

    def draw_final(self, surface):
        """最终绘制模式"""
        self.final_surface.fill((0, 0, 0, 255))
        self.draw_basic_elements(self.final_surface)
        self.apply_effects(self.final_surface)
        surface.blit(self.final_surface, (0, 0))

    def _draw_debug_info(self, surface):
        """绘制调试信息 - 修复位置重叠"""
        font = self.get_chinese_font(16)

        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.get_duration() - elapsed_time)

        # 在右侧surface的左上角显示时间信息
        info_lines = [
            f"图案: 多星星系统",
            f"帧数: {self.frame_count}",
            f"运行时间: {elapsed_time:.1f}s",
            f"剩余时间: {remaining_time:.1f}s"
        ]

        # 计算在右侧surface上的位置
        right_start_x = self.width // 2
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            surface.blit(text, (right_start_x + 10, 10 + i * 20))

    def get_duration(self):
        """返回图案建议持续时间"""
        return 30.0  # 延长到30秒

    def should_continue(self):
        """判断是否应该继续运行 - 使用精确时间计算"""
        elapsed_time = time.time() - self.start_time
        return elapsed_time < self.get_duration()

    def stop(self):
        """停止图案运行"""
        self.running = False

    def set_debug_mode(self, debug_mode):
        """设置调试模式"""
        if self.debug_mode == debug_mode:
            return

        self.debug_mode = debug_mode

        if self.debug_mode:
            self.buffer_surface = pygame.Surface((self.width // 2, self.height))
            self.final_surface = pygame.Surface((self.width // 2, self.height))
        else:
            self.buffer_surface = pygame.Surface((self.width, self.height))
            self.final_surface = pygame.Surface((self.width, self.height))

        self.buffer_surface = self.buffer_surface.convert_alpha()
        self.final_surface = self.final_surface.convert_alpha()