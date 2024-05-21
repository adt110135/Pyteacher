# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, session
import openai
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
openai.api_key = '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'

@app.route('/')
def home():
    return render_template('index.html', encoding='utf-8')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if 'message' not in data:
        return jsonify({'error': 'Message key not found'})

    user_message = data['message']

    system_responses = session.get('system_responses', [])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= system_responses + [
            {"role": "user", "content": user_message}
        ]
    )

    system_responses.append({"role": "user", "content": user_message})
    system_responses.append({"role": "system", "content": response.choices[0].message['content']})
    session['system_responses'] = system_responses

    return jsonify({'response': response.choices[0].message['content']})

@app.route('/quick-chat', methods=['POST'])
def quick_chat():
    system_responses = [
        {"role": "system", "content": "請幫我出一題數學問題"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=system_responses
    )

    return jsonify({'response': response.choices[0].message['content']})

@app.route('/switch-role', methods=['POST'])
def switch_role():
    data = request.get_json()
    if 'role' not in data:
        return jsonify({'error': 'Role key not found'})

    role = data['role']

    if role == '狗狗':
        system_responses = [
            {"role": "system", "content": "請在句首加上主人，結尾加上汪汪"}
        ]
    elif role == '媽媽':
        system_responses = [
            {"role": "system", "content":  "請在句首加上孩子，結尾尾加上乖乖"}
        ]
    elif role == '女僕':
        system_responses = [
            {"role": "system", "content": "現在請你扮演一個女僕類型的家教，請在回答的句首加上好的主人，句尾加上這樣可以嗎主人，每當出一個問題給我，在我回答正確後稱讚:您好棒喔主人；在我答錯問題，說完詳解後說沒關係的主人，加油呦!並且在我回答問題的時候不用加好的主人"}
        ]    
    else:
        return jsonify({'error': 'Invalid role'})

    session['system_responses'] = system_responses

    return jsonify({'message': 'Switched to ' + role + ' role'})

if __name__ == '__main__':
    app.run()



