/* global $ moment */

function select_nearest_appt_time(){
    const now = moment();
    let min_timediff = 99999999;
    $("SELECT[name=appointment_time] OPTION").each(function(i, el){
        const raw_time = $(el).val();
        if (raw_time){
            const time = moment(raw_time, "h:mm A");
            const timediff = Math.abs(now.diff(time));
            if (timediff < min_timediff){
                min_timediff = timediff;
                $("SELECT[name=appointment_time]").val(raw_time).selectmenu("refresh", true);
            }
        }

    });
}


function reload_waiting_customers(){
    const wc = $("#waiting_customers");
    $.post(wc.attr("src"), null, function(data){
        wc.find("tbody").empty();
        if (data.length > 0){
            for (var i in data){
                const w = data[i];
                const w_since = moment(w.signin_time).format("h:mm A");
                const h_time = moment(w.helped_time).format("h:mm A");
                wc.find("tbody").append(
                    "<tr><td>" +
                        w.name + "</td><td>" +
                        w_since + "</td><td>" +
                        (w.helped_time ?
                         ("<span class=claim_data>" + h_time + " by " + w.helped_by +
                          " <button class='unclaim' data-id="+w.id+">Unclaim</button></span>") :
                         ("<button class='claim' data-id=" + w.id + ">Claim</button>")) +
                        "</td></tr>");
            }
            $("BUTTON.claim,BUTTON.unclaim").button();
        }else{ //no waiting customers
            wc.find("tbody").append(
                "<tr><td colspan=4 class='message'>There are currently no customers waiting.</td></tr>"
            );
        }

    }, 'json');
}

function show_results(do_refresh){
    const seconds_to_wait = 5;
    $("#form_container").hide({effect: "fade", complete: function(){
        $("#results").show("fade");
    }});

    if(do_refresh){
        window.setTimeout(reset_form, seconds_to_wait * 1000);
    }
}

function reset_form(){
    $("#signin_form")[0].reset();
    $("#signin_form :input.highlighted").removeClass("highlighted");
    $("#error_output").html("");
    $("#results").hide({effect: "fade", complete: function(){
        $("#form_container").show("fade");
    }});
    $("input[name=name]").getkeyboard().reveal();
}


function check_for_username(){
    const username = window.localStorage.getItem("signin.username");
    if (!username){
        //show the entry form only
        $("#username_display").hide();
        $("#username_entry_display").show();
    }else{
        $("#username").html(username);
        $("#username_display").show();
        $("#username_entry_display").hide();
    }
}

//liberally borrowed from stackoverflow (*blush*)
function disableSelection(target){
    if (typeof target.onselectstart!="undefined") //For IE
        target.onselectstart=function(){return false;};
    else if (typeof target.style.MozUserSelect!="undefined") //For Firefox
        target.style.MozUserSelect="none";
    else //All other route (For Opera)
        target.onmousedown=function(){return false;};
    target.style.cursor = "default";
}


$(document).ready(function(){

    //stuff for the sign-in form
    if ($("#signin_form").length > 0){

        //switch the colors for the big radio selects.
        $(document).on("change", ":input[name=has_appointment]", function(){
            //switch classes
            $("FORM UL LI.radio.selected").removeClass("selected");
            $(this).closest("li").addClass("selected");

            //enable/disable the time input
            const time_input = $(":input[name=appointment_time]");
            if ($("#yes_appt").is(":checked")){
                time_input.selectmenu('enable');
                select_nearest_appt_time();
            }else{
                time_input.selectmenu("disable");
                time_input.val("").selectmenu('refresh', true);
            }
        });
        $("BUTTON[name=submit]").button();
        if (document.use_osk){
            $(":input[name=name]").keyboard({
                appendLocally: true,
                usePreview: false,
                layout: "custom",
                autoAccept: true,
                stickyShift: false,
                stayOpen: true,
                acceptValid: true,
                customLayout: {
                    "default": [
                        'Q W E R T Y U I O P {b}',
                        'A S D F G H J K L ' + (document.use_appts ? '':'{accept}'),
                        'Z X C V B N M {cancel}',
                        '{space} - ,'

                    ]
                },
                accepted: function(event, keyboard, el){
                    $(this).closest("FORM").submit();
                },
                validate: function(keyboard, value, isClosing){
                    return value.length > 0;
                }
            });
        }
        $("SELECT[name=appointment_time]").selectmenu(
            {
                width: "10em",
                refresh: true,
                position: {my: "left center", at: "right center"},
                create: function(e, ui){
                    $(ui).css({"float": "right"});
                }
            });

        $(":input[name=name]").addClass('ui-widget');

        //focus the name field on page load
        $(":input[name=name]").focus();

        //Capture form submission and do it ajax style
        $(document).on("submit", "#signin_form", function(e){
            e.preventDefault();
            //validate requireds, if the browser doesn't support it.
            let needs_input = [];
            $(":input[required]").not(":disabled").each(function(i, el){
                if ($(el).val() === ''){
                    $(el).addClass("highlighted");
                    needs_input.push($(this).attr("data-fname") || $(this).attr("name"));
                }
            });
            if (needs_input.length > 0){
                $("#error_output").html("The following field(s) are required: " + needs_input.join(", ") + ".");
                $("input[name=name]").focus();
                return false;
            }
            $.ajax({
                type: "POST",
                url: $(this).attr("action"),
                data: $(this).serialize(),
                success: function(){
                    $("#results").html("<h2>Thank You!</h2><p>You are signed in.  Someone will be with you shortly.</p>");
                    show_results(true);
                },
                error: function(){
                    $("#results").html("<h2>Error</h2><p>The system has had an error.  Please alert an employee.</p>");
                    show_results(false);
                }
            });
            return false;
        });


        //disable text-selection because it mucks with the touchscreen.
        disableSelection(document.body);

    } //end signin form-specific stuff

    if($("#waiting_customers").length >0){
        //the view page
        reload_waiting_customers();
        window.setInterval(reload_waiting_customers, 120000);
        check_for_username();
        $("#change_username").button();
        $("#set_username").button();

        //capture the enter key on the user_name entry to set username
        $(document).on('click', '#set_username', function(e){
            window.localStorage.setItem("signin.username", $('#username_entry').val());
            check_for_username();
        });

        //enable the user to change the user_name entry
        $(document).on("click", "#change_username", function(){
            $("#username_display").hide();
            $("#username_entry_display").show("fade");
        });

        //enable claim buttons
        $(document).on("click", "BUTTON.claim", function(){
            const data = {
                customer_id: $(this).attr("data-id"),
                myname: localStorage.getItem("signin.username")
            };
            $.post(document.basepath + "post/claim_customer", data, function(data){
                reload_waiting_customers();
            });
        });

        //enable unclaim buttons
        $(document).on("click", "BUTTON.unclaim", function(){
            const data = {customer_id: $(this).attr("data-id")};
            $.post(document.basepath + "post/unclaim_customer", data, function(data){
                reload_waiting_customers();
            });
        });

        //enable document download button
        $("#csv_download").button();
        $(document).on("click", "#csv_download", function(){
            window.location = document.basepath + "download/data_dump_csv";
        });
    }//end view page

});
