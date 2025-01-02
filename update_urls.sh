#!/bin/bash

# Create a backup of the original file
cp /users/noochmedia/chatbot/index.html /users/noochmedia/chatbot/index.html.bak

# Update all localhost:5002 URLs
sed -i '' 's|http://localhost:5002/|/|g' /users/noochmedia/chatbot/index.html

# Update all localhost:8000 URLs
sed -i '' 's|http://localhost:8000/|/|g' /users/noochmedia/chatbot/index.html

# Set baseUrl to empty string or window.location.origin
sed -i '' 's|const baseUrl = .*;|const baseUrl = window.location.origin;|g' /users/noochmedia/chatbot/index.html
