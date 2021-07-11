from django.db.models import Model


class YougcRouter:
    tables = {'kactivity_leaderboard', 'authme', 'kactivity_list', 'kactivity_queue', 'kactivity_roles',
              'kactivity_today',
              'kbank_accounts', 'kbank_codes', 'kbank_history', 'kbank_last_id', 'kbank_queue', 'knews_knews',
              'konline_list', 'konline_online', 'kpasswords_messages', 'roleplay_input', 'roleplay_output',
              'site_product_queue', 'site_product', 'site_product_category', 'site_product_konline_online'}

    def db_for_read(self, model, **hints):
        if model._meta.db_table in self.tables:
            return 'yougc'

    def db_for_write(self, model, **hints):
        if model._meta.db_table in self.tables:
            return 'yougc'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.db_table in self.tables and obj2._meta.db_table in self.tables:
            return True
