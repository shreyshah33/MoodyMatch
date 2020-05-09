window.addEventListener("load", function () {
    var colorBlind = document.getElementById("color-blind");
    var slider = document.getElementById("myRange");
    var output = document.getElementById("demo");
    output.textContent = slider.value;

    colorBlind.oninput = function () {
        if (colorBlind.checked) {
            document.getElementById("pickMoodColor").style.display = "none";
            document.getElementById("colorPicker").style.display = "none";
        } else {
            document.getElementById("pickMoodColor").style.display = "block";
            document.getElementById("colorPicker").style.display = "block";
        }
    };

    slider.oninput = function () {
        output.textContent = this.value;
        slider.onmouseup = function () {
            document
                .getElementById("howManyWorkHours")
                .scrollIntoView({ behavior: "smooth" });
        };
    };

    var slider2 = document.getElementById("myRange2");
    var output2 = document.getElementById("demo2");
    output2.textContent = slider2.value;

    slider2.oninput = function () {
        output2.textContent = this.value;
        slider2.onmouseup = function () {
            // Check if page is in color blind mode, and if so skip the color picker
            if (colorBlind.checked) { document.getElementById("chooseAdjectives").scrollIntoView({ behavior: "smooth" }); }
            // otherwise scroll normally
            else { document.getElementById("pickMoodColor").scrollIntoView({ behavior: "smooth" }); }
        };
    };

    // In-progress implemtation of submit button code
    const submitButton = document.getElementById("surveySubmitButton");
    submitButton.addEventListener("click", function () {
        /* This block of code loops through all the adjective radio boxes
            and checks to see which one is selected
        */
        var adjective = document.getElementsByName("adjective");
        var adjective_value = [];
        for (var i = 0; i < adjective.length; i++) {
            if (adjective[i].checked) {
                adjective_value.push(adjective[i].value);
            }
        }

        /* This block of code loops through all the person-surround radio boxes
            and checks to see which one is selected
        */
        var crowd = document.getElementsByName("person-surround");
        var crowd_value;
        for (var i = 0; i < crowd.length; i++) {
            if (crowd[i].checked) {
                crowd_value = crowd[i].value;
            }
        }

        /* This block of code loops through all the person-surround radio boxes
            and checks to see which one is selected
        */
        var location = document.getElementsByName("item");
        var location_value;
        for (var i = 0; i < location.length; i++) {
            if (location[i].checked) {
                location_value = location[i].value;
            }
        }

        var data = new FormData();
        data.append("day", slider.value);
        data.append("hours", slider2.value);
        if (!colorBlind.checked) {
            data.append(
                "color",
                document.getElementById("colorPicker").style.backgroundColor
            );
        } else {
            data.append("color", "None");
        }
        data.append("adjective", adjective_value);
        data.append("crowd", crowd_value);
        data.append("location", location_value);
        data.append("media", document.getElementById("faves").value);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/survey");
        xhr.onload = function () {
            if (xhr.status == 403 || xhr.status == 404) {
                alert("ERROR SENDING DATA TO THE SERVER");
            } else {
                window.location.replace("/results");
            }
        };
        xhr.send(data);
    });
});

function MultiSelectAdjective() {
    var checkboxes = document.getElementsByName("adjective");
    var numberOfCheckedItems = 0;
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) numberOfCheckedItems++;
    }
    if (numberOfCheckedItems > 5) {
        alert("You can't select more than 5 adjectives!");
        // Once max number of items are selected, scroll to next field
        document.getElementById("chooseCrowdSize").scrollIntoView({ behavior: "smooth" });
        // and then return
        return false;
    }
}

function scrollToChooseLocation() {
    document.getElementById("chooseLocation").scrollIntoView({ behavior: "smooth" });
}

function scrolltoEnterFavMedia() {
    document.getElementById("enterFavMedia").scrollIntoView({ behavior: "smooth" });
}