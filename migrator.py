from peewee import SqliteDatabase, CharField, DateTimeField
from playhouse.migrate import SqliteMigrator, migrate
from datetime import datetime

# Configuração do banco
db = SqliteDatabase('dtudo.db')
migrator = SqliteMigrator(db)

# Definição dos novos campos
created_at_field = DateTimeField(default=datetime.now, null=True)

def run_migration():
    print("Iniciando migração...")
    try:
        migrate(
            migrator.add_column('product', 'created_at', created_at_field),
        )
        print("Coluna 'created_at' adicionada com sucesso à tabela 'product'!")
    except Exception as e:
        print(f"Erro ao rodar migração: {e}")
        print("Dica: Se a coluna já existir, você pode ignorar este erro.")

if __name__ == '__main__':
    run_migration()
