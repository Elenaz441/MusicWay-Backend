from sqladmin import ModelView

from models import Feedback


class FeedbackAdmin(ModelView, model=Feedback):
    name = 'Обратная связь'
    name_plural = 'Обратная связь'
    can_create = False
    can_delete = False
    column_list = [Feedback.material, Feedback.comment, Feedback.is_processed]
    column_details_list = [Feedback.material, Feedback.comment, Feedback.is_processed]
    column_default_sort = [(Feedback.is_processed, False),]
    form_columns = [Feedback.is_processed,]
    column_labels = {
        Feedback.material: 'Учебный материал',
        Feedback.comment: 'Комментарий',
        Feedback.is_processed: 'Обработано'
    }
