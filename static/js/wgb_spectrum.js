$("#colorpicker").spectrum({
    preferredFormat: "name",
    color: "red",
    showPalette: true,
    showSelectionPalette: true,
    palette: [
        ['black', 'white', 'blanchedalmond'],
        ['red', 'yellow', 'green', 'blue', 'violet']
    ],
    showInitial: true,
    showInput: true,
    chooseText: "決定",
    cancelText: "キャンセル",
});

$(".sp-choose").on("click", function() {
        var color = $('#colorpicker').val();
        $('#id_color').css('color', color);
    }
);