FROM node:20-slim

WORKDIR /project/frontend

# Install dependencies first (for caching)
COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]