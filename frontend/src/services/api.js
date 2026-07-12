import axios from "axios";


const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000",

  headers: {
    "Content-Type": "application/json",
  },
});


export const testInteraction = async (
  interactionData
) => {
  const response = await api.post(
    "/api/interactions/test",
    interactionData
  );

  return response.data;
};


export const sendChatMessage = async (
  message,
  interaction
) => {
  const response = await api.post(
    "/api/chat",
    {
      message,
      interaction,
      interaction_id:
        interaction.interaction_id,
    }
  );

  return response.data;
};


export const getLatestInteraction = async () => {
  const response = await api.get(
    "/api/interactions/latest"
  );

  return response.data;
};


export default api;