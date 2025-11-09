<template>
  <div class="app-container">
    <nav class="navbar">
      <div class="logo-container">
        <router-link to="/">
          <img src="@/assets/ZoomedTransparentGator.png" alt="Logo" class="logo" />
        </router-link>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/internships" class="nav-link">Internships</router-link>
        <router-link to="/team" class="nav-link">About</router-link>
        <router-link to="/login" class="nav-link join-now">Login</router-link>
        <router-link to="/join" class="nav-link join-now">Register</router-link>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts" setup></script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Irish+Grover&display=swap');

  .job-listings,
  .job-listings * {
    font-family: Verdana;
  }

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

  *,
  *::before,
  *::after {
    box-sizing: inherit;
  }

  .app-container {
    min-height: 100vh;
    width: 100%;
    color: black;
    padding-top: 0px;
  }

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
    padding: 2rem;
    background-color: #5a7caf;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
    position: relative;
  }

  .navbar::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, #d4862d 0.01%, #5a7caf 29.33%);
    opacity: 0;
    transition: opacity 0.6s ease;
    z-index: -1;
  }

  .navbar:hover::before {
    opacity: 1;
  }

  .logo-container {
    display: flex;
    align-items: center;
    height: 100%;
  }

  .logo {
    height: 160px;
    width: auto;
    object-fit: contain;
  }

  .nav-links {
    display: flex;
    gap: 2rem;
    align-items: center;
    user-select: none;
  }

  .nav-link {
    font-family: 'Irish Grover', cursive;
    text-shadow:
      -1px -1px 0 #000,
      1px -1px 0 #000,
      -1px 1px 0 #000,
      1px 1px 0 #000;
    color: white;
    text-decoration: none;
    font-weight: bold;
    transition: opacity 0.3s ease;
    display: flex;
    align-items: center;
    height: 100%;
    font-size: 1.5rem;
    user-select: none;
    position: relative;
  }

  .nav-link:hover {
    opacity: 0.8;
  }

  .join-now {
    padding: 0.3rem 0.8rem;
    border-radius: 5px;
    transition:
      border-color 0.3s ease,
      color 0.3s ease;
    border: 2px solid #69a1b8;
    background-color: transparent;
  }

  .join-now:hover {
    color: #d4862d;
    border-color: #d4862d;
  }

  .nav-link:not(.join-now).router-link-active::after {
    content: '';
    position: absolute;
    top: 37px;
    left: 50%;
    width: 100%;
    height: 2px;
    background: white;
    transform: translateX(-50%) scaleX(0);
    animation: underlineGrow 0.3s ease-out forwards;
    box-shadow:
      -1px -1px 0 #000,
      1px -1px 0 #000,
      -1px 1px 0 #000,
      1px 1px 0 #000;
  }

  .join-now.router-link-active {
    color: #d4862d !important;
    border-color: #d4862d !important;
    background-color: rgba(212, 134, 45, 0.1) !important;
  }

  @keyframes underlineGrow {
    from {
      transform: translateX(-50%) scaleX(0);
    }

    to {
      transform: translateX(-50%) scaleX(1);
    }
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
