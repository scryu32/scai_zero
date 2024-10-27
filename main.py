from chatbot import fetch_assistant_response

system_instruction = """당신은 친근한 말투로 대화하는 챗봇입니다. 간결하고 짧게 반말로 대답하세요."""

def use_chatbot(messages):
    messages = [{"role": "system", "content": system_instruction}]
    while True:
        user_input = input("")
        if user_input == "종료":
            break
        messages.append({"role": "user", "content": user_input})
        assistant_response = fetch_assistant_response(messages)
        print(assistant_response)
        messages.append({"role": "assistant", "content": assistant_response})


