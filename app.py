from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Función para contar las palabras en un archivo
def count_words_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            word_count = len(text.split())
            return word_count
    except Exception as e:
        return str(e)

# Ruta para recibir archivos y contar palabras
@app.route('/count-words', methods=['POST'])
def count_words():
    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400
    files = request.files.getlist('files')

    if not files:
        return jsonify({"error": "No selected files"}), 400

    results = {}
    
    # Procesar cada archivo
    for file in files:
        file_path = os.path.join("/tmp", file.filename)
        file.save(file_path)
        word_count = count_words_in_file(file_path)
        results[file.filename] = word_count

    # Devolver el conteo de palabras de cada archivo
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)