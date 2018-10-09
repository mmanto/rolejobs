$( document ).ready(function() {

    console.log("postulant_form")
    
    $("#title_current")[0].textContent = "¿Cuál es tu lugar de residencia?"
    $("#bio_title")[0].textContent = " Biografía  Ver ejemplo "
    $("#desc_bio")[0].textContent = "Máximo 500 caracteres"
    $("#title_postulant")[0].textContent = "Datos personales"
    $("#title_exp")[0].textContent = "Experiencias Laborales"
    $("#desc_exp")[0].textContent = "Descripción de responsabilidades y logros"
    $("#desc_exampl")[0].textContent = "Ver ejemplo "
    $("#title_education_area")[0].textContent = "Estudios"

    $("#title_cv")[0].textContent = "Adjuntar CV"
    $("#title_anexo")[0].textContent = "Anexos"

    var sanityCheck = function(id_submit){
        // '#submit-id-bio_submit'
        $(id_submit).on('submit', function(event){
           event.preventDefault();
           console.log("form submitted!")  // sanity check
        });
    }

    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var getPostulant = function (id) {
        var info = []  
        $.ajax({
            'async': false,
            'global': false,
            'url': "/postulant/add/details/"+id+"/",
            'dataType': "json",
            'success': function (data) {
                info.push(data)
            }
        });
        return info[0];
    };

    var handler_error = function(err){
        if (err.status != 200)
           console.log(err.statusText)
        console.log(err.responseJSON)
    }

    var sendData = function(endpoint, type, data, cb){
        $.ajax({
          type: type,
          url: endpoint,
          data: data,
          success: function(success){
            cb(success)
          },
          error: function(err){
            handler_error(err, function(responseJSON){
                console.log(responseJSON)
            })
          },
          dataType: "json"
        });
    }

    var uploadPostulant = function(){

        var data = $('#postulant').serialize();
        
        sendData("/postulant/add/details/", "PUT", data, function(result){
            if(result)
                console.log(result)
        })

    }

    var addBioForm = function(){
        sendData("/postulant/add/bio/", "POST", {
            "description" : $("#id_description").val()
        }, function(result){
            if(result)
                console.log(result)
        })
    }

    var addProfessionalExperienceForm = function(){

        var data = $('#postulant').serialize();

        sendData("/postulant/add/profexp/", "POST", data, function(result){
            if(result) console.log(result)
        })
    }

    var sendEducationAreaForm = function(){
        sendData("/postulant/add/area_education/", "POST", {
            "type_education" : $("#id_type_education").val()
        }, function(result){
            if(result) console.log(result)
        })
    }

    var sendEducationForm = function(){ 
        var data = {
            "level": $("#id_level").val(),
            "country_institution": $("#id_country_institution").val(),
            "institution": $("#id_institution").val(),
            "date": $("#id_date").val()
        }
        sendData("/postulant/add/education/", "POST", data, function(result){
            if(result) console.log(result)
        })
    }

    var sendUploadCVAnexoForm = function(){
        var data = {
            "cvfile": $("#id_cvfile").val(),
            "certificados": $("#id_certificados").val()
        }
        sendData("/postulant/add/cvfile/", "POST", data, function(result){
            if(result) console.log(result)
        })
    }

});


