from Domain.enitity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repositories.repository import Repository


class UpdateOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 entity: Entity,
                 entity_after_update: Entity):

        self.repository = repository
        self.entity = entity
        self.entity_after_update = entity_after_update

    def do_undo(self):

        self.repository.update(self.entity)

    def do_redo(self):

        self.repository.update(self.entity_after_update)
