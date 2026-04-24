import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_returns_200(client):
    response = client.get('/api/users/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True

def test_get_all_has_total(client):
    response = client.get('/api/users/')
    data = response.get_json()
    assert 'total' in data
    assert isinstance(data['total'], int)

def test_get_by_id_returns_200(client):
    # Asumiendo que el usuario con ID 1 existe según app/models.py
    response = client.get('/api/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['id'] == 1

def test_get_by_id_not_found(client):
    response = client.get('/api/users/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False

def test_create_user_returns_201(client):
    new_user = {
        "name": "Prueba",
        "email": "prueba@test.com",
        "age": 30
    }
    response = client.post('/api/users/', json=new_user)
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['name'] == "Prueba"

def test_create_user_increments_id(client):
    # Primero obtenemos la lista actual para saber cuántos hay (y el máximo id)
    res_get = client.get('/api/users/')
    total_before = res_get.get_json()['total']
    users_list = res_get.get_json()['data']
    max_id_before = max((u['id'] for u in users_list), default=0)

    # Creamos un usuario nuevo
    new_user = {"name": "Test ID", "email": "testid@test.com", "age": 25}
    response = client.post('/api/users/', json=new_user)
    data = response.get_json()
    
    assert data['data']['id'] == max_id_before + 1

def test_create_user_missing_fields(client):
    response = client.post('/api/users/', json={"name": "Solo Nombre"})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_update_user_returns_200(client):
    # Actualizamos un usuario existente (ID 1)
    response = client.put('/api/users/1', json={"age": 99})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['age'] == 99

def test_update_user_not_found(client):
    response = client.put('/api/users/999', json={"age": 99})
    # Según el laboratorio, la actualización de un usuario que no existe retorna 400
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_delete_user_returns_200(client):
    # Borramos el usuario 2 para no afectar otras pruebas que asumen que el 1 existe
    response = client.delete('/api/users/2')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['id'] == 2

def test_delete_user_not_found(client):
    response = client.delete('/api/users/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False

def test_delete_removes_from_list(client):
    # Borramos al usuario 3
    delete_res = client.delete('/api/users/3')
    assert delete_res.status_code == 200

    # Intentamos obtenerlo
    get_res = client.get('/api/users/3')
    assert get_res.status_code == 404
