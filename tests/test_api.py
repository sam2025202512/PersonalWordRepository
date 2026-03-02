#functional test for the REST API

def test_create_user_success(client):
  # test that a valid user can be created
  response = client.post("/users", json={
    "email":"test@example.com",
    "password": "hashed_password"
  })
  assert response.status_code == 201
  assert "id" in response json
