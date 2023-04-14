from pydantic import BaseModel


class Message(BaseModel):
    success: bool
    message: str

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "OK",
            }
        }

    @classmethod
    def ok(cls):
        return cls(success=True, message="OK")


class App(BaseModel):
    id: int
    steam_id: int
    name: str

    class Config:
        schema_extra = {
            "example": {
                "id": 15,
                "steam_id": 620,
                "name": "Portal 2",
            },
        }
