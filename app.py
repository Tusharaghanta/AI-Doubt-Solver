"""
AI Doubt Solver – Intelligent Question Answering Chatbot
Main Flask Application with Google Gemini Integration
"""

import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from services.ai_service import AIService

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "ai-doubt-solver-dev-secret-key-12345")

# Initialize Gemini AI service
ai_service = AIService()


@app.route("/", methods=["GET"])
def home():
    """Renders the chatbot user interface."""
    try:
        return render_template("index.html")
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to load user interface: {str(e)}"
        }), 500


@app.route("/ask", methods=["POST"])
def ask():
    """
    Receives user doubts, sends them to Google Gemini,
    and returns the AI-generated answer as JSON.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({
                "status": "error",
                "message": "Invalid request. Please provide JSON data with a 'question' field."
            }), 400

        user_question = data.get("question", "").strip()
        if not user_question:
            return jsonify({
                "status": "error",
                "message": "Question cannot be empty. Please enter your doubt."
            }), 400

        # Retrieve conversation history from session if available
        chat_history = session.get("chat_history", [])

        # Call the Gemini AI service
        ai_answer = ai_service.generate_response(
            prompt=user_question,
            conversation_history=chat_history
        )

        # Update session history (keep last 10 messages to manage context length)
        chat_history.append({"role": "user", "text": user_question})
        chat_history.append({"role": "model", "text": ai_answer})
        session["chat_history"] = chat_history[-10:]

        return jsonify({
            "status": "success",
            "question": user_question,
            "answer": ai_answer
        }), 200

    except ValueError as e:
        # Handles configuration errors such as missing GEMINI_API_KEY
        return jsonify({
            "status": "error",
            "error_type": "ConfigurationError",
            "message": str(e)
        }), 400

    except RuntimeError as e:
        # Handles API errors or connectivity issues
        return jsonify({
            "status": "error",
            "error_type": "AIModelError",
            "message": str(e)
        }), 502

    except Exception as e:
        # Handles unexpected server exceptions
        return jsonify({
            "status": "error",
            "error_type": "ServerError",
            "message": f"An unexpected server error occurred: {str(e)}"
        }), 500


@app.route("/reset", methods=["POST"])
def reset():
    """Clears conversation history from session."""
    try:
        session.pop("chat_history", None)
        return jsonify({
            "status": "success",
            "message": "Conversation history cleared successfully."
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to reset conversation: {str(e)}"
        }), 500


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
    print(" * Starting AI Doubt Solver Flask Server with Google Gemini...")
    print(" * Running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
