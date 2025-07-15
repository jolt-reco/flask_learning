from flask import Flask, render_template, request, redirect, url_for
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

# 入力内容が空だった場合、エラー表示
    if not item or not price:
        return render_template("input.html", error = "エラー: 入力してください")

    with open("item.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([item, price])
    
    return redirect(url_for("list_items"))

@app.route("/list")
def list_items():
    items = []
    try:
        with open("item.csv", "r", encoding="utf-8")as f:
            reader = csv.reader(f)
            items = list(reader)
    except FileNotFoundError:
        items = []
    return render_template("list.html", items=items)

# 実行条件
if __name__ == "__main__":
    app.run(debug=True)
