<template>
    <div class="home-container">
        <h1><span class="orange-text">Orange</span> and <span class="blue-text">Blue</span> Collar</h1>

        <input type="text"
               v-model="searchQuery"
               placeholder="Search for open internship opportunities!"
               class="search-bar"
               aria-label="Search for open internship opportunities" />

        <div class="filters-wrapper">
            <div class="filters-main-container">
                <transition name="filters-transform" mode="out-in">
                    <div v-if="showFilters" key="filters-container" class="filters-row-container">
                        <div class="category-buttons-single-row">
                            <button class="category-btn"
                                    :class="{ selected: selectedCategories.includes('Software Engineering') }"
                                    @click="toggleCategory('Software Engineering')">
                                Software Engineering
                            </button>
                            <button class="category-btn"
                                    :class="{ selected: selectedCategories.includes('Product Management') }"
                                    @click="toggleCategory('Product Management')">
                                Product Management
                            </button>
                            <button class="category-btn"
                                    :class="{ selected: selectedCategories.includes('Data Science, AI & Machine Learning') }"
                                    @click="toggleCategory('Data Science/AI/ML')">
                                Data Science/AI/ML
                            </button>
                            <button class="category-btn"
                                    :class="{ selected: selectedCategories.includes('Quantitative Finance') }"
                                    @click="toggleCategory('Quantitative Finance')">
                                Quantitative Finance
                            </button>
                            <button class="category-btn"
                                    :class="{ selected: selectedCategories.includes('Hardware Engineering') }"
                                    @click="toggleCategory('Hardware Engineering')">
                                Hardware Engineering
                            </button>
                        </div>

                        <!-- New 1 row 2 column table for FAANG+ and Sponsorship -->
                        <div class="special-filters-table">
                            <button class="special-filter-btn"
                                    :class="{ selected: sponsorshipFilter !== 'all' }"
                                    @click="toggleSponsorship()">
                                Sponsorship
                            </button>
                            <button class="special-filter-btn"
                                    :class="{ selected: selectedFAANG }"
                                    @click="toggleFAANG()">
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

        <!-- Loading state -->
        <div v-if="loading" class="loading">
            Loading internships...
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="error">
            {{ error }}
            <button @click="fetchInternships" class="retry-btn">Retry</button>
        </div>

        <!-- Success state -->
        <div v-else class="job-listings">
            <div v-for="job in filteredJobs" :key="job.item.id" class="job-card">
                <div class="job-content">
                    <h2>{{ job.item.title }}</h2>
                    <p class="company">{{ job.item.company.name }} — {{ formatLocations(job.item.locations) }}</p>
                    <p class="posted-date">Posted: {{ formatDate(job.item.date_posted) }}</p>
                    <div class="job-meta">
                        <span v-if="job.item.category" class="category-tag">{{ formatCategoryDisplay(job.item.category) }}</span>
                        <span v-for="term in job.item.terms.slice(0, 2)" :key="term" class="term-tag">{{ term }}</span>
                        <span v-if="job.item.sponsorship && job.item.sponsorship !== 'Other'" class="sponsorship-tag">{{ job.item.sponsorship }}</span>
                        <span v-if="job.item.faang_plus" class="faang-tag">FAANG+</span>
                    </div>
                    <p class="source">Source: {{ job.item.source }}</p>
                </div>
                <a :href="job.item.url" target="_blank" class="apply-button">Apply Now</a>
            </div>

            <p v-if="filteredJobs.length === 0 && !loading" class="no-results">
                {{ jobs.length === 0 ? 'No internships available.' : 'No internships match your search.' }}
            </p>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { ref, computed, onMounted } from 'vue';
    import Fuse from 'fuse.js';
    import axios from 'axios';

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

    interface PaginatedResponse<T> {
        data: T[];
        total: number;
        page: number;
        pageSize: number;
        totalPages: number;
    }

    // Reactive data
    const jobs = ref<Job[]>([]);
    const searchQuery = ref('');
    const selectedCategories = ref<string[]>([]);
    const showFilters = ref(false);
    const loading = ref(false);
    const error = ref('');
    const fuse = ref<Fuse<Job> | null>(null);
    const selectedSponsorships = ref<string[]>([]);
    const selectedFAANG = ref(false);

    // API configuration - adjust port if different
    const API_BASE_URL = 'http://localhost:8000';

    // Add this function to format category display names
    const formatCategoryDisplay = (category: string): string => {
        const displayMap: { [key: string]: string } = {
            'Data Science, AI & Machine Learning': 'Data Science/AI/ML'
            // Add other mappings if needed
        };
        return displayMap[category] || category;
    };

    // Fetch internships from backend
    const fetchInternships = async () => {
        loading.value = true;
        error.value = '';
        console.log('All categories:', [...new Set(jobs.value.map(job => job.category))]);

        try {
            const response = await axios.get(`${API_BASE_URL}/listings/`, {
                params: {
                    pageSize: 200 // Get more listings at once
                }
            });

            // Extract data from the 'results' field instead of 'data'
            jobs.value = response.data.results; // ← CHANGE THIS LINE

            // Initialize Fuse.js with the fetched data
            const options = {
                keys: [
                    {
                        name: 'title',
                        weight: 2
                    },
                    {
                        name: 'company.name',
                        weight: 1.5
                    },
                    {
                        name: 'locations',
                        weight: 1.5
                    },
                    {
                        name: 'category',
                        weight: 1.2
                    },
                    {
                        name: 'terms',
                        weight: 1
                    }
                ],
                threshold: 0.4,
                includeScore: true,
                minMatchCharLength: 2,
                shouldSort: true
            };

            fuse.value = new Fuse(jobs.value, options);
        } catch (err) {
            console.error('Error fetching internships:', err);
            error.value = 'Failed to load internships. Please try again later.';
        } finally {
            loading.value = false;
        }
    };

    // Format date for display
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

    // Format locations array
    const formatLocations = (locations: string[]) => {
        if (!locations || locations.length === 0) return 'Remote';
        return locations.join(', ');
    };

    const toggleCategory = (category: string) => {
        // Map frontend display names to backend category names
        const categoryMap: { [key: string]: string } = {
            'Data Science/AI/ML': 'Data Science, AI & Machine Learning'
            // Add other mappings if needed
        };

        const backendCategory = categoryMap[category] || category;

        const index = selectedCategories.value.indexOf(backendCategory);
        if (index > -1) {
            selectedCategories.value.splice(index, 1);
        } else {
            selectedCategories.value.push(backendCategory);
        }
    };

    // Change from array to single value
    const sponsorshipFilter = ref<'all' | 'offers' | 'none'>('all');

    const toggleSponsorship = () => {
        sponsorshipFilter.value = sponsorshipFilter.value === 'all' ? 'offers' : 'all';
    };

    // Update the filteredJobs computed function:
    const filteredJobs = computed(() => {
        const query = searchQuery.value.trim();

        let filtered = jobs.value.filter(job => job.is_visible);

        // Apply category filter if any categories selected
        if (selectedCategories.value.length > 0) {
            filtered = filtered.filter(job =>
                selectedCategories.value.includes(job.category)
            );
        }

        // Apply sponsorship filter (updated)
        if (sponsorshipFilter.value !== 'all') {
            filtered = filtered.filter(job =>
                sponsorshipFilter.value === 'offers'
                    ? job.sponsorship === 'Offers Sponsorship'
                    : job.sponsorship === 'Does Not Offer Sponsorship'
            );
        }

        // Apply FAANG+ filter
        if (selectedFAANG.value) {
            filtered = filtered.filter(job => job.faang_plus);
        }

        // Apply search query if any
        if (query && fuse.value) {
            const searchResults = fuse.value.search(query);
            filtered = searchResults
                .map(result => result.item)
                .filter(job => filtered.includes(job));
        }

        return filtered.map(job => ({
            item: job,
            refIndex: jobs.value.indexOf(job)
        }));
    });

    const toggleFAANG = () => {
        selectedFAANG.value = !selectedFAANG.value;
    };

    onMounted(() => {
        fetchInternships();
    });
</script>

<style scoped>
    /* Add these new styles for loading and error states */
    .loading {
        text-align: center;
        padding: 2rem;
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
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-family: 'Irish Grover', cursive;
    }

        .retry-btn:hover {
            background: #a66a26;
        }

    .job-meta {
        margin: 1rem 0;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .category-tag, .term-tag, .sponsorship-tag, .faang-tag {
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

    /* Keep all your existing styles below */
    .home-container {
        width: 100vw;
        padding: 2rem;
        padding-top: 60px;
        color: #333;
        box-sizing: border-box;
    }

    h1 {
        font-family: 'Irish Grover', cursive;
        text-shadow: -2px -2px 0 #000, -2px 2px 0 #000, 2px -2px 0 #000, 2px 2px 0 #000, -2px 0 0 #000, 2px 0 0 #000, 0 2px 0 #000, 0 -2px 0 #000, 2px 2px 4px rgba(0, 0, 0, 0.5);
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
        transition: border-color 0.3s ease, background 0.3s ease;
        background: transparent;
        color: white;
        backdrop-filter: blur(5px);
        text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
        text-indent: 2px;
        box-sizing: border-box;
    }

        .search-bar::placeholder {
            color: white;
            font-family: 'Irish Grover', cursive;
            text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
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
        text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
    }

        .filters-toggle-btn:hover {
            background: rgba(212, 134, 45, 0.2);
            color: white;
        }

    .toggle-icon {
        font-weight: bold;
        font-size: 1rem;
        text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
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
        flex: 3; /* Increased from 2 to 3 */
        border-radius: 4px;
        overflow: hidden;
        border: 2px solid #d4862d;
    }

    /* New styles for the special filters table */
    .special-filters-table {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0;
        border-radius: 4px;
        overflow: hidden;
        border: 2px solid #d4862d;
        flex: 1; /* Kept at 1 */
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
        text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
        white-space: nowrap;
    }

    .special-filter-btn {
        padding: 0.7rem 0.8rem; /* Reduced from 1.5rem to 0.8rem */
        background: transparent;
        border: none;
        color: white;
        font-family: 'Irish Grover', cursive;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
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

    /* Remove or update the container width restriction */
    .filters-main-container {
        width: 100%; /* Change from 60% to 100% */
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
            flex: 1; /* Reset flex on mobile */
        }

        .special-filters-table {
            grid-template-columns: 1fr 1fr;
            flex: 1; /* Reset flex on mobile */
        }

        .filters-main-container {
            width: 90%; /* Keep some restriction on mobile */
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
        color: #cce0ff;
        font-family: 'Irish Grover', cursive;
        -webkit-text-stroke: 0.3px black;
    }

    h2 {
        margin: 0 0 0.5rem 0;
        font-size: 1.25rem;
        color: #fff;
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
        min-height: 0px; /* This reserves space for expanded filters */
        margin-bottom: 2rem;
    }

    .apply-button:hover {
        background-color: #734d22;
        transition: background-color 0.25s ease;
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
    }
</style>