import torch
print(torch.__version__)

# This is the information from the parsed document
text ="""
[Document(id_='26d484af-7a7a-4c5d-97e1-6e638a922778', embedding=None, metadata={'file_path': '/mnt/c/Users/Vijay/Desktop/biohack25/sample-pdfs/sample_ehr.pdf', 'file_name': 'sample_ehr.pdf', 'file_type': 'application/pdf', 'file_size': 1677, 'creation_date': '2025-03-01', 'last_modified_date': '2025-03-01'}, excluded_embed_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'], excluded_llm_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'], relationships={}, metadata_template='{key}: {value}', metadata_separator='\n', text_resource=MediaResource(embeddings=None, data=None, text='# De-identified Electronic Health Record (EHR)\n\n# Patient Information\n\nPatient ID: 123456789\n\nDate of Birth: 1985-07-12\n\nGender: Male\n\nEthnicity: Not Disclosed\n\nDate of Visit: 2025-02-28\n\n# Medical History\n\n1. Hypertension\n2. Type 2 Diabetes\n3. Hyperlipidemia\n4. No known drug allergies\n\n# Diagnoses\n\n1. Essential Hypertension (I10)\n2. Type 2 Diabetes Mellitus without complications (E11.9)\n\n# Medications\n\n1. Lisinopril 10 mg - Once daily\n2. Metformin 500 mg - Twice daily\n3. Atorvastatin 20 mg - Once daily\n\n# Recent Laboratory Results\n\n|HbA1c|6.8% (Slightly elevated)|\n|---|---|\n|Blood Pressure|130/85 mmHg|\n|LDL Cholesterol|110 mg/dL (Borderline High)|\n|Serum Creatinine|1.1 mg/dL (Normal)|', path=None, url=None, mimetype=None), image_resource=None, audio_resource=None, video_resource=None, text_template='{metadata_str}\n\n{content}')]
"""


from transformers import LlamaForCausalLM, LlamaTokenizer

# Load the model and tokenizer
model_name = "meta-llama/Llama-2-7b-hf"  # Example model from Hugging Face
model = LlamaForCausalLM.from_pretrained(model_name)
tokenizer = LlamaTokenizer.from_pretrained(model_name)

question = "How much Metformin do I take and how often?"
input_text = text + "\n\n" + question

# Tokenize the input
inputs = tokenizer(text, return_tensors="pt")

# Generate output from Llama model
output = model.generate(**inputs, max_length=500)

# Decode the output and interpret
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
print(decoded_output)