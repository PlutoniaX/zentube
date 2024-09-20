import os
import dspy
import json
import shutil
from datetime import datetime
from llm import groq_response

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

output_env = os.getenv("OUTPUT_DIR")
output_dir = os.path.expanduser(output_env)

unprocessed_dir = os.path.join(base_dir, "experiments", "youtube", "transcripts", "unprocessed")

processed_dir = os.path.join(base_dir,  "experiments", "youtube","transcripts", "processed")
        

def process_all_transcripts(roast=False):
    """Processes all transcript files in a specified directory, optionally roasting them.
    
    Args:
        roast (bool, optional): If True, roasts the transcript instead of summarizing. Defaults to False.
    
    Returns:
        None: This function doesn't return a value, but it produces side effects:
            - Prints processing status messages to the console.
            - Creates markdown files in the output directory.
            - Moves processed JSON files to the processed directory.
    
    Raises:
        Exception: If there's an error during file processing, it's caught and printed.
    """
    try:
        print("\n\n📝 Processing transcripts...\n")
        
        # DSPy is already configured in llm.py, so we don't need to do it here
        
        os.makedirs(processed_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        for filename in os.listdir(unprocessed_dir):
            print(f"📄 Processing {filename}")
            if filename.endswith(".json"):
                file_path = os.path.join(unprocessed_dir, filename)
                
                with open(file_path, 'r') as file:
                    video_data = json.load(file)
                
                if roast:
                    markdown_content = roast_transcript(video_data)

                else:
                    summary = process_transcript(
                        video_data['transcript'],
                        video_data['title'],
                        video_data['description']
                    )

                    markdown_content = create_markdown_with_frontmatter(summary, video_data)
                    

                # Create markdown filename
                md_filename = video_data['title'][:100]  # Limit length to first 100 characters
                md_filename = ''.join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in md_filename)
                md_filename = md_filename.strip() + ".md"
                md_file_path = os.path.join(output_dir, md_filename)
                
                print(f"\n📝 Writing md to {md_file_path}")
                with open(md_file_path, 'w') as md_file:
                    md_file.write(markdown_content)
                    
                    
                # Move processed JSON file
                shutil.move(file_path, os.path.join(processed_dir, filename))

                print(f"✅Processed: {filename}\n")
    except Exception as e:
        print(f"🚨 Error processing files: {e}")
            
def process_transcript(transcript, title, description):
    """Processes a YouTube video transcript and generates a summary.
    
    Args:
        transcript (str): The full transcript of the YouTube video.
        title (str): The title of the YouTube video.
        description (str): The description of the YouTube video.
    
    Returns:
        str: A formatted markdown string containing the generated summary and the full transcript.
    """
    print(f"\nProcessing transcript for {title}\n")
    summarizer = YouTubeSummarizer()
    
    result = summarizer(title=title, description=description)
    print(f"🤖 Generated summary prompt: {result.summarization_prompt}")
    
    # Generate a summary from the summarization prompt
    summary = groq_response(result.summarization_prompt, temp=0)
    print(f"\nSummary: {summary}...")
    
    
    md_data = f"""

## Summary
"""Creates a Markdown string with frontmatter containing video metadata and summary.

Args:
    summary (str): A summary of the video content.
    video_data (dict): A dictionary containing video metadata with keys:
        'title', 'channel_name', 'view_count', 'publish_date', 'description',
        'thumbnail', and 'video_url'.

Returns:
    str: A formatted Markdown string with frontmatter and video information.
"""
{summary}
        
## Transcript
{transcript}
    """
    Initialize a new instance of the class.
    
    This method initializes the object by calling the superclass's __init__ method and setting up a summarization prompt generator using dspy.ChainOfThought.
    
    Args:
        None
    
    Returns:
        None
    """
    """
    
    return md_data


"""Generates a summarization prompt based on the given title and description.

Args:
    title (str): The title of the content to be summarized.
    description (str): The description or content to be summarized.

Returns:
    dspy.Prediction: A prediction object containing the generated summarization prompt.
"""
def create_markdown_with_frontmatter(summary, video_data):
    frontmatter = f"""---
title: "{video_data['title']}"
channel_name: "{video_data['channel_name']}"
view_count: "{video_data['view_count']}"
publish_date: "{video_data['publish_date']}"
processed_date: "{datetime.now().isoformat()}"
description: "{video_data['description']}"
---

## {video_data['channel_name']}
Published: {datetime.fromisoformat(video_data['publish_date']).strftime('%B %d, %Y')}, Processed: {datetime.now().strftime('%B %d, %Y')}

[![Thumbnail]({video_data['thumbnail']})]({video_data['video_url']})

{summary}
"""
    return frontmatter


class SummarizationPromptGenerator(dspy.Signature):
    """Given the title and description of a YouTube video, generate a summarization prompt to be used with an AI assistant. The prompt should be specific to the video title and description, and aim to provide an engaging and informative summary of the video's content. Make the prompt in a way that is easy to understand and follow, and avoid using technical jargon or complex language, and remember that the general idea here is to make a prompt so that the AI can create the best possible summary of the video, packed with key takeaways and useful insights. If the video is about crypto, make sure to include actions to extract the tokens to buy or sell and why in the prompt"""
    title = dspy.InputField()
    description = dspy.InputField()
    summarization_prompt = dspy.OutputField()

    
    
class YouTubeSummarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarization_prompt_generator = dspy.ChainOfThought(SummarizationPromptGenerator)

    def forward(self, title, description):
        # Create a summarization prompt
        """Generates a markdown-formatted analysis of a video transcript, including constructive feedback and a comedic roast.
        
        Args:
            video_data (dict): A dictionary containing video information and transcript data.
        
        Returns:
            str: A markdown-formatted string containing video details, constructive feedback, and a comedic roast.
        """
        summarization_prompt = self.summarization_prompt_generator(title=title, description=description)
        
        return dspy.Prediction(summarization_prompt=summarization_prompt.summarization_prompt)
    
    
    
    

def roast_transcript(video_data):
    
    useful_video_data = f"""
    Video views: {video_data["view_count"]}
    Likes: {video_data["like_count"]}
    Comments: {video_data["comment_count"]}
    Duration: {video_data["duration"]}
    Transcript:
    {video_data["transcript"]} """
    
    constructive = groq_response(f"""You are a professional YouTuber and esteemed podcast host. Two aspiring podcasters have given you a podcast transcript from their latest episode: {video_data["title"]}, you have been tasked with giving constructive feedback. They are seeking actionable advice on how to improve the podcast. From growth tips like YouTube SEO, to delivery and content, nothing is off the table. What went well, what could improve, they want any and all feedback to improve their skills and final product. Format all responses as markdown, and remember to to be constructive and positive!

    {useful_video_data}
   """, temp=0.5)
    print(f"\nConstructive feedback: {constructive[:50]}...")


    # ROAST 'EM!!!
    roast = groq_response(f"""You're a witty comedian at a roast battle. Two aspiring podcasters have given you a podcast transcript from their latest episode: {video_data["title"]}, your job is to roast them. Comedy central style. Don't be afraid to give 'em a good ROAST!
    
    Remember to:
    1. Keep it clever and creative - puns and wordplay are your friends.
    2. Focus on their content and delivery, not personal attacks.
    3. Mix in some backhanded compliments for extra laughs.
    4. Reference specific moments or quotes from the transcript if possible.
    5. End with a light-hearted encouragement to keep improving.

    Use this info to fuel your roast:
    {useful_video_data}""", temp=1)
    print(f"\nRoast: {roast[:50]}...")
    
    
    
    
    md_data = f"""
## {video_data['channel_name']}
### Views: {video_data["view_count"]}
### Likes: {video_data["like_count"]}
### Comments: {video_data["comment_count"]}
### Duration: {video_data["duration"]}
Published: {datetime.fromisoformat(video_data['publish_date']).strftime('%B %d, %Y')}, Processed: {datetime.now().strftime('%B %d, %Y')}

[![Thumbnail]({video_data['thumbnail']})]({video_data['video_url']})
        
## Constructive Feedback
{constructive}
        
## ROAST 🔥
{roast}
    """
    return md_data