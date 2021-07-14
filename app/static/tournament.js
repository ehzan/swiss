function show_players() {
    const a_tag = `<a href='javascript:void' onclick='remove_player(event)' class='remove' title='remove'> &#10006; </a>`;
    olPlayers.innerHTML =
        players_list.map(item => `<li>${item} ${a_tag}</li>`).join('\n');
}

function add_player(name) {
    lblError.innerText = null;
    if (name == null || name == '') {
        lblError.innerText = '*Required Field';
        txtName.focus();
    }
    else if (players_list.length && players_list.findIndex(item => item.toLowerCase() == name.toLowerCase()) != -1) {
        lblError.innerText = '*Duplicated Name';
        txtName.focus();
        txtName.select();
    }
    else {
        players_list.push(name);
        txtName.value = null;
        show_players();
    }
    return false;
}

function remove_player(e) {
    let name = e.target.parentElement.innerText;
    name = name.substring(0, name.length - 2).toLowerCase();
    i = players_list.findIndex(item => item.toLowerCase() == name);
    players_list.splice(i, 1);
    // delete players_list[i];
    show_players();
}

function next() {
    theForm['players_list'].value = players_list.toString();
    theForm.action = '../schedule/'
    theForm.requestSubmit();
    // if (theForm.checkValidity())
}

function back() {
}

function load() {
    // console.log(tournamentName);
    // console.log(tournamentId);
    // console.log(sport);
    // console.log(number_of_rounds);
    if (players_list)
        players_list = players_list.split(', ');
    else
        players_list = [];
    console.log(players_list);
    if (tournamentName)
        theForm['tournamentName'].value = tournamentName;
    if (tournamentId)
        theForm['tournamentId'].value = tournamentId;
    if (sport)
        theForm['sport'].value = sport;
    if (number_of_rounds)
        theForm['number_of_rounds'].value = number_of_rounds;
    show_players();
    btnBack.disabled = true;
    //txtName.setCustomValidity("I am expecting an e-mail address!");
}