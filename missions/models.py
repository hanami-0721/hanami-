from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Mission(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('pending', '待接取'),
        ('in_progress', '已接取'),
        ('completed', '已完成'),
        ('cancelled', '已撤销'),
    )
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='published_missions',
        verbose_name="发布人"
    )
    acceptor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='accepted_missions',
        verbose_name="接取人"
    )
    title = models.CharField("标题", max_length=100)
    content = models.TextField("内容")
    reward_score = models.IntegerField("积分奖励", default=0)
    status = models.CharField("状态", max_length=20, choices=STATUS_CHOICES, default='pending')
    is_draft = models.BooleanField("是否草稿", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    class Meta:
        verbose_name = "委托"
        verbose_name_plural = "委托"
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.title} | {self.get_status_display()}"


class MissionImage(models.Model):
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="委托"
    )
    image = models.ImageField(
        "图片",
        upload_to='missions/%Y%m%d/',
        max_length=255
    )
    class Meta:
        verbose_name = "委托图片"
        verbose_name_plural = "委托图片"