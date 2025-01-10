from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import hashlib
import os

app = Flask(__name__)

# Encoding function
def encode_to_10_digits(input_str):
    hash_obj = hashlib.sha256(input_str.encode())
    hash_digest = hash_obj.hexdigest()
    numeric_hash = int(hash_digest, 16)
    return str(numeric_hash % 10**10).zfill(10)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    input_data = request.form.get("input_data")
    if not input_data:
        return render_template('result.html', result="No input provided.")
    encoded_value = encode_to_10_digits(input_data)
    return render_template('result.html', result=f"Encoded Value: {encoded_value}")

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files.get("file")
    column_name = request.form.get("column_name")
    if not file or not column_name:
        return "File and column name are required", 400

    # Read and process CSV
    df = pd.read_csv(file)
    if column_name not in df.columns:
        return f"Column '{column_name}' not found in file", 400
    df[f"{column_name}_encoded"] = df[column_name].apply(encode_to_10_digits)

    # Save and return updated CSV
    output_path = "encoded_file.csv"
    df.to_csv(output_path, index=False)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
