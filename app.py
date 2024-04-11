from flask import Flask, render_template, request, redirect, url_for, send_file
from googletrans import Translator
import re
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # 파일 저장
            filename = 'uploaded_file.txt'
            file.save(filename)
            
            # 번역
            translator = Translator()
            frequency = {}
            document_text = open(filename, 'rt' ,encoding="UTF-8")
            text_string = document_text.read().lower()
            match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
            for word in match_pattern:
                count = frequency.get(word, 0)
                frequency[word] = count + 1
            
            data = []
            for word, count in frequency.items():
                translation = translator.translate(word, dest='ko').text
                data.append({'단어': word, '번역': translation, '빈도수': count})
            
            df = pd.DataFrame(data)
            df.to_excel('translation_result.xlsx', index=False)
            
            # 파일 다운로드 링크 생성
            file_path = os.path.join(os.getcwd(), 'translation_result.xlsx')
            return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
