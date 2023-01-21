from rest_framework.serializers import ModelSerializer
from .models import User, Posts, UserGallery


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PostsSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = ['post_id','user_id', 'content', 'image']
        
class UserGalleriesSerializer(ModelSerializer):
    class Meta:
        model = UserGallery
        fields = ['gallery_id','user_id', 'image']

