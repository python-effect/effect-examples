from effect import sync_performer


class ReadLine(object):
    """An effect intent for getting input from the user."""

    def __init__(self, prompt):
        self.prompt = prompt


@sync_performer
def perform_readline_stdin(dispatcher, readline):
    """Perform a :obj:`ReadLine` intent by reading from stdin."""
    return input(readline.prompt)


if __name__ == "__main__":
    from effect import Effect, TypeDispatcher, sync_perform

    # Effect-using code:
    effect = Effect(ReadLine("Tell me your name: ")).on(
        success=lambda name: "Hello, {}!".format(name)
    )
    # Effect-dispatching code:
    dispatcher = TypeDispatcher({ReadLine: perform_readline_stdin})
    print("result of effect:", sync_perform(dispatcher, effect))
