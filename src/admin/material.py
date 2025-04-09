from sqladmin import ModelView

from models import StudyMaterial


class MaterialAdmin(ModelView, model=StudyMaterial):
    """Административный интерфейс для управления учебными материалами."""
    name = 'Учебный материал'
    name_plural = 'Учебные материалы'
    column_list = [StudyMaterial.name, StudyMaterial.block]
    column_details_list = [StudyMaterial.name, StudyMaterial.block,
                           StudyMaterial.number, StudyMaterial.video_url, StudyMaterial.text]
    form_columns = [StudyMaterial.name, StudyMaterial.block,
                    StudyMaterial.number, StudyMaterial.video_url, StudyMaterial.text]
    column_labels = {
        StudyMaterial.name: 'Наименование',
        StudyMaterial.block: 'Раздел',
        StudyMaterial.video_url: 'Ссылка на видео',
        StudyMaterial.text: 'Текст',
        StudyMaterial.number: 'Номер в разделе'
    }
    edit_template = 'sqladmin/custom_edit.html'
