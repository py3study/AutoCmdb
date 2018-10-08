from api.utils.response import BaseResponse
from rest_framework.pagination import PageNumberPagination

class SerializedData(object):  # 序列化通用格式数据
    def __init__(self,request,queryset,serializer_class):
        self.request = request
        self.queryset = queryset
        self.serializer_class = serializer_class


    def get_data(self):
        ret = BaseResponse()
        try:
            # 从数据库获取数据
            queryset = self.queryset.order_by('id')

            # 分页
            page = PageNumberPagination()
            course_list = page.paginate_queryset(queryset, self.request, self)

            # 分页之后的结果执行序列化
            ser = self.serializer_class(instance=course_list, many=True)
            # print(ser.data)

            if not ser.data:
                ret.code = 500
                ret.error = '数据为空'
            else:
                ret.data = ser.data

        except Exception as e:
            print(e)
            ret.code = 500
            ret.error = '获取数据失败'

        return ret.dict