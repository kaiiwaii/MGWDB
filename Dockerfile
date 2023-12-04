FROM node:20-alpine AS runner

WORKDIR /app

COPY . .

EXPOSE 3000

CMD ["npm", "run", "preview"]