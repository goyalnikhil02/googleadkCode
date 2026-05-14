# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio

from dotenv import load_dotenv
from google import genai
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

APP_NAME="weather_sentiment_agent"
USER_ID="user1234"
SESSION_ID="1234"

load_dotenv()
initial_state = {
    "username": "Nikhil",
    "user_preferences": {
        "favorite_color": "Blue",
        "favorite_food": "Pizza",
        "favorite_movie": "The Matrix",
        "favorite_tv_show": "Game of Thrones"
    }
}

def debug_and_inject_context(callback_context: CallbackContext,llm_request: LlmRequest):
    print("called")
    callback_context.state['username'] = "Nikhil"
    print(callback_context.state.get('username'))





root_agent = Agent(
    model="gemini-2.5-flash",
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


async def main():
    """Main function to run the agent asynchronously."""
    # Session and Runner Setup
    initial_state = {"username": "Nikhil", "user_preferences": { "favorite_color": "Blue", "favorite_food": "Rajma Rice", "favorite_movie": "Bahubali", "favorite_tv_show": "Special OPS" }    }
    session_service = InMemorySessionService()
    # Use 'await' to correctly create the session
    session=await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID,state=initial_state)
    session.state['username']='Nikhil'

    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    # Agent Interaction
    query = "Favorite  color of Nikhil"
    print(f"User Query: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    # The runner's run method handles the async loop internally
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:", final_response)

# Standard way to run the main async function
if __name__ == "__main__":
    asyncio.run(main())