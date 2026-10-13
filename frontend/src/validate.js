export function isValidSalary(value) {
  const n = Number(value);
  return Number.isFinite(n) && n > 0 && n < 1000000;
}

export function formatUSD(n) {
  return "$" + Number(n).toLocaleString("en-US");
}
