"""
AI Quiz Generator Module
Generates multiple-choice quiz questions using OpenAI GPT
"""

import os
import json
import re
from openai import OpenAI
from typing import Dict, List, Optional


class AIQuizGenerator:
    """Generate MCQ quizzes using OpenAI GPT"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Quiz Generator
        
        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Please set OPENAI_API_KEY environment variable or pass it as argument."
            )
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
    
    def generate_quiz(
        self, 
        topic: str, 
        num_questions: int = 5,
        difficulty: str = "intermediate"
    ) -> Dict[str, any]:
        """
        Generate MCQ questions for a given topic
        
        Args:
            topic: Subject/topic for the quiz (e.g., "Python Programming")
            num_questions: Number of questions to generate (default: 5)
            difficulty: Question difficulty level - "easy", "intermediate", "hard"
        
        Returns:
            Dictionary containing generated quiz questions with answers and explanations
        """
        
        if difficulty not in ["easy", "intermediate", "hard"]:
            difficulty = "intermediate"
        
        prompt = f"""Generate {num_questions} multiple-choice questions about "{topic}" with {difficulty} difficulty level.

IMPORTANT: Format your response as VALID JSON (no markdown, no extra text) with this exact structure:
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "num_questions": {num_questions},
  "questions": [
    {{
      "id": 1,
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Explanation of why this is correct",
      "category": "subcategory"
    }}
  ]
}}

Rules:
- Each question must have exactly 4 options
- Options should be labeled as full text, not just letters
- Provide clear, educational explanations
- Questions should be relevant and progressively more challenging
- Ensure variety in question types
- Return ONLY valid JSON, no additional text"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator and quiz creator. Generate high-quality multiple-choice questions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                quiz_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from the response if it contains markdown code blocks
                json_match = re.search(r'\{[\s\S]*\}', response_text)
                if json_match:
                    quiz_data = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse quiz data from AI response")
            
            return {
                "success": True,
                "data": quiz_data,
                "message": f"Successfully generated {num_questions} questions about {topic}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error generating quiz: {str(e)}"
            }
    
    def generate_custom_quiz(
        self,
        topic: str,
        subtopics: List[str],
        num_questions: int = 10,
        difficulty: str = "intermediate"
    ) -> Dict[str, any]:
        """
        Generate a customized quiz with specific subtopics
        
        Args:
            topic: Main topic
            subtopics: List of specific areas to focus on
            num_questions: Total number of questions
            difficulty: Difficulty level
        
        Returns:
            Generated quiz with mixed questions from all subtopics
        """
        
        subtopics_str = ", ".join(subtopics)
        
        prompt = f"""Generate {num_questions} multiple-choice questions about "{topic}" focusing on these areas: {subtopics_str}.
Difficulty level: {difficulty}

IMPORTANT: Format as VALID JSON (no markdown):
{{
  "topic": "{topic}",
  "subtopics": {json.dumps(subtopics)},
  "difficulty": "{difficulty}",
  "num_questions": {num_questions},
  "questions": [
    {{
      "id": 1,
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Why this is correct",
      "category": "specific subtopic"
    }}
  ]
}}

Distribute questions evenly across subtopics. Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator. Generate high-quality, diverse multiple-choice questions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            response_text = response.choices[0].message.content.strip()
            
            try:
                quiz_data = json.loads(response_text)
            except json.JSONDecodeError:
                json_match = re.search(r'\{[\s\S]*\}', response_text)
                if json_match:
                    quiz_data = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse quiz data")
            
            return {
                "success": True,
                "data": quiz_data,
                "message": f"Successfully generated customized quiz for {topic}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error generating custom quiz: {str(e)}"
            }


def test_generator():
    """Test the quiz generator"""
    try:
        generator = AIQuizGenerator()
        print("✓ Initialized AI Quiz Generator")
        
        # Test basic quiz generation
        result = generator.generate_quiz(
            topic="Python Programming Basics",
            num_questions=3,
            difficulty="easy"
        )
        
        if result["success"]:
            print("✓ Successfully generated quiz")
            print(json.dumps(result["data"], indent=2))
        else:
            print(f"✗ Failed: {result['message']}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    test_generator()
