
function Validate() {
    var password = document.getElementById("Form-pass1").value;
    var confirmPassword = document.getElementById("Form-pass2").value;
    if (password != confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }
    return true;
}