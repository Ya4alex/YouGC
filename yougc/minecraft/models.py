import secrets
import time
import uuid
from datetime import datetime
from hashlib import sha256

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class AuthmeManager(models.Manager):
    @staticmethod
    def check_password(user, password):
        def sha(_password: str):
            return sha256(_password.encode()).hexdigest()

        try:
            code, salt, _hash = user.password.split('$')[1:]
        except:
            return False
        return sha(sha(password) + salt) == _hash

    def getuser(self, username):  # not beautiful
        try:
            return self.get(realname=username)
        except:
            return None


class Authme(models.Model):
    username = models.CharField(unique=True, max_length=255)
    realname = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255, db_collation='ascii_bin')
    ip = models.CharField(max_length=40, db_collation='ascii_bin', blank=True, null=True)
    is_superuser = models.IntegerField(blank=True, null=True)
    is_staff = models.IntegerField(blank=True, null=True)
    lastlogin = models.BigIntegerField(blank=True, null=True)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    world = models.CharField(max_length=255)
    regdate = models.BigIntegerField()
    regip = models.CharField(max_length=40, db_collation='ascii_bin', blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    islogged = models.SmallIntegerField(db_column='isLogged')  # Field name made lowercase.
    hassession = models.SmallIntegerField(db_column='hasSession')  # Field name made lowercase.
    totp = models.CharField(max_length=32, blank=True, null=True)
    yaw = models.FloatField(blank=True, null=True)
    pitch = models.FloatField(blank=True, null=True)

    objects = AuthmeManager()

    class Meta:
        managed = False
        db_table = 'authme'
        verbose_name = 'Игрок (основная информация)'
        verbose_name_plural = 'Игроки (основная информация)'

    def set_password(self, raw_password):
        def sha(_password: str):
            return sha256(_password.encode()).hexdigest()

        salt = secrets.token_hex(8)
        self.password = f"$SHA${salt}${sha(sha(raw_password) + salt)}"


class KactivityLeaderboard(models.Model):
    place = models.IntegerField()
    name = models.CharField(max_length=45)
    balance = models.IntegerField()
    gotbalance = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kactivity_leaderboard'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Рейтинг игроков'


class KactivityListDeadworld(models.Model):
    name = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    balance = models.IntegerField()
    gotbalance = models.IntegerField()
    access_until = models.TextField()

    class Meta:
        managed = False
        db_table = 'kactivity_list_deadworld'
        verbose_name = 'Игрок в deadworld'
        verbose_name_plural = 'Игроки в deadworld'


class KactivityListLobby(models.Model):
    name = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    balance = models.IntegerField()
    gotbalance = models.IntegerField()
    access_until = models.TextField()

    class Meta:
        managed = False
        db_table = 'kactivity_list_lobby'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class KactivityListRoleplay(models.Model):
    name = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    balance = models.IntegerField()
    gotbalance = models.IntegerField()
    access_until = models.TextField()

    class Meta:
        managed = False
        db_table = 'kactivity_list_roleplay'
        verbose_name = 'Игрок в roleplay'
        verbose_name_plural = 'Игроки в roleplay'


class KonlineList(models.Model):
    server_id = models.IntegerField()
    player = models.CharField(max_length=45)
    date = models.TextField()

    class Meta:
        managed = False
        db_table = 'konline_list'
        verbose_name = 'Онлайн игрок'
        verbose_name_plural = 'Игроки Онлайн'


class KonlineOnline(models.Model):
    id_discord = models.TextField(blank=True, null=True)
    server = models.CharField(max_length=45)
    players = models.IntegerField()
    status = models.CharField(max_length=45)
    date = models.TextField()
    send = models.IntegerField()
    long_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'konline_online'
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'


class SiteProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=45)
    long_name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    category = models.ForeignKey('SiteProductCategory', models.DO_NOTHING, db_column='category')
    buyers_count = models.IntegerField(blank=True, null=True)
    servers = models.ManyToManyField(KonlineOnline, through='SiteProductKonlineOnline',
                                     through_fields=('site_product', 'konline_online'))

    class Meta:
        managed = False
        db_table = 'site_product'
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def get_picture(self):
        return f"{self.name}.png"

    def __str__(self):
        return self.name


class SiteProductKonlineOnline(models.Model):
    site_product = models.ForeignKey(SiteProduct, models.DO_NOTHING, db_column='site_product')
    konline_online = models.ForeignKey(KonlineOnline, models.DO_NOTHING, db_column='konline_online')

    class Meta:
        managed = False
        db_table = 'site_product_konline_online'
        verbose_name = 'продукт - сервер'
        verbose_name_plural = 'Продукты - сервера'


class SiteProductCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, unique=True)
    long_name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_product_category'
        verbose_name = 'категория продукта'
        verbose_name_plural = 'Категории продуктов'

    def __str__(self):
        return self.name


class SiteProductQueue(models.Model):
    name = models.CharField(max_length=45)
    product_text = models.TextField()
    server = models.CharField(max_length=45)
    product = models.ForeignKey(SiteProduct, models.DO_NOTHING, db_column='product')

    class Meta:
        managed = False
        db_table = 'site_product_queue'
        verbose_name = 'Продукт на получение'
        verbose_name_plural = 'Очередь продуктов'


class EmailConfirmManager(models.Manager):
    @staticmethod
    def _generate_uid_token():
        return uuid.uuid4().hex, secrets.token_urlsafe()

    def find_by_user(self, user):
        return self.filter(user=user).first()

    def create(self, user: User, url_prefix='confirm_email'):
        obj = self.filter(user=user).first()
        if obj:
            obj.delete()
        _uid, _token = self._generate_uid_token()
        obj = self.model(user=user, uid=_uid, token=_token, date=time.time())
        obj.save()
        return f"{settings.SITE_LINK}/{url_prefix}/{_uid}/{_token}"

    def only_check_uid_token(self, _uid, _token):
        obj = self.filter(uid=_uid, token=_token).first()
        if not obj or time.time() - settings.EMAIL_DELTA_TIME > obj.date:
            return None
        return obj

    def check_uid_token_user(self, _uid, _token):
        obj = self.filter(uid=_uid, token=_token).first()
        if not obj or time.time() - settings.EMAIL_DELTA_TIME > obj.date:
            return None
        user = obj.user
        obj.delete()
        user.is_active = True
        user.save()
        return user


class EmailConfirm(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    uid = models.CharField(max_length=32, null=False)
    token = models.CharField(max_length=43, null=False)
    date = models.FloatField(default=time.time())

    objects = EmailConfirmManager()

    class Meta:
        db_table = 'email_confirm'
        verbose_name = 'Подтверждение почты'
        verbose_name_plural = 'Подтверждение почты'

    def can_send_again(self):
        return time.time() - settings.EMAIL_SEND_PAUSE > self.date

    def wait_time(self):
        return datetime.utcfromtimestamp(time.time() - settings.EMAIL_SEND_PAUSE - self.date).strftime('%M:%S')


MODELS_SERVERS_LIST = {
    'roleplay': KactivityListRoleplay,
    'deadworld': KactivityListDeadworld,
    'lobby': KactivityListLobby,
}
