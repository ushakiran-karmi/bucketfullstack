import { configureStore } from "@reduxjs/toolkit";
import bucketReducer from "./bucketslice"; // Import a reducer (see next step)

const store = configureStore({
  reducer: {
    bucket: bucketReducer, // At least one reducer is required
  },
});

export default store;
