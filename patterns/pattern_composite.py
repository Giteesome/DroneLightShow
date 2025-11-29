# patterns/pattern_composite.py
# Python code, uploaded by Giteesome, 2025-11-29
# A Mimic Program Manager for Drone-Light-Show Items , beta v0.9
# tested pass on Windows 11 platform
# work with drone-light-show-main.py and other code pieces in the bundle

import pygame
import random
import math
import sys
import os
import time

# 添加当前目录到Python路径，确保可以导入其他图案
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


class PatternComposite:
    """复合图案 - 修复时间传递问题"""

    def __init__(self, width, height, debug_mode=False):
        self.width = width
        self.height = height
        self.debug_mode = debug_mode
        self.is_first_call = True
        self.frame_count = 0
        self.running = True
        self.start_time = None
        self.last_update_time = None  # 添加时间跟踪

        # 创建绘制表面
        if self.debug_mode:
            self.buffer_surface = pygame.Surface((width // 2, height))
            self.final_surface = pygame.Surface((width // 2, height))
        else:
            self.buffer_surface = pygame.Surface((width, height))
            self.final_surface = pygame.Surface((width, height))

        self.buffer_surface = self.buffer_surface.convert_alpha()
        self.final_surface = self.final_surface.convert_alpha()

        # 子图案列表
        self.sub_patterns = []
        self.sub_pattern_weights = {}

    def get_chinese_font(self, size=16):
        """获取支持中文的字体"""
        try:
            font_path = "C:/Windows/Fonts/simhei.ttf"
            return pygame.font.Font(font_path, size)
        except:
            return pygame.font.Font(None, size)

    def initialize(self):
        """初始化复合图案"""
        print("复合图案初始化 - 创建子图案")
        self.start_time = time.time()
        self.last_update_time = time.time()  # 初始化时间跟踪

        # 清空现有的子图案
        self.sub_patterns = []
        self.sub_pattern_weights = {}

        # 尝试动态导入并创建子图案
        self._try_create_star_pattern()
        self._try_create_circle_pattern()
        self._try_create_simple_pattern()
        self._try_create_neon_pattern()

        # 如果没有成功添加任何子图案，创建一个简单的备用图案
        if not self.sub_patterns:
            self._create_fallback_pattern()

        print(f"复合图案初始化完成，共 {len(self.sub_patterns)} 个子图案")
        # 打印权重信息用于调试
        for i, pattern in enumerate(self.sub_patterns):
            weight = self.sub_pattern_weights.get(id(pattern), 1.0)
            pattern_name = pattern.__class__.__name__
            print(f"  子图案 {i + 1}: {pattern_name}, 权重: {weight}")

    def _try_create_star_pattern(self):
        """尝试创建星星图案"""
        try:
            import importlib
            module = importlib.import_module('pattern_star')
            star_class = getattr(module, 'PatternStar')

            star_pattern = star_class(self.width, self.height, debug_mode=False)
            star_pattern.initialize()
            self.add_pattern(star_pattern, weight=0.8)
            print("成功添加星星子图案，权重: 0.8")
        except Exception as e:
            print(f"无法创建星星图案: {e}")

    def _try_create_circle_pattern(self):
        """尝试创建圆圈图案"""
        try:
            import importlib
            module = importlib.import_module('pattern_circle')
            circle_class = getattr(module, 'PatternCircle')

            circle_pattern = circle_class(self.width, self.height, debug_mode=False)
            circle_pattern.initialize()
            self.add_pattern(circle_pattern, weight=0.5)
            print("成功添加圆圈子图案，权重: 0.5")
        except Exception as e:
            print(f"无法创建圆圈图案: {e}")

    def _try_create_simple_pattern(self):
        """尝试创建简单图案"""
        try:
            import importlib
            module = importlib.import_module('pattern_simple')
            simple_class = getattr(module, 'PatternSimple')

            simple_pattern = simple_class(self.width, self.height, debug_mode=False)
            simple_pattern.initialize()
            self.add_pattern(simple_pattern, weight=0.3)
            print("成功添加简单子图案，权重: 0.3")
        except Exception as e:
            print(f"无法创建简单图案: {e}")

    def _try_create_neon_pattern(self):
        """尝试创建霓虹图案"""
        try:
            import importlib
            try:
                module = importlib.import_module('pattern_neon')
            except ImportError:
                module = importlib.import_module('.pattern_neon', package='patterns')

            neon_class = getattr(module, 'PatternNeon')

            neon_pattern = neon_class(self.width, self.height, debug_mode=False)
            neon_pattern.initialize()
            self.add_pattern(neon_pattern, weight=0.6)  # 确认权重为0.6
            print("成功添加霓虹子图案，权重: 0.6")
        except Exception as e:
            print(f"无法创建霓虹图案: {e}")
            import traceback
            traceback.print_exc()

    def _create_fallback_pattern(self):
        """创建备用简单图案"""

        class FallbackPattern:
            def __init__(self, width, height):
                self.width = width
                self.height = height
                self.center_x = width // 2
                self.center_y = height // 2
                self.angle = 0
                self.frame_count = 0
                self.running = True
                self.start_time = time.time()

            def initialize(self):
                pass

            def update(self, dt):
                self.angle += dt * 2
                self.frame_count += 1
                return self.should_continue()

            def draw_basic_elements(self, surface):
                surface.fill((0, 0, 0, 0))
                radius = min(self.width, self.height) // 4

                # 绘制旋转的五边形
                points = []
                for i in range(5):
                    angle = self.angle + 2 * math.pi * i / 5
                    x = self.center_x + radius * math.cos(angle)
                    y = self.center_y + radius * math.sin(angle)
                    points.append((x, y))

                if len(points) > 2:
                    pygame.draw.polygon(surface, (255, 100, 100), points, 3)

                # 绘制中心点
                pygame.draw.circle(surface, (100, 255, 100),
                                   (int(self.center_x), int(self.center_y)), 5)

            def should_continue(self):
                """判断是否应该继续运行"""
                return time.time() - self.start_time < 10.0

            def get_duration(self):
                return 10.0

        fallback = FallbackPattern(self.width, self.height)
        fallback.initialize()
        self.add_pattern(fallback, weight=1.0)
        print("创建备用图案")

    def add_pattern(self, pattern, weight=1.0):
        """添加子图案"""
        self.sub_patterns.append(pattern)
        self.sub_pattern_weights[id(pattern)] = weight

    def set_pattern_weight(self, pattern, weight):
        """设置子图案的混合权重"""
        self.sub_pattern_weights[id(pattern)] = weight

    def update(self, dt):
        """更新所有子图案 - 修复时间传递"""
        current_time = time.time()

        # 使用实际时间差，确保与帧率无关
        if self.last_update_time is not None:
            actual_dt = current_time - self.last_update_time
        else:
            actual_dt = dt

        self.last_update_time = current_time

        self.frame_count += 1

        # 更新所有子图案，传递正确的时间增量
        for pattern in self.sub_patterns:
            # 确保每个子图案都使用实际时间差
            if hasattr(pattern, 'update'):
                # 传递实际时间差，而不是主程序传递的dt
                pattern.update(actual_dt)

        return self.should_continue()

    def draw_basic_elements(self, surface):
        """绘制基础元素 - 叠加所有子图案"""
        surface.fill((0, 0, 0, 0))  # 透明背景

        # 绘制每个子图案到临时表面，然后混合
        for pattern in self.sub_patterns:
            # 创建临时表面用于子图案绘制
            temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

            # 检查图案是否有draw_basic_elements方法
            if hasattr(pattern, 'draw_basic_elements'):
                pattern.draw_basic_elements(temp_surface)
            elif hasattr(pattern, 'draw_final'):
                # 如果只有draw_final方法，使用它
                pattern.draw_final(temp_surface)
            else:
                # 如果都没有，跳过这个图案
                continue

            # 应用权重混合
            weight = self.sub_pattern_weights.get(id(pattern), 1.0)
            if weight < 1.0:
                # 调整透明度
                temp_surface.fill((255, 255, 255, int(255 * weight)),
                                  special_flags=pygame.BLEND_RGBA_MULT)

            # 混合到主表面
            surface.blit(temp_surface, (0, 0))

    def apply_effects(self, surface):
        """应用特效到复合图案"""
        # 添加全局光晕效果
        glow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 在图案中心添加光晕
        center_x, center_y = self.width // 2, self.height // 2
        max_radius = min(self.width, self.height) // 3

        for radius in range(20, max_radius, 10):
            alpha = 50 - radius // 5
            if alpha > 0:
                pygame.draw.circle(glow_surface, (255, 255, 255, alpha),
                                   (center_x, center_y), radius, 2)

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
        font = self.get_chinese_font(16)

        # 计算剩余时间
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.get_duration() - elapsed_time)

        info_lines = [
            f"图案: 复合图案",
            f"帧数: {self.frame_count}",
            f"运行时间: {elapsed_time:.1f}秒",
            f"剩余时间: {remaining_time:.1f}秒",
            f"调试模式: {self.debug_mode}",
            f"子图案数量: {len(self.sub_patterns)}"
        ]

        # 显示每个子图案的权重
        for i, pattern in enumerate(self.sub_patterns):
            weight = self.sub_pattern_weights.get(id(pattern), 1.0)
            pattern_name = pattern.__class__.__name__
            info_lines.append(f"图案{i + 1}: {pattern_name} (权重: {weight:.1f})")

        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            surface.blit(text, (10, 10 + i * 25))

    def get_duration(self):
        """返回图案建议持续时间"""
        return 15.0

    def should_continue(self):
        """判断是否应该继续运行 - 使用准确的时间计算"""
        if self.start_time is None:
            return True
        elapsed_time = time.time() - self.start_time
        return elapsed_time < self.get_duration()

    def stop(self):
        """停止图案运行"""
        self.running = False