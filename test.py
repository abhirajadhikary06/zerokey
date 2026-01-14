import requests

class GeminiProxyModel:
    def __init__(self, base_url, key_name, model="gemini-2.5-flash"):
        self.base_url = base_url.rstrip("/")
        self.key_name = key_name
        self.model = model

    def generate_content(self, prompt: str):
        response = requests.post(
            f"{self.base_url}/proxy/u/gemini/{self.key_name}",
            headers={
                "Authorization": f"Bearer apikey-gemini-{self.key_name}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json()


# Initialize the model (same pattern as genai.GenerativeModel)
model = GeminiProxyModel(
    base_url="http://localhost:8000",
    key_name="apiking",
    model="gemini-2.5-flash"
)


def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)

        # Gemini-compatible text extraction
        return (
            response["candidates"][0]
            ["content"]["parts"][0]["text"]
            .strip()
        )
    except Exception as e:
        return f"Error: {e}"


# Example usage
if __name__ == "__main__":
    question = input("Ask Gemini: ")
    answer = ask_gemini(question)
    print("\nAnswer:\n")
    print(answer)
