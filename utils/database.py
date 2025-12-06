import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import List, Dict
import uuid

class DatabaseManager:
    """Manage ChromaDB operations"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Use sentence transformers for better semantic search
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"  # Fast and accurate model
        )
        
        self.collection_name = "multimodal_data"
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            return self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
        except:
            return self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Multimodal data storage with semantic search"}
            )
    
    def add_document(self, content: str, metadata: Dict):
        """Add document to ChromaDB"""
        try:
            # Split content into chunks if it's too long
            chunks = self._chunk_text(content, max_length=500)
            
            ids = []
            documents = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                doc_id = f"{metadata['filename']}_{uuid.uuid4().hex[:8]}_chunk_{i}"
                ids.append(doc_id)
                documents.append(chunk)
                metadatas.append({
                    **metadata,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })
            
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            return True, f"Added {len(chunks)} chunks from {metadata['filename']}"
        except Exception as e:
            return False, f"Error adding document: {str(e)}"
    
    def _chunk_text(self, text: str, max_length: int = 1000) -> List[str]:
        """Split text into chunks with overlap for better context"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        sentences = text.replace('\n', ' ').split('. ')
        
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_length = len(sentence)
            
            # If single sentence is longer than max_length, split it by words
            if sentence_length > max_length:
                words = sentence.split()
                word_chunk = []
                word_length = 0
                
                for word in words:
                    word_length += len(word) + 1
                    if word_length > max_length:
                        if word_chunk:
                            chunks.append(' '.join(word_chunk))
                        word_chunk = [word]
                        word_length = len(word)
                    else:
                        word_chunk.append(word)
                
                if word_chunk:
                    chunks.append(' '.join(word_chunk))
                continue
            
            # Check if adding this sentence exceeds limit
            if current_length + sentence_length > max_length:
                if current_chunk:
                    chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length + 2  # +2 for '. '
        
        # Add remaining chunk
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return chunks if chunks else [text]
    
    def query(self, query_text: str, n_results: int = 5, filter_filename: str = None) -> Dict:
        """Query the database with semantic search"""
        try:
            where_clause = None
            if filter_filename and filter_filename != "All Documents":
                where_clause = {"filename": filter_filename}
            
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances'],
                where=where_clause
            )
            
            # Add similarity scores to results
            if 'distances' in results and results['distances']:
                # Convert distances to similarity scores (lower distance = higher similarity)
                distances = results['distances'][0]
                similarities = [1 / (1 + dist) for dist in distances]  # Normalize to 0-1
                results['similarities'] = [similarities]
            
            return results
        except Exception as e:
            return {'error': str(e)}
    
    def get_all_documents(self) -> List[str]:
        """Get list of all unique documents"""
        try:
            results = self.collection.get()
            filenames = set()
            if results and 'metadatas' in results:
                for metadata in results['metadatas']:
                    filenames.add(metadata.get('filename', 'Unknown'))
            return list(filenames)
        except Exception as e:
            return []
    
    def clear_collection(self):
        """Clear all data from collection"""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self._get_or_create_collection()
            return True, "Database cleared successfully"
        except Exception as e:
            return False, f"Error clearing database: {str(e)}"
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        try:
            results = self.collection.get()
            total_chunks = len(results['ids']) if results and 'ids' in results else 0
            unique_docs = len(self.get_all_documents())
            
            return {
                'total_chunks': total_chunks,
                'unique_documents': unique_docs
            }
        except Exception as e:
            return {'error': str(e)}