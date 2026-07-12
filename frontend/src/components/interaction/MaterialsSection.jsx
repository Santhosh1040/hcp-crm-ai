import { useSelector } from "react-redux";

function MaterialsSection() {
  const materialsShared = useSelector(
    (state) => state.interaction.materials_shared
  );

  const samplesDistributed = useSelector(
    (state) => state.interaction.samples_distributed
  );

  return (
    <div className="form-section">
      <h3>Materials Shared / Samples Distributed</h3>

      <div className="item-block">
        <div className="item-header">
          <h4>Materials Shared</h4>

          <button type="button" className="secondary-button" disabled>
            🔍 Search/Add
          </button>
        </div>

        {materialsShared.length > 0 ? (
          <p>{materialsShared.join(", ")}</p>
        ) : (
          <p className="empty-state">No materials added.</p>
        )}
      </div>

      <div className="item-block">
        <div className="item-header">
          <h4>Samples Distributed</h4>

          <button type="button" className="secondary-button" disabled>
            ＋ Add Sample
          </button>
        </div>

        {samplesDistributed.length > 0 ? (
          <p>{samplesDistributed.join(", ")}</p>
        ) : (
          <p className="empty-state">No samples added.</p>
        )}
      </div>
    </div>
  );
}

export default MaterialsSection;