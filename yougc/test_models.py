# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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

    class Meta:
        managed = False
        db_table = 'konline_online'


class KpasswordsMessages(models.Model):
    player = models.CharField(max_length=45)
    message = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'kpasswords_messages'


class MinecraftMypermissionsmixin(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'minecraft_mypermissionsmixin'


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


class SiteProductQueue(models.Model):
    name = models.CharField(max_length=45)
    product = models.TextField()
    server = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'site_product_queue'
