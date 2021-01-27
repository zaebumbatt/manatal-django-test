class LogsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.object_name == 'Log':
            return 'remote'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.object_name == 'Log':
            return 'remote'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'log':
            return db == 'remote'
        return db == 'default'
