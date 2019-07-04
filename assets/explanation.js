function navigate(from, index, subindex){
    switch(from){
        case "root":
            $('div.root-nav-opt').each(function(){
            $(this).removeClass("navigate-active");
            });
            $('div#root-nav-'+index).addClass("navigate-active");

            $('div#root-page').html("");
            switch(index){
                case 0:
                    loadPage("decision").then(()=>{
                        loadExplanation(window.explanation);
                    });
                    break;

                case 1:
                    loadPage("case").then(()=>{
                        loadCase(window.explanation);
                    });
                    break;
            }
            break;

        case "page":
            $('div.page-nav-opt').each(function(){
                $(this).removeClass("navigate-active");
            });

            $('.page-nav-opt-sub').each(function(){
                $(this).addClass("page-nav-opt-disabled");
            });
            $('div#page-nav-'+index+"-1").removeClass("page-nav-opt-disabled");

            if (subindex == 0){
                $('div#page-nav-'+index).addClass("navigate-active");
                loadCasePage(index);
            }else{
                $('div#page-nav-'+index+"-"+subindex).addClass("navigate-active");
                loadCaseSubPage(index, subindex);
            }


            break;
    }

}

function loadExplanation(data){
    $('a#page-expl-decision').html(data.decision);
    if (data.support.length > 0){
        $('a#page-expl-rationale1').html(data.support[0].text);
    }

    $('a#page-expl-qualifier').html(data.qualifier.text);
    $('a#page-expl-backing').html(data.backing.text);
}

function loadCase(data){

    var active = 0;

    // generate navigation options
    var d = data.backing.data.data.sources;
    $('#page-nav-options').empty();
    for(var i=0;i<d.length;i++){
        var div = $("<div></div>");
        $('#page-nav-options').append(div);
        div.attr("id", "page-nav-"+i);
        div.attr("navindex", i);
        div.attr("subindex", active);
        div.addClass("page-nav-opt");
        div.addClass("navigate-small");
        if (i==0){
            div.addClass("navigate-active");
        }
        div.click((el)=>{
            navigate('page', Number($(el.currentTarget).attr("navindex")), Number($(el.currentTarget).attr("subindex")));
        });

        var divi = $("<div></div>");
        div.append(divi);
        divi.addClass("nav-opt-icon-small");
        var ei = $("<i></i>");
        divi.append(ei);
        ei.addClass("navicon-small");
        ei.addClass("fa");
        ei.addClass(getIconClassFromType(d[i].type));

        var diva = $('<div></div>');
        div.append(diva);
        diva.addClass("nav-opt-text-small");
        var a = $('<a></a>');
        diva.append(a);
        a.addClass("navigate-small");
        a.addClass("unselectable");
        a.html(d[i].name);


        // add sub navigation tree
        var div = $("<div></div>");
        $('#page-nav-options').append(div);
        div.attr("id", "page-nav-"+i+"-"+1);
        div.attr("navindex", i);
        div.attr("subindex", 1);
        div.addClass("page-nav-opt");
        div.addClass("page-nav-opt-sub");
        if (i != active){
            div.addClass("page-nav-opt-disabled");
        }
        div.addClass("navigate-small");
        div.click((el)=>{
            navigate('page', Number($(el.currentTarget).attr("navindex")), Number($(el.currentTarget).attr("subindex")));
        });

        var divi = $("<div></div>");
        div.append(divi);
        divi.addClass("nav-opt-icon-small");
        var ei = $("<i></i>");
        divi.append(ei);
        ei.addClass("navicon-small");
        ei.addClass("fa");
        ei.addClass("fa-search");

        var diva = $('<div></div>');
        div.append(diva);
        diva.addClass("nav-opt-text-small");
        var a = $('<a></a>');
        diva.append(a);
        a.addClass("navigate-small");
        a.addClass("unselectable");
        a.html("Variables");
    }

    loadCasePage(0);
}

function getIconClassFromType(type){
    switch(type){
        case "static": return "fa-database";
        case "cloud": return "fa-cloud-download";
        case "sensor": return "fa-signal";
        case "camera": return "fa-camera";
        case "mobile": return "fa-mobile";
        default: return "fa-file-o";
    }
}
function getTextFromType(type){
    switch(type){
        case "static": return "Database";
        case "cloud": return "Cloud data source";
        case "sensor": return "Sensor data source";
        case "camera": return "Camera data source";
        case "mobile": return "Mobile data source";
        default: return "Generic data source";
    }
}

function loadCasePage(index){
    var d = window.explanation.backing.data.data.sources;

    $('#page-body-attr').show();
    $('#page-body-features').hide();

    //fill page
    $('#page-body-titlebar-icon-i').removeClass();
    $('#page-body-titlebar-icon-i').addClass("titleicon");
    $('#page-body-titlebar-icon-i').addClass("fa");
    $('#page-body-titlebar-icon-i').addClass(getIconClassFromType(d[index].type));
    $('#page-body-titlebar-title-a').html(d[index].name);
    $('#page-body-titlebar-subtitle-a').html(getTextFromType(d[index].type));
    $('#page-body-description-a').html(d[index].description);
    $('#page-body-attr-author').html(d[index].author.name);
    $('#page-body-attr-organization').html(d[index].author.organization);
    if (d[index].year){
        $('#page-body-attr-year-cap').html("Year");
        $('#page-body-attr-year').html(d[index].year);
    }else if(d[index].operation_duration){
        switch(d[index].operation_duration.format){
            case "since":
                $('#page-body-attr-year-cap').html("Operative since");
                $('#page-body-attr-year').html(d[index].operation_duration.value);
                break;
            case "for":
                $('#page-body-attr-year-cap').html("Operative for");
                $('#page-body-attr-year').html(d[index].operation_duration.value);
                break;
        }
    }

    $('#page-body-attr-observations').html(d[index].observations);

    if (d[index].href){
        $('#page-body-attr-ref').show();
        $('#page-body-attr-reference').attr("href", d[index].href);
    }else{
        $('#page-body-attr-ref').hide();
    }
}

function loadCaseSubPage(index, subindex){
    var d = window.explanation.backing.data.data.sources;

    $('#page-body-attr').hide();
    $('#page-body-features').show();

    $('#page-body-titlebar-icon-i').removeClass();
    $('#page-body-titlebar-icon-i').addClass("titleicon");
    $('#page-body-titlebar-icon-i').addClass("fa");
    $('#page-body-titlebar-icon-i').addClass("fa-search");
    $('#page-body-titlebar-title-a').html(d[index].name);
    $('#page-body-titlebar-subtitle-a').html("Variables");
    $('#page-body-description-a').html("This page provides an overview of the variables and their values included in this data source.");

    var f = window.explanation.input.sources[index];
    var root = $('#page-body-features');
    root.empty();
    for(var i=0; i < f.case_features.length; i++){
        var tr = $('<tr></tr>');
        root.append(tr);

        var td1 = $('<td></td>');
        td1.addClass("page-body-attr-left");
        var a1 = $('<a></a>');
        td1.append(a1);
        a1.addClass("page-header");
        a1.addClass("unselectable");
        a1.attr("title", f.data_features[i].description);
        a1.html(f.data_features[i].name);

        //find contribution index
        for (j=0;j<f.case_importance.length; j++){
            if (Number(f.case_importance[j].feature) == i){
                break;
            }
        }
        var c = Number(f.case_importance[j].contribution);

        var td3 = $('<td></td>');
        td3.addClass("page-body-attr-middle");

        if (Math.abs(Math.round(c*100)) > 0){
            var Wdiv = $('<div></div>');
            td3.append(Wdiv);
            Wdiv.addClass("page-body-attr-wdiv");
            Wdiv.attr("title", "How much and in what direction this variable contributed to the decision. Positive contributions indicate that the value of this variable is regarded as evidence towards the decision. Negative contributions indicate this feature is regarded as evidence against the decision. The percentage indicates the strength of the evidence.");
            var Wdivi = $('<div></div>');
            Wdiv.append(Wdivi);
            Wdivi.addClass('page-body-attr-wdiv-i');
            var Wi = $('<i></i>');
            Wdivi.append(Wi);
            Wi.addClass('fa');
            Wi.addClass((c>0?"fa-angle-up":"fa-angle-down"));
            Wi.addClass('page-body-attr-wi');
            Wi.addClass(c>0?'page-body-attr-wi-pos':'page-body-attr-wi-neg');
            var Wdiva = $('<div></div>');
            Wdiv.append(Wdiva);
            Wdiva.addClass('page-body-attr-wdiv-a');
            var Wa = $('<a></a>');
            Wdiva.append(Wa);
            Wa.addClass('page-body-attr-wa');
            Wa.addClass('unselectable');
            Wa.html((c>0?"+":"") + Math.round(c*100) + "%");
        }



        var td2 = $('<td></td>');
        td2.addClass("page-expl-right");
        var a2 = $('<a></a>');
        td2.append(a2);
        a2.attr("id", "page-body-f"+i);
        a2.addClass("page-content");
        a2.html((f.data_features[i].data_type!="nominal"?f.case_features[i]:f.data_features[i].nominal_value[f.case_features[i]]));

        tr.append(td3); // contributions
        tr.append(td1); // names
        tr.append(td2); // features
    }
}

function loadPage(page){
    return new Promise(resolve => {
        $.get("templates/"+page+".html", (data) => {
            $('div#root-page').html(data);
            resolve();
        }, dataType="text");
    });
}

$("document").ready(() => {
    $.getJSON("explanation.json", function( data ) {
        window.explanation = data;
        loadPage("decision").then(() =>{
            loadExplanation(data);
        });
    });
});