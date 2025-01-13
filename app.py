from flask import Flask, send_from_directory, request
import google.generativeai as genai
import typing_extensions as typing
import json
import os
import logging


# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

genai.configure(
    api_key=os.environ.get("GOOGLE_API_KEY")
)
model = genai.GenerativeModel("gemini-1.5-flash")
prompt = f'''Evaluate the research paper and classify it as either "Publishable" or "Non-Publishable" based on its content. Identify critical issues that affect its suitability for publication, such as inappropriate methodologies, incoherent arguments, or unsubstantiated claims. For example, a paper using poorly justified or unsuitable techniques, presenting disorganized or unclear arguments, or making unrealistically high claims without evidence should be deemed "Non-Publishable." Provide a clear reason to support the classification, citing specific issues or strengths of the paper. Include the exact paragraph(s) that illustrate these points. Additionally, if the paper is deemed "Publishable," suggest the most suitable conference for submission—EMNLP, CVPR, NeurIPS, or TMLR—based on its research area and scope. If no conference aligns with the paper’s context, classify it as "NA." Ensure the response is clear, concise, and well-supported.'''

app = Flask(__name__)

class PaperEvaluation(typing.TypedDict):
    publishable: bool
    reason: str
    conference: str

@app.route('/')
def index():
    user_ip = request.remote_addr
    logging.info(f'User {user_ip} visited the homepage')
    return send_from_directory('pages', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    user_ip = request.remote_addr
    logging.info(f'User {user_ip} requested for a file accessed at {path}')
    return send_from_directory('.', path)

@app.route('/analyse', methods=['POST'])
def analyse():
    user_ip = request.remote_addr
    data = request.get_json()
    base64Data = data.get('pdfData')
    logging.info(f'User {user_ip} uploaded a file for evaluation')
    try:
        response = model.generate_content(
            [{'mime_type': 'application/pdf', 'data': base64Data}, prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=PaperEvaluation,
            ),
        )
        logging.info(f'[{user_ip}] Paper evaluation completed successfully with the following response: {response.text}')
        return {"message": 'Your paper has been thoroughly evaluated, and the results of the analysis are presented below.', "response": 200, "data": json.loads(response.text)}
    except Exception as e:
        print(e)
        logging.error(f'[{user_ip}] An error occurred while evaluating the paper. Error: {e}')
        return {"message": 'An error occurred while evaluating the paper. Please try again later.', "response": 500, "error": "Check logs for more details."}

if __name__ == '__main__':
    logging.info('Starting the application...')
    app.run(debug=True)