on run
    set chatbotPath to "/Users/noochmedia/chatbot/launch_chatbot.command"
    
    tell application "Terminal"
        -- Execute the launch script
        do script quoted form of chatbotPath
        
        -- Activate Terminal
        activate
    end tell
end run