from typing import Optional

from redis_om import Field, JsonModel


class TVTimeDataModel(JsonModel):
    username: str = Field(index=True, primary_key=True)
    user_id: Optional[str]
    to_watch: Optional[dict]
    upcoming: Optional[dict]
    profile: Optional[dict]

    class Meta:  # pylint: disable=missing-class-docstring
        global_key_prefix = "tvtime"
        model_key_prefix = "data"
