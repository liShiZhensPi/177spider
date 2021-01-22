from flask import Flask, render_template
import getComic

app = Flask(__name__)

@app.route('/comic/<name>')
def comic(name):
   return render_template(name)

@app.route('/download/<number>')
def download(number):
    name = "/".join(number.split("-")[:-1])
    page_n = int(number.split("-")[-1])
    getComic.download(name,page_n)
    return getComic.success

if __name__ == '__main__':
   app.run(debug = True)