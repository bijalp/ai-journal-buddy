from google import genai
from pydantic import BaseModel
from datetime import date
from google.genai import types


client = genai.Client()


def get_current_date():
    print("🔧 TOOL CALLED: get_current_date()")
    return str(date.today())


def get_day_of_week() -> str:
    print("🔧 TOOL CALLED: get_day_of_week()")
    return date.today().strftime("%A")

class JournalAnalysis(BaseModel):
    mood: str
    energy: str
    summary: str
    follow_up_question: str


conversation = []

conversation = []

while True:
    journal_entry = input("\nYou: ")

    if journal_entry.lower() == "quit":
        break

    # Add user's message to conversation
    conversation.append(f"User: {journal_entry}")

    # Send entire conversation to the model
    prompt = "\n".join(conversation)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    # Get AI response
    buddy_response = response.text

    print(f"\nJournal Buddy: {buddy_response}")

    # Add AI response to conversation history
    conversation.append(f"Journal Buddy: {buddy_response}")


# tool_call = response.candidates[0].content.parts[0].function_call

# print("Tool requested:", tool_call.name)
# print("Arguments:", tool_call.args)


if tool_call.name == "get_current_date":
    result = get_current_date()

elif tool_call.name == "get_day_of_week":
    result = get_day_of_week()
tool_response = types.Part.from_function_response(
    name=tool_call.name,
    response={"result": result},
)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[
        types.Content(
            role="user",
            parts=[types.Part.from_text(
                text="What day is it today?"
            )],
        ),
        response.candidates[0].content,
        types.Content(
            role="user",
            parts=[tool_response],
        ),
    ],
)
print("\nSecond response parts:")

for part in response.candidates[0].content.parts:
    print(part)
