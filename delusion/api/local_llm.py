from openai import OpenAI


class LocalLLM:
    def __init__(self, model: str, base_url: str, api_key="not-needed"):
        self.model = model
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def response(self, message, **hyperparam):
        response = self.client.chat.completions.create(
            model=self.model, messages=message, stream=False, **hyperparam
        )
        return response.choices[0].message.content
