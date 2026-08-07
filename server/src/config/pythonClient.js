const axios = require("axios");
const env = require("./env");

const pythonApi = axios.create({
    baseURL: env.PYTHON_SERVICE_URL,
    timeout: 1000 * 60 * 5, // 5 minutes
    headers: {
        "Content-Type": "application/json",
    },
});

module.exports = pythonApi