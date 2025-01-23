from openai import OpenAI
import os
import yt_dlp
from sk import my_sk
from docx import Document

client = OpenAI(
    api_key=my_sk
)

while True:
    print("******Welcome to my AI-Powered Notes Generator for YouTube Videos******")
    url = input("Paste in the Video URL, you want to simplify: ")

    opts = {'outtmpl': 'output.mp4', 'format': 'best',}


    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error: {e}")

    print("The file types supported are mp3, mp4, mpeg, mpga" )
    audio_path = input("Paste the audio file here: ")


    audio_file = open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
    )

    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
                "role": "system",
                "content": "You are a helpful assistant that simplify the user's transcripts ",
                "role": "assistant",
                "content": "Create a cheat sheet using the users transcript including any formulas and definitions",
                "role": "user",
                "content": f"help me to simplify my transcript into notes, here is my {transcript} "
                }],

    )
    notes = chat_completion.choices[0].message.content

    newfile = open("Notes.doc", "w+")
    newfile.write(notes)
    newfile.close()

    answer = input("Would you like to generate notes for another Youtube video (yes/no)?").lower()
    if answer == "no":
        print("Goodbye, thanks for using my AI-Powered Notes Generator for YouTube Videos")
        False


