from pydantic import BaseModel

class discordOauthSchema(BaseModel):
    code: str
    state: str
    guild_id: str|None = None
    permissions: str|None = None