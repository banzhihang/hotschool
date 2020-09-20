import redis
from django.contrib.auth.models import AnonymousUser
from django.db.models import F
from rest_framework import serializers

from HotSchool.settings import POOL
from user.models import UserCollectFood
from .models import *


class FoodRankSerializer(serializers.ModelSerializer):
    """美食排行序列化器"""
    name = serializers.CharField()
    image_first = serializers.URLField()
    score = serializers.SerializerMethodField()

    def get_score(self,obj):
        """将分数值舍入到小数点一位来显示"""
        if obj.vote_number <20:
            return None
        else:

            return round(obj.score,1)

    class Meta:
        model = Food
        fields = ['id','name','image_first','score']


class FoodInfoSerializer(serializers.ModelSerializer):
    """美食详情序列化器"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    flavour = serializers.SerializerMethodField()
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    score = serializers.SerializerMethodField()
    is_eat = serializers.SerializerMethodField()
    is_want_eat = serializers.SerializerMethodField()
    school = serializers.CharField(source='school.name')
    #吃过的时间
    eat_record = serializers.SerializerMethodField()
    is_collect = serializers.SerializerMethodField()

    def get_flavour(self,obj):
        # 获得美食的标签
        flavours = obj.flavour.all().values_list('name')
        flavours = [i[0] for i in flavours]
        return flavours

    def get_score(self,obj):
        # 获得该美食的评分
        if obj.vote_number < 20:
            return None
        else:
            return round(obj.score, 1)

    def get_eat_record(self,obj):
        # 判断是不是游客
        user = self.context['request'].user
        if not isinstance(user, AnonymousUser):
            # 先检查该用户是否吃过,吃过则查询记录,否则直接返回空字典
            is_eat = Eated.objects.filter(user=user.pk,food=obj.pk)
            if is_eat.exists():
                #  去打分表查询是否有该用户的打分,存在就返回序列化过的数据,不存在就继续去短评表查询,若还是不存在就返回空字典
                eatrecord_set = FoodMark.objects.filter(user=user.pk,food=obj.pk)
                # 判断存不存在该用户的打分记录
                if eatrecord_set.exists():
                    eatrecord = UserMarkSerializer(instance=eatrecord_set[0],many=False)
                    return eatrecord.data
                else:
                    eatrecord_set = ShortComment.objects.filter(user=user.pk,food=obj.pk)
                    # 判断存不存在该用户的短评
                    if eatrecord_set.exists():
                        eatrecord = EatRecordSerializer(instance=eatrecord_set[0],many=False)
                        return eatrecord.data
                    else: return {}
            else: return {}
        else: return {}

    def get_is_eat(self,obj):
        user = self.context['request'].user
        if not isinstance(user, AnonymousUser):
            # 检查是否吃过
            is_eat = Eated.objects.filter(user=user.pk,food=obj.pk)
            if is_eat.exists():
                return 1
            else:
                return 0
        else: return 0

    def get_is_want_eat(self,obj):
        user = self.context['request'].user
        if not isinstance(user, AnonymousUser):
            is_want_eat = WantEat.objects.filter(user=user.pk,food=obj.pk)
            if is_want_eat.exists():
                return 1
            else:
                return 0
        else: return 0

    def get_is_collect(self,obj):
        user = self.context['request'].user
        if not isinstance(user, AnonymousUser):
            try:
                _ = UserCollectFood.objects.get(user_id=user.pk,food_id=obj.pk)
            except UserCollectFood.DoesNotExist:
                return 0
            else:
                return 1
        else:
            return 0

    class Meta:
        model = Food
        exclude = ['all_score']


class EatRecordSerializer(serializers.ModelSerializer):
    """吃过记录序列化器"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user_score = serializers.IntegerField(source='score')
    type = serializers.IntegerField(default=1)

    class Meta:
        model = ShortComment
        fields = ['type','approval_number','content','user_score','add_time']


class UserMarkSerializer(serializers.ModelSerializer):
    """用户打分记录序列化器"""
    approval_number = serializers.CharField(default='null')
    content = serializers.CharField(default='null')
    user_score = serializers.IntegerField(source='score')
    type = serializers.IntegerField(default=0)
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = FoodMark
        fields = ['type','approval_number','content','user_score','type','add_time']


class ShortCommentSerializer(serializers.ModelSerializer):
    """美食短评序列化器"""
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    user_score = serializers.SerializerMethodField()
    user_score = serializers.IntegerField(source='score')
    is_approval = serializers.SerializerMethodField()

    def get_is_approval(self,obj):
        # 判断用户是否赞过该短评
        coon = redis.Redis(connection_pool=POOL)
        user = self.context['request'].user
        # 判断用户身份
        if not isinstance(user, AnonymousUser):
            is_approval = coon.sismember('approval:'+str(user.pk),'s:'+str(obj.pk))
            if is_approval:
                return 1
            else: return 0
        else: return 0

    class Meta:
        model = ShortComment
        fields = ['id','user','user_nick_name','user_head_portrait','user_score','is_approval','content','approval_number',
                  'add_time']


class DiscussRankSerializer(serializers.ModelSerializer):
    """美食讨论排行序列化器"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')


    class Meta:
        model = Discuss
        fields = ['id','user_nick_name','user_head_portrait','title','comment_number']


class DiscussInfoSerializer(serializers.ModelSerializer):
    """讨论详情视图"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    is_approval = serializers.SerializerMethodField()
    # 判断该讨论能不能删除
    can_delete = serializers.SerializerMethodField()

    def get_is_approval(self,obj):
        # 判断用户是否赞过该讨论
        coon = redis.Redis(connection_pool=POOL)
        user = self.context['request'].user
        # 判断用户身份
        if not isinstance(user, AnonymousUser):
            is_approval = coon.sismember('approval:' + str(user.pk), 'd:' + str(obj.pk))
            if is_approval:
                return 1
            else:
                return 0
        else:
            return 0

    def get_can_delete(self,obj):
        if obj.comment_number == 0:
            return 1
        else:
            return 0

    class Meta:
        model = Discuss
        fields = ['id','user','user_nick_name','user_head_portrait','title','approval_number',
                  'comment_number','content','add_time','is_approval','can_delete']


class DiscussCommentInfoSerializer(serializers.ModelSerializer):
    """讨论评论序列化器"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    is_approval= serializers.SerializerMethodField()

    def get_is_approval(self,obj):
        # 判断用户是否赞过该评论
        coon = redis.Redis(connection_pool=POOL)
        user = self.context['request'].user
        # 判断用户身份
        if not isinstance(user, AnonymousUser):
            is_approval = coon.sismember('approval:' + str(user.pk), 'fc:' + str(obj.pk))
            if is_approval:
                return 1
            else: return 0
        else: return 0

    class Meta:
        model = FoodComment
        fields = ['id','user','user_nick_name','user_head_portrait','content','is_approval','revert_number','approval_number',
                  'add_time',]


class DiscussRevertInfoSerializer(serializers.ModelSerializer):
    """讨论回复序列化器"""
    user_nick_name = serializers.CharField(source='user.nick_name')
    user_head_portrait = serializers.ImageField(source='user.head_portrait')
    target_user_nick_name = serializers.CharField(source='target_user.nick_name')
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    is_approval = serializers.SerializerMethodField()

    def get_is_approval(self,obj):
        # 判断用户是否赞过该评论
        coon = redis.Redis(connection_pool=POOL)
        user = self.context['request'].user
        # 判断用户身份
        if not isinstance(user, AnonymousUser):
            is_approval = coon.sismember('approval:' + str(user.pk), 'fr:' + str(obj.pk))
            if is_approval:
                return 1
            else: return 0
        else: return 0

    class Meta:
        model = FoodRevert
        fields = ['id','user','user_nick_name','user_head_portrait','target_user','target_user_nick_name','content','is_approval',
                  'approval_number','add_time']


class PostFoodSerializer(serializers.ModelSerializer):
    """
    美食发布序列化器
    必须字段:name,desc,address,longitude,latitude,flavour(至少两个标签,例子:[1,2]),image_first,image_second,address_image,school
    选要字段:image_third,image_fourth,image_fifth
    """
    name = serializers.CharField(min_length=2,max_length=15,required=True,allow_blank=False,error_messages={
        'min_length':'名称最少2个字',
        'max_length':'名称最大15个字',
        'blank':'名字不允许为空'
    })
    desc = serializers.CharField(min_length=4,max_length=30,required=True,allow_blank=False,error_messages={
        'min_length':'描述最少4个字',
        'max_length':'描述最大30个字',
        'blank':'描述不允许为空'
    })
    address = serializers.CharField(required=True,allow_blank=False,error_messages={'blank':'地址不能为空'})
    longitude = serializers.DecimalField(required=True,max_digits=40,decimal_places=6,error_messages={'required':'经度不能为空'})
    latitude = serializers.DecimalField(required=True,max_digits=40,decimal_places=6,error_messages={'required':'纬度不能为空'})
    flavour = serializers.ListField(required=True,min_length=2)
    image_first = serializers.URLField(required=True,error_messages={'required':'至少2张图片','invalid':'地址不合法'})
    image_second = serializers.URLField(required=True,error_messages={'required':'至少2张图片','invalid':'地址不合法'})
    image_third = serializers.URLField(required=False,error_messages={'invalid':'地址不合法'})
    image_fourth = serializers.URLField(required=False,error_messages={'invalid':'地址不合法'})
    image_fifth = serializers.URLField(required=False,error_messages={'invalid':'地址不合法'})
    address_image = serializers.URLField(required=True,error_messages={'required':'地址图片不允许为空','invalid':'地址不合法'})

    def validate(self,attr):
        # 验证口味
        flavour_list = attr.pop('flavour',None)
        if flavour_list:
            flavour = Flavour.objects.filter(id__in=flavour_list)
            # 检查提交的口味标签是否合法
            if len(flavour_list) != flavour.count():
                raise serializers.ValidationError('标签异常')
            else:
                attr['flavour'] = flavour_list

        attr['user'] = self.context['request'].user
        return attr

    def create(self, validated_data):
        # 弹出flavour,多对多字段的创建和其他的字段不同
        flavour_list = validated_data.pop('flavour')
        food = Food.objects.create(**validated_data)
        # 设置多对多字段
        food.flavour.set(flavour_list)
        return food

    class Meta:
        model = Food
        fields = ['name','desc','address','longitude','latitude','image_first','image_second','image_third','image_fourth',
                  'image_fifth','address_image','flavour','school']


class PostShortCommentSerializer(serializers.ModelSerializer):
    """
    发布短评序列化器
    必须参数:food(美食id),score(评分)
    选要参数:content(短评内容)
    """
    content = serializers.CharField(min_length=3,max_length=300,required=False,allow_blank=False,error_messages={
        'blank':'短评不允许为空',
        'min_length':'短评最少3个字',
        'max_length':'短评最多300个字',
    })
    score = serializers.IntegerField(required=True,min_value=1,max_value=5,error_messages={
        'required':'评分不允许为空',
        'min_value':'评分最低1分',
        'max_value':'评分最高5分',
        'invalid':'分数不合法',
    })

    def validate(self,attr):
        attr['user'] = self.context['request'].user
        return attr

    def create(self,validated_data):
        # 判断是否存在content,若不存在,则说明用户只评分,但不短评,就创建用户的打分记录。若存在,则说明用户既评分又短评,则创建用户短评
        content = validated_data.get('content')
        food = validated_data['food']
        # 增加对应美食投票人数,投票总分
        food.vote_number = F('vote_number') + 1
        food.all_score = F('all_score') + validated_data['score']
        # 存在content才增加短评数
        if content:
            food.short_comment_number = F('short_comment_number') + 1
            food.save()
            return ShortComment.objects.create(**validated_data),food.id
        else:
            food.save()
            return FoodMark.objects.create(**validated_data),food.id

    class Meta:
        model = ShortComment
        fields = ['food','content','score']


class PostDiscussSerializer(serializers.ModelSerializer):
    """
    发布讨论序列化器
    必须参数:food,title
    选要参数:content
    """
    title = serializers.CharField(min_length=4,max_length=30,required=True,allow_blank=False,error_messages={
        'blank':'标题不允许为空',
        'min_length':'标题最少4个字',
        'max_length':'标题最多30个字',
    })
    content = serializers.CharField(required=False,allow_blank=True)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self,validated_data):
        food = validated_data['food']
        food.discuss_number = F('discuss_number') + 1
        food.save()
        return Discuss.objects.create(**validated_data)

    class Meta:
        model = Discuss
        fields = ['food','title','content']


class PostDiscussCommentSerializer(serializers.ModelSerializer):
    """
    发布美食讨论的评论序列化器
    必须参数:discuss(讨论id) content
    """
    content =  serializers.CharField(min_length=1,max_length=100,required=True,allow_blank=False,error_messages={
        'min_length':'评论最少一个字',
        'max_length':'评论最多100字',
        'allow_blank':'评论不允许为空',
    })

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self,validated_data):
        discuss = validated_data['discuss']
        discuss.comment_number = F('comment_number') + 1
        discuss.save()
        return FoodComment.objects.create(**validated_data),discuss.user_id

    class Meta:
        model = FoodComment
        fields = ['discuss','content']


class PostDiscussRevertSerializer(serializers.ModelSerializer):
    """
    发布回复序列化器
    必须参数:target_user(目标用户) content(内容) comment(所属评论)
    """
    content = serializers.CharField(min_length=1, max_length=100, required=True, allow_blank=False, error_messages={
        'min_length': '评论最少一个字',
        'max_length': '评论最多100字',
        'allow_blank': '评论不允许为空',
    })

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self,validated_data):
        target_user_id = validated_data['target_user'].pk
        comment = validated_data['comment']
        comment.revert_number = F('revert_number') + 1
        comment.save()
        return FoodRevert.objects.create(**validated_data),target_user_id

    class Meta:
        model = FoodRevert
        fields = ['target_user','comment','content']