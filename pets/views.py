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

    def get(self, request: Request, pet_id: int = None) -> Response:

        if pet_id:
            try:
                pet = Pet.objects.get(id=pet_id)
            except Pet.DoesNotExist:
                return Response({"detail": "Not found."}, status=404)

            serializer = PetSerializer(pet)

            return Response(serializer.data, status=200)

        trait = request.query_params.get('trait')

        if trait:
            pets = Pet.objects.filter(traits__name__iexact=trait)
        else:
            pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, request, view=self)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def delete(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        pet.delete()

        return Response(status=204)

    def patch(self, request: Request, pet_id: int) -> Response:
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        serializer = PetSerializer(pet, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.update(pet, serializer.validated_data)

        return Response(serializer.data, status=200)
