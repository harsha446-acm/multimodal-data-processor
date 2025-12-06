import google.generativeai as genai
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

class QueryEngine:
    """Handle natural language queries using Gemini"""
    
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_answer(self, query: str, context: List[str]) -> str:
        """Generate answer using Gemini with retrieved context"""
        try:
            # Combine context with better formatting
            combined_context = "\n\n".join([
                f"[Context Chunk {i+1}]:\n{doc}" 
                for i, doc in enumerate(context)
            ])
            
            # Create improved prompt
            prompt = f"""You are a helpful AI assistant analyzing documents. Answer the user's question based on the provided context chunks.

IMPORTANT INSTRUCTIONS:
1. Search through ALL the context chunks carefully to find relevant information
2. If the information is split across multiple chunks, synthesize it into a coherent answer
3. Even if the exact wording isn't present, use related information to answer if possible
4. If chunks contain partial information (like titles, headers, or fragments), look for the actual content in other chunks
5. Be specific and cite which chunk numbers you used
6. If you truly cannot find ANY relevant information after checking all chunks, only then say you don't have enough information

Context from {len(context)} chunks:
{combined_context}

User Question: {query}

Your Answer (be thorough and check all chunks):"""
            
            # Generate response
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate summary of text"""
        try:
            prompt = f"""Summarize the following text in about {max_length} words:

{text}

Summary:"""
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"