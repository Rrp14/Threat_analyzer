from app.models.graph import (
    GraphNode,
    GraphEdge,
    IOCRelationshipGraph,
)
from app.models.schemas import PipelineContext


class GraphService:

    def build(
        self,
        context: PipelineContext,
    ) -> IOCRelationshipGraph:

        nodes: list[GraphNode] = []
        edges: list[GraphEdge] = []

        # IOC nodes
        for ioc in context.iocs:

            nodes.append(
                GraphNode(
                    id=ioc.value,
                    label=ioc.value,
                    type=str(ioc.type),
                )
            )

        # MITRE nodes
        for mapping in context.mitre_mapping:

            nodes.append(
                GraphNode(
                    id=mapping.id,
                    label=mapping.technique,
                    type="mitre",
                )
            )

        # CVE nodes + edges
        if context.enrichment:

            for cve in context.enrichment.cves:

                nodes.append(
                    GraphNode(
                        id=cve.id,
                        label=cve.id,
                        type="cve",
                    )
                )

                for mapping in context.mitre_mapping:

                    edges.append(
                        GraphEdge(
                            source=cve.id,
                            target=mapping.id,
                            relationship="mapped_to",
                        )
                    )


            # IOC -> MITRE

        for ioc in context.iocs:

            for mapping in context.mitre_mapping:

               edges.append(
            GraphEdge(
                source=ioc.value,
                target=mapping.id,
                relationship="related_to",
            )
        )        

        return IOCRelationshipGraph(
            nodes=nodes,
            edges=edges,
        )