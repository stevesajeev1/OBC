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
      <input
        v-model="searchQuery"
        type="text"
        :class="$style.searchInput"
        placeholder="Companies that a gator may have interned at!"
      />
    </div>

    <!-- Loading State -->
    <div v-if="loading" :class="$style.loadingContainer">
      <p :class="$style.loadingText">Loading profiles...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" :class="$style.errorContainer">
      <p :class="$style.errorText">{{ error }}</p>
      <button :class="$style.retryButton" @click="fetchProfiles">Retry</button>
    </div>

    <!-- People Grid -->
    <div v-else :class="$style.peopleGrid">
      <div v-for="person in filteredPeople" :key="person.id" :class="[$style.profileCard, $style[person.cardVariant]]">
        <img :src="person.profileImage" alt="Profile" :class="$style.profileImage" />
        <h3 :class="$style.name">{{ person.fullName }}</h3>
        <p :class="$style.role">{{ person.role }}</p>
        <div :class="$style.internshipRow">
          <span :class="$style.internedAt">Interned at:</span>
          <div :class="$style.companyIconsRow">
            <img
              v-for="(icon, idx) in person.companyIcons"
              :key="idx"
              :src="icon"
              alt="Company"
              :class="$style.companyIcon"
            />
          </div>
        </div>
        <button :class="$style.contactButton" @click="openContact(person)">Contact</button>
      </div>
    </div>

    <!-- Modal Overlay -->
    <div v-if="showPopup && selectedPerson" :class="$style.overlay" @click.self="closePopup">
      <ContactPopup
        :username="selectedPerson.username"
        :full-name="selectedPerson.fullName"
        :profile-image-url="selectedPerson.profileImage"
        :company-icon-url="selectedPerson.companyIcons[0]"
        :email="selectedPerson.email"
        :instagram="selectedPerson.instagram"
        :linkedin="selectedPerson.linkedin"
        :roles="selectedPerson.roles"
        :company-icons="selectedPerson.companyIcons"
        :company-names="selectedPerson.companyNames"
        @close="closePopup"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted, watch } from 'vue';
  import ContactPopup from './ContactPopup.vue';
  import { getAllProfiles, type Profile as BackendProfile } from '@/api/profile';
  import { getAllCompanies, type Company } from '@/api/companies';
  import Fuse, { type IFuseOptions } from 'fuse.js';

  interface Person {
    id: number;
    username: string;
    fullName: string;
    role: string;
    profileImage: string;
    companyIcons: string[];
    companyNames: string[];
    email: string;
    instagram: string;
    linkedin: string;
    roles: string[];
    cardVariant: 'cardBlue' | 'cardDark' | 'cardRed';
  }

  const people = ref<Person[]>([]);
  const companyLogoMap = ref<Record<string, string>>({});

  // Function to map backend profile to frontend Person
  function mapProfileToPerson(profile: BackendProfile, index: number): Person {
    const variants: Array<'cardBlue' | 'cardDark' | 'cardRed'> = ['cardBlue', 'cardDark', 'cardRed'];
    const internships = profile.prev_internships || [];

    // Use the LinkedIn profile URL directly from backend
    const linkedinUrl = profile.linkedin_url || '';

    const companyNames = internships.map(i => i.company).filter(Boolean);
    const companyIcons = companyNames.map(
      name => companyLogoMap.value[name] || 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/buildkite.svg'
    );
    const roles = internships.map(i => i.role).filter(Boolean);

    return {
      id: index + 1,
      username: profile.full_name || 'Anonymous',
      fullName: profile.full_name || 'Anonymous User',
      role: internships[0]?.role || profile.major || 'Student',
      profileImage: profile.image_url || new URL('./assets/default_pfp.jpg', import.meta.url).href,
      companyIcons,
      companyNames,
      email: '', // Backend doesn't expose email in public profiles
      instagram: '', // Backend doesn't have instagram
      linkedin: linkedinUrl,
      roles,
      cardVariant: variants[index % 3]
    };
  }

  // Fetch profiles from backend
  async function fetchProfiles() {
    loading.value = true;
    error.value = null;
    try {
      // Fetch companies and build logo map first
      const companies = await getAllCompanies();
      companyLogoMap.value = companies.reduce((acc: Record<string, string>, c: Company) => {
        if (c.name) acc[c.name] = c.logo_url || acc[c.name] || '';
        return acc;
      }, {});

      const profiles = await getAllProfiles();
      people.value = profiles.map((profile, index) => mapProfileToPerson(profile, index));
    } catch (err) {
      error.value = 'Failed to load profiles. Please try again later.';
      console.error('Error fetching profiles:', err);
    } finally {
      loading.value = false;
    }
  }

  // Fetch profiles on component mount
  onMounted(() => {
    fetchProfiles();
  });

  const showPopup = ref(false);
  const selectedPerson = ref<Person | null>(null);
  const searchQuery = ref('');
  const loading = ref(true);
  const error = ref<string | null>(null);

  // Setup Fuse.js for fuzzy search across person data
  const fuse = ref<Fuse<Person> | null>(null);
  const fuseOptions: IFuseOptions<Person> = {
    includeScore: true,
    threshold: 0.35,
    ignoreLocation: true,
    keys: ['fullName', 'role', { name: 'companyNames', weight: 0.8 }]
  };

  // Reinitialize Fuse index whenever people change
  watch(
    people,
    list => {
      fuse.value = new Fuse(list, fuseOptions);
    },
    { immediate: true }
  );

  const filteredPeople = computed(() => {
    const query = searchQuery.value.trim();
    if (!query) return people.value;
    if (!fuse.value) return people.value;
    const results = fuse.value.search(query);
    return results.map(r => r.item);
  });

  function openContact(person: Person) {
    selectedPerson.value = person;
    showPopup.value = true;
  }

  function closePopup() {
    showPopup.value = false;
    selectedPerson.value = null;
  }
</script>

<style module>
  .networkingPage {
    min-height: 100vh;
    width: 100%;
    background: linear-gradient(180deg, #5a7caf 74.52%, #b5b5b5 100%);
    padding-top: 80px;
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
    text-shadow:
      1px 0 0 #000,
      0 1px 0 #000,
      -1px 0 0 #000,
      0 -1px 0 #000;
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

  .searchInput {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    font-family: 'Irish Grover', cursive;
    font-size: 24px;
    color: white;
    padding: 0;
  }

  .searchInput::placeholder {
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
    font-family: 'Irish Grover', sans-serif;
    font-size: 32px;
    color: white;
    margin: 0 0 0 84px;
    font-weight: 400;
    /* Prevent layout shift on long names */
    max-width: 220px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .role {
    font-family: 'Irish Grover', sans-serif;
    font-size: 16px;
    color: white;
    margin: 4px 0 0 84px;
    font-weight: 400;
    /* Keep role on one line with ellipsis */
    max-width: 220px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .internedAt {
    font-family: 'Irish Grover', sans-serif;
    font-size: 20px;
    color: white;
    font-weight: 400;
  }

  .internshipRow {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 18px 0 0 0;
  }

  .companyIcon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    object-fit: cover;
  }

  .companyIconsRow {
    display: flex;
    gap: 8px;
  }

  .contactButton {
    position: absolute;
    bottom: 10px;
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
    text-shadow:
      1px 0 0 #000,
      0 1px 0 #000,
      -1px 0 0 #000,
      0 -1px 0 #000;
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

  .loadingContainer {
    max-width: 1066px;
    margin: 60px auto;
    text-align: center;
  }

  .loadingText {
    font-family: 'Irish Grover', cursive;
    font-size: 24px;
    color: white;
    margin: 0;
  }

  .errorContainer {
    max-width: 1066px;
    margin: 60px auto;
    text-align: center;
  }

  .errorText {
    font-family: 'Irish Grover', cursive;
    font-size: 20px;
    color: white;
    margin: 0 0 20px 0;
  }

  .retryButton {
    background-color: #d4862d;
    border: 1px solid #000;
    border-radius: 6px;
    padding: 12px 24px;
    font-family: 'Irish Grover', cursive;
    font-size: 18px;
    color: #fafafa;
    text-shadow:
      1px 0 0 #000,
      0 1px 0 #000,
      -1px 0 0 #000,
      0 -1px 0 #000;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .retryButton:hover {
    background-color: #c07527;
    transform: translateY(-1px);
  }

  .retryButton:active {
    transform: translateY(0);
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
