import BasicDetails from "./BasicDetails";
import TopicsSection from "./TopicsSection";
import MaterialsSection from "./MaterialsSection";
import SentimentSection from "./SentimentSection";
import OutcomesSection from "./OutcomesSection";
import FollowUpSection from "./FollowUpSection";

import "../../styles/interaction.css";

function InteractionPanel() {
  return (
    <section className="interaction-panel">
      <h1>Log HCP Interaction</h1>

      <div className="interaction-content">
        <h2>Interaction Details</h2>

        <BasicDetails />
        <TopicsSection />
        <MaterialsSection />
        <SentimentSection />
        <OutcomesSection />
        <FollowUpSection />
      </div>
    </section>
  );
}

export default InteractionPanel;