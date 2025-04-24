#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it to add your OpenAI API key."
fi

# Create data directory
mkdir -p data

echo "Setup complete! You can now run the application."
echo "To activate the virtual environment in the future, run: source venv/bin/activate"
echo ""
echo "To run the example script: python example.py"
echo "To run the interactive chat: python -m pdf_rag.chat --pdf <pdf_path> --password <password> --persist_dir ./data/vectorstore"
echo "To run the web interface: streamlit run app.py"