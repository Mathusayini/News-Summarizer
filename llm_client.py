from openai import OpenAI

class LLM:
    def __init__(self, api_key="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"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = "qwen/qwen-2.5-72b-instruct:free"
    
    def ask(self, prompt):
        """Send a prompt to the AI and return the response"""
        completion = self.client.chat.completions.create(
            extra_body={},
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    bot = LLM()
    response = bot.ask("What is the meaning of life?")
    print(response)