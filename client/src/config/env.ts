export const ENV = {
  MODE: import.meta.env.MODE,
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
};

console.log("API BASE URL:", ENV.API_BASE_URL);

export const isLocal = ENV.MODE === "development";
export const isProd = ENV.MODE === "production";

console.log("is local: ", isLocal)
console.log("is prod: ", isProd)