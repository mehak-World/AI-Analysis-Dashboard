const uploadService = require("./service")

const uploadFile = async (req, res, next) => {
    try{
        if(!req.file){
            return res.json({
                message: "File not Found"
            })
        }
        const data = await uploadService.uploadFile(req.file)
        return res.json({
            data: data,
            message: "Successfully uploaded the file to S3"
        })
    }
    catch(err){
        return next(err)
    }
}

const getFile = async (req, res, next) => {
    try{
        const fileKey = req.query.key;
        if(!fileKey){
            return res.json({
                message: "File key not found"
            })
        }
        const data = await uploadService.getFile(fileKey);
        return res.json({
            data: data,
            message: "Successfully fetched the file from S3 using key"
        })
    }
    catch(err){
        return next(err)
    }
}

module.exports = {
    uploadFile,
    getFile
}