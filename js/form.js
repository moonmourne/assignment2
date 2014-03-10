$(function() {  
    function myalert(msg)
    {
        $(".msg").html(msg);
        $(".alert").show();
        $(".black-mask").show();
    }
        $(".save").click(function(){
        $(".error").remove();
        var name=$(".name").val();
        var errornum=0;
        if($(".male").is(':checked'))
            gender=1;
        else
            gender=0;
        if(name=="")
        {
            errornum++;
            showError("You must input your name","name");
        }
        var email=$(".email").val();
        if(email=="")
        {
            showError("You must input your email","email");
        }else{
            var re = /^([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;   
            if(!re.test(email)) 
            {
                showError("Invalid email","email");
            }
        }
        var age=$(".age").val();
        if(age=="")
        {
             errornum++;
             showError("You must input your age","age");
        }
        else if(age<0||age>99)
        {
             errornum++;
            showError("Out of range","age");
        }
         var years=$(".years").val();
        if(years=="")
        {
             errornum++;
             showError("You must input this","years");
        }
        else if(years<0||years>99)
        {
            errornum++;
            showError("Out of range","years");
        }
        var url=$(".url").val();
        if(url=="")
        {
             errornum++;
            showError("You must input this","url");
        }
        else if(!url.match(/^_[0-9a-z]*_[0-9]+_[\w]*$/))
        {
             errornum++;
            showError("Invalid url","url");
        }
        if( errornum==0){
            $.post("/submit/form",
                {
                    name:name,
                    age:age,
                    years:years,
                    talent_tree:url,
                    gender:gender,
                    email:email
                },function(data)
                {
                    myalert(data);
                     
                });
           
        }
      //  alert(1);
    });
    $(".search").click(function(){
        var searchemail=$(".searchemail").val()
        $.get("/search?email="+searchemail,
            function(data){
                if(data.status!='succ')
                {
                    myalert(data.msg);
                }else
                {
                    data=data.data;
                    $(".name").val(data.name);
                    $(".email").val(data.email);
                    if(data.gender==1)
                    {
                        $(".male").prop("checked",true);
                       // $(".female").attr("checked",false);
                    }else
                    { 
                      //  $(".male").attr("checked",false);
                        $(".female").prop("checked",true);

                    }
                    $(".edit-name").html(data.email);
                    $(".age").val(data.age);
                    $(".years").val(data.years);
                    $(".url").val(data.talent_tree);
                    $(".admin-show").show();
                    // $(".male").attr("checked",true);
                }
            },"json");
    })
    $(".view").click(function(){
        window.open("http://www.dungeonsanddevelopers.com/#"+$(".url").val());
    });
    function showError(msg,type){
        $("<div class='error'>*"+msg+"</div>").appendTo("."+type+"-container");
    }
    $(".numberinput").keyup(function(){     
            var tmptxt=$(this).val();     
            $(this).val(tmptxt.replace(/[^\d]/g,''));     
        }).bind("paste",function(){     
            var tmptxt=$(this).val();     
            $(this).val(tmptxt.replace(/\D|^0/g,''));     
        }).css("ime-mode", "disabled");
    $(".link").click(function(){
        $(".alert").hide();
         $(".black-mask").hide();
    })
})