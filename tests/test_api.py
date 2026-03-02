#functional test for the REST API

def test_create_user_success(client):
  # test that a valid user can be created
  response = client.post("/users", json={
    "email":"test@example.com",
    "password": "hashed_password"
  })
  assert response.status_code == 201
  assert "id" in response json

def test_create_user_missing_field(client):
  # test that missing field returns 400
  response = client.post("/users", json={
    "email":"test@example.com"
  })
  assert response.status_code == 400

def test_create_user_dubplicate_email(client):
  # test that when creating another user with same email returns 409
  client.post("/users", json={
    "email":"test@example.com",
    "password": "hashed_password"
  })
  response = client.post("/users", json={
    "email":"test@example.com",
    "password": "new_password"
  })
  assert response.status_code == 409

def test_get_user_not_found(client):
  # Test that requesting a non-existing user returns 404
  response = client.get("/users/does-not-exist")
  assert response.status_code == 404

def test_create_part_of_speech(client):
  # Test creating a valid part of speech
  response = client.post("/parts-of-speech", json={"name": "noun"})
  assert response.status_code == 201
  assert response.json["name"] == "noun"

def test_create_word_success(client):
  # Test creating a valid word
  user_resp = client.post("/users", json={
    "email":"test@example.com",
    "password": "hashed_password"
  })
  user_id = user_resp.json["id"]
  pos_resp = client.post("/parts-of-speech", json={"name": "verb"})
  pos_id = pos_resp.json["id"]
  response = client.post("/words", json={ "text": "run", "language": "en", "user_id": user_id, "part_of_speech_id": pos_id })
  assert response.status_code == 201
  assert response.json["text"] == "run"
