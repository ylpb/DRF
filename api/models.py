from django.db import models

# Create your models here.

class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True





class Book(BaseModel):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    publish = models.ForeignKey(to='Publish', related_name='books', db_constraint=False, on_delete=models.DO_NOTHING, null=True)
    authors = models.ManyToManyField(to='Author', related_name='books', db_constraint=False)


    @property
    def publish_info(self):  # 单个数据
        # from .serializers import PublishModelSerializer
        # return PublishModelSerializer(self.publish).data
        return {
            'name': self.publish.name,
            'address': self.publish.address,
        }

    @property
    def author_list(self):
        author_list_temp = []  # 存放所有作者格式化成数据的列表
        authors = self.authors.all()  # 所有作者
        for author in authors:  # 遍历处理所有作者
            author_dic = {
                'name': author.name,
            }
            try:  # 有详情才处理详情信息
                author_dic['mobile'] = author.detail.mobile
            except:
                author_dic['mobile'] = '无'

            author_list_temp.append(author_dic)  # 将处理过的数据添加到数据列表中

        return author_list_temp  # 返回处理后的结果



    def __str__(self):
        return self.name

class Publish(BaseModel):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)

    @property
    def book_info(self):
        book_list = []  # 存放所有作者格式化成数据的列表
        books = self.books.all()  # 所有作者
        for book in books:  # 遍历处理所有作者
            book_dic = {
                'name': book.name,
            }


            book_list.append(book_dic)  # 将处理过的数据添加到数据列表中

        return book_list  # 返回处理后的结果


    def __str__(self):
        return self.name

class Author(BaseModel):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class AuthorDetail(BaseModel):
    mobile = models.CharField(max_length=64)
    author = models.OneToOneField(to=Author, related_name='detail', db_constraint=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.author