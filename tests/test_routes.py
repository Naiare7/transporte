def test_index_route(client):
    """Prueba que la raíz responde correctamente"""
    response = client.get('/')
    assert response.status_code == 200
    assert "Servidor de Transporte" in response.data.decode('utf-8')