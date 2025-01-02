from transformers import AutoModelForCausalLM, AutoTokenizer

class ChatService:
    def __init__(self):
        self.model_name = "deepseek-ai/deepseek-v3"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            torch_dtype="auto"
        )

    def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_length=2048,
            temperature=0.7,
            top_p=0.95
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
