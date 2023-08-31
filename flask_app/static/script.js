
const searchInput = document.getElementById('searchInput');

searchInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        performSearch(searchInput.value);
    }
});

function performSearch(query) {
    // Replace this with your search logic
    alert(`Searching for: ${query}`);
    // You can replace the alert with actual search functionality
}


