"""
AI PDF Summarizer Module
Extracts text from PDFs, summarizes content, and generates practice questions
"""

import os
import json
import re
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
import PyPDF2
import pdfplumber


class PDFSummarizer:
    """Summarize PDF documents and generate practice questions using AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PDF Summarizer
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
    
    def extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, int]:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, num_pages)
        """
        extracted_text = ""
        num_pages = 0
        
        try:
            # Try with pdfplumber first (better for complex PDFs)
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            
            if not extracted_text.strip():
                # Fallback to PyPDF2 if pdfplumber didn't extract text
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    num_pages = len(reader.pages)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            extracted_text += text + "\n"
            
            return extracted_text, num_pages
            
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")
    
    def summarize_content(self, text: str, max_length: int = 500) -> Dict[str, any]:
        """
        Summarize PDF content using OpenAI
        
        Args:
            text: Extracted PDF text
            max_length: Maximum summary length in words
            
        Returns:
            Dictionary with summary and metadata
        """
        
        if not text.strip():
            return {
                'success': False,
                'message': 'No text found in PDF to summarize'
            }
        
        # Limit text for API (to avoid token limits)
        text_limit = text[:6000]  # ~1500 tokens
        
        prompt = f"""Analyze the following lecture notes/document and provide:

1. A concise summary (max {max_length} words)
2. List of 5-8 key points in bullet format
3. Main topics covered

Document Content:
{text_limit}

Provide response in this JSON format:
{{
  "summary": "detailed summary here",
  "key_points": ["point 1", "point 2", ...],
  "topics": ["topic 1", "topic 2", ...],
  "difficulty_level": "beginner/intermediate/advanced"
}}

Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator who creates clear, concise summaries of academic content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            response_text = response.choices[0].message.content.strip()
            
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                json_match = re.search(r'\{[\s\S]*\}', response_text)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse summary response")
            
            return {
                'success': True,
                'data': result,
                'message': 'Successfully summarized content'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error summarizing content: {str(e)}'
            }
    
    def generate_questions(
        self,
        text: str,
        summary: Dict,
        num_questions: int = 5
    ) -> Dict[str, any]:
        """
        Generate practice questions from PDF content
        
        Args:
            text: Extracted PDF text
            summary: Summary data from summarize_content
            num_questions: Number of questions to generate
            
        Returns:
            Dictionary with generated questions
        """
        
        text_limit = text[:4000]  # ~1000 tokens
        topics = summary.get('topics', [])
        key_points = summary.get('key_points', [])
        
        prompt = f"""Based on these lecture notes, generate {num_questions} multiple-choice practice questions.

Topics covered: {', '.join(topics)}
Key points:
{chr(10).join('- ' + kp for kp in key_points)}

Lecture notes excerpt:
{text_limit}

Generate questions that test understanding of the key concepts. Return as JSON:
{{
  "questions": [
    {{
      "id": 1,
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Why this is correct based on the lecture",
      "difficulty": "beginner/intermediate/advanced"
    }}
  ]
}}

Return ONLY valid JSON with exactly {num_questions} questions."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Create educational multiple-choice questions that test understanding of the provided material."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=2500
            )
            
            response_text = response.choices[0].message.content.strip()
            
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                json_match = re.search(r'\{[\s\S]*\}', response_text)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse questions")
            
            return {
                'success': True,
                'data': result,
                'message': f'Successfully generated {len(result.get("questions", []))} practice questions'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error generating questions: {str(e)}'
            }
    
    def process_pdf(
        self,
        pdf_path: str,
        num_questions: int = 5
    ) -> Dict[str, any]:
        """
        Complete PDF processing: extract, summarize, and generate questions
        
        Args:
            pdf_path: Path to PDF file
            num_questions: Number of practice questions to generate
            
        Returns:
            Complete processing result
        """
        
        try:
            # Extract text
            print("Extracting text from PDF...")
            text, num_pages = self.extract_text_from_pdf(pdf_path)
            
            if not text.strip():
                return {
                    'success': False,
                    'message': 'Could not extract text from PDF'
                }
            
            # Summarize content
            print("Summarizing content...")
            summary_result = self.summarize_content(text)
            
            if not summary_result['success']:
                return summary_result
            
            summary_data = summary_result['data']
            
            # Generate questions
            print("Generating practice questions...")
            questions_result = self.generate_questions(text, summary_data, num_questions)
            
            if not questions_result['success']:
                return questions_result
            
            return {
                'success': True,
                'data': {
                    'filename': os.path.basename(pdf_path),
                    'num_pages': num_pages,
                    'summary': summary_data,
                    'questions': questions_result['data']['questions'],
                    'text_preview': text[:500]
                },
                'message': 'PDF processed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error processing PDF: {str(e)}'
            }
    
    def save_upload(self, file_obj, upload_folder: str = 'uploads') -> Tuple[str, bool]:
        """
        Save uploaded PDF file
        
        Args:
            file_obj: Flask file object from request.files
            upload_folder: Folder to save uploads
            
        Returns:
            Tuple of (filepath, success)
        """
        
        try:
            # Create upload folder if it doesn't exist
            os.makedirs(upload_folder, exist_ok=True)
            
            # Secure filename
            filename = file_obj.filename
            if not filename.lower().endswith('.pdf'):
                return "", False
            
            filepath = os.path.join(upload_folder, filename)
            file_obj.save(filepath)
            
            return filepath, True
            
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return "", False


def test_summarizer():
    """Test the PDF summarizer"""
    print("Testing PDF Summarizer...")
    try:
        summarizer = PDFSummarizer()
        print("✓ Initialized PDF Summarizer")
        print("Ready to process PDFs!")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    test_summarizer()
