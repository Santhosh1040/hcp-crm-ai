import { useSelector } from "react-redux";


function TopicsSection() {
  const topicsDiscussed = useSelector(
    (state) => state.interaction.topics_discussed
  );


  return (
    <div className="form-section">
      <div className="form-group">

        <label>Topics Discussed</label>

        <textarea
          rows="4"
          placeholder="Enter key discussion points..."
          value={topicsDiscussed || ""}
          readOnly
        />

        <button
          className="text-action"
          type="button"
          disabled
        >
          🎙 Summarize from Voice Note (Requires Consent)
        </button>

      </div>
    </div>
  );
}


export default TopicsSection;