console.log("script.js loaded ✅");
function addWatchlist() {
  const name = prompt("Enter watchlist name:");
  if (!name) return;

  const div = document.createElement('div');
  div.className = 'watchlist-box';
  div.setAttribute('data-name', name);
  div.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <strong>${name}</strong>
      <button onclick="editWatchlist('${name}', this)">Edit</button>
    </div>
    <div class="watchlist-entry"></div>
  `;
  document.getElementById('watchlists').appendChild(div);
}

function editWatchlist(name, btn) {
  // Redirect to edit page with query param
  window.location.href = `/edit_watchlist/?name=${encodeURIComponent(name)}`;
}

// Runs only on edit_watchlist.html
function deleteWatchlist() {
  if (confirm("Are you sure you want to delete this watchlist?")) {
    window.location.href = "/dashboard"; // Redirect back to dashboard
  }
}

function addItem() {
  alert("Adding items is currently disabled.");
}

function deleteItem() {
  alert("Deleting items is currently disabled.");
}

function submitReview() {
  const text = document.getElementById("reviewText").value;
  if (!text.trim()) return;

  const reviewBox = document.createElement('div');
  reviewBox.style.border = "1px solid white";
  reviewBox.style.padding = "10px";
  reviewBox.style.marginTop = "15px";
  reviewBox.style.backgroundColor = "#005bb5";
  reviewBox.innerHTML = `
    <div style="display: flex; justify-content: space-between; font-size: 12px;">
      <span><strong>Username123</strong></span>
      <span>${new Date().toLocaleString()}</span>
    </div>
    <div style="margin-top: 5px;">${text}</div>
  `;
  document.getElementById("submittedReviews").prepend(reviewBox);
  document.getElementById("reviewText").value = '';
}
document.addEventListener("DOMContentLoaded", () => {
  console.log("script.js loaded ✅");
  const searchInput = document.getElementById("searchInput");
  const resultsBox = document.getElementById("searchResults");

  if (searchInput) {
    searchInput.addEventListener("keyup", function() {
      const query = this.value.trim();

      if (query.length === 0) {
        resultsBox.innerHTML = "";
        return;
      }

      fetch(`/search-products/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          resultsBox.innerHTML = "";
          data.results.forEach(product => {
            const li = document.createElement("li");
            li.textContent = product.name;
            li.classList.add("result-item");

            li.onclick = () => {
              window.location.href = `/product/${product.id}/`;
            };

            resultsBox.appendChild(li);
          });
        });
    });
  }
});
