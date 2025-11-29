import pygame
import time
import math


def get_chinese_font(size=24):
    """获取支持中文的字体"""
    try:
        font_path = "C:/Windows/Fonts/simhei.ttf"
        return pygame.font.Font(font_path, size)
    except:
        return pygame.font.Font(None, size)


def create_linear_gradient_rect_with_alpha(width, height, start_color, end_color):
    """创建带Alpha通道的线性渐变矩形 - 修复渐变方向"""
    start_time = time.perf_counter()

    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # 修改：沿着高度方向（长边）进行渐变
    for y in range(height):
        # 计算当前位置的插值因子 - 沿着高度方向
        t = y / (height - 1) if height > 1 else 0

        # 插值计算颜色（包括Alpha通道）
        r = int(start_color[0] * (1 - t) + end_color[0] * t)
        g = int(start_color[1] * (1 - t) + end_color[1] * t)
        b = int(start_color[2] * (1 - t) + end_color[2] * t)
        a = int(start_color[3] * (1 - t) + end_color[3] * t)

        # 绘制水平线 - 沿着宽度方向
        pygame.draw.line(surface, (r, g, b, a), (0, y), (width, y))

    end_time = time.perf_counter()
    return surface, end_time - start_time


def test_copy_performance_with_alpha(surface, copy_count, display_surface=None):
    """测试带Alpha通道的复制性能"""
    start_time = time.perf_counter()

    # 如果提供了显示表面，就在上面绘制
    if display_surface is None:
        test_surface = pygame.Surface((1200, 750), pygame.SRCALPHA)
    else:
        test_surface = display_surface

    # 使用不同的位置和Alpha混合
    for i in range(copy_count):
        x = 100 + (i * 80) % 900
        y = 100 + (i * 60) % 500

        # 创建一个临时表面来应用不同的Alpha值
        temp_surface = surface.copy()
        alpha_value = 50 + (i * 20) % 205  # 变化的Alpha值
        temp_surface.fill((255, 255, 255, alpha_value), special_flags=pygame.BLEND_RGBA_MULT)

        test_surface.blit(temp_surface, (x, y))

    end_time = time.perf_counter()
    return end_time - start_time


def test_rotate_performance_with_alpha(surface, rotation_count, display_surface=None):
    """测试带Alpha通道的旋转性能"""
    start_time = time.perf_counter()

    # 如果提供了显示表面，就在上面绘制
    if display_surface is None:
        test_surface = pygame.Surface((1200, 750), pygame.SRCALPHA)
    else:
        test_surface = display_surface

    center_x, center_y = 600, 375

    for i in range(rotation_count):
        angle = i * 10  # 每次旋转10度
        rotated_surface = pygame.transform.rotate(surface, angle)

        # 计算旋转后的位置，使其围绕中心点
        radius = 200  # 增加半径，使矩形更长
        rad_angle = math.radians(angle)
        x = center_x + radius * math.cos(rad_angle) - rotated_surface.get_width() // 2
        y = center_y + radius * math.sin(rad_angle) - rotated_surface.get_height() // 2

        # 应用不同的Alpha值以观察混合效果
        alpha_surface = rotated_surface.copy()
        alpha_value = 100 + (i * 5) % 155  # 变化的Alpha值
        alpha_surface.fill((255, 255, 255, alpha_value), special_flags=pygame.BLEND_RGBA_MULT)

        test_surface.blit(alpha_surface, (x, y))

    end_time = time.perf_counter()
    return end_time - start_time


def main():
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((1200, 750))
    pygame.display.set_caption("Pygame Alpha通道性能测试 - 修复渐变方向")
    clock = pygame.time.Clock()
    font = get_chinese_font(24)

    # 测试参数 - 使用带Alpha通道的颜色
    gradient_width = 20  # 宽度可以小一些
    gradient_height = 300  # 高度保持较大值，渐变沿着高度方向
    start_color = (255, 0, 0, 255)  # 红色，完全不透明
    end_color = (0, 0, 255, 128)  # 蓝色，半透明

    # 存储测试结果
    test_results = []

    print("开始Alpha通道性能测试...")
    print("=" * 50)

    # ① 计时开始
    total_start_time = time.perf_counter()

    # ② 创建带Alpha通道的线性渐变矩形并计时
    print("步骤②: 创建带Alpha通道的线性渐变矩形...")
    gradient_surface, creation_time = create_linear_gradient_rect_with_alpha(
        gradient_width, gradient_height, start_color, end_color
    )
    test_results.append(("创建带Alpha渐变矩形", creation_time))
    print(f"  耗时: {creation_time:.6f} 秒")

    # 创建显示表面
    display_copy_alpha = pygame.Surface((1200, 750), pygame.SRCALPHA)
    display_rotate_alpha = pygame.Surface((1200, 750), pygame.SRCALPHA)

    # ④ 带Alpha通道复制10次并计时
    print("步骤④: 带Alpha通道复制10次...")
    copy_10_alpha_time = test_copy_performance_with_alpha(gradient_surface, 10, display_copy_alpha)
    test_results.append(("带Alpha复制10次", copy_10_alpha_time))
    print(f"  耗时: {copy_10_alpha_time:.6f} 秒")

    # ⑥ 带Alpha通道复制30次并计时
    print("步骤⑥: 带Alpha通道复制30次...")
    copy_30_alpha_time = test_copy_performance_with_alpha(gradient_surface, 30, display_copy_alpha)
    test_results.append(("带Alpha复制30次", copy_30_alpha_time))
    print(f"  耗时: {copy_30_alpha_time:.6f} 秒")

    # ⑧-⑩ 带Alpha通道旋转36次并计时
    print("步骤⑧-⑩: 带Alpha通道旋转36次(每次10度)...")
    rotate_alpha_time = test_rotate_performance_with_alpha(gradient_surface, 36, display_rotate_alpha)
    test_results.append(("带Alpha旋转36次", rotate_alpha_time))
    print(f"  耗时: {rotate_alpha_time:.6f} 秒")

    # 总耗时
    total_end_time = time.perf_counter()
    total_time = total_end_time - total_start_time
    test_results.append(("总耗时", total_time))

    print("=" * 50)
    print("Alpha通道性能测试完成!")
    print(f"总执行时间: {total_time:.6f} 秒")

    # 显示模式：0=结果，1=Alpha复制测试，2=Alpha旋转测试，3=清除屏幕
    display_mode = 0

    # 显示测试结果
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    display_mode = 0  # 结果显示
                elif event.key == pygame.K_2:
                    display_mode = 1  # Alpha复制测试显示
                elif event.key == pygame.K_3:
                    display_mode = 2  # Alpha旋转测试显示
                elif event.key == pygame.K_4:
                    display_mode = 3  # 清除屏幕

        screen.fill((20, 20, 40))

        if display_mode == 0:
            # 显示测试结果
            y_offset = 50
            title_font = get_chinese_font(36)
            title = title_font.render("Alpha通道性能测试结果", True, (255, 255, 255))
            screen.blit(title, (50, 20))

            for test_name, duration in test_results:
                text = font.render(f"{test_name}: {duration:.6f} 秒", True, (255, 255, 255))
                screen.blit(text, (50, y_offset))
                y_offset += 30

            # 显示渐变矩形示例
            screen.blit(gradient_surface, (50, 300))
            pygame.draw.rect(screen, (255, 255, 255), (50, 300, gradient_width, gradient_height), 1)

            # 显示渐变方向说明
            direction_text = font.render("渐变方向: 从上到下 (红色→蓝色)", True, (255, 255, 255))
            screen.blit(direction_text, (50, 320 + gradient_height))

            # 显示说明
            info_text = [
                "按 1: 显示测试结果",
                "按 2: 显示带Alpha复制测试效果",
                "按 3: 显示带Alpha旋转测试效果",
                "按 4: 清除屏幕绘图区",
                "ESC: 退出测试"
            ]

            for i, text in enumerate(info_text):
                rendered = font.render(text, True, (200, 200, 200))
                screen.blit(rendered, (50, 370 + gradient_height + i * 25))

        elif display_mode == 1:
            # 显示带Alpha复制测试效果
            title = font.render("带Alpha通道复制测试效果 (30次复制)", True, (255, 255, 255))
            screen.blit(title, (50, 20))
            screen.blit(display_copy_alpha, (0, 50))

            # 显示说明
            info_text = [
                "显示了30次带Alpha通道的复制操作",
                "每个矩形有不同的透明度",
                "注意观察重叠区域的混合效果",
                "渐变方向: 从上到下 (红色→蓝色)",
                "按 1: 返回测试结果",
                "按 4: 清除屏幕绘图区",
                "ESC: 退出测试"
            ]

            for i, text in enumerate(info_text):
                rendered = font.render(text, True, (200, 200, 200))
                screen.blit(rendered, (50, 500 + i * 25))

        elif display_mode == 2:
            # 显示带Alpha旋转测试效果
            title = font.render("带Alpha通道旋转测试效果 (36次旋转，每次10度)", True, (255, 255, 255))
            screen.blit(title, (50, 20))
            screen.blit(display_rotate_alpha, (0, 50))

            # 显示说明
            info_text = [
                "显示了36次带Alpha通道的旋转操作",
                "每个旋转矩形有不同的透明度",
                "注意观察中心区域的混合效果",
                "渐变方向: 沿着矩形长边 (红色→蓝色)",
                "按 1: 返回测试结果",
                "按 4: 清除屏幕绘图区",
                "ESC: 退出测试"
            ]

            for i, text in enumerate(info_text):
                rendered = font.render(text, True, (200, 200, 200))
                screen.blit(rendered, (50, 500 + i * 25))

        elif display_mode == 3:
            # 清除屏幕模式
            title = font.render("屏幕已清除", True, (255, 255, 255))
            screen.blit(title, (50, 20))

            # 绘制一个简单的清除指示
            pygame.draw.rect(screen, (100, 100, 100), (100, 100, 400, 300), 2)
            clear_text = font.render("绘图区域已清空", True, (200, 200, 200))
            screen.blit(clear_text, (150, 200))

            # 显示说明
            info_text = [
                "屏幕绘图区已清除",
                "按 1: 返回测试结果",
                "按 2: 重新显示带Alpha复制测试效果",
                "按 3: 重新显示带Alpha旋转测试效果",
                "ESC: 退出测试"
            ]

            for i, text in enumerate(info_text):
                rendered = font.render(text, True, (200, 200, 200))
                screen.blit(rendered, (50, 400 + i * 25))

        pygame.display.flip()

        # 检查按键退出
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()