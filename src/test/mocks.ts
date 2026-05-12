import type { GithubRepo, GithubUser } from "../types/github";

// Real data from github.com/piyush-eon
export const mockUser: GithubUser = {
  login: "vidyakumari123",
  name: "VIDYA KUMARI",
  avatar_url: "https://avatars.githubusercontent.com/u/51760520",
  bio: "👩‍💻 Frontend Developer | MERN Stack ⚡ Passionate about building modern web apps 🚀 Always learning & growing 🎓 MCA @ NIT Raipur",
  location: "India",
  public_repos: 60,
  followers: 3200,
  following: 0,
  html_url: "https://github.com/vidyakumari123",
};

// User with all optional fields as null — for testing conditional rendering
export const mockUserMinimal: GithubUser = {
  login: "ghost",
  name: null,
  avatar_url: "https://avatars.githubusercontent.com/u/99999",
  bio: null,
  location: null,
  public_repos: 0,
  followers: 0,
  following: 0,
  html_url: "https://github.com/vidyakumari123",
};

// Real repos from piyush-eon — mix of with/without description and language
export const mockRepos: GithubRepo[] = [
  {
    id: 1,
    name: "ai-interview-platform",
    description:
      "Full Stack Interview Platform with Next JS, Supabase, Tailwind, Stream, Arcjet, Shadcn UI Tutorial",
    stargazers_count: 6,
    language: "JavaScript",
    html_url: "https://github.com/vidyakumari123/AI-Interview",
  },
  {
    id: 2,
    name: "React-19",
    description: null,
    stargazers_count: 10,
    language: null,
    html_url: "https://github.com/vidyakumari123/React-19",
  },
  {
    id: 3,
    name: "TypeScript",
    description: "This repository contains a structured introduction to TypeScript. It is organized as a sequence of example files under src/, where each file focuses on a single concept and shows hands-on code samples",
    stargazers_count: 7,
    language: "TypeScript",
    html_url: "https://github.com/vidyakumari123/TypeScript",
  },
];