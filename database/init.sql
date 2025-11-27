-- ============================
-- Users
-- ============================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE
);

-- ============================
-- Profiles
-- ============================
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name TEXT,
    major TEXT,
    grad_year INT,
    linkedin_url TEXT,
    bio TEXT,
    image_url TEXT,
    public BOOLEAN NOT NULL DEFAULT FALSE
);

ALTER TABLE profiles
ADD CONSTRAINT public_requires_full_name
CHECK (
    NOT public OR (full_name IS NOT NULL AND full_name <> '')
);

-- ============================
-- Internships
-- ============================
CREATE TABLE internships (
    id SERIAL PRIMARY KEY,
    profile_id INT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    time_period TEXT[] NOT NULL DEFAULT '{}'  -- e.g. ["Summer 2024"]
);

-- ============================
-- Companies
-- ============================
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    url TEXT NOT NULL,
    logo_url TEXT
);

-- ============================
-- Listings
-- ============================
CREATE TABLE listings (
    id UUID PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    active BOOLEAN NOT NULL,
    date_updated TIMESTAMPTZ NOT NULL,
    is_visible BOOLEAN NOT NULL,
    date_posted TIMESTAMPTZ NOT NULL,
    url TEXT NOT NULL,
    locations TEXT[] NOT NULL,
    terms TEXT[] NOT NULL,
    sponsorship TEXT NOT NULL,
    category TEXT NOT NULL,
    faang_plus BOOLEAN NOT NULL,
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE
);

-- ============================
-- Favorites
-- ============================
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    listing_id UUID REFERENCES listings(id) ON DELETE CASCADE
);

ALTER TABLE favorites
ADD CONSTRAINT favorites_user_listing_key
UNIQUE (user_id, listing_id);
