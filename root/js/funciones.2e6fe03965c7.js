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

function passData(id, titulo) {
    // Obtiene la id y el nombre del reporte y
    // lo pasa al modal
    document.getElementById("modalReporte").innerHTML = '<strong>Se eliminará: </strong><br>'+
                                    '<div class="alert alert-warning" id="tituloReporte"> '+ titulo +'</div>';
    document.getElementById("id_elmrepo").value = id;                                
  }

//function spinner() {
    
  //  document.getElementById("load").innerHTML = '<img  class="rounded mx-auto d-block" alt="Responsive image"'+ 
  //    'id="loading-image" src="https://res.cloudinary.com/mtac/image/upload/v1618507609/moneySpinner_cgpxci.gif" />';
//}

document.getElementById("form-submit").addEventListener("submit", function () {
    $('#SpinModal').modal({
        backdrop: 'static',
        keyboard: false
    });
});


 