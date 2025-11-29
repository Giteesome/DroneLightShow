# patterns/pattern_neon.py
# Python code, uploaded by Giteesome, 2025-11-29
# A Mimic Program Manager for Drone-Light-Show Items , beta v0.9
# tested pass on Windows 11 platform
# work with drone-light-show-main.py and other code pieces in the bundle

import pygame
import math
import random
import time


class PatternNeon:
    """霓虹探照灯图案 - 修复旋转速度问题"""

    def __init__(self, width, height, debug_mode=False):
        self.width = width
        self.height = height
        self.debug_mode = debug_mode
        self.frame_count = 0
        self.running = True
        self.start_time = time.time()
        self.last_update_time = time.time()

        # 创建绘制表面
        if self.debug_mode:
            self.buffer_surface = pygame.Surface((width // 2, height))
            self.final_surface = pygame.Surface((width // 2, height))
        else:
            self.buffer_surface = pygame.Surface((width, height))
            self.final_surface = pygame.Surface((width, height))

        self.buffer_surface = self.buffer_surface.convert_alpha()
        self.final_surface = self.final_surface.convert_alpha()

        # 霓虹灯相关变量 - 调整速度参数
        self.beams = []
        self.rotation_speed = 0.6  # 大幅降低旋转速度：从1.5降到0.3，又调回到 0.6
        self.color_cycle_speed = 0.02  # 降低颜色变化速度：从0.08降到0.02
        self.current_rotation = 0
        self.color_phase = 0

    def get_chinese_font(self, size=16):
        """获取支持中文的字体"""
        try:
            font_path = "C:/Windows/Fonts/simhei.ttf"
            return pygame.font.Font(font_path, size)
        except:
            return pygame.font.Font(None, size)

    def draw_simple_beam(self, surface, start_pos, angle, length, start_width, end_width, color,
                         alpha_range=(0.3, 0.8)):
        """简单但可靠的光束绘制方法"""
        angle_rad = math.radians(angle)

        # 计算光束端点
        end_x = start_pos[0] + math.cos(angle_rad) * length
        end_y = start_pos[1] - math.sin(angle_rad) * length  # Pygame Y轴向下

        # 计算垂直方向
        perp_angle = angle_rad + math.pi / 2
        perp_x = math.cos(perp_angle)
        perp_y = -math.sin(perp_angle)

        # 计算四个角点
        half_start = start_width / 2
        half_end = end_width / 2

        points = [
            (start_pos[0] + perp_x * half_start, start_pos[1] + perp_y * half_start),
            (start_pos[0] - perp_x * half_start, start_pos[1] - perp_y * half_start),
            (end_x - perp_x * half_end, end_y - perp_y * half_end),
            (end_x + perp_x * half_end, end_y + perp_y * half_end)
        ]

        # 绘制渐变多边形
        steps = 10
        for i in range(steps):
            t1 = i / steps
            t2 = (i + 1) / steps

            # 计算当前段的四个点
            segment_points = [
                (
                    points[0][0] * (1 - t1) + points[3][0] * t1,
                    points[0][1] * (1 - t1) + points[3][1] * t1
                ),
                (
                    points[1][0] * (1 - t1) + points[2][0] * t1,
                    points[1][1] * (1 - t1) + points[2][1] * t1
                ),
                (
                    points[1][0] * (1 - t2) + points[2][0] * t2,
                    points[1][1] * (1 - t2) + points[2][1] * t2
                ),
                (
                    points[0][0] * (1 - t2) + points[3][0] * t2,
                    points[0][1] * (1 - t2) + points[3][1] * t2
                )
            ]

            # 计算当前段的alpha值
            current_alpha = int(255 * (alpha_range[0] + (alpha_range[1] - alpha_range[0]) * (1 - t1)))

            # 绘制四边形
            if len(segment_points) == 4:
                pygame.draw.polygon(surface, (*color, current_alpha), segment_points)

        # 返回调试用的简单图形
        debug_buffer = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(debug_buffer, (*color, 180), (30, 30), 25)

        debug_radius = pygame.Surface((50, 20), pygame.SRCALPHA)
        debug_radius.fill((*color, 180))

        return debug_buffer, debug_radius

    def get_cycling_color(self, phase, color_type="rainbow"):
        """获取循环变化的颜色 - 修复语法错误"""
        if color_type == "rainbow":
            r = int(127 + 127 * math.sin(phase))
            g = int(127 + 127 * math.sin(phase + 2))
            b = int(127 + 127 * math.sin(phase + 4))
            return (r, g, b)
        elif color_type == "warm":
            # 修复：直接返回颜色元组，不要用int()包装
            return (255, 150, 100)  # 固定暖色
        else:  # cool
            # 修复：直接返回颜色元组，不要用int()包装
            return (100, 150, 255)  # 固定冷色

    def initialize(self):
        """初始化霓虹灯图案"""
        print("霓虹探照灯图案初始化完成")

        # 重置时间跟踪
        self.start_time = time.time()
        self.last_update_time = time.time()
        self.frame_count = 0
        self.current_rotation = 0
        self.color_phase = 0

        self.beams = []
        center_x, center_y = self.width // 2, self.height // 2

        # 简化的光束配置 - 减少光束数量和长度
        self.beams = [
            {
                'start_pos': (center_x - 150, center_y),  # 缩短距离
                'base_angle': 45,
                'length': 400,  # 缩短光束长度
                'start_width': 20,
                'end_width': 80,  # 减小末端宽度
                'color_type': 'rainbow',
                'alpha_range': (0.3, 0.6),  # 降低透明度
                'rotation_offset': 0,
                'pulse_speed': 0.5  # 降低脉冲速度
            },
            {
                'start_pos': (center_x + 150, center_y),  # 缩短距离
                'base_angle': 135,
                'length': 400,  # 缩短光束长度
                'start_width': 20,
                'end_width': 80,  # 减小末端宽度
                'color_type': 'warm',
                'alpha_range': (0.3, 0.6),  # 降低透明度
                'rotation_offset': 90,
                'pulse_speed': 0.6  # 降低脉冲速度
            }
        ]

    def update(self, dt):
        """更新霓虹灯动画 - 修复时间计算"""
        current_time = time.time()

        # 使用实际时间差，确保与帧率无关
        if hasattr(self, 'last_update_time'):
            actual_dt = current_time - self.last_update_time
        else:
            actual_dt = dt

        self.last_update_time = current_time

        self.frame_count += 1

        # 使用实际时间计算旋转和颜色变化
        self.current_rotation += self.rotation_speed * actual_dt * 30  # 进一步降低速度系数
        self.color_phase += self.color_cycle_speed * actual_dt * 30  # 进一步降低速度系数

        if self.current_rotation >= 360:
            self.current_rotation -= 360

        return self.should_continue()

    def draw_basic_elements(self, surface):
        """绘制基础光束"""
        surface.fill((0, 0, 0, 0))
        gradient_data = []

        for beam_config in self.beams:
            # 计算当前角度
            current_angle = (beam_config['base_angle'] +
                             self.current_rotation +
                             beam_config['rotation_offset'])

            # 计算脉冲效果 - 使用更慢的速度
            pulse_factor = 0.8 + 0.2 * math.sin(self.frame_count * 0.02 * beam_config['pulse_speed'])  # 降低脉冲幅度和速度
            current_length = beam_config['length'] * pulse_factor

            # 获取当前颜色
            color_phase = self.color_phase + beam_config['rotation_offset'] * 0.005  # 降低颜色变化关联
            color = self.get_cycling_color(color_phase, beam_config['color_type'])

            # 绘制光束
            buffer, radius = self.draw_simple_beam(
                surface,
                beam_config['start_pos'],
                current_angle,
                current_length,
                beam_config['start_width'],
                beam_config['end_width'],
                color,
                beam_config['alpha_range']
            )
            gradient_data.append((buffer, radius, color))

        return gradient_data

    def apply_effects(self, surface):
        """应用特效 - 减弱效果"""
        if not self.debug_mode:
            # 添加简单的光晕效果 - 减弱
            glow_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            center_x, center_y = surface.get_width() // 2, surface.get_height() // 2

            pygame.draw.circle(glow_surface, (255, 255, 255, 40),  # 降低光晕强度
                               (center_x, center_y), 80)  # 减小光晕半径

            surface.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

    def draw_debug(self, surface):
        """调试模式下的绘制"""
        if not self.debug_mode:
            return

        # 左侧：基础图形和调试信息
        self.buffer_surface.fill((20, 20, 40, 255))
        gradient_data = self.draw_basic_elements(self.buffer_surface)

        # 在左侧显示调试信息
        buffer_y = 50
        for i, (gradient_buffer, radius_surface, color) in enumerate(gradient_data):
            font = self.get_chinese_font(16)
            color_names = ["彩虹色", "暖色调"]
            text = font.render(f"光束 {i + 1}", True, (255, 255, 255))
            self.buffer_surface.blit(text, (20, buffer_y - 25))

            # 显示颜色预览
            self.buffer_surface.blit(gradient_buffer, (30, buffer_y))
            buffer_y += gradient_buffer.get_height() + 50

        # 右侧：最终效果
        self.final_surface.fill((10, 10, 30, 255))
        self.draw_basic_elements(self.final_surface)
        self.apply_effects(self.final_surface)

        # 合并到主surface
        surface.blit(self.buffer_surface, (0, 0))
        surface.blit(self.final_surface, (self.width // 2, 0))

        # 绘制调试信息
        self._draw_debug_info(surface)

    def draw_final(self, surface):
        """最终绘制模式"""
        self.final_surface.fill((0, 0, 0, 255))
        self.draw_basic_elements(self.final_surface)
        self.apply_effects(self.final_surface)
        surface.blit(self.final_surface, (0, 0))

    def _draw_debug_info(self, surface):
        """绘制调试信息"""
        font = self.get_chinese_font(16)

        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.get_duration() - elapsed_time)

        info_lines = [
            f"图案: 霓虹探照灯(慢速)",
            f"帧数: {self.frame_count}",
            f"旋转: {self.current_rotation:.1f}°",
            f"光束: {len(self.beams)}",
            f"速度: {self.rotation_speed:.1f}°/帧"
        ]

        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            surface.blit(text, (10, 10 + i * 20))

    def get_duration(self):
        return 10.0

    def should_continue(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time < self.get_duration()

    def stop(self):
        self.running = False

    def set_debug_mode(self, debug_mode):
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