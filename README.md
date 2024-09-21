## Zentube 

Break Free from Endless YouTube Scrolling. Meet ZenTube—the AI-powered tool that finds the insights you're looking for, cutting the distractions and saving you hours. You deserve to enjoy only the best parts of each video—without the mindless rabbit holes.

This documentation details the workings of Zentube, a Python-based system designed to automatically process and summarize YouTube videos. The project utilizes various APIs and libraries, including YouTube Data API, YouTube Transcript API, Exa, Groq, and dspy, for video retrieval, transcript generation, summarization, and content analysis.

### Workflow

1. **Video Acquisition:**
   - `add_videos.py` is responsible for finding YouTube videos based on user input and adding them to a specified playlist. It uses Exa's search and content functionality for relevant video discovery.
2. **Transcript Generation:**
   - `generate_transcripts.py` fetches videos from the specified playlist and generates transcripts using the YouTube Transcript API. It also stores video details like title, publish date, and view counts.
3. **Transcript Processing:**
   - `process_transcript.py` analyzes the generated transcripts and produces summaries or roasts using the Groq API. The summarization process leverages dspy for constructing summarization prompts based on video titles and descriptions.
4. **Output Generation:**
   - The processed transcripts are transformed into Markdown files containing summaries, roasts, or both. These files are organized into folders based on processing status (unprocessed, processed).

### Usage

To utilize Zentube, you'll need to:

1. **Configure:**
   - Set up environment variables (in `.env`) for API keys, playlist IDs, and output directory paths.
   - Obtain API credentials for YouTube and Google Cloud services.
2. **Run:**
   - Execute `main.py` with optional arguments like `--discover` for adding videos, `--roast` for enabling roast mode, and `--include`/`--exclude` for refining video searches.

### Functionality Overview

**add_videos.py:**
  - Searches YouTube based on user prompts. 
  - Integrates with Exa for relevant video discovery.
  - Adds discovered videos to the specified playlist.

**generate_transcripts.py:**
  - Fetches playlist items from a YouTube playlist.
  - Retrieves video details (title, publish date, view count).
  - Extracts transcripts using the YouTube Transcript API.

**process_transcript.py:**
  - Summarizes or roasts transcripts using Groq API and dspy for prompt generation.
  - Formats processed transcripts into Markdown files for easy viewing and sharing.

**llm.py:**
  - Configures Groq API and DSPy for interacting with large language models for summarization and roast generation.

**main.py:**
  - Provides command-line interface for controlling Zentube's functionality.
  - Coordinates the workflow between other modules.

**requirements.txt:**
  - Specifies the Python packages required for the project to run.

### Key Features

- Automated YouTube video processing, from discovery to summarization.
- Use of large language models (Groq) for text analysis and generation.
- Customizable summarization and roast generation options.
- User-friendly command-line interface.
- Flexible and extensible architecture for potential future enhancements.
