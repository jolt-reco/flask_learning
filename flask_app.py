from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# フォームを表示するルート
@app.route("/")
def index():
    return render_template("input.html")   # templates/input.html を描画

# フォーム送信を受け取って CSV に保存するルート
@app.route("/add", methods=["POST"])
def add():
    item  = request.form["item"]          # フォームの name="item"
    price = request.form["price"]         # フォームの name="price"

    with open("item.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([item, price])

    return f"{item}（{price}円）を登録しました！"

# 実行条件
if __name__ == "__main__":
    app.run(debug=True)
