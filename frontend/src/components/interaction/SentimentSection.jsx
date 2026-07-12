import { useDispatch, useSelector } from "react-redux";

import {
  updateInteractionField,
} from "../../store/interactionSlice";


function SentimentSection() {
  const dispatch = useDispatch();

  const sentiment = useSelector(
    (state) => state.interaction.sentiment
  );


  const updateSentiment = (value) => {
    dispatch(
      updateInteractionField({
        field: "sentiment",
        value,
      })
    );
  };


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
              onChange={() =>
                updateSentiment("Positive")
              }
            />

            <span>🙂 Positive</span>
          </label>


          <label className="sentiment-option">
            <input
              type="radio"
              name="sentiment"
              value="Neutral"
              checked={sentiment === "Neutral"}
              onChange={() =>
                updateSentiment("Neutral")
              }
            />

            <span>😐 Neutral</span>
          </label>


          <label className="sentiment-option">
            <input
              type="radio"
              name="sentiment"
              value="Negative"
              checked={sentiment === "Negative"}
              onChange={() =>
                updateSentiment("Negative")
              }
            />

            <span>☹️ Negative</span>
          </label>

        </div>
      </div>
    </div>
  );
}


export default SentimentSection;