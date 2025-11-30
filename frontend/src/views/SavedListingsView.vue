<template>
  <div class="saved-listings-view">
    <div class="container">
      <h1><span class="orange-text">Saved</span> <span class="blue-text">Listings</span></h1>

      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search your saved listings..."
        class="search-bar"
        aria-label="Search your saved listings"
      />

      <div v-if="loading" class="loading">Loading your saved listings...</div>

      <div v-else-if="filteredFavorites.length === 0" class="empty-state">
        <p v-if="searchQuery">{{ noResultsMessage }}</p>
        <p v-else>No saved listings yet!</p>
        <router-link to="/internships" class="browse-button">Browse Internships</router-link>
      </div>

      <div v-else class="job-listings">
        <div v-for="favorite in filteredFavorites" :key="favorite.id" class="job-card">
          <div class="job-header">
            <h2>{{ favorite.title }}</h2>
            <img
              v-if="favorite.company.logo_url"
              :src="favorite.company.logo_url"
              :alt="favorite.company.name + ' logo'"
              class="company-logo"
            />
          </div>
          <p class="company">{{ favorite.company.name }} � {{ formatLocations(favorite.locations) }}</p>
          <p class="posted-date">Posted: {{ formatDate(favorite.date_posted) }}</p>
          <div class="job-meta">
            <span v-if="favorite.category" class="category-tag">{{ formatCategoryDisplay(favorite.category) }}</span>
            <span v-if="favorite.sponsorship === 'Offers Sponsorship'" class="sponsorship-tag">Sponsorship</span>
            <span v-if="favorite.faang_plus" class="faang-tag">FAANG+</span>
          </div>
          <p class="source">Source: {{ favorite.source }}</p>
          <a :href="favorite.url" target="_blank" class="apply-button">Apply Now</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, computed } from 'vue';
  import Fuse from 'fuse.js';

  interface Company {
    name: string;
    logo_url?: string;
  }

  interface Favorite {
    id: string;
    title: string;
    company: Company;
    locations: string[];
    date_posted: string;
    category?: string;
    sponsorship?: string;
    faang_plus?: boolean;
    source: string;
    url: string;
  }

  const favorites = ref<Favorite[]>([]);
  const loading = ref(true);
  const searchQuery = ref('');
  const fuse = ref<Fuse<Favorite> | null>(null);

  const fuseOptions = {
    keys: [
      { name: 'title', weight: 2 },
      { name: 'company.name', weight: 1.5 },
      { name: 'locations', weight: 1.5 },
      { name: 'category', weight: 1.2 }
    ],
    threshold: 0.4,
    includeScore: true,
    minMatchCharLength: 2,
    shouldSort: true
  };

  const noResultsMessage = computed(() => {
    return `No saved listings match "${searchQuery.value}"`;
  });

  const filteredFavorites = computed(() => {
    const query = searchQuery.value.trim();

    if (!query || !fuse.value) {
      return favorites.value;
    }

    const searchResults = fuse.value.search(query);
    return searchResults.map(result => result.item);
  });

  onMounted(async () => {
    await loadFavorites();
  });

  const loadFavorites = async () => {
    loading.value = true;

    try {
      const response = await fetch('/api/favorites', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      if (response.ok) {
        favorites.value = await response.json();
        fuse.value = new Fuse(favorites.value, fuseOptions);
      } else {
        favorites.value = [];
      }
    } catch (_error) {
      // Prefix with underscore to indicate unused
      favorites.value = [];
    } finally {
      loading.value = false;
    }
  };

  const formatCategoryDisplay = (category: string): string => {
    const displayMap: { [key: string]: string } = {
      'Data Science, AI & Machine Learning': 'Data Science/AI/ML'
    };
    return displayMap[category] || category;
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return 'Recent';
    }
  };

  const formatLocations = (locations: string[]) => {
    if (!locations || locations.length === 0) return 'Remote';
    return locations.join(', ');
  };
</script>

<style scoped>
  /* Your existing CSS remains the same */
  .saved-listings-view {
    width: 100vw;
    padding: 2rem;
    padding-top: 60px;
    color: #333;
    box-sizing: border-box;
    background: linear-gradient(to bottom, #5a7caf, rgba(255, 255, 255, 0)), white;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
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
    text-align: center;
    margin-bottom: 1rem;
    font-size: 5rem;
    color: white;
  }

  .orange-text {
    color: #ffa500;
  }

  .blue-text {
    color: #1e90ff;
  }

  .search-bar {
    display: block;
    width: 100%;
    max-width: 1200px;
    margin: 0 auto 2rem auto;
    padding: 1rem 1.5rem;
    font-size: 1.3rem;
    font-family: 'Irish Grover', cursive;
    border-radius: 4px;
    border: 2px solid #d4862d;
    outline: none;
    transition:
      border-color 0.3s ease,
      background 0.3s ease;
    background: transparent;
    color: white;
    backdrop-filter: blur(5px);
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
    text-indent: 2px;
    box-sizing: border-box;
  }

  .search-bar::placeholder {
    color: white;
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
    text-indent: 8px;
  }

  .search-bar:focus,
  .search-bar:hover {
    border-color: #d4862d;
    background: rgba(255, 255, 255, 0.1);
  }

  .loading {
    text-align: center;
    padding: 2rem;
    color: #d4862d;
    font-size: 1.2rem;
    font-family: 'Irish Grover', cursive;
    -webkit-text-stroke: 0.3px black;
  }

  .empty-state {
    text-align: center;
    padding: 2rem;
    color: #d4862d;
    font-size: 2rem;
    font-family: 'Irish Grover', cursive;
    -webkit-text-stroke: 0.3px black;
  }

  .empty-state p {
    margin-bottom: 20px;
  }

  .browse-button {
    background: #d4862d;
    color: white;
    padding: 12px 24px;
    border-radius: 5px;
    text-decoration: none;
    font-family: 'Irish Grover', cursive;
    border: 2px solid #000;
    font-size: 1.2rem;
    transition: opacity 0.3s ease;
  }

  .browse-button:hover {
    opacity: 0.8;
  }

  .job-listings {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding: 2rem 0;
    width: 90%;
    margin: 0 auto;
    box-sizing: border-box;
    align-items: stretch;
  }

  .job-card {
    position: relative;
    width: 100%;
    background: linear-gradient(to bottom, #2645a3, #0e1a3d);
    border-radius: 6px;
    padding: 1.5rem;
    padding-bottom: 3rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    color: white;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    min-height: 350px;
    overflow: hidden;
  }

  .job-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(163, 102, 38, 0.5) 0%, rgba(61, 14, 14, 0.5) 100%);
    opacity: 0;
    transition: opacity 0.6s ease;
    z-index: 0;
    border-radius: 6px;
  }

  .job-card:hover::before {
    opacity: 1;
  }

  .job-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
  }

  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
    position: relative;
    padding-right: 40px;
  }

  .company-logo {
    width: 50px;
    height: 50px;
    object-fit: contain;
    border-radius: 4px;
    background: white;
    padding: 4px;
  }

  h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
    color: #fff;
    flex: 1;
    margin-right: 1rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  .company {
    color: #aad4ff;
    font-weight: bold;
    margin-bottom: 0.3rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  .posted-date {
    font-size: 0.875rem;
    color: #cce0ff;
    margin-bottom: 0.5rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  .job-meta {
    margin: 1rem 0;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .category-tag,
  .sponsorship-tag,
  .faang-tag {
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: bold;
    font-family: 'Irish Grover', cursive;
  }

  .category-tag {
    background: rgba(30, 144, 255, 0.3);
    color: #aad4ff;
  }

  .sponsorship-tag {
    background: rgba(50, 205, 50, 0.3);
    color: #99ff99;
  }

  .faang-tag {
    background: rgba(148, 0, 211, 0.3);
    color: #dda0dd;
  }

  .source {
    font-size: 0.875rem;
    color: #cce0ff;
    margin-top: 0.5rem;
    font-style: italic;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  .apply-button {
    position: absolute;
    bottom: 1.5rem;
    right: 1.5rem;
    background-color: #1e90ff;
    color: white;
    padding: 0.5rem 1rem;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    font-family: 'Irish Grover', cursive;
    transition: background-color 0.3s ease;
  }

  .job-card:hover .apply-button:not(:hover) {
    background-color: #a66a26;
    transition: background-color 0.6s ease;
  }

  .apply-button:hover {
    background-color: #734d22;
    transition: background-color 0.25s ease;
  }

  @media (max-width: 768px) {
    .job-listings {
      width: 90%;
      grid-template-columns: 1fr;
    }

    .company-logo {
      width: 40px;
      height: 40px;
    }

    .job-header h2 {
      font-size: 1.1rem;
      margin-right: 0.5rem;
    }

    .job-header {
      padding-right: 45px;
    }

    h1 {
      font-size: 3rem;
    }
  }
</style>
