import google.generativeai as genai
import google.generativeai as genai
import base64
import os
import json
import typing_extensions as typing
import csv


class Gemini_Modal:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY_RISHAB")) # Rishab's API Key
        self.modal = genai.GenerativeModel("gemini-1.5-flash") # Model Name
        # Prompt for the evaluation of the paper
        self.prompt = f'''Evaluate the research paper and classify it as either "Publishable" or "Non-Publishable" based on its content. Identify critical issues that affect its suitability for publication, such as inappropriate methodologies, incoherent arguments or unsubstantiated claims within 100 in single paragraph without any specific sybol, quotation mark or else. For example, a paper using poorly justified or unsuitable techniques, presenting disorganized or unclear arguments, or making unrealistically high claims without evidence should be deemed "Non-Publishable." Provide a clear reason to support the classification, citing specific issues or strengths of the paper. Include the exact paragraph(s) that illustrate these points. Additionally, if the paper is deemed "Publishable," suggest the most suitable conference for submission—EMNLP, CVPR, NeurIPS, or TMLR—based on its research area and scope. If no conference aligns with the paper’s context, classify it as "NA." Ensure the response is clear, concise, and well-supported.'''
        
    def Evaluate(self, file_path: str, result_structure: object):
        with open(f"{file_path}", "rb") as doc_file:
            doc_data = base64.standard_b64encode(doc_file.read()).decode("utf-8")
        response = self.modal.generate_content(
            [{'mime_type': 'application/pdf', 'data': doc_data}, self.prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=result_structure,
            ),
        )
        return json.loads(response.text)

class PaperEvaluation(typing.TypedDict):
    publishable: bool
    reason: str
    conference: str


LLM = Gemini_Modal()
result = LLM.Evaluate(f'data/Papers/P001.pdf', PaperEvaluation)
"""
[~] the valiable result is a dictionary with the following keys:
- publishable: a boolean value indicating whether the paper is publishable or not
- reason: a string containing the reason for the classification
- conference: a string containing the suggested conference for submission 
"""
print(result)

"""
# [+] for multiple papers in a directory
for dirpath, dirnames, filenames in os.walk(r"YOUR_DIRECTORY_PATH"):
    for filename in filenames:
        LLM = Gemini_Modal()
        result = LLM.Evaluate(f'{dirpath}/{filename}', PaperEvaluation)
        with open("YOUR_CSV_FILE.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=PaperEvaluation.keys())
            writer.writerow([filename, result["publishable"], result["conference"], result["reason"], result["reason"]])
print_filenames('your_directory_path')
"""

"""
Now process the result or save it to a file
"""