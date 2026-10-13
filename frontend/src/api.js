const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function req(path, opts = {}) {
  const res = await fetch(BASE + path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || `Request failed: ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  health: () => req("/api/health"),
  employees: (params) => req("/api/employees?" + new URLSearchParams(params)),
  getEmployee: (id) => req(`/api/employees/${id}`),
  updateSalary: (id, base_salary) =>
    req(`/api/employees/${id}`, { method: "PATCH", body: JSON.stringify({ base_salary }) }),
  filters: () => req("/api/employees/meta/filters"),
  summary: () => req("/api/stats/summary"),
  byDept: () => req("/api/stats/by-department"),
  byCountry: () => req("/api/stats/by-country"),
  byLevel: () => req("/api/stats/by-level"),
  topEarners: () => req("/api/stats/top-earners"),
};
