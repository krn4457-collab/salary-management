"""Stats endpoint tests."""


def test_summary(client, sample):
    r = client.get("/api/stats/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["headcount"] == 3
    assert body["total_payroll_usd"] == 9600 + 150000 + 6000
    assert body["avg_salary_usd"] > 0
    assert body["median_salary_usd"] > 0


def test_by_department(client, sample):
    rows = {r["department"]: r for r in client.get("/api/stats/by-department").json()}
    assert rows["Engineering"]["headcount"] == 2
    assert rows["Finance"]["headcount"] == 1


def test_by_country_and_level(client, sample):
    countries = {r["country"]: r for r in client.get("/api/stats/by-country").json()}
    assert countries["India"]["headcount"] == 2
    levels = {r["level"]: r for r in client.get("/api/stats/by-level").json()}
    assert levels["L3"]["headcount"] == 1


def test_top_earners(client, sample):
    rows = client.get("/api/stats/top-earners").json()
    assert rows[0]["salary_usd"] == 150000
