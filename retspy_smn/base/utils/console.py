class console:

    YES = "Sí"
    NO = "No"
    CANCEL = "Cancelar"

    YES_NO: list[str] = [YES, NO]
    YES_NO_CANCEL: list[str] = [YES, NO, CANCEL]

    @staticmethod
    def response_is(response: str, expected: str) -> bool:
        return response.strip().lower() == expected.strip().lower()

    @staticmethod
    def prompt(question: str, expect: list[str]) -> str:
        expect_lower: list[str] = [option.lower() for option in expect]

        choices: str = "/".join(expect)

        query_message: str = f"{question} ({choices}): "

        answer: str = ""

        while answer not in expect_lower:
            answer = input(query_message).strip().lower()

        return answer
