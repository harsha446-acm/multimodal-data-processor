import os
import time
from typing import List, Dict
from PyPDF2 import PdfReader
from utils.config import *  # Configure Tesseract for Windows
from docx import Document
from pptx import Presentation
from PIL import Image
import pytesseract
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import yt_dlp
import tempfile
from youtube_transcript_api import YouTubeTranscriptApi
import re

class FileProcessor:
    """Process various file types and extract text content"""
    
    @staticmethod
    def process_pdf(file_path: str) -> str:
        """Extract text from PDF"""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
    @staticmethod
    def process_docx(file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            return f"Error processing DOCX: {str(e)}"
    
    @staticmethod
    def process_pptx(file_path: str) -> str:
        """Extract text from PPTX"""
        try:
            prs = Presentation(file_path)
            text = ""
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
            return text.strip()
        except Exception as e:
            return f"Error processing PPTX: {str(e)}"
    
    @staticmethod
    def process_text(file_path: str) -> str:
        """Extract text from TXT/MD files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            return f"Error processing text file: {str(e)}"
    
    @staticmethod
    def process_image(file_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip() if text.strip() else "No text detected in image"
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    @staticmethod
    def process_audio(file_path: str) -> str:
        """Extract text from audio using speech recognition with fallbacks"""
        temp_wav_path = None
        try:
            recognizer = sr.Recognizer()
            
            # Load and preprocess audio
            audio = AudioSegment.from_file(file_path)
            
            # Enhance audio quality
            # Normalize volume
            audio = audio.normalize()
            
            # Remove silence from beginning and end
            audio = audio.strip_silence(silence_thresh=-40)
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Set sample rate to 16000 Hz (optimal for speech recognition)
            audio = audio.set_frame_rate(16000)
            
            # Check audio length - if too long, process in chunks
            duration_seconds = len(audio) / 1000  # Convert to seconds
            
            if duration_seconds > 60:  # If longer than 1 minute, chunk it
                return FileProcessor._process_audio_chunked(audio, recognizer)
            
            # For short audio, try multiple recognition services
            temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_wav_path = temp_wav.name
            temp_wav.close()
            
            audio.export(temp_wav_path, format="wav")
            
            # Try Google first
            try:
                with sr.AudioFile(temp_wav_path) as source:
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    recognizer.energy_threshold = 300  # Lower threshold for quiet audio
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                    
                if text and len(text.strip()) > 0:
                    return text
            except sr.UnknownValueError:
                pass  # Try next method
            except sr.RequestError:
                pass  # Try next method
            
            # If Google fails, try with different settings
            try:
                with sr.AudioFile(temp_wav_path) as source:
                    recognizer.energy_threshold = 100  # Even lower threshold
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language='en-US')
                    
                if text and len(text.strip()) > 0:
                    return text
            except:
                pass
            
            # If all methods fail
            return """Audio transcription failed. Possible reasons:
1. Audio quality is too poor (background noise, unclear speech)
2. Audio is too quiet or too loud
3. No speech detected in the audio
4. Language is not English

Suggestions:
- Try a YouTube URL if available (uses captions)
- Ensure clear audio with minimal background noise
- Check if the audio actually contains speech
- Try uploading a shorter clip (under 2 minutes)"""
            
        except Exception as e:
            error_msg = str(e).lower()
            if 'bad request' in error_msg or 'recognition' in error_msg:
                return """Speech recognition service error. This usually means:
1. The audio format is not supported properly
2. The audio is too long (try shorter clips under 5 minutes)
3. The audio quality is insufficient

Try these solutions:
- Use YouTube URL for videos (much more reliable)
- Convert audio to MP3 format first
- Trim to a shorter clip
- Ensure clear speech with minimal background noise"""
            return f"Error processing audio: {str(e)}"
        finally:
            # Clean up temp file
            if temp_wav_path and os.path.exists(temp_wav_path):
                try:
                    time.sleep(0.1)
                    os.unlink(temp_wav_path)
                except:
                    pass
    
    @staticmethod
    def _process_audio_chunked(audio: AudioSegment, recognizer) -> str:
        """Process long audio in chunks with better error handling"""
        temp_files = []
        try:
            # Preprocess entire audio
            audio = audio.normalize()
            if audio.channels > 1:
                audio = audio.set_channels(1)
            audio = audio.set_frame_rate(16000)
            
            # Split audio into 45-second chunks
            chunk_length_ms = 45000  # 45 seconds
            chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
            
            transcripts = []
            successful_chunks = 0
            
            for i, chunk in enumerate(chunks):
                temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                temp_path = temp_file.name
                temp_file.close()
                temp_files.append(temp_path)
                
                # Export chunk
                chunk.export(temp_path, format="wav")
                
                # Transcribe chunk with retries
                chunk_text = None
                try:
                    with sr.AudioFile(temp_path) as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.3)
                        recognizer.energy_threshold = 300
                        audio_data = recognizer.record(source)
                        chunk_text = recognizer.recognize_google(audio_data)
                        
                    if chunk_text and len(chunk_text.strip()) > 0:
                        transcripts.append(chunk_text)
                        successful_chunks += 1
                except sr.UnknownValueError:
                    transcripts.append(f"[Chunk {i+1}/{len(chunks)}: unclear audio]")
                except sr.RequestError as e:
                    transcripts.append(f"[Chunk {i+1}/{len(chunks)}: service error]")
                except Exception as e:
                    transcripts.append(f"[Chunk {i+1}/{len(chunks)}: error]")
            
            if successful_chunks == 0:
                return f"""Failed to transcribe any chunks from the audio.

Processed {len(chunks)} chunks but none contained clear speech.

Suggestions:
- Use YouTube URL if this is a YouTube video (much more reliable)
- Check if audio actually contains clear speech
- Try a shorter, clearer audio clip
- Ensure minimal background noise"""
            
            result = " ".join(transcripts)
            if successful_chunks < len(chunks):
                result += f"\n\n[Note: Successfully transcribed {successful_chunks}/{len(chunks)} chunks]"
            
            return result
                
        except Exception as e:
            return f"Error processing audio chunks: {str(e)}"
        finally:
            # Clean up temp files
            for temp_path in temp_files:
                try:
                    if os.path.exists(temp_path):
                        time.sleep(0.1)
                        os.unlink(temp_path)
                except:
                    pass
    
    @staticmethod
    def process_video(file_path: str) -> str:
        """Extract audio from video and convert to text"""
        temp_audio_path = None
        video = None
        try:
            video = VideoFileClip(file_path)
            
            # Create temp file
            temp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_audio_path = temp_audio.name
            temp_audio.close()  # Close the file handle
            
            # Extract audio
            video.audio.write_audiofile(temp_audio_path, logger=None)
            
            # Close video to release resources
            video.close()
            video = None
            
            # Process the audio
            text = FileProcessor.process_audio(temp_audio_path)
            
            return text
        except Exception as e:
            return f"Error processing video: {str(e)}"
        finally:
            # Clean up resources
            if video:
                try:
                    video.close()
                except:
                    pass
            
            # Clean up temp file
            if temp_audio_path and os.path.exists(temp_audio_path):
                try:
                    import time
                    time.sleep(0.5)  # Wait a bit for file handles to release
                    os.unlink(temp_audio_path)
                except Exception as cleanup_error:
                    # If cleanup fails, log it but don't crash
                    print(f"Warning: Could not delete temp file {temp_audio_path}: {cleanup_error}")
                    pass
    
    @staticmethod
    def extract_video_id(url: str) -> str:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def process_youtube_transcript(url: str) -> str:
        """Extract transcript from YouTube video (faster and more reliable)"""
        try:
            video_id = FileProcessor.extract_video_id(url)
            if not video_id:
                return "Invalid YouTube URL format"
            
            # Try to get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Combine all text
            text = " ".join([item['text'] for item in transcript_list])
            return text
        except Exception as e:
            error_msg = str(e)
            if "Subtitles are disabled" in error_msg or "transcript" in error_msg.lower():
                return "No subtitles/transcript available for this video. Try uploading the video as MP4 instead."
            return f"Error getting YouTube transcript: {error_msg}"
    
    @staticmethod
    def process_youtube(url: str) -> str:
        """Download and extract text from YouTube video"""
        # First try transcript method (faster and more reliable)
        transcript_result = FileProcessor.process_youtube_transcript(url)
        if transcript_result and not transcript_result.startswith("Error") and not transcript_result.startswith("No subtitles"):
            return transcript_result
        
        # If transcript fails, try audio download method
        audio_file = None
        try:
            # Enhanced options to bypass restrictions
            temp_template = tempfile.mktemp(suffix='.%(ext)s')
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }],
                'outtmpl': temp_template,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'referer': 'https://www.youtube.com/',
                'nocheckcertificate': True,
                'age_limit': None,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                audio_file = ydl.prepare_filename(info).replace('.webm', '.wav').replace('.m4a', '.wav')
            
            # Process the audio
            text = FileProcessor.process_audio(audio_file)
            
            return text
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "Forbidden" in error_msg:
                return f"YouTube processing failed. Transcript error: {transcript_result}. Download error: Update yt-dlp with 'pip install --upgrade yt-dlp' or upload video as MP4."
            return f"Error processing YouTube video: {error_msg}. Transcript error: {transcript_result}"
        finally:
            # Clean up downloaded file
            if audio_file and os.path.exists(audio_file):
                try:
                    import time
                    time.sleep(0.5)  # Wait for file handles to release
                    os.unlink(audio_file)
                except Exception as cleanup_error:
                    print(f"Warning: Could not delete temp file {audio_file}: {cleanup_error}")
                    pass
    
    @staticmethod
    def process_file(file_path: str, file_type: str) -> Dict[str, str]:
        """Process file based on its type"""
        processors = {
            'pdf': FileProcessor.process_pdf,
            'docx': FileProcessor.process_docx,
            'pptx': FileProcessor.process_pptx,
            'txt': FileProcessor.process_text,
            'md': FileProcessor.process_text,
            'png': FileProcessor.process_image,
            'jpg': FileProcessor.process_image,
            'jpeg': FileProcessor.process_image,
            'mp3': FileProcessor.process_audio,
            'wav': FileProcessor.process_audio,
            'mp4': FileProcessor.process_video,
        }
        
        processor = processors.get(file_type.lower())
        if processor:
            content = processor(file_path)
            return {
                'filename': os.path.basename(file_path),
                'content': content,
                'file_type': file_type
            }
        else:
            return {
                'filename': os.path.basename(file_path),
                'content': f"Unsupported file type: {file_type}",
                'file_type': file_type
            }