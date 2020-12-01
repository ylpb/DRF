from rest_framework import serializers
from . import models


class BookListSerializer(serializers.ListSerializer):
    def create(self,validated_data):
        return super().create(validated_data)

    def update(self, instance_list, validated_data_list):

        #这里的child是ListSerializer的一个普通的属性，用于update、create方法
        return [self.child.update(instance_list[index],attrs) for index,attrs in enumerate(validated_data_list)]



class PublishModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publish
        fields = ['name','address','book_info']




class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ['name', 'price', 'publish', 'authors',
                  'publish_info', 'author_list']

        extra_kwargs = {
            'publisher':{
                'write_only':True
            },
            'author':{
                'write_only':True
            }
        }