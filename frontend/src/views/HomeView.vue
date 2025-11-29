<template>
  <div class="home-container">
    <h1><span class="orange-text">Orange</span> and <span class="blue-text">Blue</span> Collar</h1>

    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search for open internship opportunities!"
      class="search-bar"
      aria-label="Search for open internship opportunities"
    />

    <div class="filters-wrapper">
      <div class="filters-main-container">
        <transition name="filters-transform" mode="out-in">
          <div v-if="showFilters" key="filters-container" class="filters-row-container">
            <div class="category-buttons-single-row">
              <button
                class="category-btn"
                :class="{ selected: selectedCategories.includes('Software Engineering') }"
                @click="toggleCategory('Software Engineering')"
              >
                Software Engineering
              </button>
              <button
                class="category-btn"
                :class="{ selected: selectedCategories.includes('Product Management') }"
                @click="toggleCategory('Product Management')"
              >
                Product Management
              </button>
              <button
                class="category-btn"
                :class="{ selected: selectedCategories.includes('Data Science, AI & Machine Learning') }"
                @click="toggleCategory('Data Science, AI & Machine Learning')"
              >
                Data Science/AI/ML
              </button>
              <button
                class="category-btn"
                :class="{ selected: selectedCategories.includes('Quantitative Finance') }"
                @click="toggleCategory('Quantitative Finance')"
              >
                Quantitative Finance
              </button>
              <button
                class="category-btn"
                :class="{ selected: selectedCategories.includes('Hardware Engineering') }"
                @click="toggleCategory('Hardware Engineering')"
              >
                Hardware Engineering
              </button>
            </div>

            <div class="special-filters-table">
              <button
                class="special-filter-btn"
                :class="{ selected: sponsorshipFilter !== SponsorshipFilter.ALL }"
                @click="toggleSponsorship()"
              >
                Sponsorship
              </button>
              <button class="special-filter-btn" :class="{ selected: selectedFAANG }" @click="toggleFAANG()">
                FAANG+
              </button>
            </div>
          </div>

          <button v-else class="filters-toggle-btn" @click="showFilters = true" key="button">
            Filters
            <span class="toggle-icon">+</span>
          </button>
        </transition>
      </div>
    </div>

    <div v-if="initialLoading" class="loading">Loading internships...</div>

    <div v-else-if="error" class="error">
      {{ error }}
      <button @click="fetchInitialData" class="retry-btn">Retry</button>
    </div>

    <div v-else>
      <div v-if="pageLoading || filtersLoading" class="loading">Loading internships...</div>

      <div v-else class="job-listings">
        <div v-for="job in currentPageJobs" :key="job.item.id" class="job-card">
          <div class="job-header">
            <h2>{{ job.item.title }}</h2>
            <img
              v-if="job.item.company.logo_url"
              :src="job.item.company.logo_url"
              :alt="job.item.company.name + ' logo'"
              class="company-logo"
            />
          </div>
          <p class="company">{{ job.item.company.name }} — {{ formatLocations(job.item.locations) }}</p>
          <p class="posted-date">Posted: {{ formatDate(job.item.date_posted) }}</p>
          <div class="job-meta">
            <span v-if="job.item.category" class="category-tag">{{ formatCategoryDisplay(job.item.category) }}</span>
            <span v-for="term in job.item.terms.slice(0, 2)" :key="term" class="term-tag">{{ term }}</span>
            <span v-if="job.item.sponsorship === 'Offers Sponsorship'" class="sponsorship-tag"> Sponsorship </span>
            <span v-if="job.item.faang_plus" class="faang-tag">FAANG+</span>
          </div>
          <p class="source">Source: {{ job.item.source }}</p>

          <button
            v-if="user?.admin"
            @click="deleteListing(job.item.id)"
            class="delete-btn"
            :disabled="deletingListingId === job.item.id"
            :title="`Delete ${job.item.title}`"
          >
            {{ deletingListingId === job.item.id ? 'Deleting...' : '×' }}
          </button>

          <a :href="job.item.url" target="_blank" class="apply-button">Apply Now</a>
        </div>

        <p v-if="currentPageJobs.length === 0 && !initialLoading && !filtersLoading" class="no-results">
          {{ allJobsCache.length === 0 ? 'No internships available' : 'No internships match your filters' }}
        </p>
      </div>

      <div v-if="!initialLoading && !error && !filtersLoading && totalPages > 1" class="pagination-controls">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage <= 1 || pageLoading || filtersLoading"
          class="pagination-btn"
        >
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }}</span>
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="
            (hasActiveFilters && currentPage >= totalPages) ||
            (!hasActiveFilters &&
              currentPage >= totalPages &&
              allJobsCache.length < currentPage * targetActiveJobsPerPage) ||
            pageLoading ||
            filtersLoading
          "
          class="pagination-btn"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
  import { ref, computed, onMounted, watch } from 'vue';
  import Fuse from 'fuse.js';
  import { axiosInstance } from '@/api/axios';
  import { user } from '@/state';

  enum SponsorshipFilter {
    ALL = 'all',
    OFFERS = 'offers'
  }

  interface Company {
    id: string;
    name: string;
    url: string;
    logo_url?: string;
  }

  interface Job {
    id: string;
    source: string;
    title: string;
    active: boolean;
    date_updated: string;
    is_visible: boolean;
    date_posted: string;
    url: string;
    locations: string[];
    terms: string[];
    sponsorship: string;
    category: string;
    faang_plus: boolean;
    company: Company;
  }

  const searchQuery = ref('');
  const selectedCategories = ref<string[]>([]);
  const showFilters = ref(false);
  const initialLoading = ref(false);
  const error = ref('');
  const selectedFAANG = ref(false);
  const sponsorshipFilter = ref<SponsorshipFilter>(SponsorshipFilter.ALL);
  const pageLoading = ref(false);
  const filtersLoading = ref(false);
  const deletingListingId = ref<string | null>(null);

  const currentPage = ref(1);
  const targetActiveJobsPerPage = 10;
  const allJobsCache = ref<Job[]>([]);
  const fuse = ref<Fuse<Job> | null>(null);
  const hasMorePages = ref(true);
  const nextDatabasePage = ref(1);

  const previousFilters = ref({
    categories: [] as string[],
    sponsorship: SponsorshipFilter.ALL,
    faang: false,
    search: ''
  });

  const fuseOptions = {
    keys: [
      { name: 'title', weight: 2 },
      { name: 'company.name', weight: 1.5 },
      { name: 'locations', weight: 1.5 },
      { name: 'category', weight: 1.2 },
      { name: 'terms', weight: 1 }
    ],
    threshold: 0.4,
    includeScore: true,
    minMatchCharLength: 2,
    shouldSort: true
  };

  const deleteListing = async (listingId: string) => {
    if (!confirm('Are you sure you want to delete this listing? This action cannot be undone.')) {
      return;
    }

    deletingListingId.value = listingId;

    try {
      await axiosInstance.delete(`/listings/${listingId}`);

      const index = allJobsCache.value.findIndex(job => job.id === listingId);
      if (index > -1) {
        allJobsCache.value.splice(index, 1);
      }

      if (fuse.value) {
        fuse.value = new Fuse(allJobsCache.value, fuseOptions);
      }
    } catch (_err) {
      alert('Failed to delete listing. Please try again.');
    } finally {
      deletingListingId.value = null;
    }
  };

  const formatCategoryDisplay = (category: string): string => {
    const displayMap: { [key: string]: string } = {
      'Data Science, AI & Machine Learning': 'Data Science/AI/ML'
    };
    return displayMap[category] || category;
  };

  const fetchJobsFromDatabase = async (page: number): Promise<Job[]> => {
    try {
      const response = await axiosInstance.get('/listings/', {
        params: {
          page: page,
          page_size: 100
        }
      });

      if (response.data.results && response.data.results.length > 0) {
        return response.data.results;
      } else {
        return [];
      }
    } catch (_err) {
      error.value = 'Failed to load internships. Please try again later.';
      return [];
    }
  };

  const fetchInitialData = async () => {
    initialLoading.value = true;
    error.value = '';

    try {
      const firstPageJobs = await fetchJobsFromDatabase(1);
      allJobsCache.value = firstPageJobs.filter(job => job.active);
      nextDatabasePage.value = 2;

      while (allJobsCache.value.length < targetActiveJobsPerPage) {
        const nextPageJobs = await fetchJobsFromDatabase(nextDatabasePage.value);
        const activeJobs = nextPageJobs.filter(job => job.active);
        allJobsCache.value.push(...activeJobs);
        nextDatabasePage.value++;

        if (nextPageJobs.length === 0) {
          break;
        }
      }

      const options = {
        keys: [
          { name: 'title', weight: 2 },
          { name: 'company.name', weight: 1.5 },
          { name: 'locations', weight: 1.5 },
          { name: 'category', weight: 1.2 },
          { name: 'terms', weight: 1 }
        ],
        threshold: 0.4,
        includeScore: true,
        minMatchCharLength: 2,
        shouldSort: true
      };

      fuse.value = new Fuse(allJobsCache.value, options);
    } catch (_err) {
      error.value = 'Failed to load internships. Please try again later.';
    } finally {
      initialLoading.value = false;
    }
  };

  const loadMoreJobsForPage = async (targetPage: number): Promise<boolean> => {
    const neededJobsCount = targetPage * targetActiveJobsPerPage;

    while (allJobsCache.value.length < neededJobsCount) {
      const nextPageJobs = await fetchJobsFromDatabase(nextDatabasePage.value);
      const activeJobs = nextPageJobs.filter(job => job.active);
      allJobsCache.value.push(...activeJobs);
      nextDatabasePage.value++;

      if (fuse.value && activeJobs.length > 0) {
        fuse.value = new Fuse(allJobsCache.value, fuseOptions);
      }

      if (nextPageJobs.length === 0) {
        break;
      }
    }

    return allJobsCache.value.length >= neededJobsCount;
  };

  const loadJobsForFilters = async (): Promise<boolean> => {
    currentPage.value = 1;

    if (hasActiveFilters.value) {
      filtersLoading.value = true;

      try {
        const currentFilteredCount = filteredJobs.value.length;

        if (currentFilteredCount < targetActiveJobsPerPage && hasMorePages.value) {
          while (filteredJobs.value.length < targetActiveJobsPerPage && hasMorePages.value) {
            const nextPageJobs = await fetchJobsFromDatabase(nextDatabasePage.value);
            const activeJobs = nextPageJobs.filter(job => job.active);
            allJobsCache.value.push(...activeJobs);
            nextDatabasePage.value++;

            // FIX: Update the Fuse instance with the new data
            if (fuse.value && activeJobs.length > 0) {
              fuse.value = new Fuse(allJobsCache.value, fuseOptions);
            }

            if (nextPageJobs.length === 0) {
              hasMorePages.value = false;
              break;
            }

            if (nextDatabasePage.value > 20) {
              break;
            }
          }
        }

        return filteredJobs.value.length >= targetActiveJobsPerPage;
      } catch (_err) {
        error.value = 'Failed to load filtered internships. Please try again.';
        return false;
      } finally {
        filtersLoading.value = false;
      }
    }

    return true;
  };

  const goToPage = async (page: number) => {
    if (page < 1) return;

    if (hasActiveFilters.value && page > totalPages.value) return;

    pageLoading.value = true;

    try {
      const neededJobsCount = page * targetActiveJobsPerPage;

      if (allJobsCache.value.length < neededJobsCount) {
        const success = await loadMoreJobsForPage(page);
        if (!success && page > 1) {
          const lastAvailablePage = Math.max(1, Math.ceil(allJobsCache.value.length / targetActiveJobsPerPage));
          currentPage.value = lastAvailablePage;
          return;
        }
      }

      currentPage.value = page;
    } catch (_err) {
      error.value = 'Failed to load page. Please try again.';
    } finally {
      pageLoading.value = false;
    }
  };

  const filteredJobs = computed(() => {
    const query = searchQuery.value.trim();

    let filtered = allJobsCache.value;

    if (selectedCategories.value.length > 0) {
      filtered = filtered.filter(job => selectedCategories.value.includes(job.category));
    }

    if (sponsorshipFilter.value !== SponsorshipFilter.ALL) {
      filtered = filtered.filter(job => job.sponsorship === 'Offers Sponsorship');
    }

    if (selectedFAANG.value) {
      filtered = filtered.filter(job => job.faang_plus);
    }

    if (query && fuse.value) {
      const searchResults = fuse.value.search(query);
      filtered = searchResults.map(result => result.item);
    }

    return filtered.map(job => ({
      item: job,
      refIndex: allJobsCache.value.indexOf(job)
    }));
  });

  const hasActiveFilters = computed(() => {
    return (
      selectedCategories.value.length > 0 ||
      sponsorshipFilter.value !== SponsorshipFilter.ALL ||
      selectedFAANG.value ||
      searchQuery.value.trim() !== ''
    );
  });

  const totalPages = computed(() => {
    if (hasActiveFilters.value) {
      return Math.max(1, Math.ceil(filteredJobs.value.length / targetActiveJobsPerPage));
    } else {
      const basePages = Math.max(1, Math.ceil(filteredJobs.value.length / targetActiveJobsPerPage));
      return Math.max(basePages, currentPage.value + 1);
    }
  });

  const currentPageJobs = computed(() => {
    const startIndex = (currentPage.value - 1) * targetActiveJobsPerPage;
    const endIndex = startIndex + targetActiveJobsPerPage;
    return filteredJobs.value.slice(startIndex, endIndex);
  });

  const haveFiltersChanged = () => {
    return (
      JSON.stringify(selectedCategories.value) !== JSON.stringify(previousFilters.value.categories) ||
      sponsorshipFilter.value !== previousFilters.value.sponsorship ||
      selectedFAANG.value !== previousFilters.value.faang ||
      searchQuery.value !== previousFilters.value.search
    );
  };

  const areAllFiltersCleared = () => {
    return (
      selectedCategories.value.length === 0 &&
      sponsorshipFilter.value === SponsorshipFilter.ALL &&
      !selectedFAANG.value &&
      searchQuery.value.trim() === ''
    );
  };

  const saveCurrentState = () => {
    previousFilters.value = {
      categories: [...selectedCategories.value],
      sponsorship: sponsorshipFilter.value,
      faang: selectedFAANG.value,
      search: searchQuery.value
    };
  };

  watch(
    [selectedCategories, sponsorshipFilter, selectedFAANG, searchQuery],
    async () => {
      const filtersChanged = haveFiltersChanged();

      if (filtersChanged) {
        currentPage.value = 1;

        if (areAllFiltersCleared()) {
          saveCurrentState();
        } else {
          await loadJobsForFilters();
          saveCurrentState();
        }
      }
    },
    { deep: true }
  );

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

  const toggleCategory = (category: string) => {
    saveCurrentState();

    const index = selectedCategories.value.indexOf(category);
    if (index > -1) {
      selectedCategories.value.splice(index, 1);
    } else {
      selectedCategories.value.push(category);
    }
  };

  const toggleSponsorship = () => {
    saveCurrentState();

    sponsorshipFilter.value =
      sponsorshipFilter.value === SponsorshipFilter.ALL ? SponsorshipFilter.OFFERS : SponsorshipFilter.ALL;
  };

  const toggleFAANG = () => {
    saveCurrentState();
    selectedFAANG.value = !selectedFAANG.value;
  };

  onMounted(() => {
    fetchInitialData();
    saveCurrentState();
  });
</script>

<style scoped>
  .delete-btn {
    position: absolute;
    bottom: 13.25rem;
    left: 30rem;
    width: 30px;
    height: 20px;
    border: none;
    border-radius: 6px;
    background: #ff4444;
    color: white;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .delete-btn:hover:not(:disabled) {
    background: #cc0000;
  }

  .delete-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .loading {
    text-align: center;
    padding: 2rem;
    color: #d4862d;
    font-size: 1.2rem;
    font-family: 'Irish Grover', cursive;
    -webkit-text-stroke: 0.3px black;
  }

  .page-loading {
    text-align: center;
    padding: 1rem;
    color: #d4862d;
    font-size: 1.2rem;
    font-family: 'Irish Grover', cursive;
    -webkit-text-stroke: 0.3px black;
  }

  .error {
    text-align: center;
    padding: 2rem;
    color: #d4862d;
    font-size: 1.2rem;
    font-family: 'Irish Grover', cursive;
    -webkit-text-stroke: 0.3px black;
  }

  .retry-btn {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: #1e90ff;
    color: white;
    font-size: 1.1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-family: 'Irish Grover', cursive;
  }

  .retry-btn:hover {
    background: #a66a26;
  }

  .job-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
    position: relative;
  }

  .company-logo {
    width: 50px;
    height: 50px;
    object-fit: contain;
    border-radius: 4px;
    background: white;
    padding: 4px;
  }

  .job-meta {
    margin: 1rem 0;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .category-tag,
  .term-tag,
  .sponsorship-tag,
  .faang-tag {
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: bold;
  }

  .category-tag {
    background: rgba(30, 144, 255, 0.3);
    color: #aad4ff;
  }

  .term-tag {
    background: rgba(255, 165, 0, 0.3);
    color: #ffd699;
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
  }

  .home-container {
    width: 100vw;
    padding: 2rem;
    padding-top: 60px;
    color: #333;
    box-sizing: border-box;
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

  .filters-main-container {
    width: 60%;
    margin: 0 auto 2rem auto;
    display: flex;
    justify-content: center;
  }

  .filters-transform-enter-active,
  .filters-transform-leave-active {
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .filters-transform-enter-from {
    opacity: 0;
    transform: scale(0.8);
  }

  .filters-transform-enter-to {
    opacity: 1;
    transform: scale(1);
  }

  .filters-transform-leave-from {
    opacity: 1;
    transform: scale(1);
  }

  .filters-transform-leave-to {
    opacity: 0;
    transform: scale(0.8);
  }

  .filters-toggle-btn {
    padding: 0.7rem 2rem;
    background: transparent;
    border: 2px solid #d4862d;
    border-radius: 4px;
    color: white;
    font-family: 'Irish Grover', cursive;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
  }

  .filters-toggle-btn:hover {
    background: rgba(212, 134, 45, 0.2);
    color: white;
  }

  .toggle-icon {
    font-weight: bold;
    font-size: 1rem;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
  }

  .category-buttons-expanded {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0;
    width: 100%;
    border-radius: 4px;
    overflow: hidden;
    border: 2px solid #d4862d;
  }

  .filters-row-container {
    display: flex;
    width: 100%;
    gap: 10px;
    justify-content: center;
  }

  .category-buttons-single-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0;
    flex: 3;
    border-radius: 4px;
    overflow: hidden;
    border: 2px solid #d4862d;
  }

  .special-filters-table {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    border-radius: 4px;
    overflow: hidden;
    border: 2px solid #d4862d;
    flex: 1;
  }

  .category-btn {
    padding: 0.7rem 0.8rem;
    background: transparent;
    border: none;
    color: white;
    font-family: 'Irish Grover', cursive;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border-right: 2px solid #d4862d;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
    white-space: nowrap;
  }

  .special-filter-btn {
    padding: 0.7rem 0.8rem;
    background: transparent;
    border: none;
    color: white;
    font-family: 'Irish Grover', cursive;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000,
      -1px 0 0 #000,
      1px 0 0 #000,
      0 1px 0 #000,
      0 -1px 0 #000;
    white-space: nowrap;
    border-right: 2px solid #d4862d;
  }

  .special-filter-btn:last-child {
    border-right: none;
  }

  .special-filter-btn:hover {
    background: rgba(212, 134, 45, 0.2);
    color: white;
  }

  .special-filter-btn.selected {
    background: #d4862d;
    color: white;
  }

  .category-btn:hover {
    background: rgba(212, 134, 45, 0.2);
    color: white;
  }

  .category-btn.selected {
    background: #d4862d;
    color: white;
  }

  .filters-main-container {
    width: 100%;
    margin: 0 auto 2rem auto;
    display: flex;
    justify-content: center;
  }

  @media (max-width: 768px) {
    .filters-row-container {
      flex-direction: column;
      gap: 10px;
    }

    .category-buttons-single-row {
      grid-template-columns: repeat(3, 1fr);
      flex: 1;
    }

    .special-filters-table {
      grid-template-columns: 1fr 1fr;
      flex: 1;
    }

    .filters-main-container {
      width: 90%;
    }

    .company-logo {
      width: 40px;
      height: 40px;
    }

    .job-header h2 {
      font-size: 1.1rem;
      margin-right: 0.5rem;
    }

    .delete-btn {
      width: 35px;
      height: 35px;
      font-size: 1.3rem;
      bottom: 1rem;
      left: 1rem;
    }
  }

  .category-btn:hover {
    background: rgba(212, 134, 45, 0.2);
    color: white;
  }

  .category-btn.selected {
    background: #d4862d;
    color: white;
  }

  .job-listings {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    padding: 2rem 0;
    width: 70%;
    margin: 0 auto;
    box-sizing: border-box;
    align-items: stretch;
  }

  .job-card {
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
    position: relative;
    min-height: 250px;
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

  .job-content,
  .apply-button {
    position: relative;
    z-index: 1;
  }

  .job-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
  }

  .no-results {
    grid-column: 1 / -1;
    text-align: center;
    font-size: 2rem;
    color: #d4862d;
    font-family: 'Irish Grover', cursive;
    -webkit-text-stroke: 0.3px black;
  }

  h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
    color: #fff;
    flex: 1;
    margin-right: 1rem;
  }

  .company {
    color: #aad4ff;
    font-weight: bold;
    margin-bottom: 0.3rem;
  }

  .posted-date {
    font-size: 0.875rem;
    color: #cce0ff;
    margin-bottom: 0.5rem;
  }

  .description {
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
    color: #ddeeff;
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
  }

  .job-card:hover .apply-button:not(:hover) {
    background-color: #a66a26;
    transition: background-color 0.6s ease;
  }

  .filters-wrapper {
    min-height: 0px;
    margin-bottom: 2rem;
  }

  .apply-button:hover {
    background-color: #734d22;
    transition: background-color 0.25s ease;
  }

  .pagination-controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
    padding: 1rem;
  }

  .pagination-btn {
    padding: 0.5rem 1rem;
    background: transparent;
    border: 2px solid #d4862d;
    border-radius: 4px;
    color: white;
    font-family: 'Irish Grover', cursive;
    cursor: pointer;
    transition: all 0.3s ease;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000;
  }

  .pagination-btn:hover:not(:disabled) {
    background: rgba(212, 134, 45, 0.2);
  }

  .pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .page-info {
    color: white;
    font-family: 'Irish Grover', cursive;
    font-size: 1rem;
    text-shadow:
      -1px -1px 0 #000,
      -1px 1px 0 #000,
      1px -1px 0 #000,
      1px 1px 0 #000;
  }

  @media (max-width: 768px) {
    .filters-main-container {
      width: 90%;
    }

    .category-buttons-expanded {
      grid-template-columns: 1fr;
    }

    .job-listings {
      width: 90%;
      grid-template-columns: 1fr;
    }

    .pagination-controls {
      flex-direction: column;
      gap: 0.5rem;
    }
  }
</style>
