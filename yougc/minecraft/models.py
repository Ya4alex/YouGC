from hashlib import sha256

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
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


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


class KactivityList(models.Model):
    name = models.CharField(max_length=45)
    discord = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    balance = models.IntegerField()
    gotbalance = models.IntegerField()
    server = models.CharField(max_length=45)
    last_online = models.TextField()

    class Meta:
        managed = False
        db_table = 'kactivity_list'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


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

    class Meta:
        managed = False
        db_table = 'konline_online'
        verbose_name = 'Сервер'
        verbose_name_plural = 'Сервера'


class SiteProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    long_name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    category = models.ForeignKey('SiteProductCategory', models.DO_NOTHING, db_column='category')
    buyers_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_product'
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class SiteProductCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    long_name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_product_category'
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

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
        verbose_name = 'очердь'
        verbose_name_plural = 'Очередь'
