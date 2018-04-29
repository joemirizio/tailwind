FROM node

RUN npm install yarn

COPY ./package.json ./*lock* ./
RUN yarn install

COPY . .

EXPOSE 80

RUN yarn run build

CMD ["yarn", "start"]
