var players_list = ['Radin', 'Shima', 'Ava', 'Iliya Z.', 'Iliya E.',];

function show_players() {
    const a_tag = `<a href='javascript:void' onclick='remove_player(event)' class='remove' title='remove'> &#10006; </a>`;
    olPlayers.innerHTML =
        players_list.map(item => `<li>${item} ${a_tag}</li>`).join('\n');
}

function add_player(name) {
    lblError.innerText = null;
    if (name == null || name == '') {
        lblError.innerText = 'Required Field';
        txtName.focus();
    }
    else if (players_list.findIndex(item => item.toLowerCase() == name.toLowerCase()) != -1) {
        lblError.innerText = 'Duplicated Name';
        txtName.focus();
        txtName.select();
    }
    else {
        players_list.push(name);
        show_players();
        txtName.value = null;
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
    list1.value = players_list.toString();
    theForm.submit();
}

function back() {
}

function load() {
    show_players();
    btnNext.disabled = false;
    //txtName.setCustomValidity("I am expecting an e-mail address!");
}