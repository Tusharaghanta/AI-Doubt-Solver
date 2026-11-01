"""
Unit tests for AI Doubt Solver
Stage 4: Gemini API Integration & Error Handling
"""

import unittest
from unittest.mock import patch
from app import app

class GeminiIntegrationTestCase(unittest.TestCase):
    """Test suite for Flask endpoints and Gemini integration."""

    def setUp(self):
        """Set up test client."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page(self):
        """Verify the index page renders with HTTP 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_empty_question_returns_400(self):
        """Verify submitting an empty question returns 400."""
        response = self.client.post("/ask", json={"question": "   "})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["status"], "error")
        self.assertIn("Question cannot be empty", data["message"])

    def test_missing_json_payload_returns_400(self):
        """Verify submitting non-JSON returns 400."""
        response = self.client.post("/ask", data="plain text", content_type="text/plain")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["status"], "error")

    @patch("services.ai_service.AIService.generate_response")
    def test_successful_gemini_response(self, mock_generate):
        """Verify valid question returns AI answer successfully."""
        mock_generate.return_value = "Python is a high-level programming language."
        
        response = self.client.post("/ask", json={"question": "What is Python?"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["answer"], "Python is a high-level programming language.")

    @patch("services.ai_service.AIService.generate_response")
    def test_missing_api_key_configuration_error(self, mock_generate):
        """Verify friendly error message when GEMINI_API_KEY is not configured."""
        mock_generate.side_effect = ValueError("GEMINI_API_KEY is not configured!")
        
        response = self.client.post("/ask", json={"question": "Test question"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error_type"], "ConfigurationError")
        self.assertIn("GEMINI_API_KEY is not configured", data["message"])

    @patch("services.ai_service.AIService.generate_response")
    def test_gemini_api_error_handling(self, mock_generate):
        """Verify friendly error message when Gemini API raises an exception."""
        mock_generate.side_effect = RuntimeError("Google Gemini API error: Quota exceeded")
        
        response = self.client.post("/ask", json={"question": "Test question"})
        self.assertEqual(response.status_code, 502)
        data = response.get_json()
        self.assertEqual(data["error_type"], "AIModelError")
        self.assertIn("Quota exceeded", data["message"])

    def test_reset_route(self):
        """Verify /reset route successfully clears session."""
        response = self.client.post("/reset")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")

if __name__ == "__main__":
    unittest.main()
