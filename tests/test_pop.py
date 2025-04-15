import pytest
from langchain_core.messages import AIMessage, HumanMessage


def test_messages_pop():
    # 테스트용 메시지 배열 생성
    messages = [
        HumanMessage(content="안녕하세요"),
        AIMessage(content="안녕하세요! 반갑습니다."),
        HumanMessage(content="오늘 날씨가 좋네요"),
        AIMessage(content="네, 정말 좋은 날씨입니다."),
        HumanMessage(content="마지막 메시지입니다"),
    ]

    # 원래 길이 저장
    original_length = len(messages)

    # 마지막 메시지 pop
    last_message = messages.pop()

    # 테스트 1: messages 길이가 1 줄어들었는지 확인
    assert len(messages) == original_length - 1

    # 테스트 2: pop된 메시지가 마지막 메시지인지 확인
    assert last_message.content == "마지막 메시지입니다"

    # 테스트 3: messages의 마지막 메시지가 이전 메시지인지 확인
    assert messages[-1].content == "네, 정말 좋은 날씨입니다."

    # 테스트 4: messages가 비어있지 않은지 확인
    assert len(messages) > 0


if __name__ == "__main__":
    pytest.main([__file__])
