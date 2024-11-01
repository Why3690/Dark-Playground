import tkinter as tk
from datetime import datetime
import random

class AnimationManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.animation_running = False
        self.current_animation_id = None
        self.current_step = 0
        self.current_intensity = 0
        self.color_transition_steps = self.smooth_color_transition("#FFFFFF", "#008000", 10)  # 减少渐变步骤，加快速度

    def start_animation(self):
        if self.animation_running:
            return
        self.animation_running = True
        self.current_step = 0
        self.current_intensity = 0
        self._animate_initial_canvas()

    def stop_animation(self):
        self.animation_running = False
        if self.current_animation_id:
            self.canvas.after_cancel(self.current_animation_id)
        self.canvas.delete("all")

    def _animate_initial_canvas(self):
        self.canvas.delete("all")
        margin = 20
        inner_width = self.canvas.winfo_width() - 2 * margin
        inner_height = self.canvas.winfo_height() - 2 * margin

        if inner_width <= 0 or inner_height <= 0:
            return

        cols = 23
        rows = 1
        cell_size_width = inner_width / cols
        cell_size_height = inner_height / rows
        cell_size = min(cell_size_width, cell_size_height)

        new_margin_horizontal = (inner_width - (cols * cell_size)) / 2 + margin
        new_margin_vertical = (inner_height - (rows * cell_size)) / 2 + margin

        # 先绘制所有格子为白色
        for row in range(rows):
            for col in range(cols):
                x1 = new_margin_horizontal + col * cell_size
                y1 = new_margin_vertical + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        # 启动颜色渐变动画
        self._fill_cells(new_margin_horizontal, new_margin_vertical, cell_size, rows, cols)

    def _fill_cells(self, margin_x, margin_y, cell_size, rows, cols):
        if not self.animation_running:
            return

        if self.current_step >= rows * cols:
            self.restart_animation()  # 确保动画自动重启
            return

        row = self.current_step // cols
        col = self.current_step % cols
        x1 = margin_x + col * cell_size
        y1 = margin_y + row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        # 使用颜色渐变效果
        if self.current_intensity < len(self.color_transition_steps):
            color = self.color_transition_steps[self.current_intensity]
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            self.current_intensity += 1
            self.current_animation_id = self.canvas.after(30, self._fill_cells, margin_x, margin_y, cell_size, rows, cols)  # 加快渐变速度
        else:
            self.current_step += 1
            self.current_intensity = 0
            self.current_animation_id = self.canvas.after(30, self._fill_cells, margin_x, margin_y, cell_size, rows, cols)

    def restart_animation(self):
        self.current_step = 0
        self.current_intensity = 0
        self.animation_running = True
        self._animate_initial_canvas()  # 确保动画能够不断循环

    def smooth_color_transition(self, start_color, end_color, step_count):
        # 从开始颜色平滑过渡到结束颜色的函数，使用线性插值
        start_r, start_g, start_b = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_r, end_g, end_b = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        color_steps = []
        for step in range(step_count + 1):
            r = int(start_r + (end_r - start_r) * (step / step_count))
            g = int(start_g + (end_g - start_g) * (step / step_count))
            b = int(start_b + (end_b - start_b) * (step / step_count))
            color_steps.append(f"#{r:02x}{g:02x}{b:02x}")
        return color_steps

class LifeWeeksApp:
    # 在创建 LifeWeeksApp 类时，定义一组提醒语句
    reminder_messages = [
        "人生短暂，不要让拖延成为你的常态。",
        "每一周都是宝贵的，不要浪费时间拖延！",
        "现在的每一个决定，决定了未来的你。",
        "你可以选择拖延，也可以选择现在行动，做出改变。",
        "今天做的事，决定你明天的自由。",
        "未来属于那些今天行动的人，别让拖延阻挡你。",
        "每一周你都会老去一岁，拖延只能让时间流逝得更快。",
        "你有多少个88年的周可以浪费？不要再拖延了！",
        "时间不会等待，抓住现在才能把握未来。",
        "别再拖延了，否则这些小格子只能越来越少了！",
        "时间在走，人生的进度条不会等你，赶快行动吧！",
        "如果你总是拖延，连这些格子都等不及了！",
        "今天的行动会改变你的明天，不要让拖延成为你前进的障碍。",
        "每周一个小进步，累积起来就是巨大的成就，别拖延哦！",
        "时间很快就溜走，珍惜每一周，让自己变得更好。"
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("人生周数提醒器")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # 在类初始化时，随机选择一个提醒语句
        self.current_reminder = random.choice(self.reminder_messages)
        self.reminder_paused = False

        # 定义初始状态
        self.user_birth_date = None
        self.weeks_lived = 0
        self.total_weeks = 88 * 52
        self.resize_in_progress = False

        # 创建 UI 组件
        self.create_widgets()
        self.animation_manager = AnimationManager(self.canvas)

        # 延迟启动首页动画
        self.root.after(100, self.animation_manager.start_animation)

    def create_widgets(self):
        # 出生日期输入框
        birth_label = tk.Label(self.root, text="请输入你的出生日期 (YYYY-MM-DD):", font=("微软雅黑", 12))
        birth_label.pack(pady=5)
        self.birth_entry = tk.Entry(self.root, font=("微软雅黑", 12))
        self.birth_entry.pack(pady=5)

        # 将提交按钮和返回首页按钮放到右上角
        button_frame = tk.Frame(self.root)
        button_frame.place(relx=0.95, rely=0.05, anchor="ne")

        submit_button = tk.Button(button_frame, text="提交", command=self.on_submit_click, font=("微软雅黑", 12))
        submit_button.pack(side="left", padx=5)

        home_button = tk.Button(button_frame, text="首页", command=self.back_to_home, font=("微软雅黑", 12))
        home_button.pack(side="left", padx=5)

        # 提醒信息标签，位置调整到出生日期输入下方
        self.reminder_label = tk.Label(self.root, text=self.current_reminder, font=("微软雅黑", 14, "italic"), fg="blue")
        self.reminder_label.pack(pady=(10, 20))
        self.reminder_label.bind("<Button-1>", self.toggle_reminder_pause)

        # 用于显示格子的画布
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

        # 结果标签
        self.result_label = tk.Label(self.root, text="", font=("微软雅黑", 12))
        self.result_label.pack(pady=5)

    def calculate_weeks_lived(self, birth_date, current_date):
        delta = current_date - birth_date
        return delta.days // 7

    def on_submit_click(self):
        # 每次点击提交按钮时切换提醒语句（如果未暂停）
        if not self.reminder_paused:
            self.current_reminder = random.choice(self.reminder_messages)
            self.reminder_label.config(text=self.current_reminder)

        # 继续处理提交逻辑
        birth_date_str = self.birth_entry.get()
        try:
            self.user_birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError:
            self.result_label.config(text="请输入有效的出生日期 (格式: YYYY-MM-DD)")
            return

        self.animation_manager.stop_animation()
        current_date = datetime.now()
        self.weeks_lived = self.calculate_weeks_lived(self.user_birth_date, current_date)
        self.update_canvas(self.weeks_lived, self.total_weeks)
        self.result_label.config(text=f"你已经度过了 {self.weeks_lived} 周，剩余大约 {self.total_weeks - self.weeks_lived} 周。")

    def update_canvas(self, weeks_lived, total_weeks):
        self.canvas.delete("all")
        margin = 20
        inner_width = self.canvas.winfo_width() - 2 * margin
        inner_height = self.canvas.winfo_height() - 2 * margin

        if inner_width <= 0 or inner_height <= 0:
            return

        aspect_ratio = inner_width / inner_height
        total_cells = total_weeks

        best_rows, best_cols = 1, total_cells
        min_empty_space = float('inf')

        for rows in range(1, total_cells + 1):
            cols = (total_cells + rows - 1) // rows
            calculated_aspect_ratio = cols / rows
            empty_space = abs(calculated_aspect_ratio - aspect_ratio)

            if empty_space < min_empty_space:
                min_empty_space = empty_space
                best_rows, best_cols = rows, cols

        rows, cols = best_rows, best_cols
        cell_size_width = inner_width / cols
        cell_size_height = inner_height / rows
        cell_size = min(cell_size_width, cell_size_height)

        new_margin_horizontal = (inner_width - (cols * cell_size)) / 2 + margin
        new_margin_vertical = (inner_height - (rows * cell_size)) / 2 + margin

        for row in range(rows):
            for col in range(cols):
                week_index = row * cols + col
                if week_index >= total_weeks:
                    break
                x1 = new_margin_horizontal + col * cell_size
                y1 = new_margin_vertical + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = "#008000" if week_index < weeks_lived else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def back_to_home(self):
        self.animation_manager.stop_animation()
        self.result_label.config(text="")
        if not self.reminder_paused:
            self.current_reminder = random.choice(self.reminder_messages)
            self.reminder_label.config(text=self.current_reminder)
        self.animation_manager.start_animation()

    def toggle_reminder_pause(self, event):
        # 点击提醒标签时暂停或恢复切换
        self.reminder_paused = not self.reminder_paused
        if self.reminder_paused:
            self.reminder_label.config(font=("微软雅黑", 14, "bold"), fg="red")  # 加粗并更改颜色表示暂停状态
        else:
            self.reminder_label.config(font=("微软雅黑", 14, "italic"), fg="blue")  # 恢复正常状态

    def on_resize(self, event):
        if self.resize_in_progress:
            return
        self.resize_in_progress = True

        def complete_resize():
            self.resize_in_progress = False
            if self.animation_manager.animation_running:
                self.animation_manager.stop_animation()
                self.animation_manager.start_animation()
            elif self.user_birth_date:
                self.update_canvas(self.weeks_lived, self.total_weeks)

        self.canvas.after(100, complete_resize)

if __name__ == "__main__":
    root = tk.Tk()
    app = LifeWeeksApp(root)
    root.mainloop()
