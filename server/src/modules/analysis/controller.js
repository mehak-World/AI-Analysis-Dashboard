const analysisService = require("./service");
const s3Service = require("../s3/service")

const handleUploadAndAnalyze = async (req, res, next) => {
    try{
        const {key} = await s3Service.uploadFile(req.file)

        if (!key) {
            return res.status(500).json({
                success: false,
                message: "Could not upload the file",
            });
        }

        console.log("user: ", req.user)
        const analysis = await analysisService.startAnalysis({
            userId: req.user.id,
            s3Key: key,
            originalName: req.file.originalname,
        });

        return res.status(202).json({
            success: true,
            message: "Analysis started successfully.",
            data: analysis,
        });
    }
    catch(err){
        return next(err)
    }
}


const getAnalysis = async (req, res, next) => {
    try {
        const { sessionId } = req.params;

        const session = await analysisService.getAnalysis(sessionId);

        return res.status(200).json({
            success: true,
            data: session,
        });
    } catch (err) {
        next(err);
    }
};

module.exports = {
    getAnalysis,
    handleUploadAndAnalyze
};