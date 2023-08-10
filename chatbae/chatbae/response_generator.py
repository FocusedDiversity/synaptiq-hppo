from typing import Optional


class ResponseGenerator():
    offset: int = 0

    def __init__(self):
        self.offset = 0

    def reset(self):
        self.offset = 0

    def update(self, msg: str, final: bool = False) -> Optional[str]:
        triple_backtick_count = msg[self.offset:].count("```")
        if triple_backtick_count % 2 == 1:
            return None

        new_offset = self.offset
        if triple_backtick_count > 0:
            new_offset = msg.rfind("```") + 3

        if "\n" in msg[new_offset:]:
            new_offset = msg.rfind("\n") + 1

        if new_offset > self.offset:
            old_offset = self.offset
            self.offset = new_offset
            return msg[old_offset:new_offset]
        if final:
            old_offset = self.offset
            self.offset = len(msg)
            return msg[old_offset:]
