FROM node:16
WORKDIR /app
COPY . .
RUN npm install
RUN npm install axios@0.27.2
RUN npm install --save-dev jest @testing-library/react @testing-library/jest-dom
CMD ["npm", "start"]
