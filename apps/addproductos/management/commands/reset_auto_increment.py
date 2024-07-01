from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reset auto-increment sequence for specific tables'

    def handle(self, *args, **options):
        tables_to_reset = ['addproductos_cart', 'addproductos_cartitem']  # Especifica aquí las tablas que deseas restablecer
        self.truncate_tables(tables_to_reset)
        self.reset_auto_increment(tables_to_reset)
        self.stdout.write(self.style.SUCCESS('Successfully reset auto-increment sequences for specified tables'))

    def truncate_tables(self, tables):
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys = OFF;")  # Desactivar restricciones de clave foránea
            for table_name in tables:
                cursor.execute(f"DELETE FROM {table_name};")
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
            cursor.execute("PRAGMA foreign_keys = ON;")  # Activar nuevamente restricciones de clave foránea

    def reset_auto_increment(self, tables):
        with connection.cursor() as cursor:
            for table_name in tables:
                cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name='{table_name}';")
