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

# 指定行のデータを編集
@app.route("/edit/<int:id>")
def edit(id):
    with open("item.csv", "r", encoding="utf-8")as f:
        reader = list(csv.reader(f)) # CSVのデータをリスト化
        if id < 0 or id >= len(reader):
            return "対象がありません", 404
        data = reader[id]
        item = data[0]
        price = data[1]
    return render_template("edit.html", id=id, item=item, price=price) 
    
@app.route("/update", methods=["POST"]) 
def update():
    item = request.form["item"]
    price = request.form["price"]
    id = int(request.form["id"])

    with open("item.csv", "r", encoding="UTF-8")as f:
        data = list(csv.reader(f))
    
    data[id] = [item, price]

    with open("item.csv", "w", newline="", encoding="UTF-8")as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    return redirect(url_for("list_items"))

# 実行条件
if __name__ == "__main__":
    app.run(debug=True)
