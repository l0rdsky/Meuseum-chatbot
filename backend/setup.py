#!/usr/bin/env python

import subprocess
import sys
import os

def main():
    """
    Setup script for the Museum Ticket Booking Chatbot Backend
    """
    print("Setting up Museum Ticket Booking Chatbot Backend...")
    
    # Install requirements
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please try manually: pip install -r requirements.txt")
        return
    
    # Create necessary directories
    if not os.path.exists('tickets'):
        os.makedirs('tickets')
        print("Created tickets directory")
    
    print("\nSetup complete!")
    print("\nTo run the server, use: python app.py")
    print("The server will start on http://localhost:5000")
    
    # Check if Gemini API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("\nWARNING: GEMINI_API_KEY environment variable not found!")
        print("Please make sure to set your Gemini API key in the .env file")

if __name__ == "__main__":
    main() 