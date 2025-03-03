from sqladmin import ModelView

from models import TopicBlock


class TopicBlockAdmin(ModelView, model=TopicBlock):
    name = 'Раздел'
    name_plural = 'Разделы'
    column_list = [TopicBlock.name, TopicBlock.image_url]
    column_details_list = [TopicBlock.name, TopicBlock.image_url]
    form_columns = [TopicBlock.name, TopicBlock.image_url]
    column_labels = {TopicBlock.name: 'Наименование', TopicBlock.image_url: 'Ссылка на иконку'}


