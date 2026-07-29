const Session = require("./model");

/**
 * Create analysis session
 */
const createSession = async ({ userId, s3Key, originalName }) => {
    return Session.create({
        user_id: userId,
        s3Key,
        originalName,

        status: "processing",
        currentStep: "eda",
        progress: 0,
    });
};

/**
 * Update profile (EDA)
 */
const updateProfile = async (sessionId, profile) => {
    return Session.findByIdAndUpdate(
        sessionId,
        {
            $set: {
                datasetProfile: {
                    rowCount: profile.rowCount,
                    columnCount: profile.columnCount,
                    columns: profile.columns,
                    dtypes: profile.dtypes,
                    nullPercents: profile.nullPercents,
                    duplicateRows: profile.duplicateRows,

                    datasetSizeMB: profile.datasetProfile?.datasetSizeMB,
                    numericColumns: profile.datasetProfile?.numericColumns,
                    categoricalColumns: profile.datasetProfile?.categoricalColumns,
                    datetimeColumns: profile.datasetProfile?.datetimeColumns,
                    booleanColumns: profile.datasetProfile?.booleanColumns,
                    missingValues: profile.datasetProfile?.missingValues,
                },

                sampleRows: profile.sampleRows,
                columnMetadata: profile.columnMetadata,
                numericSummary: profile.numericSummary,
                correlations: profile.correlations,
                nullCounts: profile.nullCounts,

                currentStep: "charts",
                progress: 30,
            },
        },
        {
            returnDocument: "after",
        }
    );
};

/**
 * Update generated charts
 */
const updateCharts = async (sessionId, charts) => {
    return Session.findByIdAndUpdate(
        sessionId,
        {
            $set: {
                summaryCharts: charts,

                currentStep: "ai",
                progress: 60,
            },
        },
        {
            new: true,
        }
    );
};

/**
 * Update AI insights
 */
const updateInsights = async (
    sessionId,
    {
        datasetSummary,
        statisticsExplanation,
        charts: aiCharts,
        correlations,
        recommendations,
    }
) => {
    const session = await Session.findById(sessionId);

    if (!session) {
        throw new Error("Session not found.");
    }

    session.datasetSummary = datasetSummary;
    session.statisticsExplanation = statisticsExplanation;
    session.recommendations = recommendations ?? [];

    // Merge correlation explanations
    if (Array.isArray(correlations)) {
        const correlationMap = new Map(
            correlations.map((item) => [
                `${item.columnA}:${item.columnB}`,
                item,
            ])
        );

        session.correlations = session.correlations.map((corr) => {
            const aiCorr =
                correlationMap.get(`${corr.columnA}:${corr.columnB}`) ||
                correlationMap.get(`${corr.columnB}:${corr.columnA}`);

            if (!aiCorr) {
                return corr;
            }

            corr.explanation = aiCorr.explanation;

            return corr;
        });
    }

    // Merge chart summaries
    if (Array.isArray(aiCharts)) {
        const chartMap = new Map(
            aiCharts.map((chart) => [chart.id, chart])
        );

        session.summaryCharts = session.summaryCharts.map((chart) => {
            const aiChart = chartMap.get(chart.id);

            if (!aiChart) {
                return chart;
            }

            chart.summary = aiChart.summary;
            chart.insight = aiChart.insight;

            return chart;
        });
    }

    session.currentStep = "completed";
    session.progress = 100;
    session.status = "ready";

    return session.save();
};

/**
 * Mark analysis as failed
 */
const markFailed = async (sessionId, error) => {
    return Session.findByIdAndUpdate(
        sessionId,
        {
            $set: {
                status: "error",
                error:
                    error?.message ||
                    "Unknown error occurred during analysis.",
            },
        },
        {
            new: true,
        }
    );
};

/**
 * Get analysis session
 */
const getSession = async (sessionId) => {
    return Session.findById(sessionId);
};


const getInsightsPayload = async (sessionId) => {
    const session = await Session.findById(sessionId).lean();

    if (!session) {
        throw new Error("Session not found");
    }

    return {
        datasetName: session.originalName,

        profile: {
            profile: session.datasetProfile,
            metadata: session.columnMetadata,
            correlations: session.correlations,
            statistics: session.numericSummary,
            nullCounts: session.nullCounts
        },

        charts: session.summaryCharts.map(chart => ({
            id: chart.id,
            name: chart.name,
            type: chart.type,
            reason: chart.reason,
            statistics: chart.statistics
        }))
    };
};


module.exports = {
    createSession,
    updateProfile,
    updateCharts,
    updateInsights,
    markFailed,
    getSession,
    getInsightsPayload
};