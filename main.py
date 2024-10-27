from chatbot import fetch_assistant_response
from search_engine.main_search_engine import use_search_engine

system_instruction = """당신은 친근한 말투로 대화하는 챗봇입니다. 간결하고 짧게 반말로 대답하세요. 이후에 오는 시스템 프롬프트는 사용자의 질문에 대한 대답으로, 프롬프트를 참고하여 대답해주세요."""

def use_chatbot():
    messages = [{"role": "system", "content": system_instruction}]
    while True:
        user_input = input("")
        if user_input == "종료":
            break
        messages.append({"role": "user", "content": user_input})
        search_response = use_search_engine(user_input)
        if search_response != 0:
            messages.append({"role": "system", "content": search_response})
        assistant_response = fetch_assistant_response(messages)
        print(assistant_response)
        messages.append({"role": "assistant", "content": assistant_response})


use_chatbot()