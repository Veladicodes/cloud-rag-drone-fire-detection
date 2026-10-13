import { describe, it, expect } from "vitest";
import { pushTrailPoint, MAX_TRAIL_POINTS } from "./droneTrail.js";

describe("pushTrailPoint", () => {
  it("appends a new point to an empty trail", () => {
    const trail = pushTrailPoint([], [34.0, -118.0]);
    expect(trail).toEqual([[34.0, -118.0]]);
  });

  it("appends to the end, preserving order", () => {
    const trail = pushTrailPoint([[1, 1], [2, 2]], [3, 3]);
    expect(trail).toEqual([[1, 1], [2, 2], [3, 3]]);
  });

  it("caps the trail at MAX_TRAIL_POINTS, dropping the oldest", () => {
    let trail = [];
    for (let i = 0; i < MAX_TRAIL_POINTS + 5; i++) {
      trail = pushTrailPoint(trail, [i, i]);
    }
    expect(trail.length).toBe(MAX_TRAIL_POINTS);
    expect(trail[0]).toEqual([5, 5]); // oldest 5 dropped
    expect(trail[trail.length - 1]).toEqual([MAX_TRAIL_POINTS + 4, MAX_TRAIL_POINTS + 4]);
  });

  it("does not mutate the input array", () => {
    const original = [[1, 1]];
    const result = pushTrailPoint(original, [2, 2]);
    expect(original).toEqual([[1, 1]]);
    expect(result).not.toBe(original);
  });
});
