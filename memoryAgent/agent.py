import uuid


from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService
import asyncio
import uuid
temp_service=InMemorySessionService()
async def main():

    session=await temp_service.create_session(
        app_name="nikhil_demo",
        user_id=f"nikhil{uuid.uuid4()}",
        state={"initial_key":"Hello World for State "},
        )

    print(f"Session id ('id'): {session.id}")
    print(f"Application Name : {session.app_name}")
    print(f"Session user id): {session.user_id}")
    print(f"Session State: {session.state}")
    print(f"Events: {session.events}")





if __name__ == "__main__":
    asyncio.run(main())


