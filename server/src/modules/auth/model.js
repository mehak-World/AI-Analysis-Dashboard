const mongoose = require("mongoose");

// Create the user schema
const userSchema = new mongoose.Schema(
  {
    username: {
      type: String,
      required: true,
      trim: true,
    },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
    },
    password: {
      type: String,
      required: true,
      minlength: 6,
    },
  },
  {
    timestamps: true,
  }
);

userSchema.pre("save", function () {
  if (this.isModified("email")) {
    this.email = this.email.toLowerCase().trim();
  }

  if (this.isModified("username")) {
    this.username = this.username.trim();
  }
});

module.exports = mongoose.model("User", userSchema);
