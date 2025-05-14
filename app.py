from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import easyocr
import re
app = Flask(__name__)
reader = easyocr.Reader(['pt', 'en'])

@app.route('/')
def index():
    return render_template('index.html')
import re

@app.route('/processar', methods=['POST'])
def processar():
    file = request.files['imagem']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    resultados = reader.readtext(img)
    textos = [text for (_, text, _) in resultados]

    # Regex para padrões de placa (ex: ABC1234 ou ABC1D23)
    placa_regex = r'\b([A-Z]{3}[0-9][A-Z0-9][0-9]{2})\b'

    placas_detectadas = []
    for texto in textos:
        match = re.search(placa_regex, texto.replace(" ", "").upper())
        if match:
            placas_detectadas.append(match.group(1))

    return jsonify({
        'placa': placas_detectadas[0] if placas_detectadas else "Placa não detectada",
        'textos': textos
    })


if __name__ == '__main__':
    app.run(debug=True)
