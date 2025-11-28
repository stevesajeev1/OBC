<template>
  <div :class="$style.networkingPage">
    <!-- Title -->
    <h1 :class="$style.title">
      <span :class="$style.orange">Orange</span>
      <span> and </span>
      <span :class="$style.blue">Blue</span>
      <span> Collar</span>
    </h1>

    <!-- Search Bar -->
    <div :class="$style.searchBar">
      <svg :class="$style.searchIcon" width="20" height="20" viewBox="0 0 20 20" fill="none">
        <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="2" />
        <path d="M13 13L17 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
      </svg>
      <span :class="$style.searchText">Companies that a gator may have interned at!</span>
    </div>

    <!-- Filter Positions -->
    <div :class="$style.filterPositions">
      <button :class="$style.filterButton">
        <span :class="$style.filterText">Filter Positions</span>
        <svg :class="$style.dropdownIcon" width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
      </button>
    </div>

    <!-- People Grid -->
    <div :class="$style.peopleGrid">
      <!-- Row 1 -->
      <div :class="[$style.profileCard, $style.cardBlue]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>

      <div :class="[$style.profileCard, $style.cardDark]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>

      <div :class="[$style.profileCard, $style.cardRed]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>

      <!-- Row 2 -->
      <div :class="[$style.profileCard, $style.cardBlue]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>

      <div :class="[$style.profileCard, $style.cardDark]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>

      <div :class="[$style.profileCard, $style.cardRed]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>

      <!-- Row 3 -->
      <div :class="[$style.profileCard, $style.cardBlue]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>

      <div :class="[$style.profileCard, $style.cardDark]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>

      <div :class="[$style.profileCard, $style.cardRed]">
        <img :src="profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">Bim Bob</h3>
        <p :class="$style.role">Software Engineer</p>
        <p :class="$style.internedAt">Interned at:</p>
        <img :src="companyIcon" alt="Company" :class="$style.companyIcon" />
        <button :class="$style.contactButton" @click="openContact('bim_bob')">Contact</button>
      </div>
    </div>

    <!-- Modal Overlay -->
    <div v-if="showPopup" :class="$style.overlay" @click.self="closePopup">
      <ContactPopup :username="selectedUsername" @close="closePopup" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ContactPopup from './ContactPopup.vue';


const profileImage = ref('https://media.discordapp.net/attachments/778002970112557116/1443639418362789928/bimbob.png?ex=6929cd7a&is=69287bfa&hm=f28318ffc79a8e4d6c0a364b07a3fef787cd450974fbcee180e634d054abeaff&=&format=webp&quality=lossless');
const companyIcon = ref('https://media.discordapp.net/attachments/778002970112557116/1443639943519014912/googlelogo.png?ex=6929cdf8&is=69287c78&hm=d4336bb1cfdaa688b3a04d0a806ed5f512e13ee321e4a1d583d5e6f5960e7a35&=&format=webp&quality=lossless');

const router = useRouter();
const showPopup = ref(false);
const selectedUsername = ref('');
function openContact(username: string) {
  selectedUsername.value = username;
  showPopup.value = true;
}
function closePopup() {
  showPopup.value = false;
}
</script>

<style module>
.networkingPage {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(180deg, #5a7caf 74.52%, #b5b5b5 100%);
  padding-top: 120px;
  padding-bottom: 40px;
  position: relative;
  overflow-x: hidden;
}

.title {
  font-family: 'Irish Grover', cursive;
  font-size: 80px;
  text-align: center;
  margin: 80px auto 60px;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  text-shadow: 1px 0 0 #000, 0 1px 0 #000, -1px 0 0 #000, 0 -1px 0 #000;
  color: white;
}

.orange {
  color: #d4862d;
}

.blue {
  color: #1e90ff;
}

.searchBar {
  max-width: 1065px;
  margin: 0 auto 60px;
  padding: 20px 20px 20px 17px;
  border: 1px solid #d4862d;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 17px;
}

.searchIcon {
  opacity: 0.5;
  color: white;
  flex-shrink: 0;
}

.searchText {
  font-family: 'Irish Grover', cursive;
  font-size: 24px;
  color: white;
  opacity: 0.5;
}

.filterPositions {
  max-width: 1065px;
  margin: 0 auto 40px;
  padding: 0;
}

.filterButton {
  background: transparent;
  border: 1px solid #d4862d;
  border-radius: 6px;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 40px;
}

.filterButton:hover {
  background: rgba(212, 134, 45, 0.1);
}

.filterText {
  font-family: 'Irish Grover', cursive;
  font-size: 14px;
  color: white;
  opacity: 0.5;
}

.dropdownIcon {
  opacity: 0.5;
  color: white;
}

.peopleGrid {
  max-width: 1066px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 335px);
  gap: 31px 31px;
  justify-content: center;
}

.profileCard {
  width: 335px;
  height: 188px;
  border: 1px solid #d4862d;
  border-radius: 6px;
  padding: 14px 29px;
  position: relative;
  display: flex;
  flex-direction: column;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease;
}

.profileCard:hover {
  transform: translateY(-2px);
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
}

.cardBlue {
  background: linear-gradient(180deg, #5a7caf 74.52%, #b5b5b5 100%);
}

.cardDark {
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, rgba(14, 26, 61, 0.5) 100%);
}

.cardRed {
  background: linear-gradient(180deg, rgba(244, 39, 39, 0.5) 0%, rgba(14, 26, 61, 0.5) 100%);
}

.profileImage {
  position: absolute;
  top: 12px;
  left: 32px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.name {
  font-family: 'Inria Sans', sans-serif;
  font-size: 32px;
  color: white;
  margin: 0 0 0 84px;
  font-weight: 400;
}

.role {
  font-family: 'Inria Sans', sans-serif;
  font-size: 16px;
  color: white;
  margin: 4px 0 0 84px;
  font-weight: 400;
}

.internedAt {
  font-family: 'Inria Sans', sans-serif;
  font-size: 20px;
  color: white;
  margin: 18px 0 0 0;
  font-weight: 400;
}

.companyIcon {
  position: absolute;
  top: 80px;
  left: 139px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
}

.contactButton {
  position: absolute;
  bottom: 29px;
  left: 50%;
  transform: translateX(-50%);
  width: 209px;
  height: 40px;
  background-color: #d4862d;
  border: 1px solid #000;
  border-radius: 6px;
  font-family: 'Irish Grover', cursive;
  font-size: 20px;
  color: #fafafa;
  text-shadow: 1px 0 0 #000, 0 1px 0 #000, -1px 0 0 #000, 0 -1px 0 #000;
  cursor: pointer;
  transition: all 0.2s ease;
}

.contactButton:hover {
  background-color: #c07527;
  transform: translateX(-50%) translateY(-1px);
}

.contactButton:active {
  transform: translateX(-50%) translateY(0);
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  z-index: 1000;
}

@media (max-width: 1200px) {
  .peopleGrid {
    grid-template-columns: repeat(2, 335px);
    gap: 31px;
  }

  .title {
    font-size: 60px;
  }
}

@media (max-width: 768px) {
  .networkingPage {
    padding-top: 140px;
  }

  .peopleGrid {
    grid-template-columns: 335px;
    gap: 24px;
    padding: 0 20px;
  }

  .title {
    font-size: 48px;
    padding: 0 20px;
  }

  .searchBar {
    margin: 0 20px 40px;
  }

  .filterPositions {
    padding: 0 20px;
  }

  .searchText {
    font-size: 18px;
  }
}
</style>
