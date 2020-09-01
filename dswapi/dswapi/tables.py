import django_tables2 as tables

from dswapi.models import CSVFile


class CSVListTable(tables.Table):
    file_name = tables.TemplateColumn('<a href="/csv/{{record.id}}">{{record.file_name}}</a>')

    class Meta:
        model = CSVFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_name", "download_date", "last_edited")


class CSVTable(tables.Table):
    name = tables.Column()
    height = tables.Column()
    mass = tables.Column()
    hair_color = tables.Column()
    skin_color = tables.Column()
    eye_color = tables.Column()
    birth_year = tables.Column()
    gender = tables.Column()
    homeworld = tables.Column()

    class Meta:
        attrs = {"id": "sw_table"}
