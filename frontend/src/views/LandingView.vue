<template>
  <main class="landing-page-content">
    <div class="content-wrapper">
      <div class="header-section">
        <h1><span class="orange-text">Orange</span> and <span class="blue-text">Blue</span> Collar</h1>
        <p class="subtitle">University of Florida's #1 internship board and networking site!</p>
      </div>

      <div class="main-content">
        <div class="left-section">
          <div class="button-section">
            <p class="button-description">Find the most recent internships in tech!</p>
            <router-link to="/internships" class="cta-button"> View Internships </router-link>
          </div>
        </div>

        <div class="right-section">
          <img src="@/assets/ConnectingGatorTransparentOutlined.png" alt="Connecting Gators" class="landing-image" />
        </div>
      </div>
    </div>
  </main>
</template>

<script lang="ts" setup>

</script>

<style scoped>
  .landing-page-content {
    padding: 2rem;
    width: 100vw;
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: 1rem;
  }

  .content-wrapper {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    margin-top: 1rem;
  }

  .header-section {
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
  }

  h1 {
    font-family: 'Irish Grover', cursive;
    text-shadow:
      -2px -2px 0 #000,
      -2px 2px 0 #000,
      2px -2px 0 #000,
      2px 2px 0 #000,
      -2px 0 0 #000,
      2px 0 0 #000,
      0 2px 0 #000,
      0 -2px 0 #000,
      2px 2px 4px rgba(0, 0, 0, 0.5);
    margin-bottom: 1rem;
    font-size: clamp(3rem, 8vw, 8rem);
    color: white;
    line-height: 1.1;
  }

  .subtitle {
    font-size: clamp(1.2rem, 3vw, 2rem);
    color: white;
    margin-bottom: 1rem;
    font-weight: bold;
    font-family: 'Irish Grover', cursive;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
    display: inline-block;
    max-width: none;
    white-space: nowrap; 
    width: 100%;
  }

  .main-content {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 2rem;
    flex-wrap: wrap;
    margin-top: 0;
  }

  .left-section {
    flex: 1;
    min-width: 300px;
    display: flex;
    justify-content: center;
    margin-top: 8rem;
  }

  .button-section {
    text-align: center;
    width: 1500px;
    margin-top: 0;
  }

  .button-description {
    color: white;
    font-size: clamp(3rem, 4vw, 4rem);
    margin-bottom: 1.5rem;
    font-family: 'Irish Grover', cursive;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
    line-height: 1.3;
    word-wrap: break-word;
  }

  .cta-button {
    display: inline-block;
    padding: 1rem 2rem;
    background-color: #f09d05;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-size: clamp(1.2rem, 2vw, 1.5rem);
    transition: background-color 0.3s ease;
    font-family: 'Irish Grover', cursive;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
    width: 610px;
  }

  .cta-button:hover {
    background-color: #bf7c02;
  }

  .right-section {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-width: 300px;
    margin-top: 4rem;
  }

  .landing-image {
    max-width: 100%;
    height: auto;
    max-height: 500px;
    border-radius: 10px;
    object-fit: cover;
  }

  .orange-text {
    color: #ffa500;
  }

  .blue-text {
    color: #1e90ff;
  }

 
  @media (max-width: 768px) {
    .landing-page-content {
      padding: 1rem;
      padding-top: 0.5rem;
    }

    .content-wrapper {
      margin-top: 0.5rem;
    }

    .subtitle {
      white-space: normal;
      font-size: clamp(1rem, 3vw, 1.5rem);
    }

    .main-content {
      flex-direction: column;
      gap: 2rem;
    }

    .button-section {
      max-width: 100%;
    }

    .cta-button {
      width: 100%;
      max-width: 300px;
    }

    .button-description {
      font-size: clamp(2rem, 4vw, 2.5rem);
    }
  }
</style>
