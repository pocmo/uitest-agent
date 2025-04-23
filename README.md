# UI Test Agent

A natural language-based agent for automating UI testing on mobile devices and web applications using Google's Gemini AI models.

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
   python main.py --target [android|ios|web] --query "YOUR_TEST_INSTRUCTION"
   ```
   
   Or pipe content from a file or another command:
   ```
   cat test_prompt.txt | python main.py --target [android|ios|web]
   echo "Check the login screen" | python main.py --target android
   ```

## Note
- Mobile MCP server is available as a remote service by default
- Local MCP installation is optional (~/Projects/mobile-mcp)
- The `--target` parameter is required and must be either `android`, `ios`, or `web`
- When `--query` is not provided, the tool reads from stdin, enabling piped inputs

## Examples

### Android Examples
```
python main.py --target android --query "What do you see on the current screen?"

python main.py --target android --query "Open settings and turn on airplane mode"

python main.py --target android --query "Go to the YouTube app. Search for 'meet firefox mobile, part II' then play the first video from the search results."
```

### iOS Examples
```
python main.py --target ios --query "Go to Apple Maps and find a restaurant in New York. Recommend a good one."

python main.py --target ios --query "Open the calendar and add a new appointment for tomorrow: 'Eat burrito'"
```

### Web Examples
```
python main.py --target web --query "Navigate to github.com and search for 'UI testing frameworks'. List some popular frameworks."

python main.py --target web --query "Go to a news website and tell me about the top story"

python main.py --target web --query "Go to league.com and verify that the careers page has some open positions listed"
```
