FROM mcr.microsoft.com/playwright:v1.40.0-focal
WORKDIR /app
RUN useradd -m scraper && chown -R scraper:scraper /app
USER scraper
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scraper/ ./scraper/
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright PYTHONUNBUFFERED=1
CMD ["python", "-m", "scraper.main"]
