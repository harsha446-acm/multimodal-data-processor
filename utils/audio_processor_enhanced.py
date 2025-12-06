"""
Enhanced audio processor using Whisper (local processing, no API needed)
Only use if you installed: pip install openai-whisper
"""
import os
import tempfile
from pydub import AudioSegment

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

class EnhancedAudioProcessor:
    """Process audio using Whisper for better accuracy"""
    
    def __init__(self):
        if WHISPER_AVAILABLE:
            # Load the base model (fast and accurate)
            self.model = whisper.load_model("base")
        else:
            self.model = None
    
    def process_audio_whisper(self, file_path: str) -> str:
        """Process audio using Whisper"""
        if not WHISPER_AVAILABLE:
            return "Whisper not installed. Run: pip install openai-whisper"
        
        try:
            # Convert to format Whisper likes
            audio = AudioSegment.from_file(file_path)
            
            # Create temp file
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            # Export as WAV
            audio.export(temp_path, format="wav")
            
            # Transcribe
            result = self.model.transcribe(temp_path)
            
            # Clean up
            os.unlink(temp_path)
            
            return result["text"]
            
        except Exception as e:
            return f"Error using Whisper: {str(e)}"

# Example usage:
# processor = EnhancedAudioProcessor()
# text = processor.process_audio_whisper("audio.mp3")