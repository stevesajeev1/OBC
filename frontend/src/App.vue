<script lang="ts" setup>
  import { computed, onMounted, ref, onUnmounted } from 'vue';
  import { getProfile, type Profile } from './api/profile';
  import { user } from './state';
  import { signOut } from './api/auth';
  import { useRouter } from 'vue-router';
  import defaultPfp from '@/assets/default_pfp.jpg';

  const router = useRouter();
  const profileDialogOpen = ref<boolean>(false);

  const profileData = ref<Profile | null>(null);

  onMounted(async () => {
    profileData.value = await getProfile();
  });

  const profileImageUrl = computed(() => profileData.value?.image_url || defaultPfp);
  const profileName = computed(() => profileData.value?.full_name || 'User');

  const toggleProfileDialog = () => {
    profileDialogOpen.value = !profileDialogOpen.value;
  };

  const handleDialogExit = (e: MouseEvent) => {
    let target = e.target as HTMLElement;
    while (target && target.parentElement) {
      if (['nav-profile', 'profile-dialog', 'profile-triangle'].includes(target.id)) return;
      target = target.parentElement;
    }
    profileDialogOpen.value = false;
  };

  document.addEventListener('click', handleDialogExit);
  onUnmounted(() => {
    document.removeEventListener('click', handleDialogExit);
  });

  const handleSignOut = async () => {
    await signOut();
    router.push({ name: 'login' });
  };

  const goToSavedListings = () => {
    profileDialogOpen.value = false;
    router.push({ name: 'saved-listings' });
  };

  const onProfileUpdated = (updatedProfile: { full_name: string; image_url: string }) => {
    if (profileData.value) {
      profileData.value.full_name = updatedProfile.full_name;
      profileData.value.image_url = updatedProfile.image_url;
    }
  };
</script>

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
        <router-link to="/networking" class="nav-link">Networking</router-link>
        <router-link to="/team" class="nav-link">About</router-link>

        <template v-if="user === null">
          <router-link to="/login" class="nav-link join-now">Login</router-link>
          <router-link to="/join" class="nav-link join-now">Register</router-link>
        </template>

        <div v-else id="nav-profile" @click="toggleProfileDialog">
          <img :src="profileImageUrl" :key="profileImageUrl" alt="Profile Picture" />
        </div>
      </div>
    </nav>

    <router-view v-slot="{ Component }">
      <component :is="Component" @profile-updated="onProfileUpdated" />
    </router-view>

    <dialog v-if="profileDialogOpen" id="profile-dialog" :open="profileDialogOpen">
      <span>Hi, {{ profileName }}!</span>
      <router-link :to="{ name: 'edit-profile' }" @click="profileDialogOpen = false"> Manage your Account </router-link>
      <div class="saved-listings-button" @click="goToSavedListings">Saved Listings</div>
      <div id="logout" @click="handleSignOut">Logout</div>
    </dialog>

    <div v-if="profileDialogOpen" id="profile-triangle"></div>
  </div>
</template>

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
    position: relative;
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
    z-index: 999;
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

  .nav-link:hover,
  #nav-profile:hover {
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

  #nav-profile {
    height: 75px;
    aspect-ratio: 1;
    border-radius: 50%;
    border: 2px solid black;
    transition: opacity 0.3s ease;
    z-index: 1000;
    position: relative;
    cursor: pointer;
  }

  #nav-profile img {
    height: 100%;
    width: 100%;
    border-radius: 50%;
    object-fit: cover;
  }

  #profile-dialog {
    --width: 300px;
    position: absolute;
    top: 105px;
    left: calc(100% - var(--width) - 2rem);
    width: var(--width);
    margin: 0;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #7a9ccf;
    border: 2px solid #7a9ccf;
    border-radius: 10px;
    color: #d4862d;
    font-family: 'Irish Grover', cursive;
    z-index: 1001;
    text-shadow:
      -1px -1px 0 #000,
      1px -1px 0 #000,
      -1px 1px 0 #000,
      1px 1px 0 #000;
    box-shadow:
      -2px -2px 0 #000,
      2px -2px 0 #000,
      -2px 2px 0 #000,
      2px 2px 0 #000;
  }

  #profile-triangle {
    position: absolute;
    top: 95px;
    left: calc(100% - 79px);
    width: 20px;
    height: 20px;
    background: #7a9ccf;
    transform: rotate(45deg);
    z-index: 1001;
    box-shadow:
      -2px -2px 0 #000,
      0px -0px 0 #000,
      -0px 0px 0 #000,
      0px 0px 0 #000;
  }

  #profile-dialog span {
    font-size: 2.5rem;
    margin-bottom: 15px;
  }

  #profile-dialog a {
    background: #d4862d;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    transition: opacity 0.3s ease;
    box-shadow:
      -1px -1px 0 #000,
      1px -1px 0 #000,
      -1px 1px 0 #000,
      1px 1px 0 #000;
    margin: 10px 0;
  }

  #profile-dialog a:hover {
    opacity: 0.8;
  }

  #logout {
    margin-top: 10px;
    background: black;
    color: #d4862d;
    padding: 10px 20px;
    transition: opacity 0.3s ease;
    border-radius: 5px;
    font-family: 'Irish Grover', cursive;
    cursor: pointer;
  }

  #logout:hover {
    opacity: 0.8;
  }

  .saved-listings-button {
    background: #5a7caf;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    transition: opacity 0.3s ease;
    margin: 10px 0;
    cursor: pointer;
    border: 1px solid #000;
    font-family: 'Irish Grover', cursive;
    text-align: center;
    box-shadow:
      -0.5px -0.5px 0 #000,
      0.5px -0.5px 0 #000,
      -0.5px 0.5px 0 #000,
      0.5px 0.5px 0 #000;
  }

  .saved-listings-button:hover {
    opacity: 0.8;
  }
</style>
