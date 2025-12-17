from app.models.category import Category

def get_all_categories():
    return list(Category.select())

def create_new_category(name, slug):
    if Category.select().where(Category.name == name).exists():
        return None, "Categoria já existe."
    
    category = Category.create(name=name, slug=slug)
    return category, None
    
def update_existing_category(category_id, name):
    try:
        category = Category.get_by_id(category_id)
        category.name = name
        category.save()
        return category, None
    except Category.DoesNotExist:
        return None, "Categoria não encontrada."

def delete_existing_category(category_id):
    try:
        category = Category.get_by_id(category_id)
        category.delete_instance()
        return True, None
    except Category.DoesNotExist:
        return None, "Categoria não encontrada."
