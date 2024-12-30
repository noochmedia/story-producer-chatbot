import os
import openai
import time
import tiktoken
from utils.logger import logger

class OpenAIService:
    def __init__(self):
        """Initialize OpenAI API key and token counter"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        openai.api_key = api_key
        self.encoding = tiktoken.encoding_for_model("gpt-4-1106-preview")
        self.last_request_time = 0
        self.tpm_limit = 30000  # tokens per minute limit

    def count_tokens(self, text):
        """Count tokens in a text string"""
        if not text:
            return 0
        return len(self.encoding.encode(text))
    
    def manage_rate_limit(self, total_tokens):
        """Manage rate limiting by adding delays if necessary"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < 60 and total_tokens > self.tpm_limit:
            # Wait until a minute has passed
            sleep_time = 60 - time_since_last
            logger.info(f"Rate limit approached. Waiting {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

    def get_chat_response(self, message, context=None):
        """Get a response from OpenAI's chat model"""
        try:
            # Prepare the messages
            messages = []
            total_tokens = 0
            
            # Add system message with context if available
            if context:
                context_tokens = self.count_tokens(context)
                logger.info(f"Context tokens: {context_tokens}")
                total_tokens += context_tokens
                messages.append({
                    "role": "system",
                    "content": context
                })
            
            # Add the user's message
            message_tokens = self.count_tokens(message)
            logger.info(f"Message tokens: {message_tokens}")
            total_tokens += message_tokens
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Check and manage rate limits
            self.manage_rate_limit(total_tokens)
            
            # Calculate remaining tokens for response
            response_limit = min(4000, max(1000, self.tpm_limit - total_tokens))
            logger.info(f"Setting response token limit to: {response_limit}")
            
            # Get response from OpenAI using GPT-4
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=messages,
                max_tokens=response_limit,
                n=1,
                temperature=0.7,
                top_p=0.9
            )
            
            # Extract and return the response text
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error in OpenAI chat: {str(e)}")
            raise Exception(f"Failed to get chat response: {str(e)}")
            
    @staticmethod
    def get_story_context(transcripts):
        """Generate a context message based on available transcripts"""
        if not transcripts:
            return """You are an advanced story analysis assistant powered by GPT-4, with enhanced capabilities for processing and analyzing large amounts of text. No transcripts have been uploaded yet.
            
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
        
        return f"""You are an advanced story analysis assistant powered by GPT-4, with enhanced capabilities for processing and analyzing large amounts of text. You have access to {len(transcripts)} transcripts.

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