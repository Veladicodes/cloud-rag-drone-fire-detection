// Deterministic call-sign -> color/label mapping so a given drone keeps the
// same visual identity across reconnects, independent of connection order.
export const PALETTE = [
  "#39c2a0", // teal
  "#ff7a33", // ember
  "#9b7bff", // violet
  "#4d9fff", // blue
  "#ff5c8a", // rose
  "#c6e86b", // lime
];

function hashString(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = (h * 31 + str.charCodeAt(i)) >>> 0;
  }
  return h;
}

export function colorForCallSign(callSign) {
  const h = hashString(callSign ?? "");
  return PALETTE[h % PALETTE.length];
}

export function shortLabel(callSign) {
  const cs = callSign ?? "";
  const match = cs.match(/(\d+)\s*$/);
  if (match) return `D${match[1]}`;
  return cs.slice(0, 2).toUpperCase();
}
