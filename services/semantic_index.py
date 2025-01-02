import os
import json
import numpy as np
from typing import List, Dict, Any
import requests
from utils.logger import logger

class SemanticIndex:
    def __init__(self):
        self.api_url = os.getenv('MISTRAL_API_URL')
        self.api_key = os.getenv('MISTRAL_API_KEY')
        self.index_file = 'semantic_index.json'
        self.paragraph_length = 300  # words per paragraph
        self.overlap = 50  # words overlap between paragraphs
        
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding using our self-hosted model"""
        try:
            # Prepare the API call
            headers = {
                'Content-Type': 'application/json'
            }
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            data = {
                'input': text
            }
            
            response = requests.post(
                f"{self.api_url}/v1/embeddings",
                headers=headers,
                json=data,
                verify=False
            )
            
            if response.status_code == 200:
                return response.json()['data'][0]['embedding']
            else:
                raise Exception(f"API error: {response.text}")
                
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            raise

    def prepare_paragraph(self, text: str) -> List[Dict[str, Any]]:
        """Split text into paragraphs with metadata"""
        words = text.split()
        paragraphs = []
        
        for i in range(0, len(words), self.paragraph_length - self.overlap):
            # Get words for this paragraph with overlap
            para_words = words[i:i + self.paragraph_length]
            if not para_words:
                continue
                
            # Create paragraph text
            para_text = ' '.join(para_words)
            
            # Create embedding for paragraph
            try:
                embedding = self.create_embedding(para_text)
                
                # Store paragraph with metadata
                paragraphs.append({
                    'text': para_text,
                    'position': i // (self.paragraph_length - self.overlap),
                    'word_count': len(para_words),
                    'embedding': embedding
                })
            except Exception as e:
                logger.error(f"Error processing paragraph: {str(e)}")
                continue
                
        return paragraphs

    def process_transcripts(self, transcript_service) -> None:
        """Process all transcripts and create semantic index"""
        try:
            indexed_content = []
            transcript_files = transcript_service.get_transcript_list()
            
            for transcript_id in transcript_files:
                try:
                    path = os.path.join('transcripts', transcript_id)
                    with open(path, 'r') as f:
                        content = f.read()
                    
                    # Process transcript into paragraphs
                    paragraphs = self.prepare_paragraph(content)
                    
                    # Add transcript metadata to each paragraph
                    for para in paragraphs:
                        para['transcript_id'] = transcript_id
                        indexed_content.append(para)
                        
                except Exception as e:
                    logger.error(f"Error processing transcript {transcript_id}: {str(e)}")
                    continue
            
            # Save indexed content
            self.save_index(indexed_content)
            
        except Exception as e:
            logger.error(f"Error in process_transcripts: {str(e)}")
            raise

    def save_index(self, indexed_content: List[Dict[str, Any]]) -> None:
        """Save indexed content to file"""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(indexed_content, f)
        except Exception as e:
            logger.error(f"Error saving index: {str(e)}")
            raise

    def load_index(self) -> List[Dict[str, Any]]:
        """Load indexed content from file"""
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading index: {str(e)}")
            return []

    def find_relevant_content(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Find most relevant paragraphs for a query"""
        try:
            # Create embedding for query
            query_embedding = self.create_embedding(query)
            
            # Load indexed content
            indexed_content = self.load_index()
            if not indexed_content:
                return []
            
            # Calculate similarities
            similarities = []
            for item in indexed_content:
                similarity = self.calculate_similarity(query_embedding, item['embedding'])
                similarities.append((similarity, item))
            
            # Sort by similarity and get top results
            similarities.sort(reverse=True, key=lambda x: x[0])
            return [item for _, item in similarities[:num_results]]
            
        except Exception as e:
            logger.error(f"Error finding relevant content: {str(e)}")
            return []

    @staticmethod
    def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0