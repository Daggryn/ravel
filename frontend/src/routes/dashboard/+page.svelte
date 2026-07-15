<script>
  import { onMount } from 'svelte';
  import {
    getToken,
    logout,
    fetchMyTasks,
    fetchTheirTasks,
    createTask,
    claimTask,
    markDone
  } from '$lib/api.js';
  import { goto } from '$app/navigation';
import { resolve } from '$app/paths';

  let myTasks = $state([]);
  let theirTasks = $state([]);
  let newTask = $state('');
  let loading = $state(false);
  let currentUser = $state('');

  onMount(async () => {
    if (!getToken()) {
      await goto(resolve('/'));
      return;
    }
    await load();
  });

  async function load() {
    const token = getToken();
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      currentUser = payload.sub;
    }
    [myTasks, theirTasks] = await Promise.all([
      fetchMyTasks(),
      fetchTheirTasks()
    ]);
  }

  async function handleAdd() {
    if (!newTask.trim()) return;
    loading = true;
    try {
      await createTask(newTask);
      newTask = '';
      await load();
    } finally {
      loading = false;
    }
  }

  async function handleClaim(taskId) {
    await claimTask(taskId);
    await load();
  }

  async function handleDone(taskId) {
    await markDone(taskId);
    await load();
  }

  function handleLogout() {
    logout();
    goto(resolve('/'));
  }
</script>

<main>
  <header>
    <div>
      <h1>Ravel</h1>
      <p class="greeting">Hello, {currentUser.charAt(0).toUpperCase() + currentUser.slice(1)}!</p>
    </div>
    <button class="ghost" onclick={handleLogout}>Sign out</button>
  </header>

  <section class="capture">
    <input
      type="text"
      placeholder="What's on your mind?"
      bind:value={newTask}
      onkeydown={(e) => e.key === 'Enter' && handleAdd()}
    />
    <button onclick={handleAdd} disabled={loading}>
      {loading ? 'Adding…' : 'Add'}
    </button>
  </section>

  <div class="piles">
    <section class="pile">
      <h2>My pile</h2>
      {#if myTasks.length === 0}
        <p class="empty">Nothing here. Breathe.</p>
      {/if}
      {#each myTasks as task (task.id)}
        <div class="task">
          <span class="title">{task.title}</span>
          <button class="done" onclick={() => handleDone(task.id)}>
            Done
          </button>
        </div>
      {/each}
    </section>

    <section class="pile">
      <h2>Their pile</h2>
      {#if theirTasks.length === 0}
        <p class="empty">All clear on their end.</p>
      {/if}
      {#each theirTasks as task (task.id)}
        <div class="task">
          <span class="title">{task.title}</span>
          <button class="take" onclick={() => handleClaim(task.id)}>
            I've got this
          </button>
        </div>
      {/each}
    </section>
  </div>
</main>

<style>
  main {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
    font-family: system-ui, sans-serif;
    color: #2c3e2d;
  }
  header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 2rem;
  }
  h1 {
    font-size: 2rem;
    margin: 0;
    letter-spacing: -0.02em;
  }
  .greeting {
    color: #666;
    margin: 0.25rem 0 0;
    font-style: italic;
  }
  .ghost {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
  }
  .capture {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
  }
  .capture input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
  }
  .capture button {
    padding: 0.75rem 1.25rem;
    background: #2c3e2d;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  .piles {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
  @media (max-width: 600px) {
    .piles { grid-template-columns: 1fr; }
  }
  .pile h2 {
    font-size: 1.1rem;
    margin: 0 0 0.75rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .empty {
    color: #999;
    font-style: italic;
  }
  .task {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: #f7f5f1;
    border-radius: 8px;
    margin-bottom: 0.5rem;
  }
  .title { flex: 1; }
  .take {
    background: #2c3e2d;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.4rem 0.75rem;
    cursor: pointer;
    font-size: 0.9rem;
  }
  .done {
    background: none;
    border: 1px solid #2c3e2d;
    color: #2c3e2d;
    border-radius: 6px;
    padding: 0.4rem 0.75rem;
    cursor: pointer;
    font-size: 0.9rem;
  }
</style>
