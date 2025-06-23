import pytest
from fastapi.testclient import TestClient
from backend.agent import app
import aiohttp

client = TestClient(app)

def test_generate_code_valid_request():
    """
    تست درخواست معتبر برای تولید کد.
    """
    response = client.post("/generate_code", json={"prompt": "یک تابع پایتون بنویس", "language": "python"})
    assert response.status_code == 200
    assert "generated_code" in response.json()
    assert "language" in response.json()

def test_generate_code_invalid_prompt():
    """
    تست درخواست با پرامپت نامعتبر (خالی).
    """
    response = client.post("/generate_code", json={"prompt": ""})
    assert response.status_code == 422  # خطای اعتبارسنجی Pydantic
    assert "detail" in response.json()

def test_generate_code_network_error(mocker):
    """
    تست خطای شبکه (مانند قطعی VPN یا عدم دسترسی به API).
    """
    mocker.patch("aiohttp.ClientSession.post", side_effect=aiohttp.ClientError)
    response = client.post("/generate_code", json={"prompt": "یک تابع پایتون بنویس", "language": "python"})
    assert response.status_code == 503
    assert "خطای شبکه" in response.json()["detail"]
