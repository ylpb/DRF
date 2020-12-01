from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models,serializers
from .response import APIResponse


class PublishAPIView(APIView):
    def get(self,request,*args,**kwargs):
        publish_query = models.Publish.objects.all()
        publish_ser = serializers.PublishModelSerializer(publish_query,many=True)
        return Response(data=publish_ser.data)

class BookAPIView(APIView):

    #单查群查
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            book_obj = models.Book.objects.filter(is_delete=False,pk=pk).first()
            book_ser = serializers.BookModelSerializer(book_obj)
        else:
            book_query = models.Book.objects.filter(is_delete=False).all()
            book_ser = serializers.BookModelSerializer(book_query,many=True)

        return Response(data=book_ser.data)

    # 删，单删群删
    def delete(self,request,*args,**kwargs):
        #单删
        pk = kwargs.get('pk')
        if pk:
            pks = [pk]
        else:
            pks = request.data

        try:
            #使用范围查找
            rows = models.Book.objects.filter(is_delete=False,pk__in=pks).update(is_delete=True)
        except:
            return Response({1,"数据有误"})
        if rows:
            return Response(data={0,'删除成功'})
        return Response(data={1:'删除失败'})


    #单增群增
    def post(self,request,*args,**kwargs):
        if isinstance(request.data,dict):
            many = False

        elif isinstance(request.data,list):
            many = True

        else:
            return Response(data={'detail':'数据有误'},status=400)
        book_ser = serializers.BookModelSerializer(data=request.data,many=many)
        book_ser.is_valid(raise_exception=True)
        book_obj_or_list = book_ser.save()
        return APIResponse(results=serializers.BookModelSerializer(book_obj_or_list,many=many).data)









        # 整体单改群改
    def put(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                book_instance = models.Book.objects.get(is_delete=False,pk=pk)
            except:
                return Response({'detail':'pk error'})
            book_ser = serializers.BookModelSerializer(instance=book_instance,data=request.data)
            book_ser.is_valid(raise_exception=True)
            book_obj = book_ser.save()
            return APIResponse(results=serializers.BookModelSerializer(book_obj).data)

        else:  # 群改
        # 分析（重点）：
        # 1）数据是列表套字典，每个字典必须带pk，就是指定要修改的对象，如果有一条没带pk，整个数据有误
        # 2）如果pk对应的对象已被删除，或是对应的对象不存在，可以认为整个数据有误(建议)，可以认为将这些错误数据抛出即可
            request_data = request.data
            try:
                pks = []
                for dic in request_data:
                    pk = dic.pop('pk')  # 解决分析1，没有pk pop方法就会抛异常
                    pks.append(pk)

                book_query = models.Book.objects.filter(is_delete=False, pk__in=pks).all()
                if len(pks) != len(book_query):
                    raise Exception('pk对应的数据不存在')
            except Exception as e:
                return Response({'detail': '%s' % e}, status=400)

            book_ser = serializers.BookModelSerializer(instance=book_query, data=request_data, many=True)
            book_ser.is_valid(raise_exception=True)
            book_list = book_ser.save()
            return APIResponse(results=serializers.BookModelSerializer(book_list, many=True).data)


    # 局部修改

    def patch(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                book_instance = models.Book.objects.get(is_delete=False,pk=pk)
            except:
                return Response({'detail':'pk error'},status=400)
            book_ser = serializers.BookModelSerializer(instance=book_instance,data=request.data,partial=True)
            # 设置partial=True的序列化类，参与反序列化的字段，都会置为选填字段
            # 1）提供了值得字段发生修改。
            # 2）没有提供的字段采用被修改对象原来的值
            book_ser.is_valid(raise_exception=True)
            book_obj = book_ser.save()
            return APIResponse(results=serializers.BookModelSerializer(book_obj).data)
        else:
            request_data = request.data
            try:
                pks = []
                for dic in request_data:
                    pk = dic.pop('pk')
                    pks.append(pk)
                book_query = models.Book.objects.filter(is_delete=False,pk__in=pks).all()
                if len(pks) != len(book_query):
                    raise Exception('pk对应的数据不存在')
            except Exception as e:
                return Response({'detail':"%s"%e},status=400)
            book_ser = serializers.BookModelSerializer(instance=book_query,data=request.data,many=True)
            book_ser.is_valid(raise_exception=True)
            book_list = book_ser.save()
            return APIResponse(request=serializers.BookModelSerializer(book_list,many=True).data)



