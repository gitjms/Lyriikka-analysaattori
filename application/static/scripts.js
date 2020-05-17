$('#text_send').on('change textInput input', function () {
    var val = this.value;
    $("input[name=input]").val(val);
});

function textAreaAdjust(o) {
  o.style.height = "1px";
  o.style.height = (25+o.scrollHeight)+"px";
}