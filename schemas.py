from pydantic import BaseModel, ConfigDict, Field

class WalletBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    amount: float = Field(..., ge=0)

class WalletCreate(WalletBase):
    pass

class WalletResponse(WalletBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: str