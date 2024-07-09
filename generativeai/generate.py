import os
from dotenv import load_dotenv
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


def init_setup() -> None:
    """Initialize the generative AI API with the API key from the .env file."""

    load_dotenv()
    API_PROVIDER = os.getenv("API_PROVIDER")

    try:
        if API_PROVIDER == "google-ai-studio":
            API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
            try:
                genai.configure(api_key=API_KEY)
            except Exception as e:
                print(
                    f"An error occurred during {API_PROVIDER} model initialization:\n{e}"
                )
        elif API_PROVIDER == "groq-cloud":
            API_KEY = os.getenv("GROQ_API_KEY")
            try:
                genai.configure(api_key=API_KEY)
            except Exception as e:
                print(
                    f"An error occurred during {API_PROVIDER} model initialization:\n{e}"
                )
        else:
            print(
                "Invalid API_PROVIDER. Please set the API_PROVIDER to 'google-ai-studio' or 'groq-cloud'."
            )
    except Exception as e:
        print(f"An error occurred during initialization:\n{e}")


def list_available_models() -> None:
    """List all available models for generative AI."""

    load_dotenv()
    API_PROVIDER = os.getenv("API_PROVIDER")

    if API_PROVIDER == "google-ai-studio":
        for model_card in genai.list_models():
            print(model_card)
    elif API_PROVIDER == "groq-cloud":
        print("Groq does not provide a list of available models.")
    else:
        print(
            "Invalid API_PROVIDER. Please set the API_PROVIDER to 'google-ai-studio' or 'groq-cloud'."
        )


def generate(input_text: str, model_name: str = None) -> str:
    """Generate a Linux command based on the input text"""

    load_dotenv()
    API_PROVIDER = os.getenv("API_PROVIDER")

    if API_PROVIDER == "google-ai-studio":
        API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
        model_name = "gemini-1.5-flash"
        try:
            model = genai.GenerativeModel(
                model_name=model_name, system_instruction=SYSTEM_INSTRUCTION
            )
            response = model.generate_content(input_text)
            return response.text
        except Exception as e:
            return f"An error occurred during generation:\n{e}"
    elif API_PROVIDER == "groq-cloud":
        API_KEY = os.getenv("GROQ_API_KEY")
        model_name = "llama3-70b-8192"
        try:
            client = Groq(
                api_key=API_KEY,
            )
            completion = client.chat.completions.create(
                model=model_name,
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
