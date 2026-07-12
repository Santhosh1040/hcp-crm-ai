import { useState } from "react";


function ChatInput({
  onSendMessage,
  isLoading,
}) {
  const [message, setMessage] = useState("");


  const handleSubmit = () => {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || isLoading) {
      return;
    }

    onSendMessage(trimmedMessage);

    // Clear the input after sending
    setMessage("");
  };


  const handleKeyDown = (event) => {
    // Enter sends the message
    // Shift + Enter creates a new line
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      handleSubmit();
    }
  };


  return (
    <div className="chat-input-area">

      <textarea
        rows="2"
        placeholder="Describe interaction..."
        value={message}
        onChange={(event) =>
          setMessage(event.target.value)
        }
        onKeyDown={handleKeyDown}
        disabled={isLoading}
      />


      <button
        type="button"
        className="log-button"
        onClick={handleSubmit}
        disabled={
          isLoading ||
          !message.trim()
        }
      >
        {isLoading ? "..." : "Log"}
      </button>

    </div>
  );
}


export default ChatInput;