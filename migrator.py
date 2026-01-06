from peewee import SqliteDatabase, CharField
from playhouse.migrate import SqliteMigrator, migrate

# Configuração do banco
db = SqliteDatabase('dtudo.db')
migrator = SqliteMigrator(db)

# Definição do novo campo
phone_field = CharField(unique=True, null=True)

def run_migration():
    print("Iniciando migração...")
    try:
        migrate(
            migrator.add_column('user', 'phone', phone_field),
        )
        print("Coluna 'phone' adicionada com sucesso à tabela 'user'!")
    except Exception as e:
        print(f"Erro ao rodar migração: {e}")
        print("Dica: Se a coluna já existir, você pode ignorar este erro.")

if __name__ == '__main__':
    run_migration()
