from rest_framework import serializers
import jsonschema


# Sources:
# 1) https://stackoverflow.com/a/49036841
# 2) https://www.django-rest-framework.org/api-guide/validators/#class-based
class JSONSchemaValidator:
    """Validator which uses jsonschema to validate the data."""

    def __init__(self, schema):
        self.schema = schema

    def __call__(self, value):
        try:
            jsonschema.validate(value, self.schema)
        except jsonschema.ValidationError as e:
            raise serializers.ValidationError(e.message)
