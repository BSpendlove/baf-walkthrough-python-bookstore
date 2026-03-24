from tests.conftest import SAMPLE_BOOK


class TestCreateBook:
    def test_create_book(self, client):
        response = client.post("/books", json=SAMPLE_BOOK)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == SAMPLE_BOOK["title"]
        assert data["author"] == SAMPLE_BOOK["author"]
        assert data["isbn"] == "9780306406157"
        assert data["price"] == 12.99
        assert data["id"] is not None
        assert data["created_at"] is not None
        assert data["updated_at"] is not None

    def test_create_book_normalizes_isbn(self, client):
        book = {**SAMPLE_BOOK, "isbn": "978-0-306-40615-7"}
        response = client.post("/books", json=book)
        assert response.status_code == 201
        assert response.json()["isbn"] == "9780306406157"

    def test_create_book_invalid_isbn(self, client):
        book = {**SAMPLE_BOOK, "isbn": "1234567890123"}
        response = client.post("/books", json=book)
        assert response.status_code == 422

    def test_create_book_duplicate_isbn(self, client):
        client.post("/books", json=SAMPLE_BOOK)
        response = client.post("/books", json={**SAMPLE_BOOK, "title": "Another Book"})
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_create_book_negative_price(self, client):
        book = {**SAMPLE_BOOK, "price": -5.0}
        response = client.post("/books", json=book)
        assert response.status_code == 422

    def test_create_book_invalid_year(self, client):
        book = {**SAMPLE_BOOK, "published_year": 999}
        response = client.post("/books", json=book)
        assert response.status_code == 422


class TestGetBook:
    def test_get_book(self, client):
        create_resp = client.post("/books", json=SAMPLE_BOOK)
        book_id = create_resp.json()["id"]
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        assert response.json()["title"] == SAMPLE_BOOK["title"]

    def test_get_book_not_found(self, client):
        response = client.get("/books/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"


class TestListBooks:
    def test_list_empty(self, client):
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_books(self, client):
        client.post("/books", json=SAMPLE_BOOK)
        response = client.get("/books")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_list_pagination(self, client):
        valid_isbns = [
            "9780306406157",
            "9781234567897",
            "9780140449136",
            "9780141439518",
            "9780060935467",
        ]
        for i, isbn in enumerate(valid_isbns):
            book = {**SAMPLE_BOOK, "isbn": isbn, "title": f"Book {i}"}
            client.post("/books", json=book)

        response = client.get("/books?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

        response = client.get("/books?skip=3&limit=10")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestUpdateBook:
    def test_update_book(self, client):
        create_resp = client.post("/books", json=SAMPLE_BOOK)
        book_id = create_resp.json()["id"]
        response = client.put(f"/books/{book_id}", json={"title": "Updated Title"})
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        assert response.json()["author"] == SAMPLE_BOOK["author"]

    def test_update_book_not_found(self, client):
        response = client.put("/books/999", json={"title": "Updated"})
        assert response.status_code == 404

    def test_update_book_invalid_isbn(self, client):
        create_resp = client.post("/books", json=SAMPLE_BOOK)
        book_id = create_resp.json()["id"]
        response = client.put(f"/books/{book_id}", json={"isbn": "bad"})
        assert response.status_code == 422

    def test_update_book_duplicate_isbn(self, client):
        client.post("/books", json=SAMPLE_BOOK)
        book2 = {**SAMPLE_BOOK, "isbn": "9781234567897", "title": "Second Book"}
        create_resp = client.post("/books", json=book2)
        book_id = create_resp.json()["id"]
        response = client.put(f"/books/{book_id}", json={"isbn": "9780306406157"})
        assert response.status_code == 409


class TestDeleteBook:
    def test_delete_book(self, client):
        create_resp = client.post("/books", json=SAMPLE_BOOK)
        book_id = create_resp.json()["id"]
        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 204

        response = client.get(f"/books/{book_id}")
        assert response.status_code == 404

    def test_delete_book_not_found(self, client):
        response = client.delete("/books/999")
        assert response.status_code == 404
