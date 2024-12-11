document.addEventListener("DOMContentLoaded", () => {
  const startQuestButton = document.getElementById("start-quest");
  const playerMoney = document.getElementById("player-money");
  const questDetails = document.getElementById("quest-details");

  let money = 0;
  let currentLocation = 1; // Starting airport ID

  // Fetch airport data
  async function fetchAirports() {
    try {
      const response = await fetch('/airports');
      if (!response.ok) throw new Error('Failed to fetch airports');
      const airports = await response.json();
      console.log('Available Airports:', airports);
    } catch (error) {
      console.error('Error fetching airports:', error.message);
    }
  }

  // Start a quest
  startQuestButton.addEventListener("click", async () => {
    try {
      const response = await fetch('/quests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ current_location: currentLocation })
      });
      const quest = await response.json();
      if (response.ok) {
        questDetails.textContent = quest.dialogue || "No active quest.";
        money += quest.reward || 0;
        playerMoney.textContent = `$${money}`;
      } else {
        questDetails.textContent = quest.message || "No quests available.";
      }
    } catch (error) {
      questDetails.textContent = "Error starting the quest.";
      console.error('Error:', error.message);
    }
  });

  // Add interval logic
  setInterval(() => {
    money += 10;
    playerMoney.textContent = `$${money}`;
  }, 3000);

  // Initial fetch
  fetchAirports();
});

