import axios from "axios";

const api = axios.create({ baseURL: "/api" });

export const fetchOverview = () => api.get("/dashboard/overview").then((r) => r.data);
export const fetchPositions = (openOnly = true) =>
  api.get("/positions/", { params: { open_only: openOnly } }).then((r) => r.data);
export const fetchTrades = (limit = 50) =>
  api.get("/trades/", { params: { limit } }).then((r) => r.data);
export const fetchPnl = (limit = 90) =>
  api.get("/dashboard/pnl", { params: { limit } }).then((r) => r.data);
export const fetchBotStatus = () => api.get("/bot/status").then((r) => r.data);
export const controlBot = (action) =>
  api.post("/bot/control", { action }).then((r) => r.data);
export const fetchSettings = () => api.get("/settings/").then((r) => r.data);
export const updateSettings = (settings) =>
  api.put("/settings/", settings).then((r) => r.data);

export default api;
