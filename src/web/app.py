# load the model
# load the data
# calc prediction
# serve prediction + actual values as json

from flask import Flask, jsonify, render_template
app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    '''renders the index template with json embedded as data attribute'''
    return render_template('index.html', measurements=[12, 13, 14, 15], predictions=[23, 24])


if __name__ == '__main__':
    app.run()
