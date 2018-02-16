/**
 * Created by amendrashrestha on 18-02-02.
 */

$(document).ready(function() {

    $(document).ajaxStart(function () {
        $("#loading").show();
    }).ajaxStop(function () {
        $("#loading").hide();
        $('.sidebar-middle').show();
    });

    $('button#calculate').bind('click', function() {
        $.post('/predict', {
                text1: $('textarea[name="text1"]').val(),
                text2: $('textarea[name="text2"]').val()
            }, function(data) {
                console.log(data)
//                if (data.pred_class == 1){
//                    $("#pred_result").text("Diff User");
//                }
                if(data.diff_user_prob > 85){
                    $('#pred_result').css('color', '#0B6FBB');
                    $("#pred_result").text("Olika författare");
                    $("#same_user_prob").show();
                    $("#diff_user_prob").show();
                }
                else if(data.same_user_prob > 85){
                    $('#pred_result').css('color', '#0BBB90');
                    $("#pred_result").text("Samma författare");
                    $("#same_user_prob").show();
                    $("#diff_user_prob").show();
                }
                else if(data.error_msg){
                    $('#pred_result').css('color', '#C70039');
                    $('#pred_result').css('font-size', '120%');
                    $("#pred_result").text(data.error_msg);
                    $("#same_user_prob").hide();
                    $("#diff_user_prob").hide();
                    $("#lang").hide();
                }
                else{
                    $('#pred_result').css('color', '#FF5733');
                    $("#pred_result").text("Vet ej");
                    $("#same_user_prob").show();
                    $("#diff_user_prob").show();
                }

                $("#same_user_prob").text("Samma författare: "+ data.same_user_prob + "%")
                $("#diff_user_prob").text("Olika författare: "+ data.diff_user_prob + "%")

                if(data.lang == "sv"){
                    $("#lang").text("Språk: "+ "svenska")
                    $("#lang").show();
                }
                if(data.lang == "en"){
                    $("#lang").text("Språk: "+ "engelska")
                    $("#lang").show();
                }

            }
        );
        return false;
    });
});
