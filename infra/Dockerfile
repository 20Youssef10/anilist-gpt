FROM node:20-alpine

WORKDIR /app

COPY apps/mcp-server/package.json apps/mcp-server/package-lock.json* ./
RUN npm install

COPY apps/mcp-server ./
RUN npm run build

EXPOSE 3000
CMD ["node", "dist/index.js"]
