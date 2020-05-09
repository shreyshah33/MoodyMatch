window.onload = function () {
    window.scrollTo(0, Number.POSITIVE_INFINITY);
};
window.addEventListener("load", function () {
    // [1] GET ALL THE HTML ELEMENTS
    var video = document.getElementById("vid-show"),
        canvas = document.getElementById("vid-canvas"),
        take = document.getElementById("vid-take"),
        photo = document.getElementById("photo"),
        send = document.getElementById("send");
    // video.src = "https://www.youtube.com/embed/oilZ1hNZPRM";

    // [2] ASK FOR USER PERMISSION TO ACCESS CAMERA
    // WILL FAIL IF NO CAMERA IS ATTACHED TO COMPUTER
    navigator.getUserMedia =
        navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia;
    navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(function (stream) {
            // [3] SHOW VIDEO STREAM ON VIDEO TAG
            video.srcObject = stream;
            video.play();

            // [4] WHEN WE CLICK ON "TAKE PHOTO" BUTTON
            take.addEventListener("click", function () {
                // Create snapshot from video
                var draw = document.createElement("canvas");
                draw.width = video.videoWidth;
                draw.height = video.videoHeight;
                var context2D = draw.getContext("2d");
                context2D.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
                photo.setAttribute("src", draw.toDataURL("image/png"));
                // Upload to server
            });

            send.addEventListener("click", function () {
                var draw = document.createElement("canvas");
                draw.width = video.videoWidth;
                draw.height = video.videoHeight;
                var context2D = draw.getContext("2d");
                context2D.drawImage(photo, 0, 0, video.videoWidth, video.videoHeight);
                draw.toBlob(function (blob) {
                    var data = new FormData();
                    data.append("upimage", blob);
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/webcam");
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
        })
        .catch(function (err) {
            document.getElementById("vid-controls").innerHTML =
                "Please enable access and attach a camera";
        });

    !(function (t) {
        "use strict";
        t('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
            if (
                location.pathname.replace(/^\//, "") ==
                    this.pathname.replace(/^\//, "") &&
                location.hostname == this.hostname
            ) {
                var e = t(this.hash);
                if ((e = e.length ? e : t("[name=" + this.hash.slice(1) + "]")).length)
                    return (
                        t("html, body").animate(
                            { scrollTop: e.offset().top },
                            1e3,
                            "easeInOutExpo"
                        ),
                        !1
                    );
            }
        }),
            t(".js-scroll-trigger").click(function () {
                t(".navbar-collapse").collapse("hide");
            }),
            t("body").scrollspy({ target: "#sideNav" });
    })(jQuery);
});
