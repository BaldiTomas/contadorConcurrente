from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import os
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

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
    
    # Usar ThreadPoolExecutor para procesamiento concurrente
    with ThreadPoolExecutor() as executor:
        future_to_file = {}
        for file in files:
            file_path = os.path.join("/tmp", file.filename)
            file.save(file_path)  # Guarda el archivo
            future = executor.submit(count_words_in_file, file_path)
            future_to_file[future] = file.filename  # Mapea el futuro al nombre del archivo
        
        # Procesar resultados a medida que se completan
        for future in future_to_file:
            filename = future_to_file[future]
            try:
                word_count = future.result()
                results[filename] = word_count
            except Exception as e:
                results[filename] = str(e)

    # Devolver el conteo de palabras de cada archivo
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
