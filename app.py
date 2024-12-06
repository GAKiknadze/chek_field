from fastapi import FastAPI, Form
from tinydb import TinyDB, Query
from pydantic import BaseModel, RootModel
from typing import Annotated
import re
from datetime import datetime


app = FastAPI()
db = TinyDB('database.json')


def validate_field(value: str) -> str:
    """Определяет тип строки на основе значения.

    Args:
        value (str): любое строковое значение

    Returns:
        str: тип значения
    """
    if re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return "phone"
    try:
        if datetime.strptime(value, '%d.%m.%Y'):
            return "date"
    except ValueError:
        pass
    try:
        if datetime.strptime(value, '%Y-%m-%d'):
            return "date"
    except ValueError:
        pass
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        return "email"
    return "text"


class FormInput(RootModel):
    root: dict[str, str]


def prepare_data(form_data: FormInput) -> dict:
    """Подстановка типов данных

    Args:
        form_data (FormInput): Форма со значениями

    Returns:
        dict: Типы полей
    """
    return{field: validate_field(value) for field, value in form_data.model_dump().items()}


def find_template(data: dict) -> str | None:
    """Поиск значений в базе

    Args:
        form_data (dict): Форма со значениями

    Returns:
        str: Имя формы
    """
    result = db.search(Query().fragment(data))
    return None if len(result) == 0 else result[0]['name']


class FormTemplateName(BaseModel):
    name: str


class FormFieldTypes(RootModel):
    root: dict[str, str]


@app.post("/get_form")
async def get_form(fields: Annotated[FormInput, Form(...)]) -> FormTemplateName | FormFieldTypes:
    """POST-запрос на получение формы"""
    data = prepare_data(fields)
    template_name = find_template(data)
    if template_name:
        return FormTemplateName(name=template_name)
    return FormFieldTypes(root=data)
