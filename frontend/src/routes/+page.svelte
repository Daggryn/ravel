<script>
  import { goto } from '$app/navigation';
  import { login } from '$lib/api.js';
  import { resolve } from '$app/paths';

  let username = '';
  let password = '';
  let error = '';
  let loading = false;

  async function handleSubmit() {
    error = '';
    loading = true;
    try {
      await login(username, password);
      await goto(resolve('/dashboard'));
    } catch {
      error = 'Invalid username or password';
    } finally {
      loading = false;
    }
  }
</script>

<main>
  <h1>Ravel</h1>
  <p class="tagline">Untangle together.</p>

  <form on:submit|preventDefault={handleSubmit}>
    <input
      type="text"
      placeholder="Your name"
      bind:value={username}
      required
    />
    <input
      type="password"
      placeholder="Password"
      bind:value={password}
      required
    />
    <button type="submit" disabled={loading}>
      {loading ? 'Stepping in…' : 'Enter'}
    </button>
    {#if error}
      <p class="error">{error}</p>
    {/if}
  </form>
</main>

<style>
  main {
    max-width: 320px;
    margin: 10vh auto;
    padding: 2rem;
    text-align: center;
    font-family: system-ui, sans-serif;
  }
  h1 {
    font-size: 2.5rem;
    margin: 0;
    letter-spacing: -0.02em;
  }
  .tagline {
    color: #666;
    margin: 0.25rem 0 2rem;
    font-style: italic;
  }
  form {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  input {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
  }
  button {
    padding: 0.75rem;
    background: #2c3e2d;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
  }
  button:disabled {
    opacity: 0.6;
  }
  .error {
    color: #c0392b;
    font-size: 0.9rem;
  }
</style>
