# 📄 AI PDF Summarizer

An intelligent PDF processing system that automatically summarizes lecture notes, extracts key concepts, and generates practice questions using OpenAI's GPT models.

## ✨ Features

### Core Functionality
- **PDF Upload & Processing**: Drag-and-drop or click to upload PDF files (up to 25MB)
- **Intelligent Summarization**: AI-powered summaries of PDF content
- **Key Points Extraction**: Automatic identification of important concepts
- **Topic Detection**: Categorization of covered topics
- **Auto-Generated Questions**: Multiple-choice practice questions based on content
- **Difficulty Assessment**: Automatic difficulty level detection (Easy/Intermediate/Hard)

### User Experience
- **Multi-Tab Interface**: Browse Summary, Key Points, Topics, and Questions
- **Practice Quiz Mode**: Take MCQ quizzes on extracted content
- **Instant Scoring**: Get immediate feedback on quiz performance
- **Answer Review**: See explanations for each question
- **Summary Management**: View history of all processed PDFs
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Installation

### 1. Install Dependencies

```bash
cd d:\python-main
pip install -r requirements.txt
```

**New packages added:**
- `PyPDF2==4.0.1` - PDF reading
- `pdfplumber==0.10.3` - Advanced PDF text extraction

### 2. Setup is Already Complete
The database tables and routes are automatically created when the app starts.

## 📖 Usage Guide

### Accessing the PDF Summarizer

1. **Start your Flask app:**
   ```bash
   python database.py
   ```

2. **Navigate to PDF Summarizer:**
   - Click "📄 PDF Summary" in the navigation bar
   - Or go to: `http://localhost:5000/pdf-summarizer`

### Processing a PDF

#### Step 1: Upload PDF
- Click on the drop zone or drag a PDF file
- Select number of practice questions (1-20, default: 5)
- Click "Process PDF"

#### Step 2: View Summary
The system automatically:
- Extracts text from all PDF pages
- Generates a concise summary
- Identifies key points
- Detects main topics
- Determines difficulty level

#### Step 3: Review Content
Use tabs to browse:
- **📝 Summary**: Full AI-generated summary
- **🔑 Key Points**: Bulleted important concepts
- **📚 Topics**: Main subjects covered
- **❓ Questions**: Practice MCQs

#### Step 4: Practice
- Answer all multiple-choice questions
- Submit to get instant score
- Review answers with explanations
- Retake anytime

### Manage Summaries
- Click "📊 View My PDF Summaries" to see all processed PDFs
- View statistics on total PDFs, pages, and questions
- Access any summary to review or practice

## 🏗️ Project Structure

```
d:\python-main\
├── pdf_summarizer.py                # AI PDF processing module
├── database.py                      # Flask app with PDF routes
├── requirements.txt                 # Dependencies (includes PyPDF2, pdfplumber)
├── uploads/                         # Uploaded PDF storage
├── myproject.db                     # SQLite database
├── templates/
│   ├── pdf_summarizer.html         # Upload interface
│   ├── view_summary.html           # Summary & practice view
│   └── pdf_summaries_list.html     # Summaries list
└── static/
    └── style.css                    # Stylesheet
```

## 💾 Database Schema

### pdf_summaries
```sql
CREATE TABLE pdf_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    original_filename TEXT,
    num_pages INTEGER DEFAULT 0,
    summary_text TEXT,
    key_points TEXT,                 -- JSON array
    topics TEXT,                      -- JSON array
    difficulty_level TEXT,
    upload_path TEXT,
    uploaded_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### pdf_questions
```sql
CREATE TABLE pdf_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    summary_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    options TEXT,                     -- JSON array
    correct_answer TEXT,
    explanation TEXT,
    difficulty TEXT,
    question_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(summary_id) REFERENCES pdf_summaries(id)
)
```

### pdf_question_attempts
```sql
CREATE TABLE pdf_question_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    user_answer TEXT,
    is_correct INTEGER DEFAULT 0,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(question_id) REFERENCES pdf_questions(id)
)
```

## 🔌 API Endpoints

### Upload & Process PDF
- **Endpoint**: `POST /api/upload-pdf`
- **Parameters**:
  - `pdf_file` (file, required): PDF file to upload
  - `num_questions` (int, 1-20): Questions to generate
- **Response**: JSON with summary_id and processing results

### Submit Practice Answers
- **Endpoint**: `POST /api/submit-pdf-questions/<summary_id>`
- **Parameters**:
  - `student_name` (string): Student name
  - `answers` (object): Answers mapped to question IDs
- **Response**: Score, percentage, and detailed results

### Routes
- `GET /pdf-summarizer` - Main upload page
- `GET /pdf-summary/<summary_id>` - View summary & practice
- `GET /pdf-summaries-list` - View all summaries

## 🤖 How AI Processing Works

### Text Extraction
The system uses two methods for robust extraction:
1. **pdfplumber** - Advanced text extraction (primary)
2. **PyPDF2** - Fallback extraction method

### Summarization Process
1. Extract text from all PDF pages
2. Send to OpenAI with system prompt for educational context
3. AI generates:
   - Concise summary (max 500 words)
   - 5-8 key points
   - Main topics
   - Difficulty level assessment

### Question Generation
1. Use document content and summary as context
2. Generate MCQs focused on key concepts
3. Each question includes:
   - 4 multiple-choice options
   - Correct answer
   - Educational explanation
   - Difficulty rating

## ⚙️ Configuration

### PDF Processing Settings
Edit `pdf_summarizer.py` to customize:

```python
# Maximum text for API (tokens)
text_limit = text[:6000]  # ~1500 tokens

# Summary parameters
max_length = 500  # words
temperature = 0.7  # 0.0-1.0 (creativity)

# Questions parameters
num_questions = 5  # default
max_tokens = 2500  # response length
```

### AI Model Selection
```python
# In PDFSummarizer class
self.model = "gpt-3.5-turbo"  # or "gpt-4"
```

### File Upload Limits
```python
# In upload_pdf() route
if file.size > 26214400:  # 25MB
    return error
```

## 🚨 Troubleshooting

### PDF Processing Fails
**Error**: `Could not extract text from PDF`
- **Cause**: Scanned PDF without OCR or corrupted file
- **Solution**: Try a text-based PDF or use OCR software

### No Text Extracted
**Error**: `No text found in PDF to summarize`
- **Cause**: PDF is image-based (scan)
- **Solution**: Use OCR to convert to text-based PDF

### API Token Limit Exceeded
**Error**: `token count exceeds limit`
- **Cause**: PDF too long
- **Solution**: Reduce document or split into smaller parts

### Database Errors
**Error**: `sqlite3.OperationalError`
- **Solution**: Delete `myproject.db` and restart (recreates schema)

### Poor Summary Quality
- Use clear, structured PDFs
- Ensure text is extractable (not scanned)
- Try shorter documents first
- Adjust AI temperature settings

## 💰 Cost Considerations

OpenAI API usage (per PDF):
- **GPT-3.5-Turbo**: ~$0.001-0.003 per PDF
- **GPT-4**: ~$0.01-0.03 per PDF

Typical usage:
- 50-page PDF: ~3000 tokens
- Cost with GPT-3.5: ~$0.001-0.002
- Generate 10 PDFs/day: ~$0.01-0.02/day

## 🔐 Security & Data

### Best Practices
1. PDFs stored in `uploads/` folder (local)
2. Database stores summaries in SQLite
3. API key stored in `.env` (not committed)
4. No data sent to external services except OpenAI

### Privacy
- PDFs are processed server-side only
- Summary data cached in database
- Uploaded files can be manually deleted
- No automatic deletion (user responsibility)

## 📊 Performance Tips

1. **Optimal PDF Size**: 10-50 pages
2. **Processing Time**: 30-60 seconds per PDF
3. **Batch Processing**: Upload one PDF at a time
4. **Question Count**: 5-10 for fastest processing
5. **Server**: Ensure stable internet for API calls

## 🔄 Workflow Example

```
1. Student uploads lecture notes (PDF)
   ↓
2. System extracts text from all pages
   ↓
3. AI generates summary and identifies key points
   ↓
4. AI creates 5-10 practice questions
   ↓
5. Student reviews summary in browser
   ↓
6. Student takes practice quiz
   ↓
7. System provides score and feedback
   ↓
8. Student can review or download summary
```

## 🎯 Use Cases

- **Student Learning**: Quickly review lecture notes
- **Test Preparation**: Auto-generated practice questions
- **Teacher Tools**: Fast question bank creation
- **Content Review**: Verify document understanding
- **Knowledge Assessment**: Quiz generation from materials
- **Study Groups**: Shared summaries and questions

## 🚀 Future Enhancements

Potential features:
- [ ] OCR support for scanned PDFs
- [ ] Export summaries to PDF/Word
- [ ] Flashcard generation from key points
- [ ] Collaborative notes sharing
- [ ] Progress tracking & analytics
- [ ] Multiple language support
- [ ] Custom summarization styles
- [ ] Bulk PDF processing
- [ ] Audio summary (text-to-speech)
- [ ] PDF annotation tools

## 📞 Support

### Common Issues

**Q: Can I upload scanned PDFs?**
A: Currently, only text-based PDFs work. Use OCR software first.

**Q: How long does processing take?**
A: Typically 30-60 seconds depending on PDF size and API response.

**Q: Can I edit summaries?**
A: Not yet, but it's on the roadmap.

**Q: Is there a file size limit?**
A: Current limit is 25MB, adjustable in code.

**Q: Can I delete uploaded PDFs?**
A: Currently, files are stored permanently. Manual deletion supported.

## 📄 License

Part of Study Master Pro project. Use according to project license.

## 🙏 Acknowledgments

- **PDF Processing**: PyPDF2 & pdfplumber libraries
- **AI**: OpenAI GPT models
- **Framework**: Flask
- **Database**: SQLite
- **UI**: Bootstrap 5

---

Happy learning! 📚✨

For issues or questions, refer to the [AI Quiz Generator README](AI_QUIZ_GENERATOR_README.md) for general setup help.
