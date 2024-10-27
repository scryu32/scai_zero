from search_engine.weather import forecast # forecast() 하면 현재기온 / 날씨나옴
from search_engine.search import getSearch # getSearch(검색할단어) 치면 됨
from openai import OpenAI
import os
import json

client = OpenAI(
    api_key=os.environ.get('SCAI_KEY'),
)

def fetch_search_bot(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=1600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

#Json 형식으로 리턴함
def use_search_bot(user_input):
    search_instruction = """당신은 인터넷 서핑을 하는 인공지능입니다. 앞으로 대답은 JSON 형식으로 하세요.
당신은 이런식으로 대답할 수 있습니다.
{ "search" : "현재 국제 정세" }
혹은
{ "response" : "None" }
혹은
{ "response" : "weather" }
혹은
{ "response" : "error" }

이때, 키는 반드시 search, response 이여야 하며, search의 값은 자유로운 문자열, response의 값은 None 혹은 weather로 된 문자열이여야합니다.
상대방의 질문이 실시간 정보, 혹은 최신 정보 따위를 검색하기를 원한다면 search, 아니라면 response의 None, 현재 날씨의 정보인 경우는 response의 weather을 응답하세요. 단, 미래의 날씨는 error로 대답하며, 스스로 대답할수 있는 질문(실시간 정보가 아닌것들)은 None으로 응답합니다.
두가지 이상의 대답이나 다른 대답은 허용되지 않습니다. 날씨에 대한 우선순위는 weather입니다. 자연재해(태풍, 지진)에 대한 우선순위는 search입니다.
"""
    messages = [{"role": "system", "content": search_instruction}]
    messages.append({"role": "user", "content": user_input})
    assistant_response = fetch_search_bot(messages)
    return assistant_response

def summarize_bot(search_content):
    search_summarize_instruction = """당신은 검색결과를 요약하는 인공지능으로, 여러가지 검색 결과들을 요약해서 요점을 추려내는것이 목표입니다."""
    messages = [{"role": "system", "content": search_summarize_instruction}]
    messages.append({"role": "user", "content": search_content})
    assistant_response = fetch_search_bot(messages)
    return assistant_response


def use_search_engine(user_input):
    try:
        search_response = use_search_bot(user_input)
        response_data = json.loads(search_response)
        
        search_query = response_data.get("search")
        response_type = response_data.get("response")
        
        if search_query:
            search_response_bot = getSearch(search_query)
            summarized_content =  summarize_bot(search_response_bot)
            return f"다음은 검색 결과의 요약본입니다: \n {summarized_content}"
        elif response_type == "weather":
            weather = forecast()
            return f"현재 날씨는 {weather[1]}, {weather[0]}도입니다."
        elif response_type == "error":
            return "응답을 처리할 수 없음(현재의 날씨만 답할 수 있음)"
        else:
            return 0
    except json.JSONDecodeError:
        return "JSON 파싱 오류: 응답을 처리할 수 없습니다."
    except Exception as e:
        return f"처리 중 오류가 발생했습니다: {e}"
