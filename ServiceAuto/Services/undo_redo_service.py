from typing import List

from Domain.undo_redo_operation import UndoRedoOperation


class UndoRedoService:

    def __init__(self):

        self.undo_list: List[UndoRedoOperation] = []
        self.redo_list: List[UndoRedoOperation] = []
        self.number_of_operations = 1
        self.redo_number_of_operations = 0

    def undo(self):

        if len(self.undo_list) > 0:

            for current_operation in range(self.number_of_operations):

                last_operation = self.undo_list.pop()
                last_operation.do_undo()
                self.redo_list.append(last_operation)
                self.redo_number_of_operations += 1

    def redo(self):

        if len(self.redo_list) > 0:

            if self.redo_number_of_operations > len(self.redo_list):
                self.redo_number_of_operations = len(self.redo_list)

            for current_operation in range(self.redo_number_of_operations):

                last_operation = self.redo_list.pop()
                last_operation.do_redo()
                self.undo_list.append(last_operation)

    def clear_redo(self):

        self.redo_list.clear()

    def add_operation(self, operation: UndoRedoOperation):

        self.undo_list.append(operation)

    def delete_operation(self, operation: UndoRedoOperation):

        self.undo_list.append(operation)

    def update_operation(self, operation_before_update: UndoRedoOperation):

        self.undo_list.append(operation_before_update)

    def delete_from_interval_of_time(self, operations: list):

        self.number_of_operations = len(operations)

        for operation in operations:

            self.undo_list.append(operation)

    def update_warranty(self, operations: list):

        self.number_of_operations = len(operations)

        for operation in operations:

            self.undo_list.append(operation)

    def waterfall_deletion(self, operation: UndoRedoOperation):

        self.undo_list.append(operation)
