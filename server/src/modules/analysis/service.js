const Session = require("./model");
const analysisQueue = require("./queue");
const JOBS = require("./jobs");

const startAnalysis = async ({ userId, s3Key, originalName }) => {
    // Create analysis session
    const session = await Session.create({
        user_id: userId,
        originalName,
        s3Key,

        status: "processing",
        currentStep: "eda",
        progress: 0,
    });

    // Queue first job
    await analysisQueue.add(
        JOBS.EDA,
        {
            sessionId: session._id.toString(),
            userId: userId.toString(),
            s3Key,
        },
        {
            attempts: 3,
            removeOnComplete: 100,
            removeOnFail: 100,
        }
    );

    return {
        sessionId: session._id,
        status: session.status,
        currentStep: session.currentStep,
        progress: session.progress,
    };
};

const getAnalysis = async (sessionId) => {
    const session = await Session.findById(sessionId);
    if (!session) {
        throw new Error("Analysis session not found.");
    }
    return session;
};

module.exports = {
    startAnalysis,
    getAnalysis,
};