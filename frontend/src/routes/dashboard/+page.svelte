<script>
  import { onMount } from 'svelte';
  import { getToken, logout } from '$lib/api.js';
  import { goto } from '$app/navigation';
  import { resolve } from '$app/paths';

  onMount(async () => {
    if (!getToken()) await goto(resolve('/'));
  });

  function handleLogout() {
    logout();
    goto(resolve('/'));
  }
</script>

<main>
  <h1>Welcome in</h1>
  <button on:click={handleLogout}>Sign out</button>
</main>
