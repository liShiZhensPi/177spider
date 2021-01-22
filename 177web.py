import os
from flask import Flask, render_template
from flask.templating import render_template_string
import getComic

app = Flask(__name__)

@app.route('/comic/<name>')
def comic(name):
   return render_template(name)

@app.route('/download/<number>')
def download(number):
    name = "/".join(number.split("-"))
    getComic.download(name)
    return getComic.success

@app.route('/list')
def list():
    files = os.listdir('./templates')
    files.sort()
    # print(files)
      
    urls = []
    for file in files:
        urls.append("<p><a href=\"/comic/{0}\">{1}</a></p>".format(file,file))
    
    text1 = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>index</title>
</head>
<body>
"""
    text2 = """</body>
</html>"""
    return render_template_string(text1+" ".join(urls)+text2)

 

if __name__ == '__main__':
   app.run(host="0.0.0.0",port=80)