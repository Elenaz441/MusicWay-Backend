from sqladmin import ModelView

from models import StudentClass


class StudentClassAdmin(ModelView, model=StudentClass):
    """Административный интерфейс для управления учениками в классе."""
    name = 'Ученик_класс'
    name_plural = 'Ученики_классы'
    column_list = [StudentClass.learning_class, StudentClass.student]
    column_details_list = [StudentClass.learning_class, StudentClass.student]
    form_columns = [StudentClass.learning_class, StudentClass.student]
    column_labels = {StudentClass.learning_class: 'Класс', StudentClass.student: 'Ученик'}
