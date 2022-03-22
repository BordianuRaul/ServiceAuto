from abc import abstractmethod, ABC


class UndoRedoOperation(ABC):

    @abstractmethod
    def do_undo(self):
        ...

    @abstractmethod
    def do_redo(self):
        ...
