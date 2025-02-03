
const SolrNode = require('solr-node');
const books = require('./books.json');

const afunc = () => console.log('func');

var client = new SolrNode({
  host: '127.0.0.1',
  port: '8983',
  core: 'mycore',
  protocol: 'http'
});

// // Add a bunch of docs

// books.forEach((books) => {
//   client.update(books, function(err, result) {
//     if (err) {
//       console.log(err);
//       return;
//     }
//     console.log('Response:', result.responseHeader);
//   });
// });

// // Delete

// const stringQuery = 'id:2';    // delete document with id
// const deleteAllQuery = '*';    // delete all
// const objectQUery = {id: 'd7497504-22d9-4a22-9635-88dd437712ff'};   // Object query
// client.delete(deleteAllQuery, function(err, result) {
//   if (err) {
//     console.log(err);
//     return;
//   }
//   console.log('Response:', result.responseHeader);
// });


// // Search

// // const authorQuery = {
// //   Author: 'Haruki Murakami'
// // };

// // const publisherQuery = {
// //   Publisher: 'VINTAGE'
// // };

// // const isbnQuery = {
// //   ISBN: '9780099448761'
// // };


const titleQuery = {
  Title: document.getElementById('searchid').value
};

// Build a search query var

const searchQuery = client.query()
  .q(titleQuery)
  .addParams({
    wt: 'json',
    indent: true
  })
  
  // .start(1)
  // .rows(1)

client.search(searchQuery, function (err, result) {
  if (err) {
    console.log(err);
    return;
  }

  const response = result.response;
  console.log(response);

  if (response && response.docs) {
    response.docs.forEach((doc) => {
      console.log(doc);
    })
  }
});