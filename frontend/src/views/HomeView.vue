<template>
    <div class="home-container">
        <h1>
            <span class="orange-text">Orange</span> and
            <span class="blue-text">Blue</span> Collar
        </h1>

        <!-- Search bar -->
        <input type="text"
               v-model="searchQuery"
               placeholder="Search internships..."
               class="search-bar"
               aria-label="Search internships" />

        <div class="job-listings">
            <div v-for="job in filteredJobs"
                 :key="job.id"
                 class="job-card">
                <div class="job-content">
                    <h2>{{ job.title }}</h2>
                    <p class="company">{{ job.company }} — {{ job.location }}</p>
                    <p class="posted-date">Posted: {{ job.postedDate }}</p>
                    <p class="description">{{ job.description }}</p>
                </div>
                <a :href="job.applyLink"
                   target="_blank"
                   class="apply-button">Apply Now</a>
            </div>

            <p v-if="filteredJobs.length === 0" class="no-results">
                No internships available.
            </p>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { ref, computed } from "vue";

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
            title: "Frontend Developer Intern",
            company: "Techify",
            location: "Remote",
            postedDate: "2025-10-10",
            description: "Work with our team to build user-facing features using Vue.js.",
            applyLink: "https://techify.com/careers/frontend-intern",
        },
        {
            id: 2,
            title: "Backend Engineer Intern",
            company: "CloudNova",
            location: "San Francisco, CA",
            postedDate: "2025-10-08",
            description: "Assist in developing scalable APIs using Node.js and MongoDB.",
            applyLink: "https://cloudnova.io/jobs/backend-intern",
        },
        {
            id: 3,
            title: "Data Analyst Intern",
            company: "InsightsLab",
            location: "Remote",
            postedDate: "2025-10-05",
            description: "Analyze data trends and support business decision-making.",
            applyLink: "https://insightslab.org/internships/data-analyst",
        },
        {
            id: 4,
            title: "Data Science Intern",
            company: "LabbyLabs",
            location: "Remote",
            postedDate: "2025-11-05",
            description: "I don't even know what one does here.",
            applyLink: "https://insightslab.org/internships/data-analyst",
        },
    ];

    const searchQuery = ref("");

    const filteredJobs = computed(() => {
        const query = searchQuery.value.trim().toLowerCase();
        if (!query) return jobs;

        return jobs.filter((job) => {
            return (
                job.title.toLowerCase().includes(query) ||
                job.company.toLowerCase().includes(query) ||
                job.location.toLowerCase().includes(query)
            );
        });
    });
</script>

<style scoped>
    /* Container */
    .home-container {
        width: 100vw;
        padding: 2rem;
        padding-top: 60px;
        color: #333;
        box-sizing: border-box;
    }

    /* Heading */
    h1 {
        font-family: 'Irish Grover', cursive;
        text-shadow: -2px -2px 0 #000, -2px 2px 0 #000, 2px -2px 0 #000, 2px 2px 0 #000, -2px 0 0 #000, 2px 0 0 #000, 0 2px 0 #000, 0 -2px 0 #000;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 7rem;
        color: white;
    }

    .orange-text {
        color: #FFA500;
    }

    .blue-text {
        color: #1e90ff;
    }

    /* Search Bar */
    .search-bar {
        display: block;
        width: 100%;
        max-width: 600px;
        margin: 0 auto 2rem auto;
        padding: 0.6rem 1rem;
        font-size: 1rem;
        border-radius: 8px;
        border: 1.5px solid #1e90ff;
        outline: none;
        transition: border-color 0.3s ease;
    }

        .search-bar:focus {
            border-color: #106fcc;
        }

    /* Job Listings Container — vertical layout */
    .job-listings {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        padding: 2rem 0;
        width: 100%;
        box-sizing: border-box;
        overflow: hidden;
    }

    /* Job Card */
    .job-card {
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        background: #003366;
        border-radius: 10px;
        padding: 2rem;
        padding-bottom: 3.5rem; /* extra space for button */
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease;
        color: white;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        position: relative;
    }

        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
        }

    /* Job Content */
    .job-content {
        display: flex;
        flex-direction: column;
    }

    /* Job Card Text */
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

    /* Apply Button */
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
        transition: background-color 0.3s ease;
    }

        .apply-button:hover {
            background-color: #106fcc;
        }

    /* No results */
    .no-results {
        flex: 1 0 100%;
        text-align: center;
        font-style: italic;
        color: #cce0ff;
    }
</style>
