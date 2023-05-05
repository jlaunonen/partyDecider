from pydantic import BaseModel

from .pd_types import VoteTarget, Vote


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


class NewVotingSession(BaseModel):
    duration: int | None
    name: str | None


class VotingSession(BaseModel):
    key: str
    ends_at: int | None
    name: str | None

    class Config:
        orm_mode = True


class Ballot(BaseModel):
    ballot: dict[VoteTarget, Vote]

    class Config:
        schema_extra = {
            "example": {
                "ballot": {
                    42: 1,
                    55: 1,
                    96: 2,
                    102: 3,
                }
            }
        }


class VotingItem(App):
    id: VoteTarget
    score: int | None

    class Config:
        schema_extra = {
            "example": dict(
                **App.Config.schema_extra["example"],
                score=5,
            )
        }


class VotingSessionResult(VotingSession):
    items: list[VotingItem]
