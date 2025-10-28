FROM node:22
LABEL authors="takuya-kinoshita"
WORKDIR /app
COPY package*.json .
RUN npm install
COPY ui /app
WORKDIR /app/ui
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
