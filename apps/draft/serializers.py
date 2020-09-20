from rest_framework import serializers

from draft.models import AnswerDraft, FoodDraft
from food.models import Flavour


class AnswerDraftInfoSerializer(serializers.ModelSerializer):
    """回答草稿详情序列化器"""
    question_title = serializers.CharField(source='question.title')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = AnswerDraft
        exclude = 'user'


class PostAnswerDraftInfoSerializer(serializers.ModelSerializer):
    """
    发布和更新回答草稿序列化器
    必要参数:question(所属问题id),is_anonymity(是否匿名,0不匿名,1匿名), content(回答内容)
    """
    content = serializers.CharField(required=False, allow_blank=True)
    is_anonymity = serializers.IntegerField(default=0, required=False)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        return AnswerDraft.objects.create(**validated_data)

    def update(self, instance, validated_data):
        content = validated_data.get('content')
        if content:
            instance.content = content
        instance.question = validated_data['question']
        instance.is_anonymity = validated_data['is_anonymity']
        instance.save()
        return instance

    class Meta:
        model = AnswerDraft
        fields = ['question', 'is_anonymity', 'content']


class MyAnswerDraftSerializer(serializers.ModelSerializer):
    """我的回答草稿序列器"""
    question_title = serializers.CharField(source='question.title')
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = AnswerDraft
        fields = ['id', 'content', 'question_title', 'modify_time']


class MyFoodDraftSerializer(serializers.ModelSerializer):
    """我的美食草稿序列化器"""
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = FoodDraft
        fields = ['id', 'name', 'image_first', 'desc', 'modify_time']


class FoodDraftInfoSerializer(serializers.ModelSerializer):
    """美食草稿详情序列化器"""
    modify_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    flavour = serializers.SerializerMethodField()
    school = serializers.SerializerMethodField()

    def get_flavour(self, obj):
        # 获得美食的标签
        flavours = obj.flavour.all().values_list('id', 'name')
        flavours = [{'id': i[0], 'name': i[1]} for i in flavours]
        return flavours

    def get_school(self, obj):
        schoo_info = {'id': obj.school_id, 'name': obj.school.name}
        return schoo_info

    class Meta:
        model = FoodDraft
        exclude = 'user'


class PostFoodDraftInfoSerializer(serializers.ModelSerializer):
    """
    发布和更新美食草稿序列化器
    必要参数:longitude(经度),latitude(纬度),name(名字),address(地址)
    选要参数：desc,flavour(至少两个标签,例子:[1,2]),image_first,image_second,address_image,school,image_third,image_fourth,image_fifth
    address_image
    """
    flavour = serializers.ListField(required=False)

    def validate(self, attrs):
        # 验证口味
        flavour_list = attrs.pop('flavour', None)
        if flavour_list:
            flavour = Flavour.objects.filter(id__in=flavour_list)
            # 检查提交的口味标签是否合法
            if len(flavour_list) != flavour.count():
                raise serializers.ValidationError('标签异常')
            else:
                attrs['flavour'] = flavour_list

        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        # 弹出flavour,多对多字段的创建和其他的字段不同
        flavour_list = validated_data.pop('flavour', None)
        food_draft = FoodDraft.objects.create(**validated_data)
        if flavour_list:
            food_draft.flavour.set(flavour_list)
        return food_draft

    def update(self, instance, validated_data):
        flavour = validated_data.pop('flavour', None)
        if flavour:
            instance.flavour.set(flavour)
            # save操作的目的是更新修改时间
            instance.save()
        return FoodDraft.objects.filter(pk=instance.pk).update(**validated_data)

    class Meta:
        model = FoodDraft
        fields = ['name', 'desc', 'address', 'longitude', 'latitude', 'image_first', 'image_second', 'image_third',
                  'image_fourth', 'image_fifth', 'address_image', 'flavour', 'school']
