$('#text_send').on('change textInput input', function () {
    var val = this.value;
    $("input[name=input]").val(val);
});
