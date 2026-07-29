const mongoose = require("mongoose");

const chartSchema = new mongoose.Schema(
  {
    id: {
        type: String,
        required: true,
    },
    name: { type: String, required: true },
    type: { type: String, required: true },
    reason: { type: String, default: "" },
    config: { type: mongoose.Schema.Types.Mixed, default: {} },
    data: { type: [mongoose.Schema.Types.Mixed], default: [] },

    // These were OUTSIDE the schema object before — now correctly inside
    xAxis: {
      label: { type: String, default: "" },
      unit: { type: String, default: "" },
    },
    yAxis: {
      label: { type: String, default: "" },
      unit: { type: String, default: "" },
    },
    summary: { type: String, default: "" },
    insight: { type: String, default: "" },
    statistics: {
      type: Map,
      of: mongoose.Schema.Types.Mixed,
      default: {},
    },
  },
  { _id: false },
);

const columnMetadataSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },
    dtype: String,
    unit: {
      type: String,
      default: "",
    },
    description: {
      type: String,
      default: "",
    },
    category: {
      type: String,
      enum: ["numeric", "categorical", "datetime", "boolean"],
    },
    exampleValues: {
      type: [String],
      default: [],
    },
  },
  { _id: false },
);

const conversationSchema = new mongoose.Schema(
  {
    question: {
      type: String,
      required: true,
    },

    intent: {
      type: String,
      enum: ["eda", "prediction", "general", "visualization", "filter"],
      default: "general",
    },

    answer: String,

    charts: {
      type: [chartSchema],
      default: [],
    },

    metrics: {
      type: Map,
      of: mongoose.Schema.Types.Mixed,
      default: {},
    },

    modelUsed: String,

    modelScore: {
      type: Map,
      of: mongoose.Schema.Types.Mixed,
      default: {},
    },

    predictions: {
      type: mongoose.Schema.Types.Mixed,
      default: [],
    },

    createdAt: {
      type: Date,
      default: Date.now,
    },
  },
  { _id: false },
);


const SessionSchema = new mongoose.Schema({
    user_id: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true,
    },

    originalName: String,
    s3Key: String,

    datasetProfile: {
    rowCount: Number,
    columnCount: Number,

    columns: {
        type: [String],
        default: [],
    },

    dtypes: {
        type: Map,
        of: String,
        default: {},
    },

    nullPercents: {
        type: Map,
        of: Number,
        default: {},
    },

    duplicateRows: Number,

    datasetSizeMB: Number,
    numericColumns: Number,
    categoricalColumns: Number,
    datetimeColumns: Number,
    booleanColumns: Number,
    missingValues: Number,
},

    datasetSummary: {
      overview: String,
      keyFindings: {
        type: [String],
        default: [],
      },
      businessSummary: String,
      recommendedQuestions: {
        type: [String],
        default: [],
      },
    },

    recommendations: {
      type: [String],
      default: []
    },

    sampleRows: {
      type: [mongoose.Schema.Types.Mixed],
      default: [],
    },

    columnMetadata: {
      type: [columnMetadataSchema],
      default: [],
    },

    statisticsExplanation: {
      type: Map,
      of: String,
      default: {},
    },

    nullCounts: {
      type: Map,
      of: Number,
      default: {},
    },

    numericSummary: {},

    summaryCharts: {
      type: [chartSchema],
      default: [],
    },

    correlations: [
      {
        columnA: String,
        columnB: String,
        value: Number,
        explanation: String,
      },
    ],

    status: {
      type: String,
      enum: ["processing", "ready", "error"],
      default: "processing",
    },

currentStep: {
    type: String,
    enum: [
        "eda",
        "charts",
        "ai",
        "completed"
    ],
    default: "eda"
},

progress: {
    type: Number,
    default: 0
},

error: {
    type: String,
    default: "",
},

    // AI conversations
    conversations: {
      type: [conversationSchema],
      default: [],
    },
}, {
    timestamps: true
})

module.exports = mongoose.model('Session', SessionSchema)