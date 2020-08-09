from drf_haystack.filters import BaseHaystackFilterBackend

class SchoolFilter(BaseHaystackFilterBackend):
    """学校过滤器,决定要不要显示属于校区的学校或者只显示本部校区"""
    def filter_queryset(self, request, queryset, view):
        # 若type为0,则只返回每个学校的本部,若为1则返回所有校区.若没有type,则返回空
        type = request.GET.get('type')
        if type:
            type = int(type)
            if type == 0:
                queryset = queryset.filter(type=0)
                return queryset
            elif type == 1:
                return queryset
        else:
            return queryset.none()