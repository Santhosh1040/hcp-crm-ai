import { useDispatch, useSelector } from "react-redux";

import {
  updateInteractionField,
} from "../../store/interactionSlice";


function FollowUpSection() {
  const dispatch = useDispatch();

  const followUpActions = useSelector(
    (state) => state.interaction.follow_up_actions
  );

  const aiSuggestedFollowUps = useSelector(
    (state) =>
      state.interaction.ai_suggested_follow_ups
  );


  const handleFollowUpChange = (event) => {
    const actions = event.target.value
      .split("\n");

    dispatch(
      updateInteractionField({
        field: "follow_up_actions",
        value: actions,
      })
    );
  };


  return (
    <div className="form-section">

      <div className="form-group">

        <label>Follow-up Actions</label>

        <textarea
          rows="4"
          placeholder="Enter next steps or tasks..."
          value={(followUpActions || []).join("\n")}
          onChange={handleFollowUpChange}
        />

      </div>


      <div className="ai-suggestions">

        <h4>AI Suggested Follow-ups</h4>

        {aiSuggestedFollowUps.length > 0 ? (
          <ul>
            {aiSuggestedFollowUps.map(
              (suggestion, index) => (
                <li key={index}>
                  {suggestion}
                </li>
              )
            )}
          </ul>
        ) : (
          <p>No suggestions yet.</p>
        )}

      </div>

    </div>
  );
}


export default FollowUpSection;