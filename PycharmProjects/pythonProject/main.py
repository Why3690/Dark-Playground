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
        self.color_transition_steps = self.smooth_color_transition("#FFFFFF", "#008000", 10)

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

        for row in range(rows):
            for col in range(cols):
                x1 = new_margin_horizontal + col * cell_size
                y1 = new_margin_vertical + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        self._fill_cells(new_margin_horizontal, new_margin_vertical, cell_size, rows, cols)

    def _fill_cells(self, margin_x, margin_y, cell_size, rows, cols):
        if not self.animation_running:
            return

        if self.current_step >= rows * cols:
            self.restart_animation()
            return

        row = self.current_step // cols
        col = self.current_step % cols
        x1 = margin_x + col * cell_size
        y1 = margin_y + row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        if self.current_intensity < len(self.color_transition_steps):
            color = self.color_transition_steps[self.current_intensity]
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            self.current_intensity += 1
            self.current_animation_id = self.canvas.after(30, self._fill_cells, margin_x, margin_y, cell_size, rows,
                                                          cols)
        else:
            self.current_step += 1
            self.current_intensity = 0
            self.current_animation_id = self.canvas.after(30, self._fill_cells, margin_x, margin_y, cell_size, rows,
                                                          cols)

    def restart_animation(self):
        self.current_step = 0
        self.current_intensity = 0
        self.animation_running = True
        self._animate_initial_canvas()

    @staticmethod
    def smooth_color_transition(start_color, end_color, step_count):
        start_r, start_g, start_b = tuple(int(start_color[i:i + 2], 16) for i in (1, 3, 5))
        end_r, end_g, end_b = tuple(int(end_color[i:i + 2], 16) for i in (1, 3, 5))
        color_steps = []
        for step in range(step_count + 1):
            r = int(start_r + (end_r - start_r) * (step / step_count))
            g = int(start_g + (end_g - start_g) * (step / step_count))
            b = int(start_b + (end_b - start_b) * (step / step_count))
            color_steps.append(f"#{r:02x}{g:02x}{b:02x}")
        return color_steps


class LanguageManager:
    def __init__(self):
        self.language = 'Chinese'
        self.translations = {
            'Chinese': {
                'title': "人生周数提醒器",
                'birth_label': "请输入你的出生日期 (YYYY-MM-DD):",
                'submit_button': "提交",
                'home_button': "首页",
                'language_button': "语言",
                'font_size_button': "字号",
                'reminders': [
                    "人生短暂，不要让拖延成为你的常态。",
                    "每一周都是宝贵的，不要浪费时间拖延！",
                    "现在的每一个决定，决定了未来的你。",
                    "你可以选择拖延，也可以选择现在行动，做出改变。",
                    "今天做的事，决定你明天的自由。",
                    "未来属于那些今天行动的人，别让拖延阻挡你。",
                    "拖延只能让时间流逝得更快。",
                    "你看看还有多少周可以浪费？不要再拖延了！",
                    "时间不会等待，抓住现在才能把握未来。",
                    "别再拖延了，否则这些小格子只能越来越少了！",
                    "时间在走，人生的进度条不会等你，赶快行动吧！",
                    "如果你总是拖延，连这些格子都等不及了！",
                    "今天的行动会改变你的明天，不要让拖延成为你前进的障碍。",
                    "每周一个小进步，累积起来就是巨大的成就，别拖延哦！",
                    "时间很快就溜走，珍惜每一周，让自己变得更好。"
                ],
                'result_text': "你已经度过了 {weeks_lived} 周，剩余大约 {weeks_remaining} 周。",
                'invalid_date': "请输入有效的出生日期 (格式: YYYY-MM-DD)"
            },
            'English': {
                'title': "Life Weeks Reminder",
                'birth_label': "Please enter your birth date (YYYY-MM-DD):",
                'submit_button': "Submit",
                'home_button': "Home",
                'language_button': "Language",
                'font_size_button': "Font Size",
                'reminders': [
                    "Life is short, don’t let procrastination be your norm.",
                    "Every week is precious, don't waste time procrastinating!",
                    "Every decision you make today shapes your future.",
                    "You can choose to procrastinate, or you can choose to act now and make a change.",
                    "What you do today determines your freedom tomorrow.",
                    "The future belongs to those who act today, don't let procrastination hold you back.",
                    "Every week you age a little more, procrastination only makes time pass faster.",
                    "How many 88-year weeks do you have to waste? Don't procrastinate!",
                    "Time doesn't wait, seize the moment to shape your future.",
                    "Stop procrastinating, or these squares will keep getting fewer!",
                    "Time is ticking, and the progress bar of life won't wait for you, take action now!",
                    "If you keep procrastinating, even these squares can’t wait any longer!",
                    "Today's actions will change your tomorrow, don't let procrastination be your barrier.",
                    "A small improvement each week will accumulate to great achievements, don't procrastinate!",
                    "Time slips away quickly, cherish each week, and make yourself better."
                ],
                'result_text': "You have lived {weeks_lived} weeks, approximately {weeks_remaining} weeks remaining.",
                'invalid_date': "Please enter a valid birth date (Format: YYYY-MM-DD)"
            }
        }

    def toggle_language(self):
        self.language = 'English' if self.language == 'Chinese' else 'Chinese'

    def get_translation(self, key):
        return self.translations[self.language][key]


class LifeWeeksApp:
    def __init__(self, root):
        self.root = root
        self.language_manager = LanguageManager()
        self.root.title(self.language_manager.get_translation('title'))
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        self.user_birth_date = None
        self.weeks_lived = 0
        self.total_weeks = 88 * 52
        self.resize_in_progress = False
        self.reminder_paused = False
        self.font_size = "medium"  # 默认字体大小为中等

        self.create_widgets()
        self.animation_manager = AnimationManager(self.canvas)
        self.root.after(100, self.animation_manager.start_animation)

    def create_widgets(self):
        # 顶部框架，包含按钮
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5, padx=10, anchor="n", fill="x")

        # 按钮框架在右上角
        button_frame = tk.Frame(top_frame)
        button_frame.pack(side="right")
        self.submit_button = tk.Button(button_frame, command=self.on_submit_click, font=("微软雅黑", 12))
        self.home_button = tk.Button(button_frame, command=self.back_to_home, font=("微软雅黑", 12))
        self.language_button = tk.Button(button_frame, command=self.toggle_language, font=("微软雅黑", 12))
        self.font_size_button = tk.Button(button_frame, command=self.toggle_font_size, font=("微软雅黑", 12))

        self.submit_button.pack(side="left", padx=5)
        self.home_button.pack(side="left", padx=5)
        self.language_button.pack(side="left", padx=5)
        self.font_size_button.pack(side="left", padx=5)

        # 出生日期输入框框架
        center_frame = tk.Frame(self.root)
        center_frame.pack(pady=5)

        self.birth_label = tk.Label(center_frame, font=("微软雅黑", 16))
        self.birth_entry = tk.Entry(center_frame, font=("微软雅黑", 16))
        self.birth_label.pack(side="left", padx=(0, 5))
        self.birth_entry.pack(side="left", padx=(0, 10))

        # 提醒标签
        self.reminder_label = tk.Label(self.root, font=("微软雅黑", 18, "italic"), fg="blue")
        self.reminder_label.pack(pady=(5, 10))
        self.reminder_label.bind("<Button-1>", self.toggle_reminder_pause)

        # 画布用于绘制格子
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

        # 结果标签
        self.result_label = tk.Label(self.root, font=("微软雅黑", 14))
        self.result_label.pack(pady=5)

        self.update_ui_texts()

    def update_ui_texts(self):
        self.root.title(self.language_manager.get_translation('title'))
        self.birth_label.config(text=self.language_manager.get_translation('birth_label'))
        self.submit_button.config(text=self.language_manager.get_translation('submit_button'))
        self.home_button.config(text=self.language_manager.get_translation('home_button'))
        self.language_button.config(text=self.language_manager.get_translation('language_button'))
        self.font_size_button.config(text=self.language_manager.get_translation('font_size_button'))

        if not self.reminder_paused:
            self.current_reminder = random.choice(self.language_manager.get_translation('reminders'))
            self.reminder_label.config(text=self.current_reminder)

    def calculate_weeks_lived(self, birth_date, current_date):
        delta = current_date - birth_date
        return delta.days // 7

    def on_submit_click(self):
        if not self.reminder_paused:
            self.current_reminder = random.choice(self.language_manager.get_translation('reminders'))
            self.reminder_label.config(text=self.current_reminder)

        birth_date_str = self.birth_entry.get()
        try:
            self.user_birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError:
            self.result_label.config(text=self.language_manager.get_translation('invalid_date'))
            return

        # 停止首页动画
        self.animation_manager.stop_animation()

        current_date = datetime.now()
        self.weeks_lived = self.calculate_weeks_lived(self.user_birth_date, current_date)
        weeks_remaining = self.total_weeks - self.weeks_lived
        self.result_label.config(
            text=self.language_manager.get_translation('result_text').format(weeks_lived=self.weeks_lived,
                                                                             weeks_remaining=weeks_remaining))
        self.update_canvas(self.weeks_lived, self.total_weeks)

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
        self.result_label.config(text="")
        self.user_birth_date = None
        self.weeks_lived = 0
        self.animation_manager.stop_animation()
        self.animation_manager.start_animation()
        if not self.reminder_paused:
            self.current_reminder = random.choice(self.language_manager.get_translation('reminders'))
            self.reminder_label.config(text=self.current_reminder)

    def toggle_reminder_pause(self, event):
        self.reminder_paused = not self.reminder_paused
        current_font = self.reminder_label.cget("font")
        font_family, font_size, *font_styles = current_font.split() if isinstance(current_font, str) else (
        "微软雅黑", 18, "italic")
        if self.reminder_paused:
            self.reminder_label.config(font=(font_family, int(font_size), "bold"), fg="red")
        else:
            self.reminder_label.config(font=(font_family, int(font_size), "italic"), fg="blue")

    def toggle_language(self):
        self.language_manager.toggle_language()
        self.update_ui_texts()
        if not self.reminder_paused:
            self.current_reminder = random.choice(self.language_manager.get_translation('reminders'))
            self.reminder_label.config(text=self.current_reminder)

    def toggle_font_size(self):
        if self.font_size == "small":
            self.font_size = "medium"
        elif self.font_size == "medium":
            self.font_size = "large"
        else:
            self.font_size = "small"

        # 更新字体大小并更新UI文本
        self.update_font_sizes()
        self.update_ui_texts()

    def update_font_sizes(self):
        font_sizes = {
            "small": ("微软雅黑", 12),
            "medium": ("微软雅黑", 16),
            "large": ("微软雅黑", 20)
        }

        size = font_sizes[self.font_size]

        # 按钮字体保持不变
        self.submit_button.config(font=("微软雅黑", 12))
        self.home_button.config(font=("微软雅黑", 12))
        self.language_button.config(font=("微软雅黑", 12))
        self.font_size_button.config(font=("微软雅黑", 12))

        # 其他组件字体随大小变化
        self.birth_label.config(font=size)
        self.birth_entry.config(font=size)
        reminder_font = (size[0], size[1] + 2 if size[1] > 12 else size[1], "italic") if not self.reminder_paused else (
        size[0], size[1] + 2 if size[1] > 12 else size[1], "bold")
        self.reminder_label.config(font=reminder_font)
        self.result_label.config(font=size)

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

