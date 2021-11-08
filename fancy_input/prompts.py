import sys

RESPONSES = {
    'y': True,
    'yes': True,
    True: True,
    'n': False,
    'no': False,
    False: False
}
PROMPTS = {None: 'y/n', True: 'Y/n', False: 'y/N'}


def fancy_input(question: str,
                validator: callable,
                *,
                error_message: str = None):
    error_msg = error_message if error_message is not None else 'Please enter a valid response.'
    while True:
        try:
            answer = validator(input(f'{question} '))
            return answer
        except Exception:
            answer = False
            print(f'\n{error_msg}\n', file=sys.stderr)


def boolean_prompt(prompt: str, default: bool = None):
    def validate(reply: str) -> bool:
        reply = reply.strip().lower() or default
        r = RESPONSES.get(reply, None)
        if r is None:
            raise ValueError
        return r

    return fancy_input(f'{prompt} [{PROMPTS[default]}]',
                       validate,
                       error_message="Please enter 'yes' or 'no'.")
