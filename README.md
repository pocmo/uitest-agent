# UI Test Agent

A natural language-based agent for automating UI testing on mobile devices using Google's Gemini AI models.

## Quick Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure:
   ```
   cp config.sample.yaml config.yaml
   ```
   Edit `config.yaml` with your Google API key.

3. Run:
   ```
   python main.py --query "YOUR_TEST_INSTRUCTION"
   ```

## Note
- Mobile MCP server is available as a remote service by default
- Local MCP installation is optional (~/Projects/mobile-mcp)

## Examples
```
python main.py --query "What do you see on the current screen?"

python main.py --query "Open settings and turn on airplane mode"

python main.py --query "Go to the YouTube app. Search for 'meet firefox mobile, part II' then play the first video from the search results."
```