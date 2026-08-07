const axios = require("axios");
const env = require("../../config/env");

const pythonApi = axios.create({
    baseURL: env.PYTHON_SERVICE_URL,
    timeout: 1000 * 60 * 5, // 5 minutes
    headers: {
        "Content-Type": "application/json",
    },
});

const runProfile = async ({ sessionId, s3Key }) => {
    const { data } = await pythonApi.post("/eda/profile", {
        session_id: sessionId,
        s3_key: s3Key,
    });

    return data.data;
};

const runCharts = async ({ sessionId, s3Key }) => {
    const { data } = await pythonApi.post("/eda/charts", {
        session_id: sessionId,
        s3_key: s3Key,
    });

    return data.data.charts;
};

const runInsights = async ({
    sessionId,
    datasetName,
    profile,
    charts,
}) => {
    const { data } = await pythonApi.post("/ai/insights", {
        session_id: sessionId,
        dataset_name: datasetName,
        profile,
        charts,
    });

    return data.data;
};

module.exports = {
    pythonApi,
    runProfile,
    runCharts,
    runInsights,
};