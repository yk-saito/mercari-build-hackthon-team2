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
images = pathlib.Path(__file__).parent.resolve() / "images"
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
            self.connection.commit()
        except Exception as e:
            sys.exit(e)

        return sql_result

    def __del__(self):
        try:
            self.connection.close()
        except Exception as e:
            sys.exit(e)

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def get_item():
    db = DBConnection()
    sql = "SELECT * FROM items"
    item_dict = {"items" : []}
    items = db.execute_select(sql)
    for i in range(len(items)):
            item_dict["items"].append({"id": items[i][0], "name": items[i][1], "category": items[i][2], "image_filename": items[i][3]})
    return item_dict

@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...), image: UploadFile = File(...)):
    image_title = pathlib.Path(image.filename).stem
    image_suffix = pathlib.Path(image.filename).suffix
    image_filename = hashlib.sha256(image_title.encode()).hexdigest() + image_suffix
    
    #画像を保存
    directory_name = "image"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    filepath = f"images/{image_filename}"
    with open(filepath, "w+b") as f:
        shutil.copyfileobj(image.file, f)

    #DB
    db = DBConnection()
    sql = "INSERT INTO items (name, category, image_filename) VALUES (?, ?, ?)"
    parameter = [name, category, image_filename]
    db.execute_insert(sql, parameter)
    return {"message": f"item received: {name}"}

@app.get("/items/{item_id}")
def search_item_by_id(item_id):
    db = DBConnection()
    sql = "SELECT name, category, image_filename AS items FROM items WHERE id=?"
    parameter = [item_id]
    item = db.execute_select(sql, parameter)
    return item


@app.get("/search")
def search_item(keyword: str):
    db = DBConnection()
    sql = "SELECT name, category, image_filename AS items FROM items WHERE name=?"
    parameter = [keyword]
    items = db.execute_select(sql, parameter)
    item_dict = {"items" : []}
    for i in range(len(items)):
            item_dict["items"].append({"id": items[i][0], "name": items[i][1], "category": items[i][2], "image_filename": items[i][3]})
    return item_dict
    


@app.get("/image/{items_image}")
async def get_image(items_image):
    db = DBConnection()
    # Create image path
    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    image_id = os.path.splitext(os.path.basename(items_image))[0]
    sql = "SELECT name, category, image_filename AS items FROM items WHERE id=?"
    parameter = [image_id]
    item = db.execute_select(sql, parameter)
    image = images /item[0][2]
    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
