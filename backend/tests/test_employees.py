"""Core employee API tests: list/search/filter/pagination/update."""

from app.models import to_usd


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_list_pagination(client, sample):
    r = client.get("/api/employees", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2


def test_search(client, sample):
    r = client.get("/api/employees", params={"search": "beta"})
    assert r.json()["total"] == 1
    assert r.json()["items"][0]["email"] == "b@acme.example.com"


def test_filter_country(client, sample):
    r = client.get("/api/employees", params={"country": "India"})
    assert r.json()["total"] == 2


def test_sort_salary_desc(client, sample):
    r = client.get("/api/employees", params={"sort_by": "salary_usd", "sort_dir": "desc"})
    salaries = [i["salary_usd"] for i in r.json()["items"]]
    assert salaries == sorted(salaries, reverse=True)


def test_update_salary_recomputes_usd(client, sample):
    emp_id = sample[0].id
    r = client.patch(f"/api/employees/{emp_id}", json={"base_salary": 900000})
    assert r.status_code == 200
    assert r.json()["salary_usd"] == to_usd(900000, "INR")


def test_update_salary_validation(client, sample):
    emp_id = sample[0].id
    assert client.patch(f"/api/employees/{emp_id}", json={"base_salary": -5}).status_code == 422
    assert client.patch("/api/employees/99999", json={"base_salary": 50000}).status_code == 404


def test_create_and_delete(client, sample):
    payload = {"first_name": "D", "last_name": "Delta", "email": "d@acme.example.com",
               "country": "USA", "department": "HR", "level": "L1",
               "base_salary": 40000, "currency": "USD", "join_date": "2023-01-01"}
    r = client.post("/api/employees", json=payload)
    assert r.status_code == 201
    new_id = r.json()["id"]
    assert client.delete(f"/api/employees/{new_id}").status_code == 204
    assert client.get(f"/api/employees/{new_id}").status_code == 404
