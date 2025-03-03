from sqladmin import ModelView

from models import StudyMaterial


class MaterialAdmin(ModelView, model=StudyMaterial):
    name = 'Учебный материал'
    name_plural = 'Учебные материалы'
    column_list = [StudyMaterial.name, StudyMaterial.topic]
    column_details_list = [StudyMaterial.name, StudyMaterial.topic, StudyMaterial.video_url, StudyMaterial.text]
    form_columns = [StudyMaterial.name, StudyMaterial.topic, StudyMaterial.video_url, StudyMaterial.text]
    column_labels = {
        StudyMaterial.name: 'Наименование',
        StudyMaterial.topic: 'Раздел',
        StudyMaterial.video_url: 'Ссылка на видео',
        StudyMaterial.text: 'Текст'
    }
    # create_template = 'sqladmin/custom_create.html'
    edit_template = 'sqladmin/custom_edit.html'
