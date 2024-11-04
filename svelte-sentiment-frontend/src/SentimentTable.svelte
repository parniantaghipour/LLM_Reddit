<script>
    import { onMount } from "svelte";
  
    let sentimentData = [];
    let error = "";
  
    // Fetch data from the FastAPI endpoint
    async function fetchSentimentData() {
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
      }
    }
  
    onMount(fetchSentimentData);
  </script>
  
  <style>
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    th, td {
      padding: 8px;
      border: 1px solid #ddd;
      text-align: left;
    }
  </style>
  
  <h1>Model Sentiment Analysis</h1>
  {#if error}
    <p>{error}</p>
  {:else}
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
  {/if}
  