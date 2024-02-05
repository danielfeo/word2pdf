from flask import Flask, request, jsonify
import subprocess
import base64
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    try:
        uploaded_file = request.files['file']
        input_file_path = '/app/' + uploaded_file.filename

        # Extract the filename and extension
        filename, extension = os.path.splitext(uploaded_file.filename)
        
        # Generate the output PDF filename based on the input filename
        output_file_path = f'/app/{filename}.pdf'

        # Save the uploaded file
        uploaded_file.save(input_file_path)

        # Execute the conversion command using subprocess
        command = f'soffice --convert-to pdf {input_file_path} --outdir /app'
        subprocess.run(command, shell=True)

        # Read the converted PDF file and encode it to base64
        with open(output_file_path, 'rb') as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

        # Delete the input and output files
        os.remove(input_file_path)
        os.remove(output_file_path)

        # Return the base64-encoded PDF
        return jsonify({"result": "success", "pdf_base64": base64_pdf})

    except Exception as e:
        return jsonify({"result": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
