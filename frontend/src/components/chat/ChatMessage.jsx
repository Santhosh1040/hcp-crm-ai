function ChatMessage({
  type = "assistant",
  message,
}) {
  return (
    <div
      className={`chat-message ${type}`}
    >
      {message}
    </div>
  );
}


export default ChatMessage;