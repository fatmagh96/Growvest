const searchInput = document.getElementById('searchInput');

searchInput.addEventListener('keyup', function (event) {
    if (event.key === 'Enter') {
        performSearch(searchInput.value);
    }
});

function performSearch(query) {
    // Replace this with your search logic
    alert(`Searching for: ${query}`);
    // You can replace the alert with actual search functionality
}
document.getElementById('uploadButton').addEventListener('click', function () {
    var formData = new FormData(document.getElementById('videoUploadForm'));

    // Send formData to the server using AJAX or fetch API
    // Replace the URL with your server-side upload endpoint

    // Example using fetch API
    fetch('upload.php', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Handle the server response here
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

var formfield = document.getElementById('formfield');

function add() {
    var newField = document.createElement('input');
    newField.setAttribute('type', 'text');
    newField.setAttribute('name', 'text');
    newField.setAttribute('class', 'text');
    newField.setAttribute('siz', 50);
    newField.setAttribute('placeholder', 'Optional Field');
    formfield.appendChild(newField);
}

function remove() {
    var input_tags = formfield.getElementsByTagName('input');
    if (input_tags.length > 2) {
        formfield.removeChild(input_tags[(input_tags.length) - 1]);
    }
}

