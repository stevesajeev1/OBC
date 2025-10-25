<template>
  <div class="app-container">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo-container">
        <router-link to="/">
          <img src="@/assets/ZoomedTransparentGator.png" alt="Logo" class="logo" />
        </router-link>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/team" class="nav-link">Our Team</router-link>
        <router-link to="/login" class="nav-link join-now">Login</router-link>
        <router-link to="/join" class="nav-link join-now">Join Now</router-link>
      </div>
    </nav>

    <!-- Routed Views Render Here -->
    <router-view />
  </div>
</template>

<script lang="ts" setup>
  // No logic needed here
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Irish+Grover&display=swap');

  /* Override job listings font separately */
  .job-listings,
  .job-listings * {
    font-family: Verdana;
  }

  /* Reset and base layout */
  html,
  body,
  #app {
    min-height: 100vh;
    width: 100%;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(to bottom, #5a7caf, rgba(255, 255, 255, 0)), white;
    box-sizing: border-box;
    color: black;
  }

  /* Inherit box-sizing globally */
  *,
  *::before,
  *::after {
    box-sizing: inherit;
  }

  /* Page wrapper */
  .app-container {
    min-height: 100vh;
    width: 100%;
    color: black;
    padding-top: 0px; /* space for fixed navbar */
  }

  /* Navbar — base background is blue, gradient fades in on hover */
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 100px;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    background-color: #5a7caf;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
    position: relative;
  }

  /* Gradient overlay */
  .navbar::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, #d4862d, #5a7caf);
    opacity: 0;
    transition: opacity 0.6s ease;
    z-index: -1;
  }

  /* On hover, reveal gradient */
  .navbar:hover::before {
    opacity: 1;
  }

  /* Logo container */
  .logo-container {
    display: flex;
    align-items: center;
    height: 100%;
  }

  /* Logo image */
  .logo {
    height: 160px;
    width: auto;
    object-fit: contain;
  }

  /* Nav links container */
  .nav-links {
    display: flex;
    gap: 2rem;
    align-items: center;
    user-select: none;
  }

  /* Navbar links */
  .nav-link {
    font-family: 'Irish Grover', cursive;
    text-shadow:
      -2px -2px 0 #000,
      2px -2px 0 #000,
      -2px 2px 0 #000,
      2px 2px 0 #000;
    color: white;
    text-decoration: none;
    font-weight: bold;
    transition: opacity 0.3s ease;
    display: flex;
    align-items: center;
    height: 100%;
    font-size: 1.5rem;
    user-select: none;
  }

  .nav-link:hover {
    opacity: 0.8;
  }

  /* "Join Now" and "Login" button style */
  .join-now {
    padding: 0.3rem 0.8rem;
    border-radius: 5px;
    transition: color 0.3s ease;
  }

  .join-now:hover {
    color: #d4862d;
  }

  .nav-link:hover,
  .nav-link:focus,
  .nav-link:active {
    background: none !important;
    outline: none !important;
    box-shadow: none !important;
  }

  .logo-container a:hover,
  .logo-container a:focus,
  .logo-container a:active {
    background: none !important;
    outline: none !important;
    box-shadow: none !important;
  }
</style>
