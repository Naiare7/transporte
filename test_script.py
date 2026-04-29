import pytest
from src.app import create_app

app = create_app()
with app.test_client() as client:
    res_post = client.post('/api/clientes', json={"nombre": "Cliente S.A.", "email": "cliente@test.com", "telefono": "123456"})
    print("POST /api/clientes:", res_post.status_code)
    data = res_post.json
    print("Response JSON:", data)
