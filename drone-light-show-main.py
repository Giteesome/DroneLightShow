# drone-light-show-main.py
# Python code, uploaded by Giteesome, 2025-11-30
# A Mimic Program Manager for Drone-Light-Show Items , beta v0.9
# tested pass on Windows 11 platform
# work with other code pieces in the bundle

import pygame
import sys
import os
import time

# 设置Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from pattern_manager import PatternManager

# 屏幕尺寸
WIDTH, HEIGHT = 1200, 720


def get_chinese_font(size=14):
    """获取支持中文的字体"""
    try:
        font_path = "C:/Windows/Fonts/simhei.ttf"
        return pygame.font.Font(font_path, size)
    except:
        return pygame.font.Font(None, size)


class ControlPanel:
    """控制面板 - 修复按钮响应版本"""

    def __init__(self, width, height):
        self.width = width
        self.height = 80
        self.y_position = height - self.height
        self.visible = True
        self.show_time = time.time()
        self.visible_duration = 15

        # 重新设计按钮布局，增加间距
        button_width = 100
        button_height = 35
        button_margin = 10
        start_x = 20

        self.buttons = [
            {"rect": pygame.Rect(start_x, self.y_position + 20, button_width, button_height),
             "text": "调试模式", "action": "toggle_debug"},
            {"rect": pygame.Rect(start_x + button_width + button_margin, self.y_position + 20, button_width,
                                 button_height),
             "text": "重新加载", "action": "reload"},
            {"rect": pygame.Rect(start_x + (button_width + button_margin) * 2, self.y_position + 20, button_width,
                                 button_height),
             "text": "下一图案", "action": "next_pattern"},
            {"rect": pygame.Rect(start_x + (button_width + button_margin) * 3, self.y_position + 20, button_width,
                                 button_height),
             "text": "自动播放", "action": "toggle_auto"},
            {"rect": pygame.Rect(start_x + (button_width + button_margin) * 4, self.y_position + 20, button_width,
                                 button_height),
             "text": "隐藏面板", "action": "hide_panel"}
        ]

        # 颜色定义
        self.bg_color = (40, 40, 60, 220)
        self.button_color = (70, 70, 100)
        self.button_hover_color = (90, 90, 130)
        self.button_active_color = (110, 110, 150)  # 按下状态
        self.text_color = (255, 255, 255)

        # 跟踪按钮状态
        self.button_states = {button["action"]: False for button in self.buttons}

    def show(self):
        """显示控制面板"""
        self.visible = True
        self.show_time = time.time()

    def hide(self):
        """隐藏控制面板"""
        self.visible = False

    def toggle(self):
        """切换控制面板显示状态"""
        self.visible = not self.visible
        if self.visible:
            self.show_time = time.time()

    def update(self):
        """更新面板状态"""
        if self.visible and time.time() - self.show_time > self.visible_duration:
            self.hide()

    def draw(self, surface):
        """绘制控制面板 - 修复版本"""
        if not self.visible:
            return

        # 创建半透明表面
        panel_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel_surface.fill(self.bg_color)

        # 绘制标题
        title_font = get_chinese_font(16)
        title_text = title_font.render("控制面板", True, (255, 255, 255))
        panel_surface.blit(title_text, (10, 10))

        # 绘制按钮
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            # 调整按钮坐标到面板坐标系
            button_rect_in_panel = pygame.Rect(
                button["rect"].x,
                button["rect"].y - self.y_position,
                button["rect"].width,
                button["rect"].height
            )

            # 检查鼠标状态
            is_hover = button["rect"].collidepoint(mouse_pos)
            is_active = self.button_states[button["action"]]

            # 选择颜色
            if is_active:
                color = self.button_active_color
            elif is_hover:
                color = self.button_hover_color
            else:
                color = self.button_color

            # 绘制按钮
            pygame.draw.rect(panel_surface, color, button_rect_in_panel, border_radius=5)
            pygame.draw.rect(panel_surface, (150, 150, 150), button_rect_in_panel, 2, border_radius=5)

            # 绘制按钮文字
            font = get_chinese_font(14)  # 稍小字体适应按钮
            text = font.render(button["text"], True, self.text_color)
            text_rect = text.get_rect(center=button_rect_in_panel.center)
            panel_surface.blit(text, text_rect)

        # 处理按钮状态重置
        for event in pygame.event.get(pygame.USEREVENT, pump=False):
            for button in self.buttons:
                event_id = pygame.USEREVENT + hash(button["action"]) % 1000
                if event.type == event_id:
                    self.button_states[button["action"]] = False
                    pygame.time.set_timer(event_id, 0)  # 清除定时器

        # 绘制倒计时
        time_left = self.visible_duration - (time.time() - self.show_time)
        if time_left > 0:
            timer_font = get_chinese_font(14)
            timer_text = timer_font.render(f"自动关闭: {time_left:.1f}秒", True, (200, 200, 200))
            panel_surface.blit(timer_text, (self.width - 150, 10))

        # 将面板绘制到主表面
        surface.blit(panel_surface, (0, self.y_position))

    def handle_click(self, pos):
        """处理鼠标点击 - 修复版本"""
        if not self.visible:
            return None

        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                # 设置按钮按下状态（短暂视觉反馈）
                self.button_states[button["action"]] = True
                pygame.time.set_timer(pygame.USEREVENT + hash(button["action"]) % 1000, 200)  # 200ms后重置

                if button["action"] == "hide_panel":
                    self.hide()
                return button["action"]
        return None


def main():
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("无人机灯光秀 - 模块化系统 v8")

    # 创建图案管理器
    pattern_manager = PatternManager("patterns")
    pattern_manager.discover_patterns()

    if not pattern_manager.available_patterns:
        print("错误：没有找到可用的图案！")
        return

    # 加载第一个图案（调试模式）
    current_pattern = pattern_manager.next_pattern(WIDTH, HEIGHT, debug_mode=True)

    if not current_pattern:
        print("错误：无法加载图案！")
        return

    # 创建控制面板（默认显示）
    control_panel = ControlPanel(WIDTH, HEIGHT)

    # 主循环变量
    clock = pygame.time.Clock()
    running = True
    auto_play = True  # 默认开启自动播放
    pattern_start_time = time.time()  # 图案开始时间

    # 主循环
    while running:
        current_time = time.time()
        dt = clock.tick(60) / 1000.0

        # 更新控制面板
        control_panel.update()

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # 处理键盘事件
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # 空格键切换控制面板显示状态
                    control_panel.toggle()
                    print(f"控制面板: {'显示' if control_panel.visible else '隐藏'}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 处理控制面板点击
                if event.button == 1:  # 左键
                    action = control_panel.handle_click(event.pos)
                    if action:
                        print(f"执行操作: {action}")
                        if action == "toggle_debug" and current_pattern:
                            # 切换调试模式 - 使用set_debug_mode方法
                            new_debug_mode = not current_pattern.debug_mode
                            if hasattr(current_pattern, 'set_debug_mode'):
                                current_pattern.set_debug_mode(new_debug_mode)
                            else:
                                # 备用方案
                                current_pattern.debug_mode = new_debug_mode
                                if new_debug_mode:
                                    current_pattern.buffer_surface = pygame.Surface(
                                        (WIDTH // 2, HEIGHT)).convert_alpha()
                                    current_pattern.final_surface = pygame.Surface((WIDTH // 2, HEIGHT)).convert_alpha()
                                else:
                                    current_pattern.buffer_surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
                                    current_pattern.final_surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
                            print(f"调试模式: {'开启' if new_debug_mode else '关闭'}")

                        elif action == "reload" and current_pattern:
                            # 重新加载当前图案
                            pattern_name = pattern_manager.available_patterns[pattern_manager.current_pattern_index]
                            current_pattern = pattern_manager.load_pattern(pattern_name, WIDTH, HEIGHT,
                                                                           debug_mode=current_pattern.debug_mode)
                            pattern_start_time = current_time  # 重置开始时间
                            print(f"重新加载图案: {pattern_name}")

                        elif action == "next_pattern":
                            # 切换到下一个图案
                            current_pattern = pattern_manager.next_pattern(WIDTH, HEIGHT,
                                                                           debug_mode=current_pattern.debug_mode if current_pattern else True)
                            pattern_start_time = current_time  # 重置开始时间

                        elif action == "toggle_auto":
                            # 切换自动播放
                            auto_play = not auto_play
                            pattern_start_time = current_time  # 重置开始时间
                            print(f"自动播放: {'开启' if auto_play else '关闭'}")

        # 自动播放逻辑 - 统一使用精确时间计算
        if auto_play and current_pattern and not control_panel.visible:
            pattern_elapsed = current_time - pattern_start_time

            # 获取图案的建议持续时间
            if hasattr(current_pattern, 'get_duration'):
                pattern_duration = current_pattern.get_duration()
            else:
                pattern_duration = 8.0  # 默认8秒

            # 检查图案是否应该结束
            if pattern_elapsed >= pattern_duration:
                current_pattern = pattern_manager.next_pattern(WIDTH, HEIGHT,
                                                               debug_mode=current_pattern.debug_mode if current_pattern else True)
                pattern_start_time = current_time  # 重置开始时间

        # 清空屏幕
        screen.fill((0, 0, 0))

        # 更新和绘制当前图案
        if current_pattern:
            # 统一使用精确时间差
            actual_dt = current_time - (pattern_start_time + current_pattern.frame_count / 60.0) if hasattr(
                current_pattern, 'frame_count') else dt

            # 更新图案
            if hasattr(current_pattern, 'update'):
                should_continue = current_pattern.update(actual_dt)
            else:
                should_continue = True

            # 绘制当前图案
            if current_pattern.debug_mode:
                if hasattr(current_pattern, 'draw_debug'):
                    current_pattern.draw_debug(screen)
            else:
                if hasattr(current_pattern, 'draw_final'):
                    current_pattern.draw_final(screen)

        # 绘制控制面板
        control_panel.draw(screen)

        # 显示状态信息
        font = get_chinese_font(16)
        controls = [
            "空格键: 显示/隐藏控制面板",
            "ESC: 退出程序"
        ]

        if current_pattern:
            pattern_elapsed = current_time - pattern_start_time
            if hasattr(current_pattern, 'get_duration'):
                pattern_duration = current_pattern.get_duration()
                remaining = max(0, pattern_duration - pattern_elapsed)
                controls.append(f"剩余时间: {remaining:.1f}s")

            controls.append(f"当前图案: {pattern_manager.available_patterns[pattern_manager.current_pattern_index]}")
            controls.append(f"调试模式: {getattr(current_pattern, 'debug_mode', 'N/A')}")
            controls.append(f"自动播放: {'开启' if auto_play else '关闭'}")

        # 根据控制面板是否显示调整位置
        y_offset = 10
        if control_panel.visible:
            y_offset = HEIGHT - control_panel.height - len(controls) * 30 - 10

        for i, text in enumerate(controls):
            rendered = font.render(text, True, (255, 255, 255))
            screen.blit(rendered, (WIDTH - 300, y_offset + i * 25))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


# __end__
