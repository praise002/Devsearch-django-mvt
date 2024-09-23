
const tagContainer = document.querySelector('#form__tag');

tagContainer?.addEventListener('click', (e) => {
  if (e.target.classList.contains('project-tag')) {
    const tagId = e.target.dataset.tag;
    // console.log('TAG ID', tagId);
    const projectSlug = e.target.dataset.project;
    // console.log('PROJECT ID', projectId);

    fetch('http://127.0.0.1:8000/projects/remove-tag/', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({'project_slug': projectSlug, 'tag_id': tagId}) // serialized into a JSON string
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data.success) e.target.remove(); // Remove the tag from the DOM
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }
});

function toggle(id) {
  const truncatedDescription = document.getElementById(`truncated-description-${id}`);
  const fullDescription = document.getElementById(`full-description-${id}`);

  if (truncatedDescription.style.display === "none") {
      truncatedDescription.style.display = "inline";
      fullDescription.style.display = "none";
  } else {
      truncatedDescription.style.display = "none";
      fullDescription.style.display = "inline";
  }
}

function convertServerTimeToLocalTime() {
  // Select all elements with the class 'message__date'
  const messageDateElems = document.querySelectorAll('.message__date');

  messageDateElems.forEach(messageDateElem => {
    const serverTime = messageDateElem.getAttribute('data-server-time');
    if (serverTime) {
      // Convert server time to a Date object
      const serverDate = new Date(serverTime);
    
      // Format the date according to the user's local timezone
      const localDate = serverDate.toLocaleString([], {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    
      // Update the message__date element with the local time
      messageDateElem.textContent = localDate;
    }
  });
}

convertServerTimeToLocalTime();
