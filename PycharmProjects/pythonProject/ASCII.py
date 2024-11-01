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
        self.canvas.delete("animation")

    def _animate_initial_canvas(self):
        self.canvas.delete("animation")
        margin = 20
        inner_width = self.canvas.winfo_width() - 2 * margin
        inner_height = self.canvas.winfo_height() - 2 * margin

        if inner_width <= 0 or inner_height <= 0:
            self.canvas.after(100, self._animate_initial_canvas)
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
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black", tags="animation")

        self._fill_cells(new_margin_horizontal, new_margin_vertical, cell_size, rows, cols)
        self.draw_ascii_art()

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
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="animation")
            self.current_intensity += 1
            self.current_animation_id = self.canvas.after(30, self._fill_cells, margin_x, margin_y, cell_size, rows, cols)
        else:
            self.current_step += 1
            self.current_intensity = 0
            self.current_animation_id = self.canvas.after(30, self._fill_cells, margin_x, margin_y, cell_size, rows, cols)

    def restart_animation(self):
        self.current_step = 0
        self.current_intensity = 0
        self.animation_running = True
        self._animate_initial_canvas()

    @staticmethod
    def smooth_color_transition(start_color, end_color, step_count):
        start_r, start_g, start_b = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_r, end_g, end_b = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        color_steps = []
        for step in range(step_count + 1):
            r = int(start_r + (end_r - start_r) * (step / step_count))
            g = int(start_g + (end_g - start_g) * (step / step_count))
            b = int(start_b + (end_b - start_b) * (step / step_count))
            color_steps.append(f"#{r:02x}{g:02x}{b:02x}")
        return color_steps

    def draw_ascii_art(self):
        self.canvas.delete("welcome_text")  # 确保不会重叠，先删除已有的欢迎语
        ascii_art_list = [
            r"""
  ____  ____  __  ____  ____    ____  _  _  ____    ____   __   _  _  _   
 / ___)(  __)(  )(  __)(  __)  (_  _)/ )( \(  __)  (    \/ _\ ( \/ )( \  
 \___ \ ) _)  )(  ) _)  ) _)     )(  ) __ ( ) _)    ) D (/    \ )  / \_/  
 (____/(____)(__)(____)(____)   (__) \_)(_/(____)  (____/\_/\_/(__/  (_)  
            """,
            r"""
   ____    _           __  __         ___            __
  / __/__ (_)__ ___   / /_/ /  ___   / _ \___ ___ __/ /
 _\ \/ -_) /_ // -_) / __/ _ \/ -_) / // / _ `/ // /_/ 
/___/\__/_//__ /\__/  \__/_//_/\__/ /____/\_,_/\_, (_)  
                                             /___/     
            """,
            r"""
  ██████ ▓█████  ██▓▒███████▒▓█████    ▄▄▄█████▓ ██░ ██ ▓█████    ▓█████▄  ▄▄▄     ▓██   ██▓    ▐██▌ 
▒██    ▒ ▓█   ▀ ▓██▒▒ ▒ ▒ ▄▀░▓█   ▀    ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀    ▒██▀ ██▌▒████▄    ▒██  ██▒    ▐██▌ 
░ ▓██▄   ▒███   ▒██▒░ ▒ ▄▀▒░ ▒███      ▒ ▓██░ ▒░▒██▀▀██░▒███      ░██   █▌▒██  ▀█▄   ▒██ ██░    ▐██▌ 
  ▒   ██▒▒▓█  ▄ ░██░  ▄▀▒   ░▒▓█  ▄    ░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄    ░▓█▄   ▌░██▄▄▄▄██  ░ ▐██▓░    ▓██▒ 
▒██████▒▒░▒████▒░██░▒███████▒░▒████▒     ▒██▒ ░ ░▓█▒░██▓░▒████▒   ░▒████▓  ▓█   ▓██▒ ░ ██▒▓░    ▒▄▄  
▒ ▒▓▒ ▒ ░░░ ▒░ ░░▓  ░▒▒ ▓░▒░▒░░ ▒░ ░     ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░    ▒▒▓  ▒  ▒▒   ▓▒█░  ██▒▒▒     ░▀▀▒ 
░ ░▒  ░ ░ ░ ░  ░ ▒ ░░░▒ ▒ ░ ▒ ░ ░  ░       ░     ▒ ░▒░ ░ ░ ░  ░    ░ ▒  ▒   ▒   ▒▒ ░▓██ ░▒░     ░  ░ 
░  ░  ░     ░    ▒ ░░ ░ ░ ░ ░   ░        ░       ░  ░░ ░   ░       ░ ░  ░   ░   ▒   ▒ ▒ ░░         ░ 
      ░     ░  ░ ░    ░ ░       ░  ░             ░  ░  ░   ░  ░      ░          ░  ░░ ░         ░    
                    ░                                              ░                ░ ░             
            """,
            r"""
 ____                                   __    __                  ____                       __     
/\  _`\           __                   /\ \__/\ \                /\  _`\                    /\ \    
\ \ \L\_\     __ /\_\  ____      __    \ \ ,_\ \ \___      __    \ \ \L\ \     __     __  __\ \ \   
 \/_\__ \   /'__`\/\ \/\_,`\  /'__`\   \ \ \/\ \  _ `\  /'__`\   \ \ ,__/   /'__`\  /\ \/\ \\ \ \  
   /\ \L\ \/\  __/\ \ \/_/  /_/\  __/    \ \ \_\ \ \ \ \/\  __/    \ \ \/\  /\ \L\._\ \ \_\ \\ \_\ 
   \ `\____\ \____\\ \_/\____\ \____\    \ \__\\ \_\ \_\ \____\    \ \_\ \_\ \__/\_.\/`____ \ \_/_
    \/_____/\/____/ \/_/\/____/\/____/     \/__/ \/_/\/_/\/____/     \/___/  \/_/\/_/ `/___/> \/_/ 
                                                                                      /\___/    
                                                                                      \/__/     
            """,
            r"""
███████╗███████╗██╗███████╗███████╗    ████████╗██╗  ██╗███████╗    ██████╗  █████╗ ██╗   ██╗██╗
██╔════╝██╔════╝██║╚══███╔╝██╔════╝    ╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██╔══██╗╚██╗ ██╔╝██║
███████╗█████╗  ██║  ███╔╝ █████╗         ██║   ███████║█████╗      ██║  ██║███████║ ╚████╔╝ ██║
╚════██║██╔══╝  ██║ ███╔╝  ██╔══╝         ██║   ██╔══██║██╔══╝      ██║  ██║██╔══██║  ╚██╔╝  ╚═╝
███████║███████╗██║███████╗███████╗       ██║   ██║  ██║███████╗    ██████╔╝██║  ██║   ██║   ██╗
╚══════╝╚══════╝╚═╝╚══════╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝
            """
        ]

        selected_ascii_art = random.choice(ascii_art_list)
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 4,
                                text=selected_ascii_art, font=("Courier", 10), fill="black", anchor="center", tags="welcome_text")

class LifeWeeksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("人生周数提醒器")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # 定义初始状态
        self.user_birth_date = None
        self.weeks_lived = 0
        self.total_weeks = 88 * 52
        self.resize_in_progress = False
        self.current_language = "中文"
        self.font_size = "中"
        self.reminder_locked = False
        self.last_reminder = ""

        # 创建 UI 组件
        self.create_widgets()
        self.animation_manager = AnimationManager(self.canvas)

        # 延迟启动首页动画
        self.root.after(100, self.animation_manager.start_animation)
        # 自动更新激励短语
        self.update_reminder_text_if_unlocked()

    def create_widgets(self):
        # 第一行：包含所有按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(anchor="ne", padx=(10, 10), pady=(10, 5))  # 按钮的整体框架，靠右上并留有适当间距

        self.submit_button = tk.Button(button_frame, text="提交", command=self.on_submit)
        self.submit_button.pack(side="left", padx=(5, 10))

        self.home_button = tk.Button(button_frame, text="首页", command=self.back_to_home)
        self.home_button.pack(side="left", padx=(5, 5))

        self.language_button = tk.Button(button_frame, text="语言", command=self.switch_language)
        self.language_button.pack(side="left", padx=(5, 5))

        self.font_size_button = tk.Button(button_frame, text="字号", command=self.switch_font_size)
        self.font_size_button.pack(side="left", padx=(5, 5))

        # 第二行：包含出生日期输入框和标签
        birth_frame = tk.Frame(self.root)
        birth_frame.pack(pady=(5, 10))  # 留出适当的上下边距

        self.birth_label = tk.Label(birth_frame, text="请输入你的出生日期 (YYYY-MM-DD):", font=("微软雅黑", 14))
        self.birth_label.pack(side="left")

        self.birth_entry = tk.Entry(birth_frame, font=("微软雅黑", 14), width=15)
        self.birth_entry.pack(side="left", padx=(10, 0))

        # 提醒标签 (用于激励语句)
        self.reminder_label = tk.Label(self.root, text="", font=("微软雅黑", 18, "italic"), fg="#FF8C00")
        self.reminder_label.pack(pady=5)
        self.reminder_label.bind("<Button-1>", self.toggle_reminder_lock)

        # 用于显示格子的画布
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True, pady=(10, 10))
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

        # 结果标签
        self.result_label = tk.Label(self.root, text="", font=("微软雅黑", 14))
        self.result_label.pack(pady=5)

    def switch_font_size(self):
        if self.font_size == "小":
            self.font_size = "中"
        elif self.font_size == "中":
            self.font_size = "大"
        else:
            self.font_size = "小"
        self.update_ui_font_size()

    def update_ui_font_size(self):
        size_mapping = {"小": 10, "中": 14, "大": 18}
        current_size = size_mapping[self.font_size]

        # 更新各组件的字体大小
        self.birth_label.config(font=("微软雅黑", current_size))
        self.birth_entry.config(font=("微软雅黑", current_size))
        self.reminder_label.config(font=("微软雅黑", current_size + 4, "italic"))
        self.result_label.config(font=("微软雅黑", current_size))
        self.submit_button.config(font=("微软雅黑", current_size))
        self.home_button.config(font=("微软雅黑", current_size))
        self.language_button.config(font=("微软雅黑", current_size))
        self.font_size_button.config(font=("微软雅黑", current_size))

    def on_submit(self):
        birth_date_str = self.birth_entry.get()
        try:
            self.user_birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError:
            if self.current_language == "English":
                self.result_label.config(text="Please enter a valid birth date (format: YYYY-MM-DD)")
            else:
                self.result_label.config(text="请输入有效的出生日期 (格式: YYYY-MM-DD)")
            return

        self.animation_manager.stop_animation()
        current_date = datetime.now()
        self.weeks_lived = self.calculate_weeks_lived(self.user_birth_date, current_date)
        if self.canvas.winfo_width() == 1 and self.canvas.winfo_height() == 1:
            # 如果画布还没有正确初始化，则延迟调用 update_canvas
            self.canvas.after(100, self.update_canvas, self.weeks_lived, self.total_weeks)
        else:
            self.update_canvas(self.weeks_lived, self.total_weeks)

        if self.current_language == "English":
            self.result_label.config(text=f"You have lived {self.weeks_lived} weeks, approximately {self.total_weeks - self.weeks_lived} weeks remaining.")
        else:
            self.result_label.config(text=f"你已经度过了 {self.weeks_lived} 周，剩余大约 {self.total_weeks - self.weeks_lived} 周。")
        self.reminder_locked = False  # 提交后解锁提醒
        self.canvas.delete("welcome_text")  # 提交后清除欢迎语
        self.update_reminder_text_if_unlocked()

    def update_canvas(self, weeks_lived, total_weeks):
        self.canvas.delete("animation")
        margin = 20
        inner_width = self.canvas.winfo_width() - 2 * margin
        inner_height = self.canvas.winfo_height() - 2 * margin

        if inner_width <= 0 or inner_height <= 0:
            self.canvas.after(100, self.update_canvas, weeks_lived, total_weeks)
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
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="animation")

    def calculate_weeks_lived(self, birth_date, current_date):
        delta = current_date - birth_date
        return delta.days // 7

    def back_to_home(self):
        self.animation_manager.stop_animation()
        self.result_label.config(text="")
        self.reminder_locked = False  # 解锁提醒语，使得可以重新抽取新的欢迎语
        self.update_reminder_text_if_unlocked()
        self.animation_manager.start_animation()

    def switch_language(self):
        self.current_language = "English" if self.current_language == "中文" else "中文"
        self.update_ui_language()
        self.update_reminder_text_if_unlocked()

    def update_ui_language(self):
        if self.current_language == "English":
            self.root.title("Life Weeks Reminder")
            self.birth_label.config(text="Enter your birth date (YYYY-MM-DD):")
            self.submit_button.config(text="Submit")
            self.home_button.config(text="Home")
            self.language_button.config(text="Language")
            self.font_size_button.config(text="Font Size")
            self.reminder_label.config(text="Click on this reminder for motivational phrases.")
            self.result_label.config(text=f"You have lived {self.weeks_lived} weeks, approximately {self.total_weeks - self.weeks_lived} weeks remaining." if self.user_birth_date else "")
        else:
            self.root.title("人生周数提醒器")
            self.birth_label.config(text="请输入你的出生日期 (YYYY-MM-DD):")
            self.submit_button.config(text="提交")
            self.home_button.config(text="首页")
            self.language_button.config(text="语言")
            self.font_size_button.config(text="字号")
            self.reminder_label.config(text="点击此提醒以获得激励短语。")
            self.result_label.config(text=f"你已经度过了 {self.weeks_lived} 周，剩余大约 {self.total_weeks - self.weeks_lived} 周。" if self.user_birth_date else "")
        # 自动更新激励短语
        self.update_reminder_text_if_unlocked()

    def update_reminder_text(self):
        if self.current_language == "English":
            reminders = [
                "Life is short, don’t let procrastination be your default mode.",
                "Every week is precious, don't waste time procrastinating!",
                "Every decision you make today shapes the future you.",
                "You can choose to procrastinate or act now and make a change.",
                "What you do today determines your freedom tomorrow.",
                "The future belongs to those who act today. Don’t let procrastination stand in your way.",
                "Procrastination just makes time fly by faster.",
                "How many weeks do you have left to waste? Stop procrastinating now!",
                "Time waits for no one; seize today to secure your future.",
                "Stop putting it off, or these little boxes will just keep disappearing!",
                "Time keeps moving, and the progress bar of life won't wait for you. Take action now!",
                "If you keep procrastinating, even these little boxes can't wait any longer!",
                "What you do today changes your tomorrow. Don’t let procrastination hold you back.",
                "A small step every week adds up to huge achievements. Don’t procrastinate!",
                "Time slips away quickly, cherish every week and strive to be better!"
            ]
        else:
            reminders = [
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
            ]
        possible_reminders = [r for r in reminders if r != self.last_reminder]
        if possible_reminders:
            new_reminder = random.choice(possible_reminders)
            self.reminder_label.config(text=new_reminder)
            self.last_reminder = new_reminder

    def update_reminder_text_if_unlocked(self):
        if not self.reminder_locked:
            self.update_reminder_text()

    def toggle_reminder_lock(self, event):
        self.reminder_locked = not self.reminder_locked
        if self.reminder_locked:
            self.reminder_label.config(font=("微软雅黑", 18, "italic bold"))
        else:
            self.reminder_label.config(font=("微软雅黑", 18, "italic"))

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
