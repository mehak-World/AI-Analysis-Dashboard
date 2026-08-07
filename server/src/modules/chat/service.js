const Session = require("../analysis/model");
const pythonClient = require("../../config/pythonClient");

const buildPlannerContext = (session, question) => {
  return {
    question,
    s3_key: session.s3Key,

    dataset_name: session.originalName,

    dataset_profile: session.datasetProfile,

    column_metadata: session.columnMetadata,

    dataset_summary: session.datasetSummary,

    correlations: session.correlations,

    existing_charts: (session.summaryCharts || []).map((chart) => ({
      id: chart.id,
      name: chart.name,
      type: chart.type,
      xKey: chart.config?.xKey,
      yKey: chart.config?.yKey,
      summary: chart.summary,
      insight: chart.insight,
    })),
  };
};

const chat = async ({
  sessionId,
  userId,
  question,
}) => {
  const session = await Session.findOne({
    _id: sessionId,
    user_id: userId,
  }).lean();

  if (!session) {
    throw new Error("Analysis session not found.");
  }

  const plannerContext = buildPlannerContext(
    session,
    question
  );

  const { data } = await pythonClient.post(
    "/chat/plan",
    plannerContext
  );

  return data;
};

module.exports = {
  chat,
};