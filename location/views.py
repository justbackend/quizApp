import math
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from location.serializers import LocationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


@extend_schema(request=LocationSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def get_distance(request):
    serializer = LocationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    R = 6371.0
    lat1 = 41.306195294765786
    lon1 = 69.24575803142908
    lat2 = serializer.validated_data['latitude']
    lon2 = serializer.validated_data['longitude']
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return Response({'message': distance, 'status': 200})

