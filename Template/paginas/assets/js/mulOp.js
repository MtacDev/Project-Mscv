$(function(){ 
    $("#copy").on("click", function(){
        $("#textarea option:selected").each(function(){
            $("#textarea2").append($(this).clone());
            $(this).remove();           
        });  
    });   
    $("#remove").on("click", function(){
        $("#textarea2 option:selected").each(function(){
            $("#textarea").append($(this).clone());
            $(this).remove();
        });  
    });  
});