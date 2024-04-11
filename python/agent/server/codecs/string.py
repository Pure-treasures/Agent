from typing import Any, List, Union


_DefaultStrCodec = "utf-8"
ListElement = Union[bytes, str]

def encode_str(elem: str) -> bytes:
    return elem.encode(_DefaultStrCodec)


def decode_str(encoded: ListElement, str_codec=_DefaultStrCodec) -> str:
    if encoded is None:
        return None

    if isinstance(encoded, bytes):
        return encoded.decode(str_codec)

    if isinstance(encoded, str):
        # NOTE: It may be a string already when decoded from json
        return encoded

    # TODO: Should we raise an error here?
    return ""