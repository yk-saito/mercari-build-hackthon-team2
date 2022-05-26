import os
import logging
import pathlib
import sqlite3
import hashlib
import shutil
import sys
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
 
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

class DBConnection:
    def __init__(self, dbpath="../db/mercari.sqlite3"):
        try:
            self.connection = sqlite3.connect(dbpath)
            self.cursor = self.connection.cursor()
            with open('../db/items.db') as f:
                self.cursor.executescript(f.read())
            self.connection.commit()
        except Exception as e:
            sys.exit(e)

    def execute_insert(self, sql, parameter=[]):
        try:
            self.cursor.execute(sql, parameter)
            self.connection.commit()
        except Exception as e:
            sys.exit(e)

    def execute_select(self, sql, parameter=[]):
        try:
            sql_result = self.cursor.execute(sql, parameter).fetchall()
            self.cursor.commit()
        except Exception as e:
            sys.exit(e)

        return sql_result

    def __del__(self):
        try:
            self.connection.close()
        except Exception as e:
            sys.exit(e)

db = DBConnection()

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def get_item():
    sql = "SELECT * FROM items"
    item_obj = db.execute_select(sql)
    return item_obj

@app.post("/items")
def add_item(name: str = Form(...), category_id: str = Form(...), image: UploadFile = File(...)):
    image_title = pathlib.Path(image.filename).stem
    image_suffix = pathlib.Path(image.filename).suffix
    image_filename = hashlib.sha256(image_title.encode()).hexdigest() + image_suffix
    
    #画像を保存
    filepath = f"../images/{image_filename}"
    with open(filepath, "w+b") as f:
        shutil.copyfileobj(image.file, f)

    #DB
    with sqlite3.connect("../db/mercari.sqlite3") as conn:
        #カーソル
        cur = conn.cursor()
        #テーブルがなければ作成
        cur.execute("CREATE TABLE IF NOT EXISTS items (\
            id INTEGER AUTO_INCREMENT, \
            name TEXT NOT NULL,\
            category_id INTEGER\
            image_filename TEXT NOT NULL\
            )")

        #受け取ったデータを追加
        #(?, ?, ?)はプレースホルダ
        cur.execute("INSERT INTO items (name, category_id, image_filename) VALUES (?, ?, ?)", (name, category_id, image_filename))
        #変更の反映
        conn.commit()

    return {"message": f"item received: {name}"}


@app.get("/search")
def search_item(keyword: str):
    
    with sqlite3.connect("../db/mercari.sqlite3") as conn:
        cur = conn.cursor()
        #データの取得
        cur.execute("SELECT name, category AS items FROM items WHERE name=?", (keyword,))
        item = cur.fetchall()
        item_dict = {"items" : []}
        for i in range(len(item)):
                item_dict["items"].append({"name": item[i][0], "category": item[i][1], "image_filename": item[i][2]})
        
    return item_dict
    


@app.get("/image/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image

    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
