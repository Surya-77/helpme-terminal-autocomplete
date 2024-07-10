import os
from groq import Groq
import google.generativeai as genai

SYSTEM_INSTRUCTION = """
    You are a Linux command expert. Your sole purpose is to provide a single-line command that accomplishes the user's request.

    Format:

    Input: The user will provide a natural language description of a task they want to accomplish in Linux.
    Output: You will respond with a single, accurate, and actionable Linux command that fulfills the user's request.
    Example:

    Input: How do I list all files in the current directory?
    Output: ls
    Important Notes:

    Assume basic Linux knowledge: The user understands fundamental Linux concepts like directories, files, and commands.
    Prioritize brevity: The command should be as concise as possible.
    Avoid unnecessary complexity: If multiple commands can achieve the task, choose the simplest and most efficient one.
    Be specific: Ensure the command accurately reflects the user's request.
    Follow the prompt: Only provide the single-line command; do not offer explanations or additional information.
"""


class TerminalHelper:
    def __init__(
        self,
        api_provider: str = None,  # 'google-ai-studio' or 'groq-cloud'
        api_key: str = None,  # API key for the selected API provider
        model_name: str = None,  # Model name for the selected API provider
    ) -> None:
        self.api_provider = api_provider
        self.api_key = api_key
        self.model_name = model_name

    def setup_model(self) -> None:
        """Initialize the generative AI API with the API key from the .env file."""

        try:
            if self.api_provider == "google-ai-studio":
                self.api_key = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
                try:
                    genai.configure(api_key=self.api_key)
                except Exception as e:
                    print(
                        f"An error occurred during {self.api_provider} model initialization:\n{e}"
                    )
            elif self.api_provider == "groq-cloud":
                self.api_key = os.getenv("GROQ_API_KEY")
                pass
            else:
                print(
                    "Invalid API_PROVIDER. Please set the API_PROVIDER to 'google-ai-studio' or 'groq-cloud'."
                )
        except Exception as e:
            print(f"An error occurred during initialization:\n{e}")

    def setup_system_prompt(self) -> str:
        """Set the system prompt for the generative AI model."""

        return SYSTEM_INSTRUCTION

    def init_setup(self) -> None:
        self.setup_model()

    def list_available_models(self) -> None:
        """List all available models for generative AI."""

        if self.api_provider == "google-ai-studio":
            for model_card in genai.list_models():
                print(model_card)
        elif self.api_provider == "groq-cloud":
            print("Groq does not provide a list of available models.")
        else:
            print(
                "Invalid API_PROVIDER. Please set the API_PROVIDER to 'google-ai-studio' or 'groq-cloud'."
            )

    def generate(self, input_text: str) -> str:
        """Generate a Linux command based on the input text"""

        if self.api_provider == "google-ai-studio":
            try:
                model = genai.GenerativeModel(
                    model_name=self.model_name, system_instruction=SYSTEM_INSTRUCTION
                )
                response = model.generate_content(input_text)
                return response.text
            except Exception as e:
                return f"An error occurred during generation:\n{e}"
        elif self.api_provider == "groq-cloud":
            try:
                client = Groq(
                    api_key=self.api_key,
                )
                completion = client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": input_text},
                    ],
                    temperature=0.05,
                    max_tokens=128,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                return completion.choices[0].message.content
            except Exception as e:
                return f"An error occurred during generation:\n{e}"
