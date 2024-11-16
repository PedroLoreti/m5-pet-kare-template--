from rest_framework import serializers
from groups.models import Group
from pets.models import SexChoices
from groups.serializers import GroupSerializer
from traits.models import Trait
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()

    sex = serializers.ChoiceField(
        choices=SexChoices.choices,
        default=SexChoices.NOT_INFORMED,
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def update(self, instance, validated_data):

        for field, value in validated_data.items():
            if field not in ["group", "traits"]:
                setattr(instance, field, value)

        group_data = validated_data.get("group")
        if group_data:
            group_scientific_name = group_data.get("scientific_name")
            if group_scientific_name:
                group, _ = Group.objects.get_or_create(scientific_name=group_scientific_name)
                instance.group = group

        traits_data = validated_data.get("traits", [])
        if traits_data:
            instance.traits.clear()
            for trait_data in traits_data:
                trait_name = trait_data.get("name")
                if trait_name:
                    trait_name = trait_name.lower()

                    # Verificar se o Trait já existe com o nome fornecido
                    trait = Trait.objects.filter(name__iexact=trait_name).first()
                    if not trait:
                        trait = Trait.objects.create(name=trait_name)

                    # Associar o Trait ao Pet
                    instance.traits.add(trait)

        instance.save()
        return instance
