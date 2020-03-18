# coding=utf-8
from flask import Flask, render_template, request, jsonify
from KB_query.query_main import query_main

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('qa.html')


@app.route('/api/say_name', methods=['POST'])
def say_name():
    json = request.get_json()
    question = json['question']
    return_value = query_main(question)
    # last_name = json['last_name']
    return jsonify(question=return_value)


if __name__ == '__main__':
    app.run(host='0.0.0.0',  # 任何ip都可以访问
            port=7777,  # 端口
            debug=True
            )
