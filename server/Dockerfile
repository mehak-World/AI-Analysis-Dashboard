FROM node:22-alpine

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY package*.json ./

RUN npm ci --omit=dev

# Copy application code
COPY . .

EXPOSE 3000

CMD ["npm", "start"]