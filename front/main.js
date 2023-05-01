$(document).ready(function() {
    let apiLink = "http://localhost:8000/predictNB";

    $("#submit").click(function() {
        let text = $("#textInput").val();
        text = $.trim(text);
        if(text.length == 0) {
            alert("Debe introducir texto");
            return false
        }
        let data = {id: 1, review_text: text};
        $.ajax({
            type: "POST",
            url: apiLink,
            data: JSON.stringify(data),
            success: parseResponse,
            error: parseError,
            contentType: "application/json; charset=UTF-8"
        });

        return false
    })
});

function parseResponse(data) {
    $("#resTarget").removeClass("text-bg-success");
    $("#resTarget").removeClass("text-bg-danger");
    $("#resTarget").removeClass("text-bg-secondary");
    $("#resText").show();
    if(data.label == 0) {
        $("#resTarget").text("malo")
        $("#resTarget").addClass("text-bg-danger");
    } else if (data.label == 1) {
        $("#resTarget").text("bueno")
        $("#resTarget").addClass("text-bg-success");
    } else if(data.label == 3) {
        $("#resTarget").text("neutro")
        $("#resTarget").addClass("text-bg-secondary");
        $("#alerta").show()
    }
    console.log(data);
}

function parseError(jqXHR) {
    alert("No fue posible procesar la solicitud");
    console.log(jqXHR);
}