try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore

__all__ = ["Literal"]
