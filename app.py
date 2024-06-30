from flask import Flask, request, jsonify, render_template
import os
import PyPDF2
import google.generativeai as genai

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    qp_files = request.files.getlist('qp[]')

    qp_paths = []
    qp_texts = []

    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    for qp in qp_files:
        qp_path = os.path.join(upload_dir, qp.filename)
        qp.save(qp_path)
        qp_paths.append(qp_path)

        with open(qp_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            all_text = "\n".join(page.extract_text() for page in reader.pages)
            qp_texts.append(all_text)

    genai.configure(api_key="AIzaSyB0HeJ3JJBAU_LiwIsQcZVnIJUtiefY6JQ")

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=[])

    prompt = f"these are four question papers. Do analysis and give me 'most frequently asked questions', 'most important questions'. "
    for i, qp_text in enumerate(qp_texts):
        prompt += f"question paper {i+1}: '{qp_text}' "
    prompt += ". give the response in html code and in the response don't give any instrucions directly start the Most Frequently Asked Questions. don't add the full html boilerplatecode just start froma the inner body tags because i want to use the response as the innerHtml of div and don't include the body tag and strictly don't use '*' in the response and i want you to give response without any excuse. put it in a code tag"

    convo.send_message(prompt)
    result = convo.last.text
    
    for qp_path in qp_paths:
        os.remove(qp_path)

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)