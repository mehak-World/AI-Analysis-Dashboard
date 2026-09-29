const { uploadToS3, downloadFile, streamToString } = require("../../infrastructure/s3/index")
const { generateUploadKey } = require("../../infrastructure/s3/keys")

const uploadFile = async (user, file, sessionId) => {
    const fileBody = file.buffer;
    const mimetype = file.mimetype;
    const s3Key = generateUploadKey({userId: user.id, sessionId: sessionId, originalFilename: file.originalname})
    const res = await uploadToS3({key: s3Key, body: fileBody, contentType: mimetype})

    return {
        key: s3Key
    }
}

const getFile = async (key) => {
    const res = await downloadFile(key)
    const stringRes = await streamToString(res.Body)
    return stringRes
}

module.exports = {
    uploadFile,
    getFile
}