from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializer import ServiceSerializer

service_list_docs = extend_schema(
    responses=ServiceSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of services to retrieve",
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Number of services to retrieve",
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter services by the current authenticated user (true/false)",
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Include the number of members for each service in the response",
        ),
        OpenApiParameter(
            name="by_serviceid",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Include service by id",
        ),
    ],
)
