import { useEffect, useState } from "react";
import { api } from "./api";
import { isValidSalary } from "./validate";
import "./App.css";

const PAGE_SIZE = 20;

function useStats() {
  const [stats, setStats] = useState({ summary: null, byDept: [], byCountry: [], top: [] });
  useEffect(() => {
    Promise.all([api.summary(), api.byDept(), api.byCountry(), api.topEarners()]).then(
      ([summary, byDept, byCountry, top]) => setStats({ summary, byDept, byCountry, top }),
      () => {}
    );
  }, []);
  return stats;
}

export default function App() {
  const [filters, setFilters] = useState({ search: "", country: "", department: "", level: "", sort_by: "last_name", sort_dir: "asc" });
  const [meta, setMeta] = useState({ countries: [], departments: [], levels: [] });
  const [page, setPage] = useState(1);
  const [data, setData] = useState({ total: 0, items: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState(null);
  const [newSalary, setNewSalary] = useState("");
  const { summary, byDept, byCountry, top } = useStats();

  useEffect(() => {
    api.filters().then(setMeta).catch(() => {});
  }, []);

  const reload = () => {
    setLoading(true);
    const params = { page, page_size: PAGE_SIZE, ...Object.fromEntries(Object.entries(filters).filter(([, v]) => v)) };
    api.employees(params).then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false));
  };
  useEffect(reload, [filters, page]);

  const saveSalary = async () => {
    const val = Number(newSalary);
    if (!isValidSalary(newSalary)) { setError("Salary must be between 0 and 1,000,000"); return; }
    try {
      await api.updateSalary(editing.id, val);
      setEditing(null);
      setNewSalary("");
      reload();
    } catch (e) { setError(e.message); }
  };

  const totalPages = Math.max(1, Math.ceil(data.total / PAGE_SIZE));
  const maxDept = Math.max(1, ...byDept.map((d) => d.total_usd));

  return (
    <div className="layout">
      <header className="topbar">
        <h1>ACME Salary Management</h1>
        <span className="badge">{data.total.toLocaleString()} employees</span>
      </header>

      {summary && (
        <section className="cards">
          <div className="card"><div className="label">Headcount</div><div className="value">{summary.headcount.toLocaleString()}</div></div>
          <div className="card"><div className="label">Total payroll (USD)</div><div className="value">${summary.total_payroll_usd.toLocaleString()}</div></div>
          <div className="card"><div className="label">Average (USD)</div><div className="value">${summary.avg_salary_usd.toLocaleString()}</div></div>
          <div className="card"><div className="label">Median (USD)</div><div className="value">${summary.median_salary_usd.toLocaleString()}</div></div>
        </section>
      )}

      <section className="panels">
        <div className="panel">
          <h3>Pay by department</h3>
          {byDept.map((d) => (
            <div key={d.department} className="bar-row">
              <span>{d.department}</span>
              <div className="bar"><div style={{ width: `${(d.total_usd / maxDept) * 100}%` }} /></div>
              <span className="muted">${d.avg_usd.toLocaleString()} avg</span>
            </div>
          ))}
        </div>
        <div className="panel">
          <h3>Top earners</h3>
          <ul>{top.map((t) => <li key={t.id}>{t.name} — {t.department} ({t.country}) · ${t.salary_usd.toLocaleString()}</li>)}</ul>
          <h3>Avg by country</h3>
          <ul>{byCountry.slice(0, 6).map((c) => <li key={c.country}>{c.country}: ${c.avg_usd.toLocaleString()} ({c.headcount})</li>)}</ul>
        </div>
      </section>

      <section className="toolbar">
        <input placeholder="Search name or email…" value={filters.search}
          onChange={(e) => { setPage(1); setFilters({ ...filters, search: e.target.value }); }} />
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
          <thead><tr><th>Name</th><th>Email</th><th>Country</th><th>Dept</th><th>Level</th><th>Salary</th><th>USD</th><th></th></tr></thead>
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
                <td><button className="link" onClick={() => { setEditing(e); setNewSalary(e.base_salary); }}>Edit</button></td>
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

      {editing && (
        <div className="modal-backdrop" onClick={() => setEditing(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Edit salary — {editing.first_name} {editing.last_name}</h3>
            <p className="muted">{editing.email} · {editing.currency}</p>
            <input type="number" value={newSalary} onChange={(e) => setNewSalary(e.target.value)} />
            <div className="modal-actions">
              <button onClick={() => setEditing(null)}>Cancel</button>
              <button className="primary" onClick={saveSalary}>Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
