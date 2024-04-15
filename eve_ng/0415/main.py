import os
from typing import Optional
from pydantic import BaseModel


class Input(BaseModel):

    RABBITMQ_USERNAME: Optional[str]
    RABBITMQ_PASSWORD: Optional[str]
    RABBITMQ_HOST: Optional[str]
    RABBITMQ_PORT: Optional[str]

    SITE: Optional[str]
    MR_URL: Optional[str]
    TICKET: Optional[str]


res = Input(
    RABBITMQ_USERNAME=os.getenv("RABBITMQ_USERNAME"),
    RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD"),
    RABBITMQ_HOST=os.getenv("RABBITMQ_HOST"),
    RABBITMQ_PORT=os.getenv("RABBITMQ_PORT"),
    SITE=os.getenv("SITE"),
    MR_URL=os.getenv("MR_URL"),
    TICKET=os.getenv("TICKET"),
)
print(f"{res=}")
