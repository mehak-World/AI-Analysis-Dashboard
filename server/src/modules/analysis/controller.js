const analysisService = require("./service");
const s3Service = require("../s3/service");

const handleUploadAndAnalyze = async (req, res, next) => {
    try {
        // 1. Create session first
        const session = await analysisService.createSession({
            userId: req.user.id,
            originalName: req.file.originalname,
        });

        // 2. Upload file using the session ID
        const { key } = await s3Service.uploadFile(
            req.user,
            req.file,
            session._id
        );

        if (!key) {
            return res.status(500).json({
                success: false,
                message: "Could not upload the file",
            });
        }

        // 3. Store the S3 key in the session
        session.s3Key = key;
        await session.save();

        // 4. Queue EDA
        await analysisService.startAnalysis({
            sessionId: session._id,
            userId: req.user.id,
            s3Key: key,
        });

        return res.status(202).json({
            success: true,
            message: "Analysis started successfully.",
            data: {
                sessionId: session._id,
                originalName: session.originalName,
                status: session.status,
                currentStep: session.currentStep,
                progress: session.progress,
                createdAt: session.createdAt,
                updatedAt: session.updatedAt,
            },
        });

    } catch (err) {
        return next(err);
    }
};

const getAnalysis = async (req, res, next) => {
  try {
    const { sessionId } = req.params;

    const session = await analysisService.getAnalysis(
        req.params.sessionId,
        req.user.id
    );

    return res.status(200).json({
      success: true,
      data: session,
    });
  } catch (err) {
    next(err);
  }
};

const getAllSessions = async (req, res, next) => {
  try {
    const page = Number(req.query.page) || 1;
    const limit = Number(req.query.limit) || 20;

    const result = await analysisService.getSessions(req.user.id, page, limit);

    return res.json({
      success: true,
      data: result.sessions,
      pagination: result.pagination,
    });
  } catch (err) {
    next(err);
  }
};

module.exports = {
  getAnalysis,
  handleUploadAndAnalyze,
  getAllSessions
};
