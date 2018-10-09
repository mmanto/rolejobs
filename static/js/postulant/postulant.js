var csrftoken = Cookies.get('csrftoken');
var userID = $("#user")[0].getAttribute("name") //{{ user }}"

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var edit = true;
var onClickAddShow = function(it){
    var id;
    id = it
    if(it.id) id = it.id
    $('#'+id+'_form').fadeOut('slow');
    if (edit){
        $('#'+id)[0].textContent = 'Cancelar'
        $('#'+id+'_form').fadeIn(300)
        edit = false;
    } else {
        $('#'+id)[0].textContent = 'Agregar'
        $('#'+id+'_form').fadeOut('slow');
        edit = true;
    }
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var splice_ul = function(lstul, cb){
    var _lstul = lstul['mylist']
    var ula = []; var ulb = []; var ulc = [];
    for (var i = 0; i<_lstul.length;i++)
        if (i<5) ula.push(_lstul[i])
        else if (i> 5 && i < 10) ulb.push(_lstul[i])
        else if (i>10) ulc.push(_lstul[i])
    cb(lstul['id'], ula, ulb, ulc)
}

var push_ul = function(data){
    var myLst = []
    $.each(data, function(key, item){
        if (key != "id") myLst.push("<li>"+item+"</li>")
    });
    var obj = {'id': data.id, 'mylist': myLst}
    return obj
}

var handler_error = function(err){
    if (err.status != 200)
       console.log(err.statusText)
    console.log(err.responseJSON)
}

var getInformationAPI = function(_endpoint, cb){
    var data; null;
    if (typeof cb === 'function') getSucess = cb
    $.ajax({
        async: false,
        global: false,
        url: "/postulant/add/"+_endpoint+"/",
        dataType: "json",
        success: getSucess,
        error:function(xhr, status){
            console.log('Petición rechazada', _endpoint, xhr.responseJSON)
        },
        complete : function(xhr, status) {
            //console.log('Petición realizada ', status, _endpoint, xhr);
            if (xhr.responseJSON.hasOwnProperty('results')){
                data = xhr.responseJSON['results'];
            } else if (xhr.responseJSON.hasOwnProperty('id')){
                data = xhr.responseJSON;
            } else {
                data = [];
            }
        }
    });
    return data;
}

var generateDivBox = function(mainbox, elem, _class, _id){

    var $boxMedium = $('<div/>', {
        'id': _id,
        'html':'',
        'class': _class,
        'align':'left'
    });

    mainbox.append($boxMedium.append(elem))
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

var destroyData = function(endpoint, id, cb){
    //destroyData("/postulant/add/biographic/", 1)
    $.ajax({
      type: "DELETE",
      url: endpoint+id+"/",
      success: cb,
      error: function(err){
        console.log(err)
      },
      dataType: "json"
    });
};

var show = function(result){
    if(result) console.log(result)
}

var updatePostulant = function(){
    var data = $('#postulant').serialize();
    sendData("/postulant/add/details/"+userID+"/", "PUT", data, function(datos_personales){
        if(datos_personales)
            $("#card_info_postulant").children()[0].remove()
            addDatosPersonalesCard(datos_personales)
            $("#datos_personales_card li").remove()
            $("#date_update_cv p").remove()
            addDatosPersonalesMiniCard(datos_personales)
    })
}

var updateBiographic = function(){
    var method, endpoint;
    var bio_model_edit = $('#bio_model_edit :input').val()
    if (bio_model_edit === 'AGREGAR'){
        endpoint = "/postulant/add/biographic/"
        method = "POST"
    } else {
        var id = $('#biographic')[0].name
        endpoint = "/postulant/add/biographic/"+id+"/"
        method = "PUT"
    }
    var data = $('#biographic').serializeArray();
    if (data[0].value){
        sendData(endpoint, method, data, function(res){
            if(res){
                $("#card_bio span").remove()
                $("#card_bio a").remove()
                $("#card_bio").append(
                    $('<span>', {
                        style:"font-size:12px",
                        id: "card_bio_span_id_"+res.id,
                        text:res.description
                    }),
                    $('<a>', {
                        value: "Eliminar",
                        style:"font-size:12px",
                        onClick: 'deleteBiographic(this)',
                        text: 'Eliminar',
                        id: "card_bio_id_"+res.id
                    })
                )
                onClickAddShow("edit_bio")
                getCompletCVaddCard()
            }
            $('#biographic')[0].name = res.id
            $('#bio_model_edit :input')[0].value="EDITAR"
        })
    } else {
        alert("sin datos")
    }
}


var getBiographicCard = function (bio){
    if (bio.length >= 1){
        var bio = bio[0]
        $("#biographic")[0].name = bio.id
        $("#card_bio span").remove()
        $("#card_bio a").remove()
        $("#card_bio").append(
            $('<span>', {
                style:"font-size:12px",
                id: "card_bio_span_id_"+bio.id,
                text:bio.description
            }),
            $('<a>', {
                value: "Eliminar",
                style:"font-size:12px",
                onClick: 'deleteBiographic(this)',
                text: 'Eliminar',
                id: "card_bio_id_"+bio.id
            })
        )
    }
}

var getSucess = function(data) {
    //
};

var cardsEndpoints = {
    "card_bio": {
        "endpoint": "/postulant/add/biographic/", 
        "msg": "No hay biografia cargada"
    },
    "card_profesional_experience": {
        "endpoint": "/postulant/add/experience/",
        "msg": "No hay experiencias laborales cargadas"
    },
    "card_education_primary": {
        "endpoint": "/postulant/add/education_primary/",
        "msg": "No hay estudios Primarios cargados"
    },
    "card_education_universitary": {
        "endpoint": "/postulant/add/education_universitary/",
        "msg": "No hay estudios Universitarios cargados"
    },
    "card_idiomas": {
        "endpoint": "/postulant/add/language/", 
        "msg": "No hay idiomas cargados"
    },
    "card_informatica":{
        "endpoint":"/postulant/add/knowledge_technology/",
        "msg":"No hay conocimientos informaticos cargados"
    },
    "card_certification": {
        "endpoint": "/postulant/add/certification_technology/",
        "msg": "No hay certificados informaticos cargados"
    },
    "card_seminaries": {
        "endpoint":"/postulant/add/additional_knowledge/",
        "msg":"No hay otros conocimientos cargados"
    },
    "card_reference_experience": {
        "endpoint":"/postulant/add/reference_experience/",
        "msg":"No hay referencias laborales cargadas"
    },
    "card_objective_job":{
        "endpoint":"/postulant/add/objectivejob/",
        "msg":"No hay objetivos laborales cargados"
    },
    "card_reference_social_network":{
        "endpoint":"/postulant/add/reference_sn/",
        "msg":"No hay enlace a linkedin/twitter/facebook"
    }, "card_cvfile": {
        "endpoint": "/postulant/add/cv/",
        "msg":"No hay anexos y/o cv subido en formato .pdf o .word"
    }
}

var deleteBiographic = function(it){
    var card = it.id.split("_id_")[0]
    var id = it.id.split("_id_")[1]
    destroyData(cardsEndpoints[card]["endpoint"], id, function(success){
        $("#"+it.id).remove() // card_bio_id_8
        $("#"+it.id.replace("_id_", "_span_id_")).remove() // card_bio_span_id_8
        $("#"+card).append($('<span>', {
            style:'font-size:12px',
            text:cardsEndpoints[card]['msg']
        }))
        $('#bio_model_edit :input')[0].value="AGREGAR"
        $('#id_description')[0].value=""
        getCompletCVaddCard()
    });
};

var getCompletCVaddCard = function() {
    
    var getCompletCV = getInformationAPI('view_complete_cv')
    var msg_default;
    $("#complete:first")[0].innerText = getCompletCV.complete

    if (getCompletCV.validate === true){
        // cv completo
        $("#msg_default:first")[0].innerText = "Tu CV está Completo"
        $("#msg_alert:first")[0].innerText ="¡Yá podés postularte!"
    } else {
        // cv incompleto
        $("#msg_default:first")[0].innerText = "Tu CV está incompleto"
        $("#msg_alert:first")[0].innerText = "Aún no podrás aplicar a ninguna oferta ni ser encontrado por ninguna empresa"
        $("#lst_msg li").remove()
        var message = getCompletCV.message.splice(0, 5)
        for (var i =0; i<message.length;i++){
            $("#lst_msg").append("<li>"+message[i]+"</li>")
        }
    }

};

var addEducationCard = function(education, id){
    $("#"+ id +" span").remove()
    if ($("#"+id).children().length >= 1)
        $("#"+id).children().remove()

    var $mainBox = $('<div/>', {'class' : 'large-12 columns left'});
    var lstul;

    $.each(education, function(key, exp){
        lstul = push_ul(exp)
        splice_ul(lstul, function(_id, ula, ulb, ulc){
            generateDivBox($mainBox, '<ul>'+ula.join("")+'</ul>', 'large-4 columns left', _id)
            $("#"+id).append($mainBox)
        })
        var $mainDiv = $('<div/>', {'class' : 'large-4 columns left'});
        $mainDiv.append(
            $('<a>', {
                value: "Eliminar",
                style:"font-size:12px",
                onClick: 'deleteEducation(this)',
                text: 'Eliminar',
                name: id,
                id: exp.id
            })
        )
        $mainBox.append($mainDiv)
    });
}

var deleteEducation = function(it) {
    var card_education = $('#'+it.name)
    var endpoint = cardsEndpoints[it.name]["endpoint"]
    var msg = cardsEndpoints[it.name]["msg"]
    destroyData(endpoint, it.id, function(success){
        card_education.find("div").filter('#'+it.id).remove()
        card_education.find("a").filter('#'+it.id).remove()
        if ($("#"+it.name).find("li").length === 0){
            $("#"+it.name).append($('<span>', {
                style:'font-size:12px',
                text: msg
            }))
        }
        getCompletCVaddCard()
    });
};

var addEducationAll = function(education){
    if (education["education_primary"].length >= 1 && education["education_universitary"].length >= 1){
        addEducationCard(education["education_primary"], "card_education_primary")
        addEducationCard(education["education_universitary"], "card_education_universitary")
    } else if (education["education_primary"].length >= 1){
        addEducationCard(education["education_primary"], "card_education_primary")
    } else if (education["education_universitary"].length >= 1){
        addEducationCard(education["education_universitary"], "card_education_universitary")
    }
};

var lastUpdateCV = function(updated_at){
    var date = new Date(updated_at)
    var update_date = date.getDay()+ "/" +date.getMonth()+ "/" +date.getFullYear()
    return update_date
}

var addProfesionalExperienceCard = function(experience){
    
    $("#card_profesional_experience span").remove()

    if ($("#card_profesional_experience").children().length > 1)
        $("#card_profesional_experience").children()[0].remove()

    var $mainBox = $('<div/>', {
        'id': 'mainBox',
        'html': '',
        'class' : 'large-12 columns left',
        'style' : ''//'margin-bottom:20px'
    });

    var lstul;
    $.each(experience, function(key, exp){
        $mainBox.append($('<a>', {
            value: "Eliminar",
            style:"font-size:12px",
            onClick: 'deleteProfessionalExperience(this)',
            text: 'Eliminar',
            id: exp.id
        }))
        lstul = push_ul(exp)
        splice_ul(lstul, function(_id, ula, ulb, ulc){
            generateDivBox($mainBox, '<ul>'+ula.join("")+'</ul>', 'large-4 columns', _id)
            generateDivBox($mainBox, '<ul>'+ulb.join("")+'</ul>', 'large-4 columns', _id)
            generateDivBox($mainBox, '<ul>'+ulc.join("")+'</ul>', 'large-4 columns', _id)
            $("#card_profesional_experience").append($mainBox)
        })
    });
}

var deleteProfessionalExperience = function(it){
    var profesional_experience = $("#card_profesional_experience")
    destroyData(cardsEndpoints["card_profesional_experience"]["endpoint"], it.id, function(sucess){
        profesional_experience.find("div").filter('#'+it.id).remove()
        profesional_experience.find("a").filter('#'+it.id).remove()
        if ($("#card_profesional_experience").find("li").length === 0){
            $("#card_profesional_experience").append($('<span>', {
                style:'font-size:12px',
                text:cardsEndpoints["card_profesional_experience"]['msg']
            }))
        }

        getCompletCVaddCard()
    });
};

var createProfessionalExperience = function(){
    var data = $('#experience').serializeArray();
    $.each(data, function(a, b){
        if (["show_salary", "with_experience"].indexOf(b.name) > -1)
            if (b.value == 'on') data[a].value = 'True'
    })
    sendData("/postulant/add/experience/", "POST", data, function(exp){
        addProfesionalExperienceCard([exp])
        onClickAddShow('add_professional_experience')
        $.each($("#experience :input"), function(a,input){
            input.value=''
            if (input.type == 'submit'){
                input.value = "AGREGAR"
            } else if (input.type=='reset'){
                input.value = "CANCELAR"
            }
            // if (input.id == 'id_currency'){
            //     input.value = '-----------'
            // } else if(input.id == 'id_budget'){
            //     input.value = 'F'
            // } else {
            //     input.value = '0'
            // }
        })
        getCompletCVaddCard()
    })
}

var addLineInputs = function(argument) {}

var addDatosPersonalesCard  = function(datos) {

    // <div class="large-12 columns left" style="margin-bottom:20px">
            // <div class="large-3 columns" align="left">
                // <ul>
                    // <li><span style="font-size:12px">{% trans "Luis Uranga " %}</span></li>
    
    var $mainBox = $('<div/>', {
        'id':'',
        'html': '',
        'class' : 'large-12 columns left',
        'style' : ''//'margin-bottom:20px'
    });

    var mylist = [];
    // var mylistTwo = '';
    $.each(datos, function(key, item) {
        if (['view_current_location','email','phone_number',
            'dni','marital_status_display','sex_display',
            'date_of_birth','view_name_complete',].indexOf(key) > -1)
            //mylistTwo += '<li>' + item + '</li>';
            mylist.push('<li>' + item + '</li>')
    });
    
    // card_info_postulant
    lst_one = mylist.splice(mylist.length/2).join("")
    lst_two = mylist.splice(-mylist.length/2).join("")
    //ul_lst = '<ul>'+lst_one+'</ul>'

    generateDivBox($mainBox, '<ul>'+lst_one+'</ul>', 'large-4 columns')
    generateDivBox($mainBox, '<ul>'+lst_two+'</ul>', 'large-7 columns')
    $("#card_info_postulant").append($mainBox)

}

var addDatosPersonalesMiniCard = function(datos) {
    var lstFilter = ['email', 'mobile_number', 'phone_number', 'country', 'marital_status_display']
    $("#datos_personales_card").append('<li>' + datos["name"] +' '+ datos["last_name"] + '</li>');
    for (var i =0;i<lstFilter.length;i++)
        $("#datos_personales_card").append('<li>' + datos[lstFilter[i]] + '</li>');
    $("#datos_personales_card").append('<li>' + "DNI " + datos["dni"] + '</li>');
    $("#date_update_cv").append('<p>Ultima actualización del CV '+lastUpdateCV(datos["updated_at"])+'</p>')
}


var allFormsHide = function(){
    var lst_ids = [
        'edit_postulant_form','edit_bio_form','add_professional_experience_form',
        'add_education_form','add_idiomas_form','add_informatica_form',
        'add_certificados_form','add_seminarios_form','add_reference_form','add_objetivo_form',
        'edit_cvfile_form','edit_redes_form'
    ]

    for (var i=0; i<lst_ids.length;i++){
        // console.log(lst_ids[i])
        $('#'+lst_ids[i]).hide()
    }
};

var formStudyHide = function() {
    $('#form_primary').hide()
    $('#form_universitary').hide()
    $('#study_submit').hide()
};


$("#options_study").click(function(argument){
    var id_study_slct = $( "#options_study option:selected" )[0].id
    if (id_study_slct == 'university'){
        $('#form_primary').hide()
        $('#form_universitary').show()
        $('#study_submit').show()
    } else if (id_study_slct == 'primary'){
        $('#form_universitary').hide()
        $('#form_primary').show()
        $('#study_submit').show()
    } else {
        formStudyHide()
    }
})

var addStudyCard = function(education, _id){
    var $mainBox = $('<div/>', {'class' : 'large-12 columns left'});
    var obj = push_ul(education)
    generateDivBox($mainBox, '<ul>'+obj['mylist'].join('')+'</ul>', 'large-4 columns', obj['id'])
    var $mainDiv = $('<div/>', {'class' : 'large-4 columns left'});
    $mainDiv.append(
        $('<a>', {
            value: "Eliminar",
            style:"font-size:12px",
            onClick: 'deleteEducation(this)',
            text: 'Eliminar',
            name: _id,
            id: education.id}
        )
    )
    $mainBox.append($mainDiv)    
    $('#'+_id).append($mainBox)
}

var createStudy = function() {
    var data = $('#study').serializeArray();
    
    if (data[3].name == 'on_study_primary' && data[3].value == 'on') data[3].value = 'true'

    var selc_endpoint = $('#options_study option:selected')[0].id
    var endpoint = null

    if (selc_endpoint == 'university'){
        endpoint = 'education_universitary'
    } else if (selc_endpoint == 'primary') {
        endpoint = 'education_primary'
    }

    sendData('/postulant/add/'+endpoint+'/', 'POST', data, function(education){
        if (endpoint == 'education_primary'){
            $("#card_education_primary span").remove()
            addStudyCard(education, 'card_education_primary')
        }
        if (endpoint == 'education_universitary'){
            $("#card_education_universitary span").remove()
            addStudyCard(education, 'card_education_universitary')
        }
        getCompletCVaddCard()
    })
};

var addLenguageCard = function(language, mainBox){
    
    var lst_view = ["view_name","view_writing_level","view_reading_level","view_speaking_level"]
    var show_languages = []
    $.each(language, function(index, item) {
        if (lst_view.indexOf(index) >= 0) show_languages.push(item)
    })

    var obj = push_ul(show_languages)
    generateDivBox(mainBox, "<ul>"+obj['mylist'].join("")+"</ul>", 'large-4 columns', language['id'])

};

var addAllLenguageCard = function(languages) {

    $('#card_idiomas span').remove()
    if ($("#card_idiomas").children().length >= 1) $("#card_idiomas").children().remove()
    
    var $mainBox = $('<div/>', {'class' : 'large-12 columns left'});

    $.each(languages, function(key, item) {
        addLenguageCard(item, $mainBox)
        var $mainDiv = $('<div/>', {'class' : 'large-4 columns left'});
        $mainDiv.append(
            $('<a>', {
                value: "Eliminar",
                style:"font-size:12px",
                onClick: 'deleteLanguage(this)',
                text: 'Eliminar',
                id: item.id
            })
        )
        $mainBox.append($mainDiv)
    })

    $("#card_idiomas").append($mainBox)
};

var createLanguage = function() {
    var data = $('#idiomas_form').serializeArray();
    var $mainBox = $('<div/>', {'class' : 'large-12 columns left'});
    if (data.length == 5)
        if (data[4].name == 'native' && data[4].value == 'on') data[4].value = 'true'
    sendData("/postulant/add/language/", "POST", data, function(res){
        $("#card_idiomas span").remove()
        addLenguageCard(res, $mainBox)
        var $mainDiv = $('<div/>', {'class' : 'large-4 columns left'});
        $mainDiv.append(
            $('<a>', {
                value: "Eliminar",
                style:"font-size:12px",
                onClick: 'deleteLanguage(this)',
                text: 'Eliminar',
                id: res.id
            })
        )
        $mainBox.append($mainDiv)
        $("#card_idiomas").append($mainBox)
        getCompletCVaddCard()
    })
};

var deleteLanguage = function(it){
    var card_education = $('#card_idiomas')
    var endpoint = cardsEndpoints["card_idiomas"]["endpoint"]
    var msg = cardsEndpoints["card_idiomas"]["msg"]
    destroyData(endpoint, it.id, function(success){
        card_education.find("div").filter('#'+it.id).remove()
        card_education.find("a").filter('#'+it.id).remove()
        if ($("#card_idiomas").find("li").length === 0){
            $("#card_idiomas").append($('<span>', {
                style:'font-size:12px',
                text: msg
            }))
        }
        getCompletCVaddCard()
    });
};

var createTechnology = function(){
    var data = $('#technology').serializeArray();
    sendData("/postulant/add/knowledge_technology/", "POST", data, function(res){
        $("#card_informatica span").remove()
        var $mainBox = $('<div/>', {'class' : 'large-12 columns left'});
        var obj = push_ul(res)
        generateDivBox($mainBox, "<ul>"+obj['mylist'].join("")+"</ul>", 'large-4 columns', obj['id'])
        var $mainDiv = $('<div/>', {'class' : 'large-12 columns left'});
        $mainDiv.append(
            $('<a>', {
                value: "Eliminar",
                style:"font-size:12px",
                onClick: 'deleteTechnology(this)',
                text: 'Eliminar',
                id: obj['id']
            })
        )
        $mainBox.append($mainDiv)
        $("#card_informatica").append($mainBox)
        getCompletCVaddCard()
    })
};

var deleteTechnology = function(it){
    var card_education = $('#card_informatica')
    var endpoint = cardsEndpoints["card_informatica"]["endpoint"]
    var msg = cardsEndpoints["card_informatica"]["msg"]
    destroyData(endpoint, it.id, function(success){
        card_education.find("div").filter('#'+it.id).remove()
        card_education.find("a").filter('#'+it.id).remove()
        if ($("#card_informatica").find("li").length === 0){
            $("#card_informatica").append($('<span>', {
                style:'font-size:12px',
                text: msg
            }))
        }
        getCompletCVaddCard()
    });
}

var addAllTechnologyData = function(informatica){
    if ($("#card_informatica").children().length >= 1) $("#card_informatica").children().remove()
    var $mainBox = $('<div/>', {'class' : 'large-12 columns left'});
    var obj;
    $.each(informatica, function(key, item){
        obj = push_ul(item)
        generateDivBox($mainBox, "<ul>"+obj['mylist'].join("")+"</ul>", 'large-4 columns', obj['id'])
        var $mainDiv = $('<div/>', {'class' : 'large-12 columns left', 'id':item.id});
        $mainDiv.append(
            $('<a>', {
                value: "Eliminar",
                style:"font-size:12px",
                onClick: 'deleteTechnology(this)',
                text: 'Eliminar',
                id: obj['id']
            })
        )
        $mainBox.append($mainDiv)
    })
    $("#card_informatica").append($mainBox)
};

var postFormSerializer = function(_serializer, _endpoint, _card, _fn, cb){
    var data = $('#'+_serializer).serializeArray();
    if (typeof cb === 'function') data = cb(data);
    sendData("/postulant/add/"+_endpoint+"/", "POST", data, function(res){
        var $mainBox = $('<div/>', {'class' : 'large-12 columns left'});
        var obj = push_ul(res);
        generateDivBox($mainBox, "<ul>"+obj['mylist'].join("")+"</ul>", 'large-4 columns', obj['id'])
        $("#"+_card).append($mainBox)
        var $mainDiv = $('<div/>', {'class' : 'large-12 columns left'});
        $mainDiv.append(
            $('<a>', {
                value: "Eliminar",
                style:"font-size:12px",
                onClick: _fn+'(this)',
                text: 'Eliminar',
                id: obj['id']
            })
        )
        $mainBox.append($mainDiv)
        $("#"+_card).append($mainBox)
        getCompletCVaddCard()
    });
};

var deleteData = function(_card, _id) {
    var elem = $("#"+_card)
    destroyData(cardsEndpoints[_card]["endpoint"], _id, function(sucess){
        elem.find("div").filter('#'+_id).remove()
        elem.find("a").filter('#'+_id).remove()
        if ($("#"+_card).find("li").length === 0){
            elem.find("div").remove()
            // var $mainDiv = $('<div/>', {'class' : 'large-12 columns left', 'style' : 'margin-bottom:20px'})
            // $mainDiv.append()
            $("#"+_card).append($('<span>', {
                style:'font-size:12px',
                text:cardsEndpoints[_card]['msg']
            }))
        }
        getCompletCVaddCard()
    });
};

var deleteCertification = function(it) {
    deleteData("card_certification", it.id)
};

var createCertification = function(){
    $("#card_certification span").remove()
    postFormSerializer("certification", "certification_technology", "card_certification", 'deleteCertification')
};

var deleteAdditionalKnowledge = function(it) {
    deleteData("card_seminaries", it.id)
};

var createAdditionalKnowledge = function(){
    postFormSerializer("seminaries", "additional_knowledge", "card_seminaries", "deleteAdditionalKnowledge")
    $("#card_seminaries span").remove()
};

var getInformationAddCard = function(_endpoint, _id, _fn_delete){
    var _result = [];
    var $mainBox = $('<div/>', {'class' : 'large-12 columns left'});
    $.ajax({
        'async': false,
        'global': false,
        'url': "/postulant/add/"+ _endpoint +"/",
        'dataType': "json",
        'success': function (data){
            _result = data;
            // console.log(_result)
            if (_result.length >= 1){
                if ($("#"+_id).children().length >= 1) $("#"+_id).children().remove()
                $.each(_result["results"], function(key, item){
                    var obj = push_ul(item)
                    generateDivBox($mainBox, "<ul>"+obj['mylist'].join("")+"</ul>", 'large-4 columns', obj['id'])
                    var $mainDiv = $('<div/>', {'class' : 'large-12 columns left'});
                    $mainDiv.append(
                        $('<a>', {
                            value: "Eliminar",
                            style:"font-size:8px",
                            onClick: _fn_delete+'(this)',
                            text: 'Eliminar',
                            id: obj['id']
                        })
                    )
                    $mainBox.append($mainDiv)                    
                });
                $("#"+_id).append($mainBox)
            }
        }
    });
    return _result["results"];
}

var deleteReferenceSocialNetwork = function(it) {
    deleteData("card_reference_social_network", it.id)
};

var createReferenceSocialNetwork = function() {
    $("#card_reference_social_network span").remove()
    postFormSerializer("reference_social_network", "reference_sn", "card_reference_social_network", "deleteReferenceSocialNetwork")
};

var deleteObjectiveJob = function(it){
    deleteData("card_objective_job", it.id)
};

var createObjectiveJob = function(){
    $("#card_objective_job span").remove()
    postFormSerializer("objective_job", "objectivejob", "card_objective_job", "deleteObjectiveJob", function(data){
        $.each(data, function(index, item){
            if (["relocation_country", "relocation_city"].indexOf(item.value) >= -1)
                if (item.value == 'on') data[index].value = 'True' 
        })
        return data
    });
};

var deleteReferenceExperience = function(it) {
    deleteData("card_reference_experience", it.id)
};

var createReferenceExperience = function(){
    $("#card_reference_experience span").remove()
    postFormSerializer("reference_experience", "reference_experience", "card_reference_experience", "deleteReferenceExperience")
};

var createCVFile = function(){

    $("#cvfile span").remove()
    var data = $('#cvfile').serializeArray();
    $.each($("#cvfile :file"), function(index, input){
        data.push({
            'name': input.name,
            'value': "input.value"
        })
    });
    sendData("/postulant/add/cv/", "POST", data, show, function() {
        getCompletCVaddCard();
    })
};

var deleteCVFile = function(it) {
    console.log(it.id)
    getCompletCVaddCard()
};

var getBiographic = getInformationAPI("biographic")
var getPersonalInfo = getInformationAPI("details/"+userID);
var getProfesionalExperience = getInformationAPI('experience');
var getTechnology = getInformationAPI("knowledge_technology");
var getLanguage = getInformationAPI("language");

var getAllEducation = (function (){
    var education = {}
    education["education_universitary"] = getInformationAPI('education_universitary')
    education["education_primary"] = getInformationAPI('education_primary')
    return education
})();

if (getAllEducation["education_primary"] && getAllEducation["education_universitary"])
    addEducationAll(getAllEducation)

getInformationAddCard("certification_technology", "card_certification", "deleteCertification")
getInformationAddCard("additional_knowledge", "card_seminaries", "deleteAdditionalKnowledge")
getInformationAddCard("reference_experience", "card_reference_experience", "deleteReferenceExperience")
getInformationAddCard("objectivejob", "card_objective_job", "deleteObjectiveJob")
getInformationAddCard("reference_sn", "card_reference_social_network", "deleteReferenceSocialNetwork")

if (getProfesionalExperience.length >= 1){
    addProfesionalExperienceCard(getProfesionalExperience)
}

getBiographicCard(getBiographic)
getCompletCVaddCard()
addDatosPersonalesMiniCard(getPersonalInfo)
addDatosPersonalesCard(getPersonalInfo)
formStudyHide()
allFormsHide()

if (getLanguage)
    if (getLanguage.length >= 1)
        addAllLenguageCard(getLanguage)

if (getTechnology.length >= 1)
    addAllTechnologyData(getTechnology)

$(function(){
    $("#id_date_of_birth" ).datepicker({ dateFormat: 'yy-mm-dd' });
    $("#id_date_entry_primary" ).datepicker({ dateFormat: 'yy-mm-dd' });
    $("#id_date_entry_university" ).datepicker({ dateFormat: 'yy-mm-dd' });

    $( "#id_date_start" ).datepicker({ dateFormat: 'yy-mm-dd' });
    $( "#id_date_end" ).datepicker({ dateFormat: 'yy-mm-dd' });
});