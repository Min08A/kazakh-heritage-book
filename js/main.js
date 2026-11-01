import { createBook } from './book.js';

const root = document.getElementById('app');
try {
  root.replaceChildren();
  createBook(root);
  document.documentElement.classList.add('js-ready');
} catch (err) {
  console.error(err);
  root.innerHTML = '<p class="fatal">Sorry, the book could not be opened in this browser. Please try a current version of Chrome, Safari, Firefox or Edge.</p>';
}
