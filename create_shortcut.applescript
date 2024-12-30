tell application "Finder"
    set desktop_path to (path to desktop) as text
    set app_name to "Story Producer Chatbot.app"
    set app_path to desktop_path & app_name
    
    try
        -- Create the application bundle
        tell application "Script Editor"
            -- The actual script content
            set app_content to "on run
                set chatbotPath to \"/Users/noochmedia/chatbot/launch_chatbot.command\"
                
                tell application \"Terminal\"
                    -- Execute the launch script
                    do script quoted form of chatbotPath
                    
                    -- Activate Terminal
                    activate
                end tell
            end run"
            
            make new document with properties {text:app_content}
            save document 1 in app_path as "application"
            quit
        end tell
        
        -- Set executable permission on the launch script
        do shell script "chmod +x '/Users/noochmedia/chatbot/launch_chatbot.command'"
        
        -- Show success message
        display dialog "Desktop shortcut 'Story Producer Chatbot' has been created successfully!" buttons {"OK"} default button "OK"
        
    on error errMsg
        display dialog "Error creating shortcut: " & errMsg buttons {"OK"} default button "OK" with icon stop
    end try
end tell