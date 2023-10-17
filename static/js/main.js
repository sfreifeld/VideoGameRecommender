// GAME SEARCH FUNCTIONS


$("#game-search").autocomplete({
    source: function(request, response) {
        $.ajax({
            url: "/search_game",
            type: "GET",
            data: {
                query: request.term
            },
            success: function(data) {
                response(data.slice(0, 9));
            }
        });
    },
    minLength: 3,
    select: function(event, ui) {
        displayGame({
            name: ui.item.label,
            cover: ui.item.sample_cover
        });
        $('#spacing-q1').hide();
    }
});

function displayGame(game) {
    var gameContainer = document.getElementById('games-container');
    
    // Count the number of existing games
    var existingGames = gameContainer.getElementsByClassName('selected-game');
    
    // Only append the new game if there are less than 5 existing games
    if (existingGames.length < 5) {
        var gameElement = document.createElement('div');
        gameElement.className = 'selected-game';
        
        // Create a container for the game title and delete button
        var titleContainer = document.createElement('div');
        titleContainer.className = 'title-container';
        
        var gameName = document.createElement('p');
        gameName.textContent = game.name;
        
        // Create a delete button
        var deleteButton = document.createElement('button');
        deleteButton.textContent = 'X';
        deleteButton.className = 'delete-button';
        deleteButton.addEventListener('click', function() {
            // Remove the game element when the delete button is clicked
            gameContainer.removeChild(gameElement);
        });
        
        // Append the game name and delete button to the title container
        titleContainer.appendChild(gameName);
        titleContainer.appendChild(deleteButton);
        
        var gameCover = document.createElement('img');
        gameCover.className = 'game-cover';
        gameCover.src = game.cover;
        gameCover.alt = game.name;
        
        gameElement.appendChild(titleContainer); // Append the title container to the game element
        gameElement.appendChild(gameCover);
        
        gameContainer.appendChild(gameElement);
    } else {
        alert('You can only select up to 5 games.');
    }
}

// QUESTION 2 FUNCTIONS

var buttons = document.getElementsByClassName('game-btn');

// Add a click event listener to each button
for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function() {
        // Toggle the 'clicked' class
        this.classList.toggle('clicked');

        // Count the number of already clicked buttons
        var clickedButtons = document.getElementsByClassName('clicked');

        // If there are 5 clicked buttons, disable the unclicked buttons
        if (clickedButtons.length >= 5) {
            for (var j = 0; j < buttons.length; j++) {
                if (!buttons[j].classList.contains('clicked')) {
                    buttons[j].classList.add('disabled');
                    buttons[j].disabled = true;
                }
            }
        } else {
            // If there are less than 5 clicked buttons, enable all buttons
            for (var j = 0; j < buttons.length; j++) {
                buttons[j].classList.remove('disabled');
                buttons[j].disabled = false;
            }
        }
    });
}



// RECOMMENDATIONS

document.querySelector('#submit-btn').addEventListener('click', function() {
    // Get the user's selected favorite games
    var favoriteGames = Array.from(document.querySelectorAll('#games-container .selected-game')).map(function(gameElement) {
        return gameElement.querySelector('p').textContent.trim();
    });

    // Get the user's selected favorite video game elements
    var favoriteElements = Array.from(document.querySelectorAll('.game-btn.clicked')).map(function(button) {
        return button.textContent.trim();
    });

    // Get the user's selected console
    var consoleDropdown = document.getElementById('console');
    var consoleName = consoleDropdown.options[consoleDropdown.selectedIndex].text;

    // Create the prompt
    var prompt = `Please give me 5 video game recommendations using the following information.  
    The response should be in this format, replacing 'title' with its respective title.  All spaces in the title name should be replaced with _
    ['title','title','title','title','title']
    Please do not return any text besides the one array.
    My favorite games are: ${favoriteGames.join(', ')}
    They should have these elements: ${favoriteElements.join(', ')} 
    They must be on this console: ${consoleName}`;

    console.log(prompt)
   

    $.ajax({
        url: '/get_recommendations',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ prompt: prompt }),
        success: function(response) {
            // Clear previous recommendations
            $('#recommendations-container').empty();

            // Display the recommendation
            response.recommendation.forEach(function(game) {
                // Replace underscores with spaces
                var gameName = game.replace(/_/g, ' ');

                // Create a new paragraph element for the game
                var gameElement = $('<p>').text(gameName);

                // Append the game element to the container
                $('#recommendations-container').append(gameElement);
            });
        }
    });
});