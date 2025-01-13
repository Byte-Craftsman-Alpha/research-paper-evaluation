# Al for research paper analysis

This Al will analyze if the following research paper is suitable for publication or not and if suitable then most appropriate conference to submit this paper along with the reason to support its response.

### result.csv
| Paper ID | Publishable | Conference | Rationale |
|---|---|---|---|
| P001 | True | CVPR | The paper presents a novel approach to dron .... |
| P002 | False | NA | The paper is non-publishable due to its .... |
| P003 | False | NA | The paper incorporates elements of fantasy .... |
| P004 | True | NeurIPS | The paper introduces a novel concept of training-free .... |
| .... | .... | .... | .... |
| P135 | True | NeurIPS | The paper presents a novel decentralized stochastic .... |

## File  Structure
```
Innovation_Warehouse_KDSH_ROUND2.zip/ 
├── data/
│   ├── Papers/
│   │   ├── P001.pdf
│   │   ├── P002.pdf
│   │   └── ...
│   ├── R001.pdf
│   ├── R002.pdf
│   └── ...
├── Demo/
│   ├── pages/
│   │   └── index.html
│   ├── resources/
│   │   └── style.css
│   ├── app.log
│   └── app.py
├── main.py
├── Report.pdf
├── readme.md
└── result.csv
```
## Demo
> install the required dependencies
```bash
pip install -r requirements.txt
```
> run Flask server
```bash
cd Demo
python app.py
```
Now, open your browser and navigate to [localhost:5000](http://127.0.0.1:5000/), upload your paper and process it, see the `app.log` file for error and other logs. 

## Set Envirenment Variables
Open Environment Variable Editor
```bash
nano ~/.zshrc
```
Write the variable
```bash
export GOOGLE_API_KEY="YOUR API KEY"
```
Refresh Environment Variable
```bash
source ~/.zshrc
```
Varify it
```bash
echo $GOOGLE_API_KEY
```

## Code 
> Gemini LLM Modal

Before executing the code please read the Gemini API documentation for clear understanding
```python
class Gemini_Modal:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")) # Gemini API Key
        self.modal = genai.GenerativeModel("gemini-1.5-flash") # Model Name
        self.prompt = f"YOUR PROMPT" # Prompt for the evaluation of the paper
        
    def Evaluate(self, file_path: str, result_structure: object):
        with open(f"{file_path}", "rb") as doc_file: # Read File
            doc_data = base64.standard_b64encode(doc_file.read()).decode("utf-8")
        response = self.modal.generate_content(
            [{'mime_type': 'application/pdf', 'data': doc_data}, self.prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=result_structure,
            ),
        )
        return json.loads(response.text)
```
> Response 
```python
Response = {
    "publishable": True
    "reason": "REASON"
    "conference": "CONFERENCE"
}
```
