import { useSelector } from "react-redux";


function BasicDetails() {
  const interaction = useSelector(
    (state) => state.interaction
  );


  return (
    <div className="form-section">

      <div className="two-column-grid">

        <div className="form-group">
          <label>HCP Name</label>

          <input
            type="text"
            placeholder="Search or select HCP..."
            value={interaction.hcp_name || ""}
            readOnly
          />
        </div>


        <div className="form-group">
          <label>Interaction Type</label>

          <select
            value={
              interaction.interaction_type ||
              "Meeting"
            }
            disabled
          >
            <option value="Meeting">
              Meeting
            </option>

            <option value="Call">
              Call
            </option>

            <option value="Email">
              Email
            </option>

            <option value="Virtual Meeting">
              Virtual Meeting
            </option>
          </select>
        </div>


        <div className="form-group">
          <label>Date</label>

          <input
            type="date"
            value={
              interaction.interaction_date || ""
            }
            readOnly
          />
        </div>


        <div className="form-group">
          <label>Time</label>

          <input
            type="time"
            value={
              interaction.interaction_time || ""
            }
            readOnly
          />
        </div>

      </div>


      <div className="form-group">
        <label>Attendees</label>

        <input
          type="text"
          placeholder="Enter names or search..."
          value={
            (interaction.attendees || []).join(", ")
          }
          readOnly
        />
      </div>

    </div>
  );
}


export default BasicDetails;