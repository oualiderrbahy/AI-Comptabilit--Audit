from chatbot import answer_question


def test_answer_question_tva():
    answer = answer_question("Quelle est la TVA ?")
    assert "20 %" in answer


def test_answer_question_unknown():
    answer = answer_question("Que pensez-vous du climat ?")
    assert "Essayez" in answer
