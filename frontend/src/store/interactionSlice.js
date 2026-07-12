import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  interaction_id: null,
  hcp_name: "",
  interaction_type: "Meeting",
  interaction_date: "",
  interaction_time: "",
  attendees: [],
  topics_discussed: "",
  materials_shared: [],
  samples_distributed: [],
  sentiment: null,
  outcomes: "",
  follow_up_actions: [],
  ai_suggested_follow_ups: [],
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    // Replace/update the interaction using data returned by the AI
    setInteraction: (state, action) => {
      return {
        ...state,
        ...action.payload,
      };
    },

    // Update one individual field
    updateInteractionField: (state, action) => {
      const { field, value } = action.payload;
      state[field] = value;
    },

    // Clear the entire interaction form
    resetInteraction: () => initialState,
  },
});

export const {
  setInteraction,
  updateInteractionField,
  resetInteraction,
} = interactionSlice.actions;

export default interactionSlice.reducer;