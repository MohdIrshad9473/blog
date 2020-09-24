window.onload = function () {
    document.getElementById("sendMessageButton").addEventListener("click", function (event) {
        // submit button clcik pe fire hoga

        // 1. Dob validation implemnt kiya hai 
        var name = document.form1.fname.value;
        var secondpassword = document.form1.sp.value;
        var firstpassword = document.form1.fp.value;
        var dateofbirth = document.form1.dob.value;
        // string
        var today_date = new Date();
        var eighteen_years_ago = new Date(today_date - 1000 * 60 * 60 * 24 * 365 * 18); // today's date object
        var user_date = new Date(dateofbirth);
        var isError = false;
        for (var i = 0; i < name.length; i++) {
            if (i == 0 && name[0] != name[0].toUpperCase()) {
                alert("Enter first letter upper case");
                event.preventDefault();
                isError = True;
            }
            if (isError == false) {
                if (i != 0 && name[i] != name[i].toLowerCase()) {
                    alert("enter second to last letter lower case");
                    isError = True;
                    event.preventDefault();
                }
            }
        }
        if (isError == false) {
            if (eighteen_years_ago > user_date) { } else {
                alert("you are not 18+ age");
                isError = True;
                event.preventDefault();
            }
        }


        console.log(firstpassword);
        if (isError == false) {
            if (firstpassword.length > 6) { } else {
                alert('password must be greater than 6');
                isError = true;
                event.preventDefault();
            }
        }
        if (isError == false) {
            if (firstpassword == secondpassword) {

            } else {
                alert('password ia not matche');
                event.preventDefault();
            }
        }

    });
}