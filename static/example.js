if (document.body.dataset.loggedIn == 1) {
    getUserEmail();
}

const submitButton = document.getElementById("submitButton");
if (submitButton != null) {
    submitButton.addEventListener("click", function() {
        signUp();
    })
}

const logoutButton = document.getElementById("logoutButton");
if (logoutButton != null) {
    logoutButton.addEventListener("click", function() {
        logout();
    })
}

async function getUserEmail() {
    const response = await fetch("/getUserInformation");
    const data = await response.json();
    if (data.result == "success") {
        console.log(data.info["email"]);
        emailText.innerHTML = data.info["email"];
    } else {
        alert(data.info);
    }
}

async function signUp() {
    const response = await fetch("/signUp/"+email.value+"/"+password.value);
    const data = await response.json();
    if (data.result == "fail") {
        alert(data.info);
    } else if (data.result == "login") {
        const response = await fetch("/logIn/"+email.value+"/"+password.value);
        const data = await response.json();
        if (data.result) {
            alert(data.info);
        } else {
            console.log("log in success");
            location.reload();
        }
    } else {
        alert(data.info);
        location.reload();
    }
}

async function logout() {
    const response = await fetch("/logout");
    const data = await response.json();
    if (data.result == "success") {
        location.reload()
    } else {
        alert("Something went wrong.")
    }
}