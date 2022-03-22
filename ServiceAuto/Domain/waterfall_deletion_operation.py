from Domain.enitity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repositories.repository import Repository


class WaterfallDeletion(UndoRedoOperation):

    def __init__(self,
                 repository_1: Repository,
                 repository_2: Repository,
                 repository_3: Repository,
                 entity_1: Entity,
                 entity_2: Entity,
                 entity_3: Entity
                 ):

        self.repository_1 = repository_1
        self.repository_2 = repository_2
        self.repository_3 = repository_3
        self.entity_1 = entity_1
        self.entity_2 = entity_2
        self.entity_3 = entity_3

    def do_undo(self):

        self.repository_1.create(self.entity_1)
        self.repository_2.create(self.entity_2)
        self.repository_3.create(self.entity_3)

    def do_redo(self):

        self.repository_1.delete(self.entity_1.id_entity)
        self.repository_2.delete(self.entity_2.id_entity)
        self.repository_3.delete(self.entity_3.id_entity)
