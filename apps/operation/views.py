import redis
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView

from HotSchool.settings import POOL
from food.models import WantEat, Food, Eated, ShortComment, Discuss, FoodComment, FoodRevert
from operation.extra import load_answer_operation, add_user_dynamic
from puclic import Authtication, check_undefined
from question.extra import add_question_operation_data, add_user_operation_data
from question.models import Comment, Revert
from question.tasks import push_to_user
from user.models import UserCollectFood, UserCollectQuestion


class ApprovalView(APIView):
    """赞同视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self, request):
        """
        给回答，评论，回复赞同或者取消赞同
        参数:url参数,answer(回答id) type(当answer存在时,0表示反对回答,1为赞同回答) comment(评论id) revert(回复id)
        want_eat(想吃食物id) eated(吃过id) short_comment(短评id) discuss(讨论id) discuss_comment(讨论评论id) discuss_revert(讨论回复id)
        以上参数只能存在一个 answer为特殊,当answer存在时,必须存在type
        """
        parameter_list = list(request.query_params.items())
        if not parameter_list:
            return Response({'status':'fail','error':'无参数'})
        parameter,value= parameter_list[0][0],parameter_list[0][1]
        try:
            value = int(value)
        except:
            return Response({'status': 'fail', 'error': '值错误'})
        user_id = request.user.pk
        coon = redis.Redis(connection_pool=POOL)

        try:
            if parameter == 'answer':
                answer_id = int(value)
                # 同步该回答的数据到redis
                target_user_id, question_id = load_answer_operation(answer_id)
                #  若target_user_id为None,说明该回答不存在,返回 错误信息
                if not target_user_id:
                    return Response({'status': 'fail', 'error': '该回答不存在'})
                # 若type存在,则继续,否则返回错误
                if parameter_list[1][0] == 'type':
                    type = int(parameter_list[1][1])
                    # 增加对应问题的赞同或者反对量
                    add_question_operation_data('approval', question_id)
                    # 若type为1,赞同,为0 为反对
                    if type == 1:
                        # 查询是否赞同过,若赞同过,这次操作为取消赞同,若没有赞同过,则为赞同
                        is_approval = coon.sismember('approval:' + str(user_id), 'a:' + str(answer_id) + ':1')
                        if not is_approval:
                            # 若没有赞同过,增加对应回答的赞同量和投票总数,同时将该回答id添加到该赞同者的赞同集合
                            coon.hincrby('ad:' + str(answer_id), 'approval', 1)
                            coon.hincrby('ad:' + str(answer_id), 'vote', 1)
                            coon.sadd('approval:' + str(user_id), 'a:' + str(answer_id) + ':1')
                            add_user_dynamic(operation='add', type=0, user_id=user_id, answer_id=answer_id)
                            # 增加该作者的赞同量
                            add_user_operation_data('approval', target_user_id, type='add')
                            # 更新回答的分数在load_answer_operation函数中30分钟后执行

                        elif is_approval:
                            # 若赞同过,则为取消赞同,减少该回答的赞同数和投票数,同时将该回答的id从该用户的赞同集合删除
                            coon.hincrby('ad:' + str(answer_id), 'approval', -1)
                            coon.hincrby('ad:' + str(answer_id), 'vote', -1)
                            coon.srem('approval:' + str(user_id), 'a:' + str(answer_id) + ':1')
                            # 删除该条动态
                            add_user_dynamic(operation='delete', type=0, user_id=user_id, answer_id=answer_id)
                            add_user_operation_data('approval', target_user_id, type='reduce')

                    elif type == 0:
                        # 查询是否反对过,若反对过,这次操作为取消反对,若没有反对过,则为反对
                        is_oppose = coon.sismember('approval:' + str(user_id), 'a:' + str(answer_id) + ':0')
                        if not is_oppose:
                            # 若没有反对过,增加对应回答的投票总数,同时将该回答id添加到该赞同者的反对集合
                            coon.hincrby('ad:' + str(answer_id), 'vote', 1)
                            coon.sadd('approval:' + str(user_id), 'a:' + str(answer_id) + ':0')
                        elif is_oppose:
                            # 若反对过,则为取消反对,减少该回答的投票数,同时将该回答的id从该用户的反对集合删除
                            coon.hincrby('ad:' + str(answer_id), 'vote', -1)
                            coon.srem('approval:' + str(user_id), 'a:' + str(answer_id) + ':0')
                else:
                    return Response({'status': 'ok', 'error': '发生错误'})

            elif parameter == 'comment':
                # 检查用户是否赞过该评论
                is_approval = coon.sismember('approval:' + str(user_id), 'c:' + str(value))
                try:
                    comment = Comment.objects.get(pk=value)
                except Comment.DoesNotExist:
                    return Response({'status': 'fail', 'error': '该评论不存在'})
                # 若赞过,则这次操作为取消赞
                if is_approval:
                    # 将该评论id从用户赞过的id集和删除
                    coon.srem('approval:' + str(user_id), 'c:' + str(value))
                    # 该评论的获赞数减一
                    comment.approval_number = F('approval_number') - 1
                # 若没有赞过,这次操作为赞
                else:
                    # 将该评论id添加进用户赞过的id集和
                    coon.sadd('approval:' + str(user_id), 'c:' + str(value))
                    # 该评论的获赞数加一
                    comment.approval_number = F('approval_number') + 1
                comment.save()

            # 回复的操作和评论一样
            elif parameter == 'revert':
                is_approval = coon.sismember('approval:' + str(user_id), 'r:' + str(value))
                try:
                    revert = Revert.objects.get(pk=value)
                except Revert.DoesNotExist:
                    return Response({'status': 'fail', 'error': '该回复不存在'})
                if is_approval:
                    coon.srem('approval:' + str(user_id), 'r:' + str(value))
                    revert.approval_number = F('approval_number') - 1
                else:
                    coon.sadd('approval:' + str(user_id), 'r:' + str(value))
                    revert.approval_number = F('approval_number') + 1
                revert.save()

            # 想吃
            elif parameter == 'want_eat':
                is_want_eat = WantEat.objects.filter(user=user_id,food=value)
                food = Food.objects.get(pk=value)
                if is_want_eat.exists():
                    is_want_eat.delete()
                    food.want_eat_number = F('want_eat_number') -1
                else:
                    WantEat.objects.create(user=request.user,food_id=value)
                    food.want_eat_number = F('want_eat_number') + 1
                food.save()

            # 吃过
            elif parameter == 'eated':
                is_eat = Eated.objects.filter(user=user_id,food=value)
                food = Food.objects.get(pk=value)
                if is_eat.exists():
                    is_eat.delete()
                    food.eat_number = F('eat_number') - 1
                else:
                    # 查看有没有想吃记录,有的话就删除
                    is_want_eat = WantEat.objects.filter(user=user_id,food=value)
                    if is_want_eat.exists():
                        is_want_eat.delete()
                    Eated.objects.create(user=request.user,food_id=value)
                    food.eat_number = F('eat_number') + 1
                food.save()

            # 短评
            elif parameter == 'short_comment':
                is_approval = coon.sismember('approval:' + str(user_id), 's:' + str(value))
                try:
                    short_comment = ShortComment.objects.get(pk=value)
                except ShortComment.DoesNotExist:
                    return Response({'status':'fail','error':'该短评不存在'})
                if is_approval:
                    coon.srem('approval:' + str(user_id), 's:' + str(value))
                    short_comment.approval_number = F('approval_number') - 1
                else:
                    coon.sadd('approval:' + str(user_id), 's:' + str(value))
                    short_comment.approval_number = F('approval_number') + 1
                short_comment.save()

            # 讨论
            elif parameter == 'discuss':
                is_approval = coon.sismember('approval:' + str(user_id), 'd:' + str(value))
                try:
                    discuss = Discuss.objects.get(pk=value)
                except Discuss.DoesNotExist:
                    return Response({'status': 'fail', 'error': '该讨论不存在'})
                if is_approval:
                    coon.srem('approval:' + str(user_id), 'd:' + str(value))
                    discuss.approval_number = F('approval_number') - 1
                else:
                    coon.sadd('approval:' + str(user_id), 'd:' + str(value))
                    discuss.approval_number = F('approval_number') + 1
                discuss.save()

            # 讨论评论
            elif parameter == 'discuss_comment':
                is_approval = coon.sismember('approval:' + str(user_id), 'fc:' + str(value))
                try:
                    discuss_comment = FoodComment.objects.get(pk=value)
                except FoodComment.DoesNotExist:
                    return Response({'status': 'fail', 'error': '该评论不存在'})
                if is_approval:
                    coon.srem('approval:' + str(user_id), 'fc:' + str(value))
                    discuss_comment.approval_number = F('approval_number') - 1
                else:
                    coon.sadd('approval:' + str(user_id), 'fc:' + str(value))
                    discuss_comment.approval_number = F('approval_number') + 1
                discuss_comment.save()

            # 讨论回复
            elif parameter == 'discuss_revert':
                is_approval = coon.sismember('approval:' + str(user_id), 'fr:' + str(value))
                try:
                    discuss_revert = FoodRevert.objects.get(pk=value)
                except FoodRevert.DoesNotExist:
                    return Response({'status': 'fail', 'error': '该回复不存在'})
                if is_approval:
                    coon.srem('approval:' + str(user_id), 'fr:' + str(value))
                    discuss_revert.approval_number = F('approval_number') - 1
                else:
                    coon.sadd('approval:' + str(user_id), 'fr:' + str(value))
                    discuss_revert.approval_number = F('approval_number') + 1
                discuss_revert.save()

        except Exception:
            return Response({'status': 'fail', 'error': '发生错误'})
        else:
            return Response({'status': 'ok', 'error': ''})


class LikeView(APIView):
    """喜欢视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self, request):
        """
        喜欢回答
        参数:url参数:answer(回答id)
        """
        answer_id = request.GET.get('answer')
        user_id = request.user.pk
        coon = redis.Redis(connection_pool=POOL)

        if answer_id:
            answer_id = int(answer_id)
            target_user_id, question_id = load_answer_operation(answer_id)
            #  若target_user_id为None,说明该回答不存在,返回 错误信息
            if not question_id:
                return Response({'status': 'fail', 'error': '该回答不存在'})
            try:
                #  查看是否喜欢,若已经喜欢,则为取消喜欢
                is_like = coon.getbit('al:' + str(answer_id), user_id)
                if is_like:
                    # 将该用户的喜欢位1设置为0,表示取消喜欢记录
                    coon.setbit('al:' + str(answer_id), user_id, 0)
                    # 减少该回答的作者的当天喜欢数
                    add_user_operation_data('like', target_user_id, 'reduce')
                else:
                    # 将该用户的喜欢位0设置为1,表示增加喜欢记录
                    coon.setbit('al:' + str(answer_id), user_id, 1)
                    # 增加对应问题的喜欢量
                    add_question_operation_data('approval', question_id)
                    add_user_operation_data('like', target_user_id, 'add')
            except Exception:
                return Response({'status': 'fail', 'error': '发生错误'})
            else:
                return Response({'status': 'ok', 'error': ''})
        else:
            return Response({'status': 'fail', 'error': '没有id'})


class CollectView(APIView):
    """收藏视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self, request):
        """
        收藏问题或者回答
        参数url参数 answer或者question二选一,为收藏或者回答的id
        """
        answer_id = request.GET.get('answer')
        question_id = request.GET.get('question')
        food_id =request.GET.get('food')
        user = request.user
        user_id = request.user.pk
        coon = redis.Redis(connection_pool=POOL)

        try:
            # 若存在answer, 则为对answer操作,
            if answer_id:
                answer_id = int(answer_id)
                # 同步该回答的数据到reids
                target_user_id, question_id = load_answer_operation(answer_id)
                # 检查是否收藏过
                is_collect = coon.sismember('collect:' + str(user_id), answer_id)
                # 若已经收藏过
                if is_collect:
                    # 将该回答的id从用户搜藏set删除
                    coon.srem('collect:' + str(user_id), answer_id)
                    # 减少该回答的收藏量
                    coon.hincrby('ad:' + str(answer_id), 'collect', -1)
                    # 删除该用户收藏回答这条动态
                    add_user_dynamic(operation='delete',type=1,user_id=user_id,answer_id=answer_id)
                else:
                    # 将该回答的id添加到用户搜藏set删除
                    coon.sadd('collect:' + str(user_id), answer_id)
                    # 增加对应回答的当天收藏量
                    add_question_operation_data('collect', question_id)
                    # 增加对应作者的当天创作数据
                    add_user_operation_data('collect', target_user_id,'add')
                    # 增加该回答的收藏数
                    coon.hincrby('ad:' + str(answer_id), 'collect', 1)
                    # 创建该用户的动态
                    add_user_dynamic(operation='add',type=1,user_id=user_id,answer_id=answer_id)

            elif question_id:
                question_id = int(question_id)
                try:
                    is_collect = UserCollectQuestion.objects.get(user_id=user_id,question_id=question_id)
                except UserCollectQuestion.DoesNotExist:
                    UserCollectQuestion.objects.create(user_id=user_id,question_id=question_id)
                    # 增加该问题收藏量
                    add_question_operation_data('attention', question_id, 'add')
                    # 创建动态
                    add_user_dynamic(operation='add', type=3, user_id=user_id, question_id=question_id)
                else:
                    is_collect.delete()
                    # 减少该问题的关注量
                    add_question_operation_data('attention', question_id, 'reduce')
                    # 删除该条动态
                    add_user_dynamic(operation='delete', type=3, user_id=user_id, question_id=question_id)

            # 美食收藏
            elif food_id:
                food_id = int(food_id)
                try:
                    is_collect = UserCollectFood.objects.get(user_id=user_id,food_id=food_id)
                except UserCollectFood.DoesNotExist:
                    UserCollectFood.objects.create(user_id=user_id,food_id=food_id)
                else:
                    is_collect.delete()

        except Exception:
            return Response({'status':'fail', 'error': '发生错误'})
        else:
            return Response({'status':'ok','error':''})


class AttentionView(APIView):
    """关注视图"""
    authentication_classes = [Authtication, ]

    @check_undefined
    def get(self,request):
        target_user_id = request.GET.get('target')
        user_id = request.user.pk
        coon = redis.Redis(connection_pool=POOL)

        if target_user_id:
            target_user_id = int(target_user_id)
            # 检查是否关注
            is_attention = coon.sismember('attention:'+str(user_id),target_user_id)
            if is_attention:
                # 将目标用户id从关注者关注set删除,同时将关注者id从被关注着被关注set删除
                coon.srem('attention:'+str(user_id),target_user_id)
                coon.srem('beattention:'+str(target_user_id),user_id)
                # 添加被关注者当天的关注量
                add_user_operation_data('attention',target_user_id,'reduce')
            else:
                coon.sadd('attention:'+str(user_id),target_user_id)
                coon.sadd('beattention:' + str(target_user_id), user_id)
                add_user_operation_data('attention', target_user_id, 'add')
                # 异步推送消息给目标用户
                push_to_user.delay(request.user,target_user_id,2)
            return Response({'status':'ok','error':''})
        else:
            return Response({'status': 'fail', 'error': '发生错误'})


