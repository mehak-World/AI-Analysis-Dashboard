// const path = require("path");
// const dotenv = require("dotenv");
// const fs = require("fs");

// const environment = process.env.NODE_ENV || "development";

// const envPath = path.resolve(__dirname, "..", ".envs", `.env.${environment}`);

// if (!fs.existsSync(envPath)) {
//     throw new Error(`Environment file not found: ${envPath}`);
// }

// dotenv.config({ path: envPath });

// module.exports = {
//     NODE_ENV: environment,

//     PORT: process.env.PORT,
    
//     JWT_SECRET: process.env.JWT_SECRET,

//     MONGO_URL: process.env.MONGO_URL,

//     AWS_REGION: process.env.AWS_REGION,

//     AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID,

//     AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY,

//     S3_BUCKET_NAME: process.env.S3_BUCKET_NAME,

//     REDIS_HOST: process.env.REDIS_HOST,
//     REDIS_PORT: process.env.REDIS_PORT,
//     REDIS_USERNAME: process.env.REDIS_USERNAME,
//     REDIS_PASSWORD: process.env.REDIS_PASSWORD,
//     REDIS_DB: process.env.REDIS_DB,

//     PYTHON_SERVICE_URL: process.env.PYTHON_SERVICE_URL
// };

require("dotenv").config();

module.exports = {
    NODE_ENV: process.env.NODE_ENV || "development",

    PORT: process.env.PORT,

    JWT_SECRET: process.env.JWT_SECRET,

    MONGO_URL: process.env.MONGO_URL,

    AWS_REGION: process.env.AWS_REGION,
    AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY,
    S3_BUCKET_NAME: process.env.S3_BUCKET_NAME,

    REDIS_HOST: process.env.REDIS_HOST,
    REDIS_PORT: process.env.REDIS_PORT,
    REDIS_USERNAME: process.env.REDIS_USERNAME,
    REDIS_PASSWORD: process.env.REDIS_PASSWORD,
    REDIS_DB: process.env.REDIS_DB,

    PYTHON_SERVICE_URL: process.env.PYTHON_SERVICE_URL,
};