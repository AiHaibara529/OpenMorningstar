from django.db import models
from Morningstar.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '话题'
        verbose_name_plural = '话题'


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['-updated', '-created']


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(
        null=True, blank=True)  # NOTE: null 是针对数据库而言，blank 是针对表单而言
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)  # NOTE: 多对多关系的模型中，如果没有设置 related_name，默认的 related_name 是 model_name_set。

    # NOTE: auto_now每次更改模型时都会更新这个字段
    updated = models.DateTimeField(auto_now=True)
    # NOTE: auto_now_add每次创建模型时都会更新这个字段
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '房间'
        verbose_name_plural = '房间'
        ordering = ['-updated', '-created']
