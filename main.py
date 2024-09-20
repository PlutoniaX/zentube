import argparse
import os
from generate_transcripts import generate_transcripts   
from add_videos import add_videos
from process_transcript import process_all_transcripts


NUMBER_OF_VIDEOS_TO_ADD = 5
TEXT_TO_INCLUDE = None
TEXT_TO_EXCLUDE = None
ROAST_CHANNEL_ID = os.environ.get("ROAST_CHANNEL_ID")

def ensure_directories_exist():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    directories = ["experiments", "youtube", "transcripts", "unprocessed"]
    
    current_path = base_dir
    for directory in directories:
        current_path = os.path.join(current_path, directory)
        if not os.path.exists(current_path):
            os.makedirs(current_path)
            print(f"Created directory: {current_path}")
        else:
            print(f"Directory already exists: {current_path}")

def main():
    # Ensure necessary directories exist
    ensure_directories_exist()

    parser = argparse.ArgumentParser(description="YouTube video processing script")
    parser.add_argument("--roast", action="store_true", help="Enable roast mode")
    parser.add_argument("--discover", nargs='+', help="Search for videos and add them to the playlist")
    parser.add_argument("--include", nargs='+', default=TEXT_TO_INCLUDE, help="Include videos with these words in the title")
    parser.add_argument("--exclude", nargs='+', default=TEXT_TO_EXCLUDE, help="Exclude videos with these words in the title")
    parser.add_argument("--num", type=int, default=NUMBER_OF_VIDEOS_TO_ADD, help="Number of videos to add (default: 5)")

    args = parser.parse_args()
    if args.roast:
        print("Roast mode enabled!\n")
        return
    elif args.discover:
        query = ' '.join(args.discover)
        print(f"Discovering videos for: {query}")
        print(f"Number of videos to add: {args.num}")
        if args.include:
            print(f"Including text: {args.include[0]}")
        if args.exclude:
            print(f"Excluding text: {args.exclude[0]}")
        add_videos(prompt=query, num_results=args.num, include=args.include[0] if args.include else None, exclude=args.exclude[0] if args.exclude else None)
    
    # Generate transcripts for the videos in the playlist
    generate_transcripts()
    
    process_all_transcripts()
        
    print("\n\n🏁 Done!\n\n")
    
if __name__ == "__main__":
    main()