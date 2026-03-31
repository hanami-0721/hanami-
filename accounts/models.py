from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    username = None  # 不用默认username，改用学号登录
    email = models.EmailField(_("邮箱"), unique=True)
    student_id = models.CharField(_("学号"), max_length=20, unique=True)
    nickname = models.CharField(_("昵称"), max_length=50)
    score = models.IntegerField(_("积分"), default=0)
    is_part_admin = models.BooleanField(_("管理员"), default=False)
    USERNAME_FIELD = "student_id"
    REQUIRED_FIELDS = ["email", "nickname"]
    def __str__(self):
        return f"{self.student_id} | {self.nickname}"

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ScoreLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="score_logs")
    score_change = models.IntegerField("变动积分")
    source = models.CharField("来源", max_length=30)
    created_at = models.DateTimeField("时间", auto_now_add=True)
    def __str__(self):
        return f"{self.user.nickname} {self.score_change}"
    class Meta:
        verbose_name = "积分日志"
        verbose_name_plural = "积分日志"