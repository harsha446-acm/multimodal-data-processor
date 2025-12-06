import streamlit as st
import os
from utils.file_processors import FileProcessor
from utils.database import DatabaseManager
from utils.query_engine import QueryEngine
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Multimodal Data Processor",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager()
if 'query_engine' not in st.session_state:
    st.session_state.query_engine = QueryEngine()
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Header
st.title("📚 Multimodal Data Processing System")
st.markdown("Upload documents, images, audio, or video files and ask questions!")

# Sidebar
with st.sidebar:
    st.header("📊 System Info")
    
    # Database stats
    stats = st.session_state.db_manager.get_stats()
    st.metric("Total Chunks", stats.get('total_chunks', 0))
    st.metric("Unique Documents", stats.get('unique_documents', 0))
    
    st.divider()
    
    # Processed files
    st.subheader("📁 Uploaded Files")
    docs = st.session_state.db_manager.get_all_documents()
    if docs:
        for doc in docs:
            st.text(f"✓ {doc}")
    else:
        st.info("No files uploaded yet")
    
    st.divider()
    
    # Clear database button
    if st.button("🗑️ Clear All Data", type="secondary"):
        success, message = st.session_state.db_manager.clear_collection()
        if success:
            st.session_state.processed_files = []
            st.success(message)
            st.rerun()
        else:
            st.error(message)

# Main content - Tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload Files", "❓ Ask Questions", "ℹ️ About"])

# Tab 1: Upload Files
with tab1:
    st.header("Upload Your Files")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'docx', 'pptx', 'txt', 'md', 'png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4'],
            accept_multiple_files=True,
            help="Supported formats: PDF, DOCX, PPTX, TXT, MD, PNG, JPG, MP3, WAV, MP4"
        )
        
        # YouTube URL input (optional - comment out if having issues)
        st.info("💡 Tip: For YouTube videos, try videos with captions/subtitles for best results")
        youtube_url = st.text_input(
            "Or paste a YouTube URL (optional)",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        # Manual transcript option
        with st.expander("📝 Or paste a manual transcript (if video upload fails)"):
            st.caption("If video/audio processing fails, you can manually paste the transcript here")
            manual_transcript = st.text_area(
                "Paste transcript text:",
                placeholder="Paste the video/audio transcript here...",
                height=150
            )
            transcript_name = st.text_input(
                "Name for this transcript:",
                placeholder="e.g., My Video Transcript"
            )
            
            if manual_transcript and transcript_name:
                if st.button("📤 Upload Transcript"):
                    success, message = st.session_state.db_manager.add_document(
                        content=manual_transcript,
                        metadata={
                            'filename': transcript_name,
                            'file_type': 'manual_transcript'
                        }
                    )
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

    
    with col2:
        st.info("""
        **Supported Formats:**
        - 📄 Documents: PDF, DOCX, PPTX, TXT, MD
        - 🖼️ Images: PNG, JPG
        - 🎵 Audio: MP3, WAV (under 5 min recommended)
        - 🎥 Video: MP4 (under 5 min recommended)
        
        **Audio/Video Tips:**
        - Clear speech, minimal background noise
        - Shorter files process faster
        - English language works best
        """)
        
        st.warning("""⚠️ **Important for Videos:**
        
For videos, we **strongly recommend** using the YouTube URL option instead of uploading MP4 files. Here's why:

✅ **YouTube URL** (Recommended):
- Uses official captions/transcripts
- Much faster (no audio processing)
- More accurate results
- Works with longer videos

❌ **MP4 Upload**:
- Requires clear audio
- May fail with background noise
- Limited to short clips
- Slower processing

If MP4 upload fails, get the YouTube link!
        """)


    
    # Process uploaded files
    if uploaded_files:
        if st.button("🚀 Process Files", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing: {uploaded_file.name}")
                
                # Save file
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Get file extension
                file_ext = Path(uploaded_file.name).suffix[1:].lower()
                
                # Process file
                result = FileProcessor.process_file(file_path, file_ext)
                
                # Add to database
                if result['content'] and not result['content'].startswith('Error'):
                    success, message = st.session_state.db_manager.add_document(
                        content=result['content'],
                        metadata={
                            'filename': result['filename'],
                            'file_type': result['file_type']
                        }
                    )
                    
                    if success:
                        st.session_state.processed_files.append(result['filename'])
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error(f"❌ {result['content']}")
                
                # Update progress
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.text("Processing complete!")
            st.balloons()
    
    # Process YouTube URL
    if youtube_url:
        if st.button("🎥 Process YouTube Video", type="primary"):
            with st.spinner("Downloading and processing YouTube video..."):
                result = {
                    'filename': f"YouTube: {youtube_url}",
                    'content': FileProcessor.process_youtube(youtube_url),
                    'file_type': 'youtube'
                }
                
                if result['content'] and not result['content'].startswith('Error'):
                    success, message = st.session_state.db_manager.add_document(
                        content=result['content'],
                        metadata={
                            'filename': result['filename'],
                            'file_type': result['file_type']
                        }
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error(f"❌ {result['content']}")

# Tab 2: Ask Questions
with tab2:
    st.header("Ask Questions About Your Documents")
    
    # Check if documents are uploaded
    if st.session_state.db_manager.get_stats()['total_chunks'] == 0:
        st.warning("⚠️ Please upload some documents first in the 'Upload Files' tab!")
    else:
        # Query input
        user_query = st.text_input(
            "Enter your question:",
            placeholder="What is the main topic discussed in the documents?"
        )
        
        col1, col2, col3 = st.columns([2, 2, 3])
        with col1:
            n_results = st.slider("Context chunks", 5, 20, 10)
        with col2:
            # Document filter
            docs = ["All Documents"] + st.session_state.db_manager.get_all_documents()
            selected_doc = st.selectbox("Search in:", docs)
        with col3:
            st.caption("💡 Tip: Increase chunks if answer is incomplete")
        
        if user_query:
            if st.button("🔍 Search", type="primary"):
                with st.spinner("Searching and generating answer..."):
                    # Query database
                    filter_doc = None if selected_doc == "All Documents" else selected_doc
                    results = st.session_state.db_manager.query(
                        user_query, 
                        n_results=n_results,
                        filter_filename=filter_doc
                    )
                    
                    if 'error' in results:
                        st.error(f"Error: {results['error']}")
                    else:
                        # Extract documents
                        documents = results.get('documents', [[]])[0]
                        metadatas = results.get('metadatas', [[]])[0]
                        similarities = results.get('similarities', [[]])[0] if 'similarities' in results else None
                        
                        if documents:
                            # Generate answer
                            answer = st.session_state.query_engine.generate_answer(
                                user_query, 
                                documents
                            )
                            
                            # Display answer
                            st.markdown("### 💡 Answer")
                            st.markdown(answer)
                            
                            # Show debug info
                            st.divider()
                            st.caption(f"📊 Retrieved {len(documents)} chunks from database")
                            
                            # Show sources with relevance scores
                            with st.expander("📚 View Retrieved Chunks (Ranked by Relevance)", expanded=False):
                                for i, (doc, meta) in enumerate(zip(documents, metadatas)):
                                    # Show relevance score if available
                                    relevance_text = ""
                                    if similarities:
                                        relevance = similarities[i] * 100
                                        relevance_color = "🟢" if relevance > 70 else "🟡" if relevance > 50 else "🔴"
                                        relevance_text = f"{relevance_color} **Relevance: {relevance:.1f}%**"
                                    
                                    chunk_info = f"Chunk {meta.get('chunk_index', '?')+1}/{meta.get('total_chunks', '?')}" if 'chunk_index' in meta else ""
                                    
                                    st.markdown(f"**Chunk {i+1}:** {meta.get('filename', 'Unknown')} - {chunk_info} {relevance_text}")
                                    
                                    # Show full chunk in a text area for easy reading
                                    with st.container():
                                        st.text_area(
                                            f"Content of Chunk {i+1}",
                                            doc,
                                            height=150,
                                            key=f"chunk_{i}",
                                            disabled=True
                                        )
                                    st.divider()
                        else:
                            st.warning("No relevant documents found for your query.")

# Tab 3: About
with tab3:
    st.header("About This System")
    
    st.markdown("""
    ### 🎯 Features
    
    This Multimodal Data Processing System allows you to:
    
    - **📄 Process Text Documents**: PDF, DOCX, PPTX, TXT, MD
    - **🖼️ Extract Text from Images**: PNG, JPG (using OCR)
    - **🎵 Transcribe Audio**: MP3, WAV files
    - **🎥 Process Videos**: MP4 files and YouTube URLs
    - **🔍 Smart Search**: Natural language queries using ChromaDB
    - **🤖 AI Answers**: Context-aware responses using Google Gemini
    
    ### 🛠️ Technology Stack
    
    - **Frontend**: Streamlit
    - **Vector Database**: ChromaDB
    - **LLM**: Google Gemini (Free)
    - **OCR**: Tesseract
    - **Speech Recognition**: Google Speech API
    
    ### 📖 How to Use
    
    1. **Upload Files**: Go to the "Upload Files" tab and select your files
    2. **Process**: Click the "Process Files" button to extract and store content
    3. **Ask Questions**: Navigate to "Ask Questions" tab and enter your query
    4. **Get Answers**: The system will search your documents and provide AI-generated answers
    
    ### ⚙️ System Requirements
    
    - Python 3.8+
    - Tesseract OCR installed
    - FFmpeg (for audio/video processing)
    - Internet connection (for Gemini API)
    
    ### 🔐 Privacy Note
    
    All data is processed locally and stored in ChromaDB on your machine. 
    Only queries are sent to Google Gemini API for answer generation.
    """)
    
    st.divider()
    
    st.markdown("""
    ### 💻 Developer Info
    
    Built with ❤️ using Streamlit, ChromaDB, and Google Gemini
    
    **Version**: 1.0.0
    """)

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 10px;'>
    Multimodal Data Processing System | Powered by Gemini & ChromaDB
    </div>
    """,
    unsafe_allow_html=True
)