require('./open-telemetry.js');

const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');

const authors = [
  {
    id: '1',
    name: 'Kate Chopin',
  },
  {
    id: '2',
    name: 'Paul Auster',
  },
];

const publishers = [
  {
    id: '1',
    name: 'Penguinn',
  },
];

const books = [
  {
    id: '1',
    title: 'What is Vibe Coding',
    authorId: '1',
    publisherId: '1'
  },
  {
    id: '2',
    title: 'Help! Im Drowning in the Javascript Ecosystem',
    authorId: '2',
    publisherId: '1'
  },
    {
    id: '3',
    title: 'The 1 Billion Dollar Vibe Coding Company',
    authorId: '2',
    publisherId: '1'
  },
];

const typeDefs = `#graphql
  type Author {
    id: ID!
    name: String
  }

  type Publisher {
    id: ID!
    name: String
  }

  type Book {
    id: ID!
    title: String
    author: Author
    publisher: Publisher
  }

  type Query {
    books: [Book]
    authors: [Author]
    publisers: [Publisher]
  }
`;

const resolvers = {
  Query: {
    books: () => books,
    authors: () => authors,
  },
  Book: {
    author: async (parent) => {
      console.log("author called!")
      await new Promise(resolve => setTimeout(resolve, 1000));
      return authors.find(author => author.id === parent.authorId);
    },
    publisher: async (parent) => {
      await new Promise(resolve => setTimeout(resolve, 2500));
      return publishers.find(publisher => publisher.id === parent.publisherId);
    },
  },
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

startStandaloneServer(server, {
  listen: { port: 4000 },
}).then(({ url }) => {
  console.log(`🚀 Server listening at ${url}`);
});