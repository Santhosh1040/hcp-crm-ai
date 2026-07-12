import { useDispatch, useSelector } from "react-redux";

import {
  updateInteractionField,
} from "../../store/interactionSlice";


function TopicsSection() {
  const dispatch = useDispatch();

  const topicsDiscussed = useSelector(
    (state) => state.interaction.topics_discussed
  );


  const handleChange = (event) => {
    dispatch(
      updateInteractionField({
        field: "topics_discussed",
        value: event.target.value,
      })
    );
  };


  return (
    <div className="form-section">
      <div className="form-group">

        <label>Topics Discussed</label>

        <textarea
          rows="4"
          placeholder="Enter key discussion points..."
          value={topicsDiscussed || ""}
          onChange={handleChange}
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