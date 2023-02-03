import os
import pyrogram
import whisper
from pydub import AudioSegment
import random
from dotenv import load_dotenv

load_dotenv("config.env")
BOT_TOKEN= os.getenv('BOT_TOKEN')
convert = os.getenv("convert")
error_message = os.getenv("error_message")
app = pyrogram.Client("my_account",1138546, "b7b0949f6eefb3927c20c1684dff4958", bot_token=BOT_TOKEN)
model = whisper.load_model("base")


@app.on_message(filters=pyrogram.filters.text)
async def greeting(client, message):
    if message.text == '/start':
        await message.reply_text("welcome to the transcribe bot\nmy creator is p5pro\n github.com/nimmadev")

@app.on_message(pyrogram.filters.voice  or pyrogram.filters.AudioFile)
async def download_audio(client, message):
    message_reply = await client.send_message(
            chat_id=message.chat.id,
            text=convert,
            reply_to_message_id=message.id
        )
    
    file_path = await message.download()
    output = random.randint(9999, 99999)
    sound = AudioSegment.from_file(file_path)
    sound.export(f"{output}.wav", format="wav")

    try:
        data = model.transcribe(f"{output}.wav")
        await message_reply.edit_text(data["text"])
        os.remove(file_path)
        os.remove(f"{output}.wav")
        print(data["text"])
    except:
        await message_reply.edit_text(error_message)
        os.remove(file_path)
        os.remove(f"{output}.wav")

app.run()