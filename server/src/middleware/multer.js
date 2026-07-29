const multer = require("multer");

const storage = multer.memoryStorage();

const fileFilter = (req, file, cb) => {

    if (
        file.mimetype === "text/csv" ||
        file.originalname.endsWith(".csv")
    ) {
        return cb(null, true);
    }

    cb(new Error("Only CSV files are allowed."));
};

const upload = multer({
    storage,

    limits: {
        fileSize: 50 * 1024 * 1024, // 50 MB
    },

    fileFilter,
});

module.exports = upload;