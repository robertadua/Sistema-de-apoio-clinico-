const mongoose = require("mongoose");

const connectDB = async() => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log("Mongo conectado 🟢");
  } catch (error) {
    console.log("Erro no Mongo 🔴", error);
  }
};

module.exports = connectDB;

