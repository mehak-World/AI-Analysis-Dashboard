const { Worker } = require("bullmq");

const { getRedisClient } = require("../../infrastructure/redis/client");

const JOBS = require("./jobs");
const analysisQueue = require("./queue");

const pythonClient = require("./python.client");
const sessionService = require("./session.service");

const worker = new Worker(
    "analysis",
    async (job) => {
        const { sessionId, s3Key } = job.data;

        try {
            switch (job.name) {
                case JOBS.EDA: {
                    console.log(`Running EDA for session ${sessionId}`);

                    const profile = await pythonClient.runProfile({
                        sessionId,
                        s3Key,
                    });

                    await sessionService.updateProfile(
                        sessionId,
                        profile
                    );

                    await analysisQueue.add(JOBS.CHARTS, {
                        sessionId,
                        s3Key,
                    });

                    break;
                }

                case JOBS.CHARTS: {
                    console.log(`Generating charts for ${sessionId}`);

                    const charts = await pythonClient.runCharts({
                        sessionId,
                        s3Key,
                    });

                    await sessionService.updateCharts(
                        sessionId,
                        charts
                    );

                    await analysisQueue.add(JOBS.AI, {
                        sessionId
                    });

                    break;
                }

                case JOBS.AI: {
                    console.log(`Generating AI insights for ${sessionId}`);

                    const payload = await sessionService.getInsightsPayload(sessionId);

                    const insights = await pythonClient.runInsights({
                        sessionId,
                        datasetName: payload.datasetName,
                        profile: payload.profile,
                        charts: payload.charts,
                    });

                    await sessionService.updateInsights(
                        sessionId,
                        insights
                    );

                    break;
                }

                default:
                    throw new Error(`Unknown job: ${job.name}`);
            }
        } catch (error) {
            console.error(error);

            await sessionService.markFailed(sessionId, error);

            throw error;
        }
    },
    {
        connection: getRedisClient(),
    }
);

worker.on("completed", (job) => {
    console.log(`Job ${job.id} (${job.name}) completed.`);
});

worker.on("failed", (job, error) => {
    console.error(
        `Job ${job?.id} (${job?.name}) failed:`,
        error.message
    );
});

worker.on("error", (error) => {
    console.error("BullMQ Worker Error:", error);
});

module.exports = worker;