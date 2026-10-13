import { useEffect, useState } from "react";
import { api } from "./api";
import "./App.css";

const PAGE_SIZE = 20;

export default function App() {
  const [filters, setFilters] = useState({ search: "", country: "", department: "", level: "", sort_by: "last_name", sort_dir: "asc" });
  const [meta, setMeta] = useState({ countries: [], departments: [], levels: [] });
  const [page, setPage] = useState(1);
  const [data, setData] = useState({ total: 0, items: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.filters().then(setMeta).catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    setError("");
    const params = { page, page_size: PAGE_SIZE, ...Object.fromEntries(Object.entries(filters).filter(([, v]) => v)) };
    api.employees(params).then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, [filters, page]);

  const totalPages = Math.max(1, Math.ceil(data.total / PAGE_SIZE));

  return (
    <div className="layout">
      <header className="topbar">
        <h1>ACME Salary Management</h1>
        <span className="badge">{data.total.toLocaleString()} employees</span>
      </header>

      <section className="toolbar">
        <input
          placeholder="Search name or email…"
          value={filters.search}
          onChange={(e) => { setPage(1); setFilters({ ...filters, search: e.target.value }); }}
        />
        <select value={filters.country} onChange={(e) => { setPage(1); setFilters({ ...filters, country: e.target.value }); }}>
          <option value="">All countries</option>
          {meta.countries.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <select value={filters.department} onChange={(e) => { setPage(1); setFilters({ ...filters, department: e.target.value }); }}>
          <option value="">All departments</option>
          {meta.departments.map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
        <select value={filters.level} onChange={(e) => { setPage(1); setFilters({ ...filters, level: e.target.value }); }}>
          <option value="">All levels</option>
          {meta.levels.map((l) => <option key={l} value={l}>{l}</option>)}
        </select>
        <select value={filters.sort_by} onChange={(e) => setFilters({ ...filters, sort_by: e.target.value })}>
          <option value="last_name">Sort: name</option>
          <option value="salary_usd">Sort: salary</option>
          <option value="join_date">Sort: join date</option>
        </select>
      </section>

      {error && <div className="error">{error}</div>}
      {loading ? <div className="loading">Loading…</div> : (
        <table className="grid">
          <thead>
            <tr><th>Name</th><th>Email</th><th>Country</th><th>Dept</th><th>Level</th><th>Salary</th><th>USD</th></tr>
          </thead>
          <tbody>
            {data.items.map((e) => (
              <tr key={e.id}>
                <td>{e.first_name} {e.last_name}</td>
                <td className="muted">{e.email}</td>
                <td>{e.country}</td>
                <td>{e.department}</td>
                <td>{e.level}</td>
                <td>{e.base_salary.toLocaleString()} {e.currency}</td>
                <td>${e.salary_usd.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div className="pager">
        <button disabled={page <= 1} onClick={() => setPage(page - 1)}>← Prev</button>
        <span>Page {page} / {totalPages}</span>
        <button disabled={page >= totalPages} onClick={() => setPage(page + 1)}>Next →</button>
      </div>
    </div>
  );
}
