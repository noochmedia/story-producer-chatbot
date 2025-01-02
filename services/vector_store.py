import os
import json
import numpy as np
from typing import List, Dict, Any
import requests
from utils.logger import logger

class VectorStore:
    def __init__(self):
        self.api_url = os.getenv('MISTRAL_API_URL')
        self.api_key = os.getenv('MISTRAL_API_KEY')
        self.embeddings_file = 'embeddings.json'
        self.chunk_size = 500  # words per chunk
        self.overlap = 100     # words overlap between chunks
        
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text using Mistral AI"""
        try:
            response = requests.post(
                f"{self.api_url}/v1/embeddings",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": "mistral-embed",
                    "input": text
                }
            )
            
            if response.status_code == 200:
                return response.json()['data'][0]['embedding']
            else:
                raise Exception(f"API error: {response.text}")
                
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            raise

    def chunk_transcript(self, text: str, transcript_id: str) -> List[Dict[str, Any]]:
        """Split transcript into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            # Create chunk with metadata
            chunk = {
                'text': chunk_text,
                'transcript_id': transcript_id,
                'position': i // (self.chunk_size - self.overlap),
                'word_count': len(chunk_words)
            }
            chunks.append(chunk)
            
        return chunks

    def process_transcripts(self, transcript_service) -> None:
        """Process all transcripts and create embeddings"""
        try:
            all_chunks = []
            transcript_files = transcript_service.get_transcript_list()
            
            for transcript_id in transcript_files:
                try:
                    path = os.path.join('transcripts', transcript_id)
                    with open(path, 'r') as f:
                        content = f.read()
                    
                    # Create chunks for this transcript
                    chunks = self.chunk_transcript(content, transcript_id)
                    
                    # Create embeddings for each chunk
                    for chunk in chunks:
                        embedding = self.create_embedding(chunk['text'])
                        chunk['embedding'] = embedding
                        all_chunks.append(chunk)
                        
                except Exception as e:
                    logger.error(f"Error processing transcript {transcript_id}: {str(e)}")
                    continue
            
            # Save all chunks with their embeddings
            self.save_embeddings(all_chunks)
            
        except Exception as e:
            logger.error(f"Error in process_transcripts: {str(e)}")
            raise

    def save_embeddings(self, chunks: List[Dict[str, Any]]) -> None:
        """Save chunks and their embeddings to file"""
        try:
            with open(self.embeddings_file, 'w') as f:
                json.dump(chunks, f)
        except Exception as e:
            logger.error(f"Error saving embeddings: {str(e)}")
            raise

    def load_embeddings(self) -> List[Dict[str, Any]]:
        """Load chunks and their embeddings from file"""
        try:
            if os.path.exists(self.embeddings_file):
                with open(self.embeddings_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading embeddings: {str(e)}")
            return []

    def find_relevant_chunks(self, query: str, num_chunks: int = 5) -> List[Dict[str, Any]]:
        """Find most relevant chunks for a query"""
        try:
            # Create embedding for query
            query_embedding = self.create_embedding(query)
            
            # Load all chunks
            chunks = self.load_embeddings()
            if not chunks:
                return []
            
            # Calculate similarities
            similarities = []
            for chunk in chunks:
                chunk_embedding = chunk['embedding']
                similarity = self.calculate_similarity(query_embedding, chunk_embedding)
                similarities.append((similarity, chunk))
            
            # Sort by similarity and get top chunks
            similarities.sort(reverse=True, key=lambda x: x[0])
            top_chunks = [chunk for _, chunk in similarities[:num_chunks]]
            
            return top_chunks
            
        except Exception as e:
            logger.error(f"Error finding relevant chunks: {str(e)}")
            return []

    @staticmethod
    def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0