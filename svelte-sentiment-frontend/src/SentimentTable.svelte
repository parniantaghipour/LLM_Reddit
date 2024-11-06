<script>
  import { onMount } from "svelte";

  let sentimentData = [];
  let error = "";
  let loading = true;
  let isDarkMode = false;

  // Fetch data from the FastAPI endpoint
  async function fetchSentimentData() {
      loading = true;
      error = "";
      try {
          const res = await fetch("http://127.0.0.1:8000/model_sentiment");
          const data = await res.json();
          if (data.status === "success") {
              sentimentData = data.data;
          } else {
              error = data.message;
          }
      } catch (err) {
          error = "Error fetching data.";
          console.error(err);
      } finally {
          loading = false;
      }
  }

  // Toggle dark mode
  function toggleDarkMode() {
      isDarkMode = !isDarkMode;
  }

  onMount(fetchSentimentData);
</script>

<style>
  :root {
      --background-color: #f5f5f5; /* Off-white background */
      --text-color: #333;
      --heading-color: #4a90e2;
      --table-border: #ccc;
      --row-hover: #e6e6e6;
      --table-header-background: #e6e6e6;
  }

  /* Dark mode variables */
  .dark-mode {
      --background-color: #1e1e1e;
      --text-color: #e0e0e0;
      --heading-color: #76baff;
      --table-border: #444;
      --row-hover: #333;
      --table-header-background: #444;
  }

  /* Container styling */
  .container {
      max-width: 800px;
      margin: 20px auto;
      padding: 20px;
      font-family: Arial, sans-serif;
      color: var(--text-color);
      background-color: var(--background-color);
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  h1 {
      text-align: center;
      color: var(--heading-color);
  }

  /* Table styling */
  .table-container {
      overflow-x: auto;
      margin-top: 20px;
  }

  table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
  }

  th, td {
      padding: 12px;
      border-bottom: 1px solid var(--table-border);
      text-align: left;
  }

  th {
      background-color: var(--table-header-background);
      font-weight: bold;
  }

  tr:hover {
      background-color: var(--row-hover);
  }

  /* Loading and error message styling */
  .loading, .error-message {
      text-align: center;
      color: #888;
      font-size: 1.1em;
  }

  /* Retry button styling */
  .retry-button {
      background-color: #4a90e2;
      color: white;
      padding: 8px 12px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
  }

  .retry-button:hover {
      background-color: #357ABD;
  }

  /* Dark mode toggle button */
  .dark-mode-toggle {
      display: flex;
      justify-content: flex-end;
      margin-bottom: 15px;
  }

  .toggle-button {
      background-color: #333;
      color: white;
      padding: 6px 10px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
  }

  .toggle-button:hover {
      background-color: #555;
  }
</style>

<div class:dark-mode={isDarkMode}>
  <div class="container">
      <div class="dark-mode-toggle">
          <button class="toggle-button" on:click={toggleDarkMode}>
              {isDarkMode ? 'Switch to Day Mode' : 'Switch to Dark Mode'}
          </button>
      </div>
      <h1>Model Sentiment Analysis</h1>

      {#if loading}
          <p class="loading">Loading data, please wait...</p>
      {:else if error}
          <p class="error-message">{error}</p>
          <button class="retry-button" on:click={fetchSentimentData}>Retry</button>
      {:else}
          <div class="table-container">
              <table>
                  <thead>
                      <tr>
                          <th>Model</th>
                          <th>Mentions</th>
                          <th>Average Sentiment</th>
                      </tr>
                  </thead>
                  <tbody>
                      {#each sentimentData as item}
                          <tr>
                              <td>{item.Model}</td>
                              <td>{item.Mentions}</td>
                              <td>{item['Average Sentiment'].toFixed(2)}</td>
                          </tr>
                      {/each}
                  </tbody>
              </table>
          </div>
      {/if}
  </div>
</div>
