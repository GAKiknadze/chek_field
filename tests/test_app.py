import pytest
from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


@pytest.fixture
def test_data_with_names():
    return [
        {
            "input": {"user_email": "test@example.com", "user_phone": "+7 123 456 78 90"},
            "expected_output": {"name": "Contact Form"},
        },
        {
            "input": {"order_date": "2023-10-10", "customer_phone": "+7 987 654 32 10"},
            "expected_output": {"name": "Order Form"},
        },
    ]


@pytest.fixture
def test_data_without_names():
    return [
        {
            "input": {"random_field": "hello world"},
            "expected_output": {"random_field": "text"},
        },
    ]


def test_valid_templates(test_data_with_names):
    """Проверка совпадения формы с шаблонами"""
    for case in test_data_with_names:
        response = client.post("/get_form", data=case["input"],
                        headers={'Content-Type': 'application/x-www-form-urlencoded'})
        assert response.status_code == 200
        assert response.json() == case["expected_output"]


def test_infer_field_types(test_data_without_names):
    """Проверка типизации для формы без совпадений"""
    for case in test_data_without_names:
        response = client.post("/get_form", data=case["input"],
                            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        assert response.status_code == 200
        assert response.json() == case["expected_output"]
