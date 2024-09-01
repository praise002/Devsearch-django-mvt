
const tagContainer = document.querySelector('#form__tag');

tagContainer.addEventListener('click', (e) => {
  if (e.target.classList.contains('project-tag')) {
    const tagId = e.target.dataset.tag;
    // console.log('TAG ID', tagId);
    const projectId = e.target.dataset.project;
    // console.log('PROJECT ID', projectId);

    fetch('http://127.0.0.1:8000/projects/remove_tag/', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({'project_id': projectId, 'tag_id': tagId}) // serialized into a JSON string
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

// TODO: TRANSFER TOGGLE HERE

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


