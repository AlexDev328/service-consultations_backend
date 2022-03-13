import base64
import datetime
import os
import uuid

from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class AuthCode(models.Model):
    auth_code = models.CharField(max_length=255, editable=False, null=True, blank=True, default=uuid.uuid4)
    used = models.BooleanField(default=False)

    def regenerate_code(self):
        self.auth_code = uuid.uuid4()
        self.used = False
        self.save()
        return self

    class Meta:
        verbose_name = "Авторизационный код"
        verbose_name_plural = "Авторизационные коды"


class UserProfile(models.Model):
    auth_code = models.OneToOneField(AuthCode, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", primary_key=True)
    city = models.CharField(verbose_name="Город", max_length=70, default='', blank=True, )
    filial = models.CharField(verbose_name="филиал", max_length=255, default='', blank=True, )
    peerid = models.UUIDField(verbose_name="uuid пользователя(товароведа)", default=uuid.uuid4, editable=False)
    consultant = models.BooleanField(verbose_name="Консультант", default=False, blank=True, )
    user_inner_id = models.CharField("Внешний id пользователя", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def username(self):
        return self.user.first_name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


statuses = (
    (0, 'В очереди'),
    (1, 'В работе'),
    (3, 'Завершена')
)


class Consultation(models.Model):
    insigator = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="инициатор",
                                  related_name='insigator')
    consultant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    cons_text = models.TextField(verbose_name="Заключение консультанта", default='', blank=True)
    user_text = models.TextField(verbose_name="Комментарий товароведа", default='', blank=True)
    amount = models.DecimalField(verbose_name="Сумма оценки", blank=True, null=True, decimal_places=2, max_digits=10)
    data = models.JSONField("Данные о предмете", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    final = models.BooleanField(default=False)
    status = models.IntegerField(choices=statuses, default=0)

    def as_json(self):
        return dict(
            text=self.cons_text,
            final_ver=self.final,
        )

    def get_all_photo(self):
        return [p for p in Photo.objects.filter(conclusion=self)]

    class Meta:
        verbose_name = "Заключение"
        verbose_name_plural = "Заключения"


class Photo(models.Model):
    img = models.ImageField(verbose_name="фотография")
    conclusion = models.ForeignKey(Consultation, on_delete=models.CASCADE, blank=True)

    def photo_tag(self):
        return mark_safe('<a href="/media/{0}"><img src="/media/{0}"></a>'.format(self.img))

    photo_tag.short_description = 'Photo of prescription'
    photo_tag.allow_tags = True

    def toDataString(self, format='png'):
        """
        :param `image_file` for the complete path of image.
        :param `format` is format for image, eg: `png` or `jpg`.
        """
        print(self.img.url)
        if not os.path.isfile(self.img.path):
            return None

        encoded_string = ''
        with open(self.img.path, 'rb') as img_f:
            encoded_string = base64.b64encode(img_f.read()).decode("utf-8")
        return (encoded_string)

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"