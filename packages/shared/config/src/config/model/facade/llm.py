from enum import StrEnum, unique
from typing import Annotated, Literal

from pydantic import AnyHttpUrl, Field, SecretStr, StringConstraints
from pydantic_settings import BaseSettings

type NonEmptyString = Annotated[
    str, StringConstraints(min_length=1, strip_whitespace=True)
]


@unique
class LLMProviderKind(StrEnum):
    OpenAICompatible = "openai-compatible"


class OpenAICompatibleModelConfig(BaseSettings):
    kind: Literal[LLMProviderKind.OpenAICompatible]
    model: NonEmptyString
    url: AnyHttpUrl
    api_key: SecretStr


LLMConfig = Annotated[OpenAICompatibleModelConfig, Field(discriminator="kind")]
