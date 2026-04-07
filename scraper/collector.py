class StatsCollector:
    def __init__(self):
        self.data = {
            "junior": {},
            "middle": {},
            "senior": {},
            "not specified": {},
        }
        self.cache_skills = {
            "python",
            "sql",
            "postgresql",
            "github",
            "git",
            "html",
            "css",
            "django",
            "fastapi",
            "aws",
            "asyncio",
            "docker",
            "javascript",
            "react",
            "django rest framework",
            "flask",
            "typescript",
        }
        self.synonyms = {
            "js": "javascript",
            "ts": "typescript",
            "node.js": "nodejs",
            "next.js": "nextjs",
            "react.js": "react",
            "reactjs": "react",
            "react-js": "react",
            "drf": "django rest framework",
            "fast api": "fastapi",
            "aws": "amazon web services",
            "beautiful soup": "beautifulsoup",
            "bs4": "beautifulsoup",
            "postgres": "postgresql",
            "postgre": "postgresql",
            "pl/sql": "sql",
            "mongo": "mongodb",
            "ms sql server": "mssql",
            "oracle database": "oracle",
            "google cloud platform": "googlecp",
            "google cloud": "googlecp",
            "ms azure": "azure",
            "docker compose": "docker compose",
            "docker-compose": "docker compose",
            "github actions": "ci/cd",
            "c/c++": "c++",
            "cpp": "c++",
        }

        self.exclude_words = {
            "responsibility",
            "troubleshooting",
            "agile",
            "scrum",
            "english",
            "http",
            "json",
            "xml",
            "rest",
            "rest api",
            "web api",
            "restful",
            "csv",
            "performance optimization",
            "solid principles",
            "work with the database",
            "confluence",
        }

    def add_skill(self, level, skill):
        if skill in self.exclude_words:
            return
        normalized = self.synonyms.get(skill, skill)

        self.data[level][normalized] = self.data[level].get(normalized, 0) + 1


stats_storage = StatsCollector()
