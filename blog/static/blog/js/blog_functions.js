/**
 * Created by Antrax on 18.11.15.
 */
//$(function blogcounter(){
//
//});

$(function(){
    $('#toggletoggle').click(function(){
        $('#asList').toggleClass('hidden');
        $('#asTable').toggleClass('hidden');
//        alert('Toggle toggle toggle')
        });
});

$(function(){
    $('#emailMe').click(function(){
        myDialog()
    });
});

function myDialog() {
    $("#example").dialog({
        draggable: false
    });
}
