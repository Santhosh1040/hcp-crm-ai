import { useSelector } from "react-redux";


function OutcomesSection() {
  const outcomes = useSelector(
    (state) => state.interaction.outcomes
  );


  return (
    <div className="form-section">
      <div className="form-group">

        <label>Outcomes</label>

        <textarea
          rows="4"
          placeholder="Key outcomes or agreements..."
          value={outcomes || ""}
          readOnly
        />

      </div>
    </div>
  );
}


export default OutcomesSection;