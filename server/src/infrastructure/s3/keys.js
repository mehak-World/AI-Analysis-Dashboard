const path = require("path");

function generateUploadKey({ userId, sessionId, originalFilename }) {
    const extension = path.extname(originalFilename);

    return `uploads/${userId}/${sessionId}${extension}`;
}

module.exports = {
    generateUploadKey,
};