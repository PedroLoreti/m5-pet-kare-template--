from rest_framework.views import APIView, Request, Response
from pets.models import Pet
from groups.models import Group
from traits.models import Trait
from pets.serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        group_data = validated_data.pop('group')
        group, _ = Group.objects.get_or_create(
            scientific_name=group_data['scientific_name'],
            defaults=group_data

        )

        traits_data = validated_data.pop('traits')
        traits = []

        for trait_data in traits_data:
            trait, _ = Trait.objects.get_or_create(
                name__iexact=trait_data['name'],
                defaults=trait_data
            )
            traits.append(trait)

        pet = Pet.objects.create(group=group, **validated_data)

        pet.traits.set(traits)

        serializer = PetSerializer(pet)

        return Response(serializer.data, status=201)

    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, request, view=self)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
