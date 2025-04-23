# UI Test Agent

A natural language-based agent for automating UI testing on mobile devices and web applications using Google's Gemini AI models. This tool allows testers and developers to write test instructions in plain English and have them executed on Android, iOS, or web platforms.

> **Note:** This is a prototype/experimental project. While functional, it is not yet ready for production use. Use at your own risk.

## Features

- Natural language interface for UI automation and testing
- Cross-platform support (Android, iOS, Web)
- Integration with Google's Gemini AI models
- Support for complex, multi-step test scenarios
- Real-time feedback and test results

## Requirements

- Python 3.8+
- Google Gemini API key 
- For mobile testing: Android device/emulator or iOS device connected to your machine
- For web testing: Compatible browser

## Quick Setup

0. Create and activate a virtual environment (recommended):
   ```
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

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

## Configuration Options

The `config.yaml` file supports the following options:

- `google_api_key`: Your Google API key for Gemini models
- `use_vertex_ai`: Boolean to use Google Cloud Vertex AI (default: false)
- `model_name`: The Gemini model to use (default: "gemini-2.5-pro-preview-03-25")
- `mobile_mcp_path`: Optional path to local mobile-mcp installation
- `web_mcp_path`: Optional path to local playwright-mcp installation

## Usage Notes

- Mobile MCP server is available as a remote service by default
- Local MCP installation is optional
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

## System Prompts and Instruction Files

The UI Test Agent uses specialized instruction files (system prompts) to guide the AI's behavior when testing different platforms. These files are located in the `prompts/` directory:

### Available Instruction Files

- **agent_instruction.txt**: Core instructions for the UI testing agent that apply to all platforms
- **mobile_instruction.txt**: General mobile testing instructions shared by Android and iOS platforms
- **android_instruction.txt**: Android-specific testing instructions
- **ios_instruction.txt**: iOS-specific testing instructions
- **web_instruction.txt**: Web platform testing instructions

When you run a test with a specific target (android, ios, or web), the system combines the appropriate instruction files to create a comprehensive prompt for the AI. For example, when testing an Android app:

1. First, it loads the core `agent_instruction.txt`
2. Then appends the general `mobile_instruction.txt`
3. Finally adds the target-specific `android_instruction.txt`
