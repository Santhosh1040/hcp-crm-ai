import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

import { setInteraction } from "../../store/interactionSlice";
import {
  getLatestInteraction,
  sendChatMessage,
} from "../../services/api";

import "../../styles/chat.css";


function AIAssistant() {
  const dispatch = useDispatch();

  // Current HCP interaction stored in Redux
  const interaction = useSelector(
    (state) => state.interaction
  );

  // Messages displayed in the chat panel
  const [messages, setMessages] = useState([]);

  // Prevent multiple requests while the AI is processing
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
  const loadLatestInteraction = async () => {
    try {
      const response = await getLatestInteraction();

      if (response.interaction) {
        dispatch(
          setInteraction({
            ...response.interaction,
            interaction_id: response.interaction_id,
          })
        );
      }
    } catch (error) {
      console.error(
        "Unable to load latest interaction:",
        error
      );
    }
  };

  loadLatestInteraction();
}, [dispatch]);


  const handleSendMessage = async (message) => {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || isLoading) {
      return;
    }

    // Immediately display the user's message
    setMessages((previousMessages) => [
      ...previousMessages,
      {
        type: "user",
        message: trimmedMessage,
      },
    ]);

    setIsLoading(true);

    try {
      // Send the user's message and current form state
      // to the FastAPI + LangGraph backend
      const response = await sendChatMessage(
        trimmedMessage,
        interaction
      );

      // Update Redux with both the interaction data
      // and the database interaction ID
      if (response.interaction) {
        dispatch(
          setInteraction({
            ...response.interaction,
            interaction_id: response.interaction_id,
          })
        );
      }

      // Display the backend response in the chat
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          type: "assistant",
          message:
            response.message ||
            "Request completed successfully.",
        },
      ]);

    } catch (error) {
      console.error(
        "Error communicating with AI assistant:",
        error
      );

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          type: "error",
          message:
            "Unable to process the request. Please try again.",
        },
      ]);

    } finally {
      setIsLoading(false);
    }
  };


  return (
    <aside className="ai-assistant">

      <div className="assistant-header">
        <h2>🤖 AI Assistant</h2>
        <p>Log Interaction details here via chat</p>
      </div>


      <div className="chat-messages">

        <ChatMessage
          type="info"
          message='Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.'
        />


        {messages.map((chatMessage, index) => (
          <ChatMessage
            key={index}
            type={chatMessage.type}
            message={chatMessage.message}
          />
        ))}


        {isLoading && (
          <ChatMessage
            type="assistant"
            message="Processing..."
          />
        )}

      </div>


      <ChatInput
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />

    </aside>
  );
}


export default AIAssistant;