from pydantic import BaseModel
from typing import Dict

class TierRoleSchema(BaseModel):
    tierRole: Dict[str, str]