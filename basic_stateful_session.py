import asyncio
import os

import content_types
from dotenv import load_dotenv
from pprint import pprint
import uuid
from google.genai import types
from google.adk import Runner, Agent
from google.adk.sessions import InMemorySessionService
from google.genai.types import Part

load_dotenv()

root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="root_agent",
    description="An agent that answers questions about user preferences",
    instruction="""
    Helpful assistant that answers questions about the user's preferences.

    The user's name is {username}.

    The user has the following preferences:
    - Favorite color: {user_preferences.favorite_color}
    - Favorite food: {user_preferences.favorite_food}
    - Favorite movie: {user_preferences.favorite_movie}
    - Favorite TV show: {user_preferences.favorite_tv_show}

    Always answer questions about the user's preferences based on this information.
    """
)

# Load environment variables
load_dotenv()

async def main():
    initial_state = {"username": "Nikhil", "user_preferences": { "favorite_color": "Blue", "favorite_food": "Rajma Rice", "favorite_movie": "Bahubali", "favorite_tv_show": "Special OPS" }    }
    #ceate an in-memory session service
    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())
    session = await session_service.create_session(app_name="NikhilBot",user_id="nikhil_bot",session_id=session_id,state=initial_state)
    runner = Runner( root_agent=root_agent,session_service=session_service)
    query="Whats it he favourtite choice for Nikhil"
    print(f"User Query : {query} ")
    content_prompt=types.Content( role="user",parts=[types.Part(text=query)])
    events=runner.run(user_id="nikhil_bot",session_id=session_id,new_message=content_prompt)
    for event in events:
        if event.is_final_response():
            final_response=event.content.parts[0].text
            print("Agent Response : ", final_response)
            print("Session ID:", session_id)
            print("\nSession State Exploration:")
            print(session.state)



# Standard way to run the main async function
if __name__ == "__main__":
    asyncio.run(main())