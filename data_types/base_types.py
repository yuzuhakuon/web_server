from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class BaseResponse:
    errorCode: int = 0
    errorMessage: str = "success"
    data: Optional[Dict[str, Any]] = None
