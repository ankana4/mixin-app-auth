from rest_framework import serializers
from mixin_app.models import Post

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'title', 'content', 'author']
        

post_instance = Post.objects.first()
serializer = PostModelSerializer(post_instance)
print(serializer.data)        