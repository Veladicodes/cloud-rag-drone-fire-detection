import { describe, it, expect } from "vitest";
import { colorForCallSign, shortLabel, PALETTE } from "./droneIdentity.js";

describe("colorForCallSign", () => {
  it("returns a color from the palette", () => {
    expect(PALETTE).toContain(colorForCallSign("SIM-1"));
  });

  it("is deterministic for the same call sign", () => {
    expect(colorForCallSign("SIM-2")).toBe(colorForCallSign("SIM-2"));
  });

  it("assigns different colors to different call signs when possible", () => {
    const colors = new Set(["SIM-1", "SIM-2", "SIM-3", "SIM-4"].map(colorForCallSign));
    expect(colors.size).toBeGreaterThan(1);
  });

  it("handles an empty string without throwing", () => {
    expect(() => colorForCallSign("")).not.toThrow();
    expect(PALETTE).toContain(colorForCallSign(""));
  });
});

describe("shortLabel", () => {
  it("extracts the numeric suffix from a SIM-N call sign", () => {
    expect(shortLabel("SIM-1")).toBe("D1");
    expect(shortLabel("SIM-12")).toBe("D12");
  });

  it("falls back to the first two characters for non-numeric call signs", () => {
    expect(shortLabel("MAV-7")).toBe("D7");
    expect(shortLabel("ALPHA")).toBe("AL");
  });

  it("handles an empty string without throwing", () => {
    expect(() => shortLabel("")).not.toThrow();
  });
});
