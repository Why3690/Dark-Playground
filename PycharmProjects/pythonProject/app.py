from flask import Flask, render_template, request
from datetime import datetime
import random

app = Flask(__name__)

# 配置激励短语（英文和中文）
reminders_en = [
    "Life is short, don’t let procrastination be your default mode.",
    "Every week is precious, don't waste time procrastinating!",
    "Every decision you make today shapes the future you.",
    "You can choose to procrastinate or act now and make a change.",
    "What you do today determines your freedom tomorrow.",
    "The future belongs to those who act today. Don’t let procrastination stand in your way.",
    "Procrastination just makes time fly by faster.",
    "How many weeks do you have left to waste? Stop procrastinating now!",
    "Time waits for no one; seize today to secure your future.",
]

reminders_cn = [
    "人生短暂，不要让拖延成为你的常态。",
    "每一周都是宝贵的，不要浪费时间拖延！",
    "现在的每一个决定，决定了未来的你。",
    "你可以选择拖延，也可以选择现在行动，做出改变。",
    "今天做的事，决定你明天的自由。",
    "未来属于那些今天行动的人，别让拖延阻挡你。",
    "拖延只能让时间流逝得更快。",
    "你看看还有多少周可以浪费？不要再拖延了！",
]


# 计算已经度过的周数
def calculate_weeks_lived(birth_date):
    current_date = datetime.now()
    delta = current_date - birth_date
    return delta.days // 7


# 首页路由，显示表单和结果
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        birth_date_str = request.form.get("birth_date")
        language = request.form.get("language")

        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            weeks_lived = calculate_weeks_lived(birth_date)
            total_weeks = 88 * 52
            weeks_remaining = total_weeks - weeks_lived

            # 选择激励短语
            if language == "English":
                reminder = random.choice(reminders_en)
                result_text = f"You have lived {weeks_lived} weeks, approximately {weeks_remaining} weeks remaining."
            else:
                reminder = random.choice(reminders_cn)
                result_text = f"你已经度过了 {weeks_lived} 周，剩余大约 {weeks_remaining} 周。"

            return render_template("result.html", result_text=result_text, reminder=reminder)

        except ValueError:
            error = "请输入有效的出生日期 (格式: YYYY-MM-DD)" if language == "中文" else "Please enter a valid birth date (format: YYYY-MM-DD)"
            return render_template("index.html", error=error)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
