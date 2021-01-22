from flask import Flask, render_template

app = Flask(__name__)

@app.route('/comic/<name>')
def hello_name(name):
   return render_template(name)

if __name__ == '__main__':
   app.run(debug = True)