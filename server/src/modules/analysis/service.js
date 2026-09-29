const Session = require("./model");
const analysisQueue = require("./queue");
const JOBS = require("./jobs");

const createSession = async ({ userId, originalName }) => {
    const session = await Session.create({
        user_id: userId,
        originalName,
        status: "processing",
        currentStep: "eda",
        progress: 0,
    });

    return session;
};

const startAnalysis = async ({
    sessionId,
    userId,
    s3Key,
}) => {
    await analysisQueue.add(
        JOBS.EDA,
        {
            sessionId: sessionId.toString(),
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
        sessionId,
    };
};

const getAnalysis = async (sessionId, userId) => {
    const session = await Session.findOne({
        _id: sessionId,
        user_id: userId,
    });

    if (!session) {
        throw new Error("Analysis session not found.");
    }

    return session;
};

const getSessions = async (userId, page = 1, limit = 20) => {
    console.log("user id: ", userId);

    const skip = (page - 1) * limit;

    const [sessions, total] = await Promise.all([
        Session.find({ user_id: userId })
            .select(
                "originalName status currentStep progress createdAt updatedAt"
            )
            .sort({ updatedAt: -1 })
            .skip(skip)
            .limit(limit)
            .lean(),

        Session.countDocuments({ user_id: userId }),
    ]);

    return {
        sessions,
        pagination: {
            page,
            limit,
            total,
            totalPages: Math.ceil(total / limit),
        },
    };
};

module.exports = {
    createSession,
    startAnalysis,
    getAnalysis,
    getSessions,
};