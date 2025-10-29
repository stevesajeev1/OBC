<template>
    <div class="home-container">
        <h1><span class="orange-text">Orange</span> and <span class="blue-text">Blue</span> Collar</h1>

        <!-- Search bar -->
        <input type="text"
               v-model="searchQuery"
               placeholder="Search for open internship opportunities!"
               class="search-bar"
               aria-label="Search for open internship opportunities" />

        <!-- Filters Container -->
        <div class="filters-container">
            <transition name="filters-transform" mode="out-in">
                <!-- Filter options when expanded -->
                <div v-if="showFilters" class="category-buttons-expanded" key="filters">
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
                            :class="{ selected: selectedCategories.includes('Data Science/AI/ML') }"
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

                <!-- Filter button when collapsed -->
                <button v-else class="filters-toggle-btn" @click="showFilters = true" key="button">
                    Filters
                    <span class="toggle-icon">+</span>
                </button>
            </transition>
        </div>

        <div class="job-listings">
            <div v-for="job in filteredJobs" :key="job.item.id" class="job-card">
                <div class="job-content">
                    <h2>{{ job.item.title }}</h2>
                    <p class="company">{{ job.item.company }} — {{ job.item.location }}</p>
                    <p class="posted-date">Posted: {{ job.item.postedDate }}</p>
                    <p class="description">{{ job.item.description }}</p>
                </div>
                <a :href="job.item.applyLink" target="_blank" class="apply-button">Apply Now</a>
            </div>

            <p v-if="filteredJobs.length === 0" class="no-results">No internships available.</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { ref, computed, onMounted } from 'vue';
    import Fuse from 'fuse.js';

    interface Job {
        id: number;
        title: string;
        company: string;
        location: string;
        postedDate: string;
        description: string;
        applyLink: string;
    }

    const jobs: Job[] = [
        {
            id: 1,
            title: 'Frontend Developer Intern',
            company: 'Techify',
            location: 'Remote',
            postedDate: '2025-10-10',
            description: 'Work with our team to build user-facing features using Vue.js.',
            applyLink: 'https://techify.com/careers/frontend-intern'
        },
        {
            id: 2,
            title: 'Backend Engineer Intern',
            company: 'CloudNova',
            location: 'San Francisco, CA',
            postedDate: '2025-10-08',
            description: 'Assist in developing scalable APIs using Node.js and MongoDB.',
            applyLink: 'https://cloudnova.io/jobs/backend-intern'
        },
        {
            id: 3,
            title: 'Data Analyst Intern',
            company: 'InsightsLab',
            location: 'Remote',
            postedDate: '2025-10-05',
            description: 'Analyze data trends and support business decision-making.',
            applyLink: 'https://insightslab.org/internships/data-analyst'
        },
        {
            id: 4,
            title: 'Data Science Intern',
            company: 'LabbyLabs',
            location: 'Remote',
            postedDate: '2025-11-05',
            description: "I don't even know what one does here.",
            applyLink: 'https://insightslab.org/internships/data-analyst'
        }
    ];

    const searchQuery = ref('');
    const selectedCategories = ref<string[]>([]);
    const showFilters = ref(false);
    const fuse = ref<Fuse<Job> | null>(null);

    onMounted(() => {
        const options = {
            keys: [
                {
                    name: 'title',
                    weight: 2
                },
                {
                    name: 'company',
                    weight: 1.5
                },
                {
                    name: 'location',
                    weight: 1.5
                },
                {
                    name: 'description',
                    weight: 1
                }
            ],
            threshold: 0.4,
            includeScore: true,
            minMatchCharLength: 1,
            shouldSort: true
        };

        fuse.value = new Fuse(jobs, options);
    });

    const toggleCategory = (category: string) => {
        const index = selectedCategories.value.indexOf(category);
        if (index > -1) {
            selectedCategories.value.splice(index, 1);
        } else {
            selectedCategories.value.push(category);
        }
    };

    const filteredJobs = computed(() => {
        const query = searchQuery.value.trim();

        if (!query) return jobs.map(job => ({ item: job, refIndex: job.id - 1 }));

        if (!fuse.value) return [];

        const results = fuse.value.search(query);
        return results;
    });
</script>

<style scoped>
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
        /* Text outline for better readability */
        text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
        /* Fix text cutoff */
        text-indent: 2px; /* Add space from left edge */
        box-sizing: border-box; /* Ensure padding is included in width */
    }

        .search-bar::placeholder {
            color: white;
            font-family: 'Irish Grover', cursive;
            /* Text outline for placeholder text */
            text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
            /* Fix placeholder positioning */
            text-indent: 8px;
        }

        .search-bar:focus,
        .search-bar:hover {
            border-color: #d4862d;
            background: rgba(255, 255, 255, 0.1);
        }

    .filters-container {
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
        color: white; /* Changed from rgba(255, 255, 255, 0.75) to white */
        font-family: 'Irish Grover', cursive;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        /* Text outline for better readability */
        text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
    }



        .filters-toggle-btn:hover {
            background: rgba(212, 134, 45, 0.2);
            color: white;
        }

    .toggle-icon {
        font-weight: bold;
        font-size: 1rem;
        /* Text outline for the toggle icon */
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

    .category-btn {
        padding: 0.7rem 0.4rem;
        background: transparent;
        border: none;
        color: white; /* Changed from rgba(255, 255, 255, 0.75) to white */
        font-family: 'Irish Grover', cursive;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border-right: 2px solid #d4862d;
        /* Text outline for better readability */
        text-shadow: -1px -1px 0 #000, -1px 1px 0 #000, 1px -1px 0 #000, 1px 1px 0 #000, -1px 0 0 #000, 1px 0 0 #000, 0 1px 0 #000, 0 -1px 0 #000;
    }

        .category-btn:last-child {
            border-right: none;
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
        width: 60%;
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
        font-style: italic;
        color: #cce0ff;
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

    /* Orange when job card is hovered but apply button is not */
    .job-card:hover .apply-button:not(:hover) {
        background-color: #a66a26;
        transition: background-color 0.6s ease;
    }

    /* Dark brown when apply button is hovered (regardless of job card hover) */
    .apply-button:hover {
        background-color: #734d22;
        transition: background-color 0.25s ease;
    }

    @media (max-width: 768px) {
        .filters-container {
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