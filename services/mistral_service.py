import requests
import time
from utils.logger import logger
from config import Config
from prompts.prompt_manager import PromptManager

class MistralService:
    def __init__(self):
        """Initialize Mistral API configuration"""
        self.api_url = Config.MISTRAL_API_URL
        self.api_key = Config.MISTRAL_API_KEY
        self.last_request_time = 0
        self.min_request_interval = 0.5  # minimum time between requests in seconds

    def manage_rate_limit(self):
        """Simple rate limiting to prevent overwhelming the API"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

    def chunk_text(self, text, max_chunk_size=20000):
        """Split text into chunks that won't exceed token limits"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_size += len(word) + 1  # +1 for space
            if current_size > max_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = len(word) + 1
            else:
                current_chunk.append(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def get_chat_response(self, message, context=None):
        """Get a response from Mistral's chat model"""
        try:
            # Prepare the messages
            messages = []
            
            # Detect prompt type from message and handle context accordingly
            if context:
                prompt_type = PromptManager.detect_prompt_type(message)
                if prompt_type:
                    # Use appropriate prompt-based context
                    context = self.prepare_context_with_prompt(context, prompt_type)
                elif len(context) > 24000:  # If no specific prompt detected but context is large
                    # Default to summary approach for large context
                    context = self.summarize_context(context)
                
                messages.append({
                    "role": "system",
                    "content": context
                })
            
            # Add the user's message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Apply rate limiting
            self.manage_rate_limit()
            
            # Make the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000  # Reduced to ensure we stay within limits
            }
            
            response = requests.post(
                f"{self.api_url}/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                error_msg = f"API request failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            response_json = response.json()
            return response_json['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            logger.error(f"Error in Mistral chat: {str(e)}")
            raise Exception(f"Failed to get chat response: {str(e)}")
            
    def prepare_context_with_prompt(self, context, prompt_type):
        """Prepare context with appropriate prompt based on type"""
        prompt = PromptManager.get_prompt(prompt_type)
        if not prompt:
            return context

        # Split context into manageable chunks
        chunks = self.chunk_text(context, 20000)
        
        # Combine prompt with appropriate amount of context
        if chunks:
            # For character analysis, include more chunks as characters might be mentioned throughout
            if prompt_type == 'character_brief':
                context_text = "\n---\n".join(chunks[:3])  # Use up to 3 chunks
            else:
                context_text = chunks[0]  # Use first chunk for other types
            
            return f"{prompt}\n\nAnalyze the following transcript(s):\n\n{context_text}"
        
        return context

    def extract_character_info(self, context):
        """Extract information about characters from the context"""
        return self.prepare_context_with_prompt(context, 'character_brief')
    
    def summarize_context(self, context):
        """Create a summary of the context that fits within token limits"""
        return self.prepare_context_with_prompt(context, 'story_summary')
    
    @staticmethod
    def get_story_context(transcripts):
        """Generate a context message based on available transcripts"""
        if not transcripts:
            return """You are an advanced story analysis assistant, with enhanced capabilities for processing and analyzing large amounts of text. No transcripts have been uploaded yet.
            
Please let users know they need to upload transcripts before you can analyze them.

Your capabilities include:
1. Comprehensive story analysis across multiple dimensions (structure, themes, pacing, etc.)
2. Advanced character psychology and development tracking
3. Recognition of subtle narrative patterns and literary techniques
4. Cross-referencing with literary and cinematic traditions
5. Generation of detailed, actionable insights

You can help users with:
- Understanding story structure and narrative flow
- Character development and arc analysis
- Theme identification and exploration
- Plot consistency and pacing analysis
- Guidance on using the system's features and transcript upload process

Feel free to provide detailed, nuanced responses that demonstrate your deep understanding of storytelling and narrative craft."""
        
        return f"""You are an advanced story analysis assistant with enhanced capabilities for processing and analyzing large amounts of text. You have access to {len(transcripts)} transcripts.

Your capabilities include:
1. Comprehensive narrative analysis:
   - Story structure and plot progression
   - Theme identification and development
   - Pacing and dramatic tension
   - Genre conventions and innovations
   - Narrative voice and perspective

2. Advanced character analysis:
   - Psychological profiling and development
   - Relationship dynamics and evolution
   - Character arcs and transformations
   - Motivation and conflict analysis
   - Dialogue patterns and voice consistency

3. Literary and dramatic techniques:
   - Symbolism and metaphor tracking
   - Foreshadowing and callbacks
   - Subtext and layered meanings
   - Narrative devices and their effects
   - Style analysis and tone mapping

4. Story development support:
   - Plot hole identification
   - Consistency checking
   - Character development opportunities
   - Theme reinforcement suggestions
   - Pacing optimization recommendations

Please use the available transcript content to inform your responses and provide specific examples when relevant. Your analysis should be thorough and nuanced, taking advantage of your enhanced capabilities for processing complex narratives and generating detailed insights.

When analyzing the transcripts, feel free to:
- Draw connections between different parts of the story
- Identify subtle patterns and recurring elements
- Suggest potential improvements or alternative approaches
- Provide concrete examples from the text
- Offer detailed explanations of your observations

Remember to maintain a balance between high-level analysis and specific textual details in your responses."""