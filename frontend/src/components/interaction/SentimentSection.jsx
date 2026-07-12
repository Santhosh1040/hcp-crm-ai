import { useSelector } from "react-redux";


function SentimentSection() {
  const sentiment = useSelector(
    (state) => state.interaction.sentiment
  );


  return (
    <div className="form-section">
      <div className="form-group">

        <label>
          Observed/Inferred HCP Sentiment
        </label>

        <div className="sentiment-options">

          <label className="sentiment-option">
            <input
              type="radio"
              name="sentiment"
              value="Positive"
              checked={sentiment === "Positive"}
              readOnly
            />

            <span>🙂 Positive</span>
          </label>


          <label className="sentiment-option">
            <input
              type="radio"
              name="sentiment"
              value="Neutral"
              checked={sentiment === "Neutral"}
              readOnly
            />

            <span>😐 Neutral</span>
          </label>


          <label className="sentiment-option">
            <input
              type="radio"
              name="sentiment"
              value="Negative"
              checked={sentiment === "Negative"}
              readOnly
            />

            <span>☹️ Negative</span>
          </label>

        </div>
      </div>
    </div>
  );
}


export default SentimentSection;