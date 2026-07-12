import { useDispatch, useSelector } from "react-redux";

import {
  updateInteractionField,
} from "../../store/interactionSlice";


function BasicDetails() {
  const dispatch = useDispatch();

  const interaction = useSelector(
    (state) => state.interaction
  );


  const updateField = (field, value) => {
    dispatch(
      updateInteractionField({
        field,
        value,
      })
    );
  };


  return (
    <div className="form-section">

      <div className="two-column-grid">

        <div className="form-group">
          <label>HCP Name</label>

          <input
            type="text"
            placeholder="Search or select HCP..."
            value={interaction.hcp_name || ""}
            onChange={(event) =>
              updateField(
                "hcp_name",
                event.target.value
              )
            }
          />
        </div>


        <div className="form-group">
          <label>Interaction Type</label>

          <select
            value={
              interaction.interaction_type ||
              "Meeting"
            }
            onChange={(event) =>
              updateField(
                "interaction_type",
                event.target.value
              )
            }
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
            onChange={(event) =>
              updateField(
                "interaction_date",
                event.target.value
              )
            }
          />
        </div>


        <div className="form-group">
          <label>Time</label>

          <input
            type="time"
            value={
              interaction.interaction_time || ""
            }
            onChange={(event) =>
              updateField(
                "interaction_time",
                event.target.value
              )
            }
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
          onChange={(event) =>
            updateField(
              "attendees",
              event.target.value
                .split(",")
                .map((name) => name.trim())
                .filter(Boolean)
            )
          }
        />
      </div>

    </div>
  );
}


export default BasicDetails;