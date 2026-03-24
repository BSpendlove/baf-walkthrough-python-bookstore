from tests.conftest import SAMPLE_BOOK


def _seed_books(client):
    books = [
        {**SAMPLE_BOOK, "isbn": "9780306406157", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {**SAMPLE_BOOK, "isbn": "9781234567897", "title": "To Kill a Mockingbird", "author": "Harper Lee"},
        {**SAMPLE_BOOK, "isbn": "9780140449136", "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
    ]
    for book in books:
        client.post("/books", json=book)


class TestSearchBooks:
    def test_search_by_title(self, client):
        _seed_books(client)
        response = client.get("/books/search?q=gatsby")
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["title"] == "The Great Gatsby"

    def test_search_by_author(self, client):
        _seed_books(client)
        response = client.get("/books/search?q=dostoevsky")
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["author"] == "Fyodor Dostoevsky"

    def test_search_case_insensitive(self, client):
        _seed_books(client)
        response = client.get("/books/search?q=GATSBY")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_search_partial_match(self, client):
        _seed_books(client)
        response = client.get("/books/search?q=kill")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_search_no_results(self, client):
        _seed_books(client)
        response = client.get("/books/search?q=nonexistent")
        assert response.status_code == 200
        assert response.json() == []

    def test_search_pagination(self, client):
        _seed_books(client)
        response = client.get("/books/search?q=the&skip=0&limit=1")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_search_requires_query(self, client):
        response = client.get("/books/search")
        assert response.status_code == 422
