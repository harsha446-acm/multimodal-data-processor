# 📚 Multimodal Data Processing System

A powerful AI-powered application that processes various file formats (documents, images, audio, video) and enables intelligent question-answering using natural language queries. Built with Streamlit, ChromaDB, and Google Gemini.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

### 📄 Document Processing
- **PDF**: Extract text from single or multi-page PDFs
- **Word Documents**: Process .docx files
- **PowerPoint**: Extract text from presentations (.pptx)
- **Text Files**: Support for .txt and .md files

### 🖼️ Image Processing
- **OCR Technology**: Extract text from images using Tesseract
- **Supported Formats**: PNG, JPG, JPEG
- **Use Cases**: Scanned documents, screenshots, photos with text

### 🎵 Audio Processing
- **Format Support**: MP3, WAV
- **Speech-to-Text**: Automatic transcription using Google Speech Recognition
- **Smart Chunking**: Handles long audio files by processing in segments
- **Audio Enhancement**: Automatic noise reduction and normalization

### 🎥 Video Processing
- **Direct Upload**: MP4 file processing
- **YouTube Integration**: Direct URL processing with transcript extraction
- **Dual Mode**: Transcript extraction (fast) or audio extraction (fallback)
- **Manual Transcript**: Option to paste transcripts manually

### 🔍 Intelligent Search
- **Semantic Search**: Uses ChromaDB with sentence transformers for meaning-based search
- **Context-Aware**: Retrieves relevant chunks ranked by similarity
- **Document Filtering**: Search within specific documents
- **Relevance Scoring**: Visual indicators (🟢🟡🔴) show chunk relevance

### 🤖 AI-Powered Answers
- **Google Gemini**: Uses Gemini Pro for natural language responses
- **Context Synthesis**: Combines information from multiple chunks
- **Source Attribution**: Shows which documents were used
- **Multi-Document Reasoning**: Answers questions spanning multiple files

---

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Type Support](#file-type-support)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [API Keys](#api-keys)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### System Requirements

#### Windows
- Tesseract OCR
- FFmpeg

#### Mac
- Homebrew
- Tesseract OCR
- FFmpeg

#### Linux (Ubuntu/Debian)
- Tesseract OCR
- FFmpeg

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/multimodal-data-processor.git
cd multimodal-data-processor
```

---

### Step 2: Install System Dependencies

#### Windows

**Install Tesseract OCR:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (note installation path, usually `C:\Program Files\Tesseract-OCR`)
3. Add to System PATH:
   ```cmd
   # Press Win+R, type: sysdm.cpl
   # Environment Variables → System Variables → Path → Edit → New
   # Add: C:\Program Files\Tesseract-OCR
   ```

**Install FFmpeg:**
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH

**Verify Installation:**
```cmd
tesseract --version
ffmpeg -version
```

#### Mac

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install tesseract
brew install ffmpeg

# Verify
tesseract --version
ffmpeg -version
```

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt-get update

# Install Tesseract
sudo apt-get install tesseract-ocr

# Install FFmpeg
sudo apt-get install ffmpeg

# Verify
tesseract --version
ffmpeg -version
```

---

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

---

### Step 4: Install Python Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**If installation fails, install manually:**

```bash
pip install streamlit==1.29.0
pip install google-generativeai==0.3.2
pip install chromadb==0.4.22
pip install python-dotenv==1.0.0
pip install PyPDF2==3.0.1
pip install python-docx==1.1.0
pip install python-pptx==0.6.23
pip install Pillow==10.1.0
pip install pytesseract==0.3.10
pip install moviepy==1.0.3
pip install speechrecognition==3.10.1
pip install pydub==0.25.1
pip install yt-dlp
pip install youtube-transcript-api==0.6.1
pip install langchain==0.1.0
pip install langchain-google-genai==0.0.6
pip install sentence-transformers==2.2.2
```

---

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# .env
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Get Your Gemini API Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into `.env` file

---

## ⚙️ Configuration

### Project Structure

```
multimodal-data-processor/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── README.md                   # This file
├── test_installations.py       # System dependency test script
├── test_semantic_search.py     # Semantic search test script
├── utils/
│   ├── __init__.py            # Package initializer
│   ├── config.py              # Configuration (Tesseract path)
│   ├── file_processors.py     # File processing logic
│   ├── database.py            # ChromaDB operations
│   └── query_engine.py        # AI query handling
├── uploads/                    # Temporary file storage (auto-created)
└── chroma_db/                  # Vector database storage (auto-created)
```

### Configuration Files

#### `.env` File
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

#### `utils/config.py` (Windows Users)
Automatically configures Tesseract path. Edit if your installation is different:

```python
import pytesseract
import platform

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🎯 Usage

### Starting the Application

```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

### Basic Workflow

#### 1. Upload Files

**Tab: Upload Files**

1. Click "Browse files" or drag-and-drop
2. Select one or multiple files
3. Click "🚀 Process Files"
4. Wait for processing to complete

**Supported uploads:**
- Documents: PDF, DOCX, PPTX, TXT, MD
- Images: PNG, JPG, JPEG
- Audio: MP3, WAV
- Video: MP4
- YouTube: Paste URL

#### 2. Ask Questions

**Tab: Ask Questions**

1. Type your question in natural language
2. Adjust settings:
   - **Context chunks**: 5-20 (more = more context)
   - **Search in**: Filter by specific document
3. Click "🔍 Search"
4. View answer and source documents

#### 3. View Results

- **Answer**: AI-generated response based on your documents
- **Source Documents**: Click expander to see:
  - Retrieved chunks with relevance scores
  - Full content of each chunk
  - Which document each chunk came from

---

## 📁 File Type Support

### Documents

#### PDF Files
**Best for:** Reports, research papers, books, forms

**Example Questions:**
- "What are the main findings in this research paper?"
- "Summarize the executive summary"
- "What data is presented in Table 3?"

**Tips:**
- Works with text-based PDFs
- Scanned PDFs need OCR (convert to image first)
- Multi-page support

#### Word Documents (.docx)
**Best for:** Essays, reports, documentation

**Example Questions:**
- "What is the thesis statement?"
- "List the key recommendations"
- "What sources are cited?"

#### PowerPoint (.pptx)
**Best for:** Presentations, slides, lecture notes

**Example Questions:**
- "What are the main topics covered?"
- "Summarize slide 5"
- "What statistics are presented?"

**Note:** Extracts text from slides, not images or charts

#### Text Files (.txt, .md)
**Best for:** Notes, code documentation, logs

**Example Questions:**
- "What is this document about?"
- "Find all mentions of [topic]"
- "Summarize the content"

---

### Images

#### Image OCR (PNG, JPG, JPEG)
**Best for:** Screenshots, scanned documents, photos with text

**Example Questions:**
- "What text is in this image?"
- "Extract the information from this screenshot"
- "What does this sign say?"

**Requirements:**
- Text should be clear and legible
- Good lighting/contrast
- Horizontal text works best

**Tips:**
- ✅ Screenshots of documents
- ✅ Photos of whiteboards
- ✅ Scanned receipts/forms
- ❌ Handwritten text (low accuracy)
- ❌ Artistic/stylized fonts

---

### Audio Files

#### MP3/WAV Processing
**Best for:** Interviews, podcasts, recordings, lectures

**Example Questions:**
- "What topics were discussed?"
- "What did the speaker say about [topic]?"
- "Summarize the main points"

**Requirements:**
- Clear speech
- Minimal background noise
- English language
- Under 10 minutes (recommended)

**Tips:**
- ✅ One speaker at a time
- ✅ Quiet environment
- ✅ Good microphone quality
- ❌ Music with lyrics
- ❌ Multiple overlapping speakers
- ❌ Heavy accent (may reduce accuracy)

**Audio Quality Checklist:**
- [ ] No background music
- [ ] Clear pronunciation
- [ ] Single speaker or turn-taking
- [ ] Minimal echo/reverb
- [ ] Good volume (not too quiet/loud)

---

### Video Files

#### MP4 Videos
**Best for:** Lectures, tutorials, presentations, interviews

**Example Questions:**
- "What are the main steps in this tutorial?"
- "What did they say about [topic]?"
- "Summarize the video content"

**Limitations:**
- Extracts audio only (visual content not analyzed)
- Requires clear speech
- Processing can be slow

**⚠️ Important:** MP4 upload is NOT recommended. Use YouTube URL instead!

#### YouTube Videos (Recommended! ⭐)
**Best for:** Any YouTube video with captions

**How to use:**
1. Copy YouTube URL
2. Paste in "YouTube URL" field
3. Click "Process YouTube Video"

**Advantages:**
- ✅ Uses official captions (much faster)
- ✅ More accurate than audio processing
- ✅ Works with longer videos
- ✅ No audio quality issues
- ✅ Handles any language (if captions available)

**Example URLs:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
```

---

### Manual Transcripts

If video/audio processing fails, you can paste transcripts manually:

1. Get transcript:
   - YouTube: Click "..." → "Show transcript" → Copy
   - Use transcription service (otter.ai, rev.com)
   - Type it yourself

2. In app:
   - Expand "📝 Or paste a manual transcript"
   - Paste transcript
   - Give it a name
   - Click "Upload Transcript"

---

## 💡 Best Practices

### For Best Results

#### Document Uploads
- ✅ Upload related documents together
- ✅ Use descriptive filenames
- ✅ Combine when answering requires multiple sources
- ❌ Don't upload duplicate content

#### Writing Queries
- ✅ **Specific**: "What is the baking temperature for chocolate cake?"
- ❌ **Vague**: "Tell me about the document"
- ✅ **Direct**: "What did the CEO say about Q4 revenue?"
- ❌ **Indirect**: "Is there financial information?"

#### Adjusting Settings
- **Few chunks (5-7)**: Simple, focused questions
- **Medium chunks (10-12)**: Standard questions
- **Many chunks (15-20)**: Complex questions across documents

#### Document Filtering
- Use "Search in" dropdown to search specific documents
- Helpful when you know which document has the answer
- Faster and more accurate results

### Query Examples by Type

#### Academic Papers
```
✅ "What is the research methodology?"
✅ "What are the main findings?"
✅ "What limitations are mentioned?"
✅ "Who are the authors?"
```

#### Business Documents
```
✅ "What is the Q3 revenue?"
✅ "What are the key risks identified?"
✅ "What strategies are recommended?"
✅ "When is the project deadline?"
```

#### Technical Documentation
```
✅ "How do I install this software?"
✅ "What are the system requirements?"
✅ "What is the API endpoint for authentication?"
✅ "What error codes are defined?"
```

#### Video/Audio Content
```
✅ "What are the main steps explained?"
✅ "What ingredients are needed?"
✅ "What did the speaker say about [topic]?"
✅ "Summarize the key takeaways"
```

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: "tesseract is not recognized"

**Symptoms:** Error when processing images

**Solutions:**

**Windows:**
```cmd
# Check if Tesseract is installed
tesseract --version

# If not found, add to PATH:
# Win+R → sysdm.cpl → Environment Variables
# System Variables → Path → Edit → New
# Add: C:\Program Files\Tesseract-OCR

# Restart Command Prompt/VS Code
```

**Mac/Linux:**
```bash
# Reinstall Tesseract
brew install tesseract  # Mac
sudo apt-get install tesseract-ocr  # Linux

# Verify
tesseract --version
```

---

#### Issue 2: "ffmpeg not found"

**Symptoms:** Audio/video processing fails

**Solutions:**

**Windows:**
```cmd
# Verify FFmpeg
ffmpeg -version

# If not found, download from:
# https://www.gyan.dev/ffmpeg/builds/
# Extract to C:\ffmpeg
# Add C:\ffmpeg\bin to PATH
```

**Mac/Linux:**
```bash
brew install ffmpeg  # Mac
sudo apt-get install ffmpeg  # Linux
```

---

#### Issue 3: "Bad Request" or Audio Recognition Error

**Symptoms:** Audio/video transcription fails

**Solutions:**

1. **Use YouTube URL instead** (most reliable)
2. **Check audio quality:**
   - Clear speech?
   - Minimal background noise?
   - Under 5 minutes?
3. **Try manual transcript:**
   - Get transcript from YouTube or transcription service
   - Paste in "Manual Transcript" section
4. **Pre-process audio:**
   - Use noise reduction tools
   - Convert to MP3 format
   - Trim to shorter clips

---

#### Issue 4: "Module not found" Errors

**Symptoms:** Import errors when running app

**Solutions:**

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt

# Or install specific package:
pip install [package-name]
```

---

#### Issue 5: "Not enough information" in Answer

**Symptoms:** AI can't answer despite relevant documents

**Solutions:**

1. **Increase context chunks** to 15-20
2. **Use document filter** to search specific file
3. **Check retrieved chunks:**
   - Click "View Retrieved Chunks"
   - Verify if answer is in the chunks
4. **Rephrase your question:**
   - Be more specific
   - Use keywords from the document
5. **Re-upload documents:**
   - Delete database: `rmdir /s chroma_db`
   - Restart app and re-upload

---

#### Issue 6: Wrong Chunks Retrieved

**Symptoms:** Retrieved chunks don't match query

**Solutions:**

1. **Clear and rebuild database:**
   ```bash
   # Stop app (Ctrl+C)
   # Delete database
   rmdir /s chroma_db  # Windows
   rm -rf chroma_db    # Mac/Linux
   # Restart app
   streamlit run app.py
   # Re-upload all files
   ```

2. **Adjust chunk size** in `utils/database.py`:
   ```python
   def _chunk_text(self, text: str, max_length: int = 1000):
   # Try 700 or 1500
   ```

3. **Use more specific queries**

---

#### Issue 7: Gemini API Errors

**Symptoms:** "API key not found" or quota errors

**Solutions:**

1. **Check .env file exists:**
   ```bash
   # File should contain:
   GOOGLE_API_KEY=your_actual_key_here
   ```

2. **Verify API key:**
   - Visit https://makersuite.google.com/app/apikey
   - Regenerate key if needed
   - Update .env file

3. **Check API quota:**
   - Free tier has limits
   - Wait and retry
   - Consider upgrading

---

### Testing Your Installation

#### Test System Dependencies
```bash
python test_installations.py
```

**Expected output:**
```
Testing Required Software Installation
==================================================

✅ Tesseract OCR is installed!
   Version: 5.3.3

✅ FFmpeg is installed!
   ffmpeg version ...

✅ pytesseract can access Tesseract!
   Version: 5.3.3

==================================================
✅ All systems ready! You can run the application.
==================================================
```

#### Test Semantic Search
```bash
python test_semantic_search.py
```

**Expected output:**
```
Testing Semantic Search...
==================================================
✓ Added: python_intro.txt
✓ Added: ml_basics.txt
...

🔍 Query: 'What is machine learning?'
--------------------------------------------------
Top Results:

  1. ml_basics.txt (Relevance: 85.3%)
     Preview: Machine learning is a subset...

==================================================
Test Complete!
==================================================
```

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                     Streamlit UI                         │
│  (User Interface - File Upload, Query Input, Results)   │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│ File Processors │    │  Query Engine    │
│  - PDF          │    │  - Gemini API    │
│  - DOCX         │    │  - Prompt Gen    │
│  - Images (OCR) │    │  - Response      │
│  - Audio (STT)  │    └──────────────────┘
│  - Video        │              │
└────────┬────────┘              │
         │                       │
         ▼                       ▼
┌──────────────────────────────────────────┐
│          ChromaDB                         │
│  - Vector Storage                         │
│  - Semantic Search                        │
│  - Sentence Transformers (Embeddings)    │
└──────────────────────────────────────────┘
```

### Data Flow

1. **File Upload** → User selects files
2. **Processing** → File processors extract text/transcripts
3. **Chunking** → Text split into 1000-char semantic chunks
4. **Embedding** → Chunks converted to vectors (sentence-transformers)
5. **Storage** → Vectors stored in ChromaDB
6. **Query** → User asks question
7. **Search** → Semantic search finds relevant chunks
8. **Generation** → Gemini generates answer from chunks
9. **Display** → Answer shown with sources

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web interface |
| **Vector DB** | ChromaDB | Semantic search |
| **Embeddings** | Sentence Transformers | Text → Vectors |
| **LLM** | Google Gemini Pro | Answer generation |
| **OCR** | Tesseract | Image text extraction |
| **Speech-to-Text** | Google Speech API | Audio transcription |
| **Video** | MoviePy, yt-dlp | Video processing |
| **Documents** | PyPDF2, python-docx, python-pptx | Document parsing |

---

## 🔑 API Keys

### Google Gemini API

**Free Tier Limits:**
- 60 requests per minute
- 1,500 requests per day
- 1 million tokens per month

**Getting Started:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy key to `.env` file

**Upgrading:**
- For higher limits, consider paid plans
- Visit: https://ai.google.dev/pricing

**Best Practices:**
- Don't commit API key to Git
- Use `.env` file (already in `.gitignore`)
- Regenerate if exposed
- Monitor usage in Google AI Studio

---

## 🤝 Contributing

Contributions are welcome! Here's how:

### Reporting Issues

1. Check existing issues first
2. Provide detailed description
3. Include error messages
4. Share system info (OS, Python version)

### Feature Requests

1. Describe the feature
2. Explain use case
3. Suggest implementation (optional)

### Pull Requests

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Test thoroughly
5. Submit pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/multimodal-data-processor.git

# Create branch
git checkout -b feature/your-feature-name

# Make changes and test

# Commit
git commit -m "Add: your feature description"

# Push
git push origin feature/your-feature-name

# Create pull request on GitHub
```

---

## 📝 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

### Getting Help

- **Documentation**: Read this README
- **Issues**: https://github.com/yourusername/multimodal-data-processor/issues
- **Discussions**: https://github.com/yourusername/multimodal-data-processor/discussions

### Frequently Asked Questions

**Q: Can I use other LLMs besides Gemini?**
A: Yes! Modify `utils/query_engine.py` to use OpenAI, Anthropic, or other APIs.

**Q: How do I process non-English content?**
A: Update language settings in `utils/file_processors.py` for audio processing.

**Q: Can I deploy this online?**
A: Yes! Deploy to Streamlit Cloud, Heroku, or any cloud platform.

**Q: Is my data stored anywhere?**
A: Data is stored locally in `chroma_db/`. Only queries are sent to Gemini API.

**Q: Can I process password-protected PDFs?**
A: Not directly. Remove password first using PDF tools.

---

## 🎓 Educational Use

This project is perfect for:
- Learning multimodal AI applications
- Understanding vector databases
- Exploring semantic search
- Building RAG (Retrieval-Augmented Generation) systems
- Document intelligence projects

---

## 🚀 Future Enhancements

Potential improvements:
- [ ] Support for more file formats (Excel, CSV)
- [ ] Multi-language support
- [ ] Conversation history
- [ ] Export results to PDF/DOCX
- [ ] Batch processing
- [ ] Custom embedding models
- [ ] User authentication
- [ ] Cloud deployment guide
- [ ] Docker containerization
- [ ] Advanced analytics dashboard

---

## 📚 Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

### Tutorials
- [Building RAG Systems](https://python.langchain.com/docs/use_cases/question_answering/)
- [Semantic Search Guide](https://www.pinecone.io/learn/semantic-search/)
- [Streamlit Tutorial](https://docs.streamlit.io/library/get-started)

---

## ✨ Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Google Gemini](https://ai.google.dev/) - LLM
- [Tesseract](https://github.com/tesseract-ocr/tesseract) - OCR
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Audio transcription
- [Sentence Transformers](https://www.sbert.net/) - Embeddings

---

## 📊 Project Status

**Current Version:** 1.0.0

**Status:** Active Development

**Last Updated:** December 2024

---

**Made with ❤️ for learning and exploration**

For questions, issues, or contributions, please visit the [GitHub repository](https://github.com/yourusername/multimodal-data-processor).