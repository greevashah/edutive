function validateForm() {
    alert('insideform');
    var password = document.getElementById("Form-pass1").value;
    var confirmPassword = document.getElementById("Form-pass2").value;
    var errorpass = document.getElementById("errorpass").value;
    var errorcon= document.getElementById("errorconfirm").value;
    var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    // errorpass.textContent = '';
    // errorcon.textContent = '';
    // validate password
    if (!strongRegex.test(password)) {
      errorpass.innerHTML = 'password should be valid';
    }
    if (password != confirmPassword) {
        errorcon.innerHTML = 'password not matching';
    }
 
}