from django.db import models
from datetime import datetime, date


# 一级分类
class ParentCategory(models.Model):
    name = models.CharField(verbose_name="分类名称", max_length=64)
    url = models.CharField(verbose_name="分类地址", max_length=128)
    slug = models.CharField(verbose_name="子链接", max_length=16, default="")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "一级分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)

    # 获取下一级分类的名字
    def get_category(self):
        category = Category.objects.filter(
            father__slug=self.slug
        ).all()
        return category

    # 首页 获取该分类下的商品
    def get_product(self, num=4):
        product = TagAndProduct.objects.filter(
            tag__father__father_id=self.id
        ).all()[:num]
        # print(product)
        return product


# 二级分类
class Category(models.Model):
    father = models.ForeignKey("ParentCategory", verbose_name="父类", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="分类名称", max_length=64)
    url = models.CharField(verbose_name="分类地址", max_length=128)
    slug = models.CharField(verbose_name="子链接", max_length=16, default="")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "二级分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.father.name, self.name)

    # 提取下一级分类
    def get_tag(self):
        tag = TagPro.objects.filter(
            father__slug=self.slug
        ).all()
        return tag


# 三级分类
class TagPro(models.Model):
    father = models.ForeignKey("Category", verbose_name="父类", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="分类名称", max_length=64)
    url = models.CharField(verbose_name="分类地址", max_length=128)
    slug = models.CharField(verbose_name="子链接", max_length=16, default="")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "三级分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.father.name, self.name)


# 所有商品 商品ID就是自增ID
class Product(models.Model):
    title = models.CharField(verbose_name="商品名称", max_length=512)
    image = models.ImageField(upload_to="image", verbose_name="封面图", max_length=100, default="")
    recomand = models.TextField(verbose_name="摘要", default="")
    # 启用四级分类
    four_name = models.CharField(verbose_name="四级分类", max_length=128, default="")
    four_url = models.CharField(verbose_name="四级分类", max_length=128, default="")
    # 相关属性
    author_name = models.CharField(verbose_name="作者", max_length=120, default="")
    publisher = models.CharField(verbose_name="出版社", max_length=512, default="")
    pub_time = models.DateField(verbose_name="出版时间", default="")
    open = models.CharField(verbose_name="开本", max_length=512, default="")
    page = models.CharField(verbose_name="页数", max_length=64, default="")
    startWrap = models.FloatField(verbose_name="读者评分", default=5)
    # 版权信息
    ISBN = models.CharField(verbose_name="ISBN号", max_length=64, default="")
    code = models.CharField(verbose_name="条形码", max_length=128, default="")
    ZhuangZhen = models.CharField(verbose_name="装帧", max_length=64, default="暂无")
    BanCi = models.CharField(verbose_name="版次", max_length=64, default="暂无")
    CeShu = models.CharField(verbose_name="册数", max_length=64, default="暂无")
    ZhongLiang = models.CharField(verbose_name="重量", max_length=64, default="暂无")
    YinShuaCiShu = models.CharField(verbose_name="印刷次数", max_length=64, default="暂无")
    # 正文内容
    specialist = models.TextField(verbose_name="本书特色", default="")
    brief = models.TextField(verbose_name="内容简介", default="")
    catalog = models.TextField(verbose_name="目录", default="")
    xiangguan = models.TextField(verbose_name="相关资料", default="")
    excerpt = models.TextField(verbose_name="内容节选", default="")
    zuozhejianjie = models.TextField(verbose_name="作者简介", default="")
    # 相关数据
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    sales = models.IntegerField(default=0, verbose_name="销量")
    sku = models.IntegerField(default=0, verbose_name="库存")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    support = models.IntegerField(default=0, verbose_name="点赞人数")
    comment_nums = models.IntegerField(default=0, verbose_name="评论数")
    # 是否上架商品／上架／下架

    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "商品管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.title)

    # # 点击 + 1
    # def add_click_nums(self, num=1):
    #     self.click_nums = self.click_nums + num
    #     return self.click_nums
    #
    # # 销量 + 1
    # def add_sale(self, num=1):
    #     self.sales = self.sales + num
    #     return self.sales
    #
    # # 库存 - 1
    # def del_sku(self, num=1):
    #     self.sku = self.sku - num
    #     return self.sku
    #
    # # 收藏 + 1
    # def add_fav(self, num=1):
    #     self.fav_nums = self.fav_nums + num
    #     return self.fav_nums
    #
    # # 点赞 + 1
    # def add_support(self, num=1):
    #     self.support = self.support + num
    #     return self.support
    #
    # # 评论 + 1
    # def add_comment(self, num=1):
    #     self.comment_nums = self.comment_nums + num
    #     return self.comment_nums

    # 获取价格
    def get_price(self):
        price = Price.objects.filter(product=self.id).first()
        return price.price

    # 获取对应的标签
    def get_tag(self):
        tags = TagPro.objects.filter(
            id=TagAndProduct.objects.filter(
                product=self.id
            ).first().tag_id
        ).first()
        return tags


# 图书作者 一本书有多个作者 一个作者也可以多本书
class Author(models.Model):
    product = models.ForeignKey("Product", verbose_name="书名", on_delete=models.CASCADE)
    author = models.CharField(verbose_name="作者名字", max_length=128)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.author, self.product.title)


# 出版社
class Publish(models.Model):
    product = models.ForeignKey("Product", verbose_name="书名", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="出版社名字", max_length=128)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.name, self.product.title)


# 创建中间模型 由于书和分类属于多对多关系 一本书属于多个分类 一个分类多本书
class TagAndProduct(models.Model):
    tag = models.ForeignKey("TagPro", verbose_name="所属分类", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", verbose_name="关联商品", on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "商品/分类标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.tag.name, self.product.title)


# 各个平台详情页列表
class ProductDetailLink(models.Model):
    product = models.ForeignKey("Product", verbose_name="关联商品", on_delete=models.CASCADE)
    china_book_url = models.CharField(verbose_name="中国图书网平台链接", max_length=512)
    dang_dang_url = models.CharField(verbose_name="当但平台链接", max_length=512)
    jing_dong_url = models.CharField(verbose_name="京东平台链接", max_length=512)
    tian_mao_url = models.CharField(verbose_name="天猫平台链接", max_length=512)

    class Meta:
        verbose_name = "商品地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.product.title)


# 价格表 对比多个商城的价格 如：当当/京东/天猫/中国图书网
class Price(models.Model):
    TERRACE_CHOICE = (
        ("d_dang", "当当"),
        ("j_dong", "京东"),
        ("t_mao", "天猫"),
        ("china_book", "中国图书"),
    )
    product = models.ForeignKey("Product", verbose_name="关联商品", on_delete=models.CASCADE)
    terrace = models.CharField(verbose_name="所属平台", max_length=16, choices=TERRACE_CHOICE)
    url = models.CharField(verbose_name="详情页地址", max_length=512)
    price = models.FloatField(verbose_name="原来价格", default=0)
    sellPrice = models.FloatField(verbose_name="销售价", default=0)
    discount = models.FloatField(verbose_name="折扣", default=10)
    data = models.DateField(verbose_name="日期", default=date.today)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "商品价格"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {} {}".format(self.product.title, self.terrace, self.price)


# 轮播商品
class CarouselPro(models.Model):
    product = models.ForeignKey("Product", verbose_name="关联商品", on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.product.title, self.add_time)
