<template>
  <div class="about-page">
    <h2 class="team-title">Our Team:</h2>
    <ul class="team-list">
      <li>Steve Sajeev</li>
      <li>Kushagra Katiyar</li>
      <li>Swarith Chinta</li>
      <li>Sriram Yerramsetty</li>
    </ul>
  </div>
</template>

<style scoped>
  .about-page {
    padding: 2rem;
    width: 100vw;
    text-align: center;
  }

  .team-title {
    font-family: 'Irish Grover', cursive;
    color: #ffa500;
    text-shadow:
      -2px -2px 0 #000,
      -2px 2px 0 #000,
      2px -2px 0 #000,
      2px 2px 0 #000;
    font-size: 10rem;
    margin-bottom: 2rem;
  }

  .team-list {
    list-style-type: none;
    padding: 0;
  }

  .team-list li {
    font-family: 'Irish Grover', cursive;
    color: white;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000;
    font-size: 3rem;
    margin-bottom: 1rem;
  }
</style>
