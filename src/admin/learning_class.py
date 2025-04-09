from sqladmin import ModelView

from models import LearningClass


class LearningClassAdmin(ModelView, model=LearningClass):
    """Административный интерфейс для управления классами."""
    name = 'Класс'
    name_plural = 'Классы'
    column_list = [LearningClass.class_number, LearningClass.week_day, LearningClass.class_time, LearningClass.teacher]
    column_details_list = [LearningClass.class_number, LearningClass.week_day,
                           LearningClass.class_time, LearningClass.teacher]
    form_columns = [LearningClass.class_number, LearningClass.week_day, LearningClass.class_time, LearningClass.teacher]
    column_labels = {
        LearningClass.class_number: 'Номер класса',
        LearningClass.week_day: 'День недели урока',
        LearningClass.class_time: 'Время урока',
        LearningClass.teacher: 'Преподаватель'
    }
