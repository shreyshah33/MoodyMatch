window.addEventListener("load", function () {
    var pk = new Piklor(".color-picker", [
            "#1abc9c"
        , "#762b99"
        , "#255ebe"
        , "#49a2f0"
        , "#e786f2"
        , "#9a253e"
        , "#e87f5f"
        , "#f1ec67"
        , "#f7e5c5"
        , "#000000"
        ], {
            open: ".picker-wrapper .btn"
        })
      , wrapperEl = pk.getElm(".picker-wrapper")
      , header = pk.getElm("header")
      , footer = pk.getElm("footer")
      ;

    pk.colorChosen(function (col) {
        wrapperEl.style.backgroundColor = col;
        header.style.backgroundColor = col;
        footer.style.backgroundColor = col;
    });
});
