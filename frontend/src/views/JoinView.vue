<script setup lang="ts">
  import { register } from '@/api/auth';
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  const username = ref<string>('');
  const password = ref<string>('');

  const goBack = () => {
    router.back();
  };

  const handleRegister = async () => {
    const response = await register(username.value, password.value);

    if (response.success) {
      router.push({ name: 'home' });
    } else {
      alert(`Join failed: ${response.message}`);
    }
  };
</script>
<template>
  <div id="login-page">
    <div id="login-card">
      <button id="back-button" @click="goBack">&#9664;</button>

      <div id="card-content">
        <div id="image-area">
          <img src="@/assets/Color Logo Round.png" alt="Orange and Blue Collar mascot" id="alligator-mascot" />
        </div>

        <div id="form-area">
          <h1 id="welcome-text">
            Welcome to <br />
            <span id="orange-text">Orange</span> and <span id="blue-text">Blue</span> Collar!
          </h1>

          <input v-model.trim="username" type="text" placeholder="Username" class="form-input" />
          <input v-model.trim="password" type="password" placeholder="Password" class="form-input" />

          <button id="join-button" @click="handleRegister">Join Now!</button>

          <p id="account-prompt">
            Already have an account?
            <router-link to="/login" id="sign-in-link">Sign in</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  #login-page {
    background-color: #7990b5;
    background: linear-gradient(to bottom, #7990b5 0%, #3e506e 100%);

    min-height: 100vh;
    width: 100vw;

    display: flex;
    justify-content: center;
    align-items: center;

    padding: 20;

    padding: 20px;
    box-sizing: border-box;
  }

  #login-card {
    background-image: linear-gradient(to bottom, rgba(95, 136, 198, 0.25) 96%, #c28b3a 100%);

    width: 100%;
    max-width: 700px;

    padding: 5px;

    border-radius: 20px;
    box-shadow:
      0 0 15px rgba(255, 165, 0, 0.5),
      0 0 0 2px #c28b3a;
    position: relative;

    margin-top: -200px;
  }

  #back-button {
    position: absolute;
    top: 30px;
    left: 35px;

    font-size: 32px;
    color: #fff;
    background: none;
    border: none;

    text-decoration: none;
    cursor: pointer;
  }

  .back-button:hover {
    background: none;
  }

  #card-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  #image-area {
    flex-shrink: 0;
    width: 40%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #alligator-mascot {
    width: 100%;
    max-width: 300px;
    height: auto;
    border-radius: 50%;
    object-fit: cover;
  }

  #form-area {
    flex-grow: 1;
    max-width: 500px;
    width: 50%;
    margin-top: -5px;
    margin-right: 10px;
  }

  #welcome-text {
    font-family: 'Irish Grover', cursive;
    color: #f7f1e3;
    font-size: 36px;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
    text-align: center;
    line-height: 1.2;
    margin-bottom: 20px;
    width: 400px;

    margin-top: -10px;
    margin-left: -10px;
  }

  #orange-text {
    color: #d4862d;
  }

  #blue-text {
    color: #1e90ff;
  }

  #google-sign-in {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    flex-shrink: 0;

    width: 320px;
    height: 40px;
    min-height: 40px;
    max-height: 40px;
    margin: 0 auto 15px auto;

    padding: 8px 16px;

    border-radius: 6px;
    border: 1px solid #000;
    background: #c0d1eb;
    box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.25);

    color: #000;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .google-sign-in:hover {
    background-color: #a4bde0;
  }

  #google-icon {
    height: 18px;
    width: auto;
  }

  #join-button {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;

    font-family: 'Irish Grover', cursive;
    box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.25);

    width: 320px;
    height: 40px;
    min-height: 40px;
    max-height: 40px;
    margin: 20px auto 10px auto;

    padding: 8px 16px;

    border-radius: 6px;
    border: 1px solid #000;
    background: #d4862d;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s ease;
    font-size: 1.05em;
  }

  #join-button:hover {
    background-color: #ae6c25;
  }

  .form-input {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;

    width: 320px;
    min-width: 320px;
    max-width: 320px;
    height: 40px;
    min-height: 40px;
    max-height: 40px;

    margin: 0 auto 15px auto;

    padding: 8px 12px;

    border-radius: 6px;
    border: 1px solid #000;
    background: var(--White, #fff);
    box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.25);

    color: #333;
  }

  #or-divider {
    text-align: center;
    flex-shrink: 0;

    margin: 15px auto;

    width: 15px;
    height: 17px;

    color: #fff;
    font-family: 'Irish Grover', cursive;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;

    -webkit-text-stroke-width: 0.25px;
    -webkit-text-stroke-color: #000;
  }

  #account-prompt {
    margin-top: 5px;
    margin-bottom: -5px;

    color: #fff;
    font-family: 'Irish Grover', cursive;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;

    position: relative;
    top: 10px;
    left: 70px;
  }

  #sign-in-link {
    color: #d4862d;
    text-decoration: underline;
    text-decoration-style: solid;

    font-family: 'Irish Grover', cursive;
    font-weight: 400;
    line-height: normal;

    position: relative;
  }

  #sign-in-link:hover {
    opacity: 0.8;
  }
</style>
