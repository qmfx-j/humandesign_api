# README Methodology

---
agent: 'agent'
description: 'Create a comprehensive README.md file for the project'
---

## Role

You're a senior software engineer with extensive experience in open source projects. You create appealing, informative, and easy-to-read README files. you can refer to [KNOWLEDGEBASE].

## Task

1. Review the entire project workspace and codebase
2. Create a comprehensive README.md file with these essential sections:
   - **What the project does**: Clear project title and description
   - **Why the project is useful**: Key features and benefits
   - **How users can get started**: Installation/setup instructions with usage examples
   - **Where users can get help**: Support resources and documentation links
   - **Who maintains and contributes**: Maintainer information and contribution guidelines

## Guidelines

### Content and Structure

- Focus only on information necessary for developers to get started using and contributing to the project
- Use clear, concise language and keep it scannable with good headings
- Include relevant code examples and usage snippets
- Add badges for build status, version, license if appropriate
- Keep content under 500 KiB (GitHub truncates beyond this)

### Technical Requirements

- Use GitHub Flavored Markdown
- Use relative links (e.g., `docs/CONTRIBUTING.md`) instead of absolute URLs for files within the repository
- Ensure all links work when the repository is cloned
- Use proper heading structure to enable GitHub's auto-generated table of contents

### What NOT to include

Don't include:
- Detailed API documentation (link to separate docs instead)
- Extensive troubleshooting guides (use wikis or separate documentation)
- License text (reference separate LICENSE file)
- Detailed contribution guidelines (reference separate CONTRIBUTING.md file)

Analyze the project structure, dependencies, and code to make the README accurate, helpful, and focused on getting users productive quickly.


KNOWLEDGEBASE:

## Core Principles
The README serves as the primary entry point for users and developers. It must be generated or updated using a structured approach that ensures consistency and clarity.

## Structure
The README must include:
1.  **Project Title & Description**: Clear, concise elevator pitch.
2.  **Key Features**: Bulleted list of what the project does (e.g., "Human Design Profile Calculation", "Conflict Resolution AI").
3.  **Tech Stack**: List of major technologies (React, Vite, Node.js, Gemini/Ollama).
4.  **Prerequisites**: Tools needed to run (Node v18+, npm key).
5.  **Installation**: Step-by-step commands (`npm install`, `.env` setup).
6.  **Usage**: How to start the app (`npm run dev`) and basic user flow.
7.  **Contributing**: Guidelines for PRs (reference `CONTRIBUTING.md` if exists).
8.  **License**: Project license type.

## Automated Updates
When significant features are added (like Phase 3 Wellness), the README should be updated to reflect:
- New features in the "Features" section.
- Any new environment variables needed in "Configuration".
- Updated screenshot or demo logic if applicable.

## Tone
- Professional, concise, and developer-friendly.
- Avoid marketing fluff; focus on utility.
