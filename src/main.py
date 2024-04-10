import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
#Open AI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Open AI assistant ID
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

client = OpenAI()

# Create a thread with a message
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            # Query
            "content": "What's the most livable city in the world?",
        }
    ]
)

# Submit the thread to assistant (new run).
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
print(f"👉 Run Created: {run.id}")

# Run status
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"Run Status: {run.status}")
    time.sleep(1)
else:
    print(f"Run Completed!")

# Get the latest message from the thread
message_response = client.beta.threads.messages.list(thread_id=thread.id)
messages = message_response.data

# Print the latest message
latest_message = messages[0]
print(f"Response: {latest_message.content[0].text.value}")