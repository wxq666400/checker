import os
from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)
df = pd.read_excel("scores.xlsx")  # 读取成绩表
df = df.replace({"√": "已提交", "×": "未提交"})
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    praise1 = ""  # 新增变量用于存储鼓励语
    praise2 = ''
    if request.method == "POST":
        input_name = request.form.get("name").strip()
        sid = request.form.get("sid").strip()

        if len(input_name) <= 3:
            matched = df[df["姓名"].apply(lambda full_name: full_name.startswith(input_name) and (len(full_name) <= 3 or full_name[:3] == input_name))]
        else:
            matched = df[df["姓名"] == input_name]

        student = matched[matched["学号"].astype(str) == sid]

        if not student.empty:
            row = student.iloc[0]
            scores = row.drop(labels=["姓名", "学号"])
            score_details = "<br>".join([f"{col}：{val}" for col, val in scores.items()])
            result = f"{row['姓名']}（学号: {sid}）的作业/非标小测提交情况如下：<br>{score_details}"

            # 判断是否鼓励
            submit_count = row.get("提交作业次数", 0)
            quiz_status = row.get("非标小测", "")
            if submit_count >= 10 and quiz_status == "已提交":
                praise1 = "🌟 你很棒，已交齐全部作业与非标小测！👍"
            else:
                praise2 = "请补齐作业或非标小测！！！"
        else:
            result = "未找到匹配的学生信息，请检查输入是否正确。"

    return render_template("index.html", result=result, praise1=praise1,praise2 = praise2)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 从环境变量读取端口
    app.run(host="0.0.0.0", port=port)
