from drf_haystack.filters import BaseHaystackFilterBackend

class SchoolFilter(BaseHaystackFilterBackend):
    """学校过滤器,决定要不要显示属于校区的学校或者只显示本部校区"""
    def filter_queryset(self, request, queryset, view):
        # 若type为0,则只返回每个学校的本部,若为1则返回所有校区.若没有type,则返回空
        type = request.GET.get('type')
        text = request.GET.get('text')
        # 若存在text，去除text的空白。若text为空字符串,则返回空结果
        if text:
            text = text.strip()
        if not text:
            return queryset.none()

        if type:
            type = int(type)
            if type == 0:
                queryset = queryset.filter(type=0,text=text)
                return queryset
            elif type == 1:
                return queryset.filter(text=text)
        else:
            return queryset.none()


class FoodEmptyFilter(BaseHaystackFilterBackend):
    """美食空过滤"""
    def filter_queryset(self, request, queryset, view):
        text = request.GET.get('text')
        school = request.GET.get('school')
        if text:
            text = text.strip()
        if not text:
            return queryset.none()
        else:
            if school:
                return queryset.filter(text=text,school=school)
            else:
                return queryset.filter(text=text)


class AllEmptyFilter(BaseHaystackFilterBackend):
    """所有搜索空过滤"""
    def filter_queryset(self, request, queryset, view):
        text = request.GET.get('text')
        if text:
            text = text.strip()
        if not text:
            return queryset.none()
        else:
            return queryset.filter(text=text)