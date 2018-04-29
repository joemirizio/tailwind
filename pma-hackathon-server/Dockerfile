FROM node

RUN npm install yarn

COPY ./package.json ./*lock* ./
RUN yarn install

COPY . .

EXPOSE 8000

CMD ["yarn", "start"]
