// js/gh_projects.js

// Functie om GitHub repositories op te halen en weer te geven
$.fn.getRepos = function (username) {
    const displayProjects = this;
    $.ajax({
      url: `https://api.github.com/users/davonisher/repos`,
      dataType: 'json',
      success: function (data) {
        const repos = data.map(repo => {
          return `
            <div class="repo">
              <h3><a href="${repo.html_url}" target="_blank">${repo.name}</a></h3>
              <p>${repo.description || 'No description'}</p>
            </div>
          `;
        }).join('');
        displayProjects.html(repos);
      },
      error: function () {
        displayProjects.html('<p>Failed to load repositories</p>');
      }
    });
  };