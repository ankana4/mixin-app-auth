from rest_framework import serializers

post = {
    'title': 'Harry Potter and series',
    'content': 'A series of fantasy novels written by British author J. K. Rowling.',
    'author': 'J. K. Rowling',
}

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=300)
    content = serializers.CharField()
    author = serializers.CharField(max_length=100)
    
    
serializer = PostSerializer(post)
print(serializer.data)   