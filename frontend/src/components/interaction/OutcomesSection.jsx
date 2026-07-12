import { useDispatch, useSelector } from "react-redux";

import {
  updateInteractionField,
} from "../../store/interactionSlice";


function OutcomesSection() {
  const dispatch = useDispatch();

  const outcomes = useSelector(
    (state) => state.interaction.outcomes
  );


  const handleChange = (event) => {
    dispatch(
      updateInteractionField({
        field: "outcomes",
        value: event.target.value,
      })
    );
  };


  return (
    <div className="form-section">
      <div className="form-group">

        <label>Outcomes</label>

        <textarea
          rows="4"
          placeholder="Key outcomes or agreements..."
          value={outcomes || ""}
          onChange={handleChange}
        />

      </div>
    </div>
  );
}


export default OutcomesSection;