from typing import Any

from pydantic import BaseModel, model_validator

NON_DELETE_PROPERTIES = ["id", "delete"]


class BaseCZMLObject(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def validate_model_before(cls, data: dict[str, Any]) -> Any:
        if (
            data is not None
            and isinstance(data, dict)
            and "delete" in data
            and data["delete"]
        ):
            return {
                "delete": True,
                "id": data.get("id"),
                **{k: None for k in data if k not in NON_DELETE_PROPERTIES},
            }
        return data

    def __str__(self) -> str:
        return self.to_json()

    def dumps(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def to_json(self, *, indent: int = 4) -> str:
        return self.model_dump_json(exclude_none=True, indent=indent)
