# 🤖 AI Master Quiz Generator

A powerful AI-powered quiz generation system integrated into the **Study Master Pro** platform. Generate unlimited multiple-choice quizzes (MCQs) on any topic using OpenAI's GPT models.

## ✨ Features

- **AI-Powered Quiz Generation**: Create unlimited quizzes on any topic
- **Customizable Difficulty Levels**: Easy, Intermediate, and Hard
- **Flexible Question Counts**: Generate 1-20 questions per quiz
- **Automatic Scoring**: AI-powered answer evaluation
- **Quiz History**: Track all generated quizzes and scores
- **Detailed Reviews**: View explanations for each question
- **Performance Analytics**: Track your learning progress
- **Beautiful UI**: Modern, responsive design with Bootstrap

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
# Navigate to your project directory
cd d:\python-main

# Install required packages
pip install -r requirements.txt
```

### 2. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy the key (it will only be shown once)

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and paste your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Save the file

**⚠️ Important Security Notes:**
- Never commit `.env` to version control
- Keep your API key secret
- Use `.gitignore` to exclude `.env` file

### 4. Update Database

The database schema will be automatically updated when the app starts. The `init_db()` function creates two new tables:

- `ai_generated_quizzes`: Stores all generated quizzes
- `ai_quiz_scores`: Stores student quiz attempts and scores

## 📖 Usage Guide

### Accessing the AI Quiz Generator

1. Start your Flask application:
   ```bash
   python database.py
   ```

2. Navigate to: `http://localhost:5000/ai-quiz-generator`

### Generating a Quiz

1. **Enter Topic**: Enter any subject or topic (e.g., "Python List Methods", "Cloud Computing", "Database Design")
2. **Select Difficulty**: Choose from Easy, Intermediate, or Hard
3. **Set Question Count**: Choose 1-20 questions
4. **Generate**: Click "Generate Quiz" and wait for AI to create your quiz

### Taking a Quiz

1. Click "Take This Quiz Now" after generation
2. Answer each question by selecting an option
3. Navigate between questions using Previous/Next buttons
4. Track time with the built-in timer
5. Submit your quiz
6. Review your results and explanations

### Viewing History

- Click "View Quiz History & Scores" to see:
  - All generated quizzes
  - Number of attempts per quiz
  - Average scores
  - Performance trends

## 🏗️ Project Structure

```
d:\python-main\
├── ai_quiz_generator.py          # Main AI generator module
├── database.py                   # Flask app with AI routes
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .env                          # Environment config (not in git)
├── myproject.db                  # SQLite database
├── templates/
│   ├── base.html                # Base template
│   ├── ai_quiz_generator.html    # Quiz generator page
│   ├── take_ai_quiz.html         # Quiz taking page
│   └── ai_quiz_history.html      # History/stats page
└── static/
    └── style.css                # Stylesheet
```

## 🔌 API Endpoints

### Generate Quiz
- **Endpoint**: `POST /api/generate-quiz`
- **Parameters**:
  - `topic` (string, required): Topic for the quiz
  - `num_questions` (int, 1-20): Number of questions
  - `difficulty` (string): "easy", "intermediate", or "hard"
- **Response**: JSON with quiz data and quiz_id

### Submit Quiz
- **Endpoint**: `POST /api/submit-quiz/<quiz_id>`
- **Parameters**:
  - `student_name` (string): Student name
  - `answers` (object): User answers mapped to question IDs
- **Response**: Score, percentage, and detailed results

### Routes
- `GET /ai-quiz-generator`: Main generator page
- `GET /ai-quiz/<quiz_id>`: Take a specific quiz
- `GET /ai-quiz-history`: View all quizzes and scores

## 🎯 Quiz Format

Each generated quiz includes:

```json
{
  "topic": "Python Programming Basics",
  "difficulty": "intermediate",
  "num_questions": 5,
  "questions": [
    {
      "id": 1,
      "question": "What is a Python list?",
      "options": [
        "An ordered collection of items",
        "A loop structure",
        "A conditional statement",
        "A function definition"
      ],
      "correct_answer": "An ordered collection of items",
      "explanation": "A Python list is an ordered, mutable collection...",
      "category": "Data Structures"
    }
  ]
}
```

## 💾 Database Schema

### ai_generated_quizzes
```sql
CREATE TABLE ai_generated_quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    difficulty TEXT DEFAULT 'intermediate',
    num_questions INTEGER DEFAULT 5,
    quiz_data TEXT NOT NULL,         -- JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT
)
```

### ai_quiz_scores
```sql
CREATE TABLE ai_quiz_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    score INTEGER DEFAULT 0,
    total_questions INTEGER,
    user_answers TEXT,               -- JSON format
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(quiz_id) REFERENCES ai_generated_quizzes(id)
)
```

## 🔧 Customization

### Modifying AI Quiz Generator

Edit `ai_quiz_generator.py` to customize:

```python
# Change the AI model
self.model = "gpt-4"  # or "gpt-3.5-turbo"

# Adjust temperature (creativity vs consistency)
temperature=0.7  # Range: 0.0-1.0

# Modify max tokens (response length)
max_tokens=2000
```

### Adding Custom Quiz Criteria

The `AIQuizGenerator` class has a method for custom quizzes:

```python
generator.generate_custom_quiz(
    topic="Python Programming",
    subtopics=["Lists", "Dictionaries", "Functions"],
    num_questions=10,
    difficulty="intermediate"
)
```

## 🚨 Troubleshooting

### API Key Error
```
ValueError: OpenAI API key not found
```
**Solution**: Ensure `.env` file exists and contains valid `OPENAI_API_KEY`

### Rate Limiting (429 Error)
**Solution**: Reduce number of questions or wait a moment before generating again

### Database Errors
```
sqlite3.OperationalError: database is locked
```
**Solution**: Close other connections to the database and try again

### Poor Quiz Quality
- Use more specific topics (e.g., "Python List Methods" instead of "Python")
- Try different difficulty levels
- Higher difficulty may take longer to generate

## 📊 Performance Tips

- **Reduce questions** for faster generation (1-5 questions)
- **Use specific topics** for better quality quizzes
- **Cache generated quizzes** if creating the same quiz multiple times
- **Batch operations** by generating multiple quizzes together

## 💰 Cost Considerations

OpenAI charges for API usage:
- **GPT-3.5 Turbo**: ~$0.0005 per 1K tokens (cheaper)
- **GPT-4**: ~$0.03 per 1K tokens (more capable)

A typical 5-question quiz uses ~200-300 tokens (~$0.0001)

## 🔐 Security Notes

1. **Never hardcode API keys** in your code
2. **Use .env files** with `.gitignore`
3. **Rotate API keys** regularly on OpenAI dashboard
4. **Monitor usage** on OpenAI dashboard
5. **Set spending limits** to prevent unexpected charges

## 📝 Integration with Existing App

The AI Quiz Generator is fully integrated with your Study Master Pro app:

1. **Database Integration**: Uses existing SQLite database
2. **Navigation**: Added to main navigation bar (optional - add link in base.html)
3. **Authentication**: Works with existing Flask session system
4. **Styling**: Inherits Bootstrap and custom CSS from base template

## 🎓 Use Cases

- **Student Practice**: Generate quizzes for any subject before exams
- **Teacher Creation**: Quickly create diverse question banks
- **Competitive Practice**: Track scores across multiple topics
- **Adaptive Learning**: Use difficulty levels to match skill level
- **Concept Review**: Generate quizzes on specific topics to review

## 🚀 Future Enhancements

Potential features to add:
- [ ] Question difficulty distribution analysis
- [ ] Time-based quiz mode
- [ ] Collaborative quizzes (multiple students)
- [ ] Export quizzes to PDF/Word
- [ ] Question bank management
- [ ] Detailed progress analytics
- [ ] Leaderboards
- [ ] Short answer questions support
- [ ] Image-based questions
- [ ] Custom branding

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review OpenAI API documentation: https://platform.openai.com/docs
3. Check Flask documentation: https://flask.palletsprojects.com/

## 📄 License

This AI Quiz Generator is part of Study Master Pro. Use according to your project's license.

## 🙏 Acknowledgments

- Built with **OpenAI GPT** for question generation
- Uses **Flask** for web framework
- Styled with **Bootstrap 5** for UI
- Database powered by **SQLite**

---

Happy studying! 🎓✨
