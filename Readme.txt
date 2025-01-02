=== RECONNECTION PROMPT ===

We are working on a Story Producer Chatbot application that helps media producers analyze interview transcripts, extract character information, and generate insights. The application processes interview transcripts to identify characters, relationships, and key story elements using AI.

We lost connection. We are migrating the Story Producer Chatbot from Digital Ocean to RunPod. Here's our status:

Current Setup:
- RunPod A100 PCIe (80GB GPU, $1.64/hr)
- 1TB Storage (100GB Container, 1024GB Volume)
- Project files migrated from DO to /workspace/chatbot
- Virtual environment: /workspace/deepseek_env

Current Task: Installing DeepSeek-V3 using AWQ quantization
- Downloading 163 shards (~700GB total)
- Speed: ~43MB/s
- Location: /workspace/chatbot/test_deepseek.py

Project Status:
- All files transferred from DO
- Requirements installed
- Directory structure maintained
- Ready for DeepSeek integration

Next Steps:
1. Complete DeepSeek download
2. Integrate with Flask application
3. Update prompts and services
4. Test functionality

Previous DO server (162.243.42.76) can be decommissioned.

You can find:
- Project files in /workspace/chatbot
- Logs in /workspace/chatbot/logs
- Installation progress in test_deepseek.py
- Virtual environment in /workspace/deepseek_env

We were in the process of downloading DeepSeek-V3 to replace Mistral due to token limit issues. The download is happening on the RunPod server and continues even if disconnected."

CURRENT STATE:
- Basic transcript processing working
- Character extraction implemented but needs optimization
- UI framework in place with sidebar and main chat area
- Basic error handling and logging implemented
- Recently fixed character list refresh functionality

CRITICAL FILES:
- services/character_service.py: Character extraction and management
- services/transcript_service.py: Transcript processing
- routes/character.py: Character-related endpoints
- routes/transcript.py: Transcript handling endpoints
- prompts/character_brief.py: Character analysis prompts
- prompts/extract_characters.py: Name extraction prompts

Here's a detailed summary of what we've done and what remains to be done:
COMPLETED:
	0.	Added character refresh functionality
	0.	Added notification system
	0.	Fixed character name extraction with chunking
	0.	Added character extraction prompt
	0.	Improved error handling
REMAINING TASKS WITH DETAILS:
	0.	Source Management
	•	Add delete source button to UI (partially done)
	•	Add delete confirmation dialog with options:
	•	Show filename to be deleted
	•	Warning about character list updates
	•	Confirm/Cancel buttons
	•	Implement source hide/show toggle:
	•	Add toggle button to source list items
	•	Save state in localStorage
	•	Update UI to reflect hidden sources
	•	Add visual feedback:
	•	Highlight selected source
	•	Show loading state during operations
	•	Update character list after source changes
	0.	Character Interface
	•	Update character display to show full names:
	•	Modify character list items to show full name
	•	Add tooltip with basic info
	•	Handle long names with proper truncation
	•	Implement character click behavior:
	•	Show brief summary in a popup/sidebar
	•	Include quick stats/info
	•	Add close/minimize options
	•	Update character brief generation to include:
	•	Full name
	•	Age (if mentioned)
	•	Position/job
	•	Relationships to other characters
	•	Role in story
	•	Add character list refresh after any source changes:
	•	Auto-refresh on source deletion
	•	Auto-refresh on new uploads
	•	Add manual refresh button (completed)
	0.	Chat Agent Improvements
	•	Integrate new prompts from /users/noochmedia/desktop/new_prompts:
	•	Add new prompt files
	•	Update prompt manager
	•	Modify routing logic
	•	Implement prompt routing system:
	•	Add context awareness
	•	Route to appropriate prompt based on query type
	•	Handle multi-part questions
	•	Add session memory persistence:
	•	Store conversation history
	•	Maintain context across page reloads
	•	Clean up old sessions
	•	Improve response targeting:
	•	Better question analysis
	•	More focused responses
	•	Handle follow-up questions
	•	Add context awareness:
	•	Track current conversation topic
	•	Remember referenced characters/events
	•	Link related information
	0.	Status Indicator (UI Updates)
	•	Remove "Using GPT-4 Turbo" text
	•	Add connection status indicator:
	•	Green dot for connected
	•	Red for disconnected
	•	Yellow for processing
	•	Add server health check:
	•	Periodic API status check
	•	Monitor response times
	•	Show warning on slow responses
	•	Add visual feedback:
	•	Loading spinners
	•	Progress indicators
	•	Success/error states
	0.	Error Handling
	•	Add comprehensive error logging:
	•	Client-side errors
	•	API failures
	•	System errors
	•	Improve error messages:
	•	User-friendly descriptions
	•	Suggested actions
	•	Clear error codes
	•	Add retry mechanism:
	•	Auto-retry on network errors
	•	Backoff strategy
	•	Max retry limits
	•	Add connection recovery:
	•	Auto-reconnect on disconnect
	•	Save pending changes
	•	Resume operations after reconnect
	0.	UI/UX Improvements
	•	Add loading states:
	•	Skeleton loaders
	•	Progress indicators
	•	Cancel options
	•	Improve notification system:
	•	Multiple notification support
	•	Different severity levels
	•	Custom notification duration
	•	Add keyboard shortcuts:
	•	Navigation
	•	Common actions
	•	Help overlay
	•	Improve mobile responsiveness:
	•	Better layout on small screens
	•	Touch-friendly controls
	•	Responsive typography
	0.	Workspace Implementation
	•	User Authentication:
	•	Login system
	•	Password management
	•	Session handling
	•	Workspace Management:
	•	Create/edit workspaces
	•	User permissions
	•	Resource allocation
	•	Transcript Storage:
	•	Digital Ocean integration
	•	Workspace-specific storage
	•	Access control
	•	Multi-user Support:
	•	Concurrent access
	•	User activity tracking
	•	Collaboration features

Current System State:
	•	Backend: Python Flask application
	•	Frontend: HTML/JS with custom UI components
	•	Storage: Local file system + Digital Ocean (planned)
	•	Authentication: Not yet implemented
	•	Character System: Basic implementation with refresh capability
	•	Error Handling: Basic implementation with logging
	•	UI: Partial implementation of modern interface
Next Steps Priority:
	1.	Complete source management features
	2.	Enhance character interface
	3.	Implement workspace system
	4.	Improve error handling
	5.	Add advanced chat features
	6.	Polish UI/UX
	7.	Add monitoring and health check


ADDITIONAL  INFORMATION: 
PROJECT OVERVIEW:
Story Producer Chatbot application for analyzing interview transcripts, extracting character information, 
and generating insights using AI. The system processes interview transcripts to identify characters, 
relationships, and key story elements.

LOCATIONS AND PATHS:
Local Development:
- Main Directory: /users/noochmedia/chatbot/
- Transcripts: /users/noochmedia/chatbot/transcripts/
- New Prompts: /users/noochmedia/desktop/new_prompts/
- Logs: /users/noochmedia/chatbot/flask.log

Production (Digital Ocean):
- Repository: github.com/noochmedia/story-producer-chatbot
- Storage: spaces.digitalocean.com/noochmedia-transcripts
- App URL: story-producer-chatbot-xyz.ondigitalocean.app

KEY FILES AND STRUCTURE:
/users/noochmedia/chatbot/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── index.html            # Frontend interface
├── requirements.txt      # Python dependencies
├── services/
│   ├── character_service.py    # Character extraction
│   ├── transcript_service.py   # Transcript processing
│   ├── chat_service.py        # AI chat handling
│   └── storage.py            # File storage management
├── routes/
│   ├── character.py          # Character endpoints
│   ├── transcript.py         # Transcript endpoints
│   └── chat.py              # Chat endpoints
├── prompts/
│   ├── character_brief.py    # Character analysis
│   ├── extract_characters.py # Name extraction
│   └── story_summary.py     # Story analysis
└── transcripts/             # Uploaded files

DEVELOPMENT ENVIRONMENT:
Local Server: http://localhost:5002
Launch Command: ./launch_local.command
Python Version: 3.11+
Key Dependencies:
- Flask
- OpenAI API
- Mistral AI API
- Digital Ocean SDK

Configuration Structure:
class Config:
    OPENAI_API_KEY = 'sk-...'
    MISTRAL_API_KEY = '...'
    DO_SPACES_KEY = '...'
    DO_SPACES_SECRET = '...'
    UPLOAD_FOLDER = 'transcripts'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

DEPLOYMENT WORKFLOW:
1. Local Development: localhost:5002
2. Git Push: Triggers DO deployment
3. DO Build: Automated via App Platform
4. Production: Uses DO Spaces for storage
