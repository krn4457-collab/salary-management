import { describe, expect, it } from "vitest";
import { formatUSD, isValidSalary } from "./validate";

describe("isValidSalary", () => {
  it("accepts normal salaries", () => {
    expect(isValidSalary(50000)).toBe(true);
    expect(isValidSalary("900000")).toBe(true);
  });
  it("rejects zero, negative, huge and non-numeric", () => {
    expect(isValidSalary(0)).toBe(false);
    expect(isValidSalary(-5)).toBe(false);
    expect(isValidSalary(1000000)).toBe(false);
    expect(isValidSalary("abc")).toBe(false);
    expect(isValidSalary("")).toBe(false);
  });
});

describe("formatUSD", () => {
  it("formats with dollar sign and separators", () => {
    expect(formatUSD(150000)).toBe("$150,000");
  });
});
