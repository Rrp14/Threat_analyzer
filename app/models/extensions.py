from pydantic import Field

from app.models.attack_path import AttackStage
from app.models.common import DomainModel


class ExtensionFeatures(DomainModel):


    graph_data: dict | None = Field(
        default=None,
        description="Serialized relationship graph data.",
    )

    attack_path: list[AttackStage] = Field(
        default_factory=list,
        description="Predicted attack path.",
    )

    feed_sources: list[str] = Field(
        default_factory=list,
        description="Threat intelligence feeds used during analysis.",
    )

    @property
    def has_graph(self) -> bool:
        return self.graph_data is not None

    @property
    def has_attack_path(self) -> bool:
        return bool(self.attack_path)

    @property
    def has_feed_sources(self) -> bool:
        return bool(self.feed_sources)