from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    
    def ready(signals):
        import accounts.signals