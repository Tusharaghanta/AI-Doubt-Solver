"""
Google Gemini AI Service Module
Handles API communication, system tutor instructions, and conversation context.
Uses the official Google Gen AI Python SDK (google-genai).
"""

import os
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Educational Tutor System Instruction
SYSTEM_INSTRUCTION = (
    "You are 'AI Doubt Solver', an expert, patient, and encouraging academic AI tutor. "
    "Your primary goal is to help students understand doubts clearly and thoroughly.\n\n"
    "Follow these educational guidelines:\n"
    "1. General Knowledge & Concepts: Explain concepts in simple, easy-to-understand language using analogies where helpful.\n"
    "2. Mathematics: Break problems down into clear, numbered step-by-step solutions, showing formulas and reasoning.\n"
    "3. Programming & Code: Provide clean, well-commented code snippets with syntax explanations and time/space complexity if relevant.\n"
    "4. Grammar & Spelling: Clearly point out the mistake, provide the corrected sentence, and explain the rule simply.\n"
    "5. Telugu <-> English Translation: Accurately translate between English and Telugu while preserving context, idioms, and natural tone.\n"
    "6. Essays & Summaries: Structure essays with introductions, body paragraphs, and conclusions. Use bullet points for summaries.\n"
    "7. Formatting: Always format output using clean Markdown (bold text, lists, and language-tagged code blocks) for easy reading."
)

class AIService:
    """Service class encapsulating Google Gemini API operations."""

    def __init__(self):
        # Read API key securely from environment variable
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
        self._client = None

    def _get_client(self) -> genai.Client:
        """Initializes and returns the Gemini client if API key is valid."""
        # Check if the key is missing or set to placeholder
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY is not configured! Please open your .env file "
                "and paste your valid Gemini API key from Google AI Studio."
            )

        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def generate_response(self, prompt: str, conversation_history: list = None) -> str:
        """
        Sends the user's prompt (with optional conversation history) to Gemini
        and returns the AI-generated text response.

        Args:
            prompt: The student's question or instruction.
            conversation_history: Optional list of past messages dicts:
                                  [{"role": "user", "text": "..."}, {"role": "model", "text": "..."}]

        Returns:
            str: Generated explanation/answer from Gemini.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        client = self._get_client()

        # Build message contents
        contents = []

        # If previous conversation turns exist, add them for multi-turn context
        if conversation_history:
            for message in conversation_history:
                role = "user" if message.get("role") == "user" else "model"
                text = message.get("text", "")
                if text:
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=text)]
                        )
                    )

        # Append current user prompt
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt.strip())]
            )
        )

        # Configure system instructions and parameters
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
        )

        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config,
            )
            
            if response.text:
                return response.text
            else:
                return "I received your question, but no text response was generated. Please try rephrasing your doubt."

        except APIError as e:
            # Handle official Gemini API errors (e.g. quota limits, invalid key)
            raise RuntimeError(f"Google Gemini API error: {e.message}") from e
        except Exception as e:
            # Catch other unexpected network or runtime issues
            raise RuntimeError(f"Error communicating with Gemini AI: {str(e)}") from e
