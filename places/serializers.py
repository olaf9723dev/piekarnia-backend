from rest_framework import serializers

from authentication.serializers import UserSerializer
from places.models import Place, OpeningHours, CustomOpeningHours, PlaceReview


class PlaceSerializer(serializers.ModelSerializer):
    zipCode = serializers.CharField(source='zip_code')
    isEnabled = serializers.BooleanField(source='is_enabled')
    enableDate = serializers.DateField(source='enable_date')

    class Meta:
        model = Place
        fields = ["id", "name", "latitude", "longitude", "address", "zipCode", "city", "logo", "description",
                  "isEnabled", "enableDate", "telephone"]


class OpeningHoursSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()
    dayOfWeek = serializers.IntegerField(source='day_of_week')
    startTime = serializers.TimeField(source='start_time')
    endTime = serializers.TimeField(source='end_time')

    class Meta:
        model = OpeningHours
        fields = ["id", "place", "dayOfWeek", "startTime", "endTime"]


class CustomOpeningHoursSerializers(serializers.ModelSerializer):
    place = PlaceSerializer()
    startTime = serializers.TimeField(source='start_time')
    endTime = serializers.TimeField(source='end_time')
    isClosed = serializers.BooleanField(source='is_closed')

    class Meta:
        model = CustomOpeningHours
        fields = ["id", "place", "date", "startTime", "endTime", "isClosed"]


class PlaceReviewSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()
    author = UserSerializer()
    isAccepted = serializers.BooleanField(source='is_accepted')

    class Meta:
        model = PlaceReview
        fields = ["id", "place", "author", "rate", "date", "isAccepted", "comment"]
