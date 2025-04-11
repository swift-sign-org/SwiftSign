from BackEnd.Database.ProjectDatabase import *



# Insert a new entity into the database
def insertEntity(model, **kwargs):
    with app.app_context():
        new_entity = model(**kwargs)
        db.session.add(new_entity)
        db.session.commit()
        print(f"New {model.__name__} inserted successfully.")



# Update an entity in the database by its ID
def updateEntityById(
        model,
        entityId,
        idFieldName,
        **kwargs
):
    with app.app_context():
        entity = model.query.filter_by(**{idFieldName: entityId}).first()
        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            db.session.commit()
            print(f"{model.__name__} with ID {entityId} updated successfully.")
        else:
            print(f"No {model.__name__} found with ID {entityId}.")


# Delete an entity from the database by its ID
def deleteEntity(
        modelClass,
        entityId,
        idFieldName
):
    with app.app_context():
        entity = modelClass.query.filter(getattr(modelClass, idFieldName) == entityId).first()
        if entity:
            db.session.delete(entity)
            db.session.commit()
            print(f"✅ {modelClass.__name__} with {idFieldName}={entityId} deleted successfully.")
        else:
            print(f"❌ No {modelClass.__name__} found with {idFieldName}={entityId}.")





