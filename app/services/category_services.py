from app.models.category import Category

def get_all_categories():
    # return only root categories (parent is null); to_dict() will include children recursively
    return list(Category.select().where(Category.parent.is_null()))

def create_new_category(name, slug, parent_id=None):
    if Category.select().where(Category.name == name).exists():
        return None, "Categoria já existe."
    
    parent = None
    if parent_id is not None:
        try:
            parent = Category.get_by_id(parent_id)
        except Category.DoesNotExist:
            return None, "Categoria pai não encontrada."

    category = Category.create(name=name, slug=slug, parent=parent)
    return category, None
    
def update_existing_category(category_id, name, parent_id=None):
    try:
        category = Category.get_by_id(category_id)
        category.name = name
        if parent_id is not None:
            if parent_id == category.id:
                return None, "Uma categoria não pode ser pai dela mesma."
            try:
                parent = Category.get_by_id(parent_id)
            except Category.DoesNotExist:
                return None, "Categoria pai não encontrada."
            category.parent = parent
        category.save()
        return category, None
    except Category.DoesNotExist:
        return None, "Categoria não encontrada."

def delete_existing_category(category_id):
    try:
        category = Category.get_by_id(category_id)
        category.delete_instance(recursive=True)  # remove filhos se existir
        return True, None
    except Category.DoesNotExist:
        return None, "Categoria não encontrada."
