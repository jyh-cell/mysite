from django.db import models


class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = models.CharField(max_length=128, unique=True)  # unique表明字段唯一
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")   # choise提供了选择 默认为男
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # 使用__str__方法帮助人性化显示对象信息；
        return self.name

    class Meta:      # 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

# Create your models here.
