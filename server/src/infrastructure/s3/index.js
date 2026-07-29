const {
    PutObjectCommand,
    GetObjectCommand,
    DeleteObjectCommand,
    HeadObjectCommand,
} = require("@aws-sdk/client-s3");

const { getSignedUrl } = require("@aws-sdk/s3-request-presigner");

const { s3, env } = require("../../config");

async function uploadToS3({
    key,
    body,
    contentType,
}) {
    const command = new PutObjectCommand({
        Bucket: env.S3_BUCKET_NAME,
        Key: key,
        Body: body,
        ContentType: contentType,
    });

    await s3.send(command);

    return key;
}

async function downloadFile(key) {
    const command = new GetObjectCommand({
        Bucket: env.S3_BUCKET_NAME,
        Key: key,
    });

    return s3.send(command);
}


async function deleteFile(key) {
    const command = new DeleteObjectCommand({
        Bucket: env.S3_BUCKET_NAME,
        Key: key,
    });

    await s3.send(command);
}

async function fileExists(key) {
    try {

        await s3.send(
            new HeadObjectCommand({
                Bucket: env.S3_BUCKET_NAME,
                Key: key,
            })
        );

        return true;

    } catch {

        return false;

    }
}

async function generatePresignedUrl(
    key,
    expiresIn = 300
) {
    const command = new GetObjectCommand({
        Bucket: env.S3_BUCKET_NAME,
        Key: key,
    });

    return getSignedUrl(
        s3,
        command,
        { expiresIn }
    );
}

async function streamToBuffer(stream) {
    const chunks = [];

    for await (const chunk of stream) {
        chunks.push(chunk);
    }

    return Buffer.concat(chunks);
}

async function streamToString(stream) {
    const chunks = [];

    for await (const chunk of stream) {
        chunks.push(chunk);
    }

    return Buffer.concat(chunks).toString("utf8");
}

module.exports = {
    uploadToS3,
    downloadFile,
    fileExists,
    deleteFile,
    streamToBuffer,
    streamToString
}