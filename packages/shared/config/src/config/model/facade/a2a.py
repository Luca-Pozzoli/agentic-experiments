from enum import StrEnum, unique
from typing import Annotated, Literal

from pydantic import Field, IPvAnyAddress
from pydantic_settings import BaseSettings

from config.model.facade.llm import LLMConfig

type NetworkPort = Annotated[int, Field(ge=1, le=65535)]


@unique
class FacadeKind(StrEnum):
    A2A = "a2a"


class A2AFacadeConfig(BaseSettings):
    kind: Literal[FacadeKind.A2A]
    host: IPvAnyAddress
    port: NetworkPort
    llm: LLMConfig


FacadeConfig = Annotated[A2AFacadeConfig, Field(discriminator="kind")]
