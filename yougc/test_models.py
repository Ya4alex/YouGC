# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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

    class Meta:
        managed = False
        db_table = 'authme'


class KactivityLeaderboard(models.Model):
    place = models.IntegerField()
    name = models.CharField(max_length=45)
    balance = models.IntegerField()
    gotbalance = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kactivity_leaderboard'


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


class KactivityQueue(models.Model):
    name = models.CharField(max_length=45)
    action = models.CharField(max_length=45)
    balance = models.IntegerField()
    gotbalance = models.IntegerField()
    server = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'kactivity_queue'


class KactivityRoles(models.Model):
    roles = models.CharField(max_length=45)
    points = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kactivity_roles'


class KactivityToday(models.Model):
    name = models.CharField(max_length=45)
    total = models.TextField()
    server = models.CharField(max_length=45)
    got = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kactivity_today'


class KbankAccounts(models.Model):
    name = models.CharField(max_length=45)
    balance = models.IntegerField()
    password = models.CharField(max_length=45)
    verif = models.IntegerField()
    discord = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'kbank_accounts'


class KbankCodes(models.Model):
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=45)
    date = models.TextField()

    class Meta:
        managed = False
        db_table = 'kbank_codes'


class KbankHistory(models.Model):
    accountfrom = models.CharField(db_column='accountFROM', max_length=45)  # Field name made lowercase.
    accountto = models.CharField(db_column='accountTO', max_length=45)  # Field name made lowercase.
    money = models.IntegerField()
    action = models.CharField(max_length=45)
    banker = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'kbank_history'


class KbankLastId(models.Model):
    last_post = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kbank_last_id'


class KbankQueue(models.Model):
    accountfrom = models.CharField(db_column='accountFROM', max_length=45)  # Field name made lowercase.
    accountto = models.CharField(db_column='accountTO', max_length=45)  # Field name made lowercase.
    money = models.IntegerField()
    action = models.CharField(max_length=45)
    verif = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'kbank_queue'


class KnewsKnews(models.Model):
    last_post = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'knews_knews'


class KonlineList(models.Model):
    server_id = models.IntegerField()
    player = models.CharField(max_length=45)
    date = models.TextField()

    class Meta:
        managed = False
        db_table = 'konline_list'


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


class KpasswordsMessages(models.Model):
    player = models.CharField(max_length=45)
    message = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'kpasswords_messages'


class Punishmenthistory(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)
    uuid = models.CharField(max_length=35, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    operator = models.CharField(max_length=16, blank=True, null=True)
    punishmenttype = models.CharField(db_column='punishmentType', max_length=16, blank=True, null=True)  # Field name made lowercase.
    start = models.TextField(blank=True, null=True)
    end = models.TextField(blank=True, null=True)
    calculation = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punishmenthistory'


class Punishments(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)
    uuid = models.CharField(max_length=35, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    operator = models.CharField(max_length=16, blank=True, null=True)
    punishmenttype = models.CharField(db_column='punishmentType', max_length=16, blank=True, null=True)  # Field name made lowercase.
    start = models.TextField(blank=True, null=True)
    end = models.TextField(blank=True, null=True)
    calculation = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punishments'


class RoleplayInput(models.Model):
    message = models.TextField()

    class Meta:
        managed = False
        db_table = 'roleplay_input'


class RoleplayOutput(models.Model):
    message = models.TextField()

    class Meta:
        managed = False
        db_table = 'roleplay_output'


class SiteProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=45)
    long_name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    category = models.ForeignKey('SiteProductCategory', models.DO_NOTHING, db_column='category')
    buyers_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_product'


class SiteProductCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=45)
    long_name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_product_category'


class SiteProductKonlineOnline(models.Model):
    site_product = models.ForeignKey(SiteProduct, models.DO_NOTHING, db_column='site_product')
    konline_online = models.ForeignKey(KonlineOnline, models.DO_NOTHING, db_column='konline_online')

    class Meta:
        managed = False
        db_table = 'site_product_konline_online'


class SiteProductQueue(models.Model):
    name = models.CharField(max_length=45)
    product_text = models.TextField()
    server = models.CharField(max_length=45)
    product = models.ForeignKey(SiteProduct, models.DO_NOTHING, db_column='product')

    class Meta:
        managed = False
        db_table = 'site_product_queue'
