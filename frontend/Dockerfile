FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN yarn install

# Copy the application code
COPY . .

# Build the application
RUN yarn build

# Install serve to serve the application
RUN yarn global add serve

# Expose the port the app runs on
EXPOSE 8080

# Run the application with the --single flag
# CMD ["serve", "-s", "dist", "-l", "8080", "--single"]
CMD ["yarn", "dev"]
